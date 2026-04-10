from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field, asdict

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    studyability: float = 0.0
    niche_score: float = 0.0

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _user_prefs(self, user: UserProfile) -> Dict:
        """Convert a UserProfile into the dict format expected by score_song()."""
        return {
            "genre":        user.favorite_genre,
            "mood":         user.favorite_mood,
            "energy":       user.target_energy,
            "acousticness": 0.85 if user.likes_acoustic else 0.15,
        }

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Score every song against the user profile and return the top k sorted by score."""
        prefs = self._user_prefs(user)
        scored = [
            (song, score_song(prefs, asdict(song))[0])
            for song in self.songs
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable string explaining why a song was recommended."""
        prefs = self._user_prefs(user)
        _, reasons = score_song(prefs, asdict(song))
        return "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file using Python's built-in csv module.
    Numeric fields are explicitly cast so math operations work downstream.
    Required by src/main.py
    """
    import csv

    int_fields   = {"id", "tempo_bpm"}
    float_fields = {"energy", "valence", "danceability", "acousticness",
                    "studyability", "niche_score"}

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in int_fields:
                if field in row:
                    row[field] = int(row[field])
            for field in float_fields:
                if field in row:
                    row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    Algorithm Recipe — maximum possible score: 6.25
    ─────────────────────────────────────────────────
    Categorical (exact match bonuses):
      Genre match  → +2.00   (strong taste signal, but brittle)
      Mood match   → +1.50   (heavier than genre; mood = felt experience)

    Numeric (proximity reward, each scaled to its max):
      Energy       → up to +1.00  (1.0 - |song - target|)
      Valence      → up to +0.75  (happy/dark axis)
      Acousticness → up to +0.50  (organic vs. electronic)
      Studyability → up to +0.25  (optional; skipped if not in user_prefs)
      Niche score  → up to +0.25  (optional; skipped if not in user_prefs)
    ─────────────────────────────────────────────────
    Why mood outweighs genre: a "chill" listener won't enjoy "intense"
    metal even if genre matches. Mood is the primary vibe signal.
    Why genre > energy: genre encodes cultural/production context that
    numeric features can't capture (e.g., lofi texture vs. ambient texture).
    """
    score = 0.0
    reasons = []

    # --- Categorical bonuses ---
    if song['genre'] == user_prefs.get('genre', ''):
        score += 2.0
        reasons.append(f"Genre match ({song['genre']}): +2.00")

    if song['mood'] == user_prefs.get('mood', ''):
        score += 1.5
        reasons.append(f"Mood match ({song['mood']}): +1.50")

    # --- Numeric proximity scores: reward = 1.0 - |difference| ---
    def proximity(song_val: float, target: float, weight: float, label: str) -> float:
        pts = (1.0 - abs(song_val - target)) * weight
        reasons.append(f"{label}: +{pts:.2f}")
        return pts

    score += proximity(song['energy'],      user_prefs.get('energy', 0.5),      1.00, "Energy proximity")
    score += proximity(song['valence'],     user_prefs.get('valence', 0.5),     0.75, "Valence proximity")
    score += proximity(song['acousticness'],user_prefs.get('acousticness', 0.5),0.50, "Acousticness proximity")

    # Optional features — only scored if the user profile includes them
    if 'studyability' in user_prefs:
        score += proximity(song['studyability'], user_prefs['studyability'], 0.25, "Studyability proximity")
    if 'niche_score' in user_prefs:
        score += proximity(song['niche_score'],  user_prefs['niche_score'],  0.25, "Niche proximity")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs, sort by score descending, and return the top k with explanations."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, reasons))
    
    # Sort by score descending
    scored.sort(key=lambda x: x[1], reverse=True)
    
    # Take top k
    top = scored[:k]
    
    # Format explanation
    result = []
    for song, score, reasons in top:
        explanation = "; ".join(reasons)
        result.append((song, score, explanation))
    
    return result
