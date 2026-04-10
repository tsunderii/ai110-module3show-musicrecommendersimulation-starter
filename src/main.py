"""
Command line runner for the Music Recommender Simulation.

Profiles:
  1. High-Energy Pop      — mainstream gym/party listener
  2. Chill Lofi           — study/focus listener
  3. Deep Intense Rock    — hard-rock listener
  4. [ADVERSARIAL] Conflicted Energy — high energy but sad mood (contradictory)
  5. [ADVERSARIAL] Acoustic Metalhead — metal genre but very high acousticness
  6. [ADVERSARIAL] Blank Slate       — all mid-range values, no genre/mood signal

Inline Chat prompt used to design the table output:
    "Use tabulate to display the top-k recommendations as a table with columns
    for Rank, Title, Artist, Genre, Mood, Score, and a Reasons column that
    shows each scoring factor on its own line inside the cell. Use the 'grid'
    table format so the reasons stay readable. Print a profile header above
    each table showing the genre, mood, and energy target."
"""

from tabulate import tabulate
from .recommender import load_songs, recommend_songs


PROFILES = [
    # ── Standard profiles ──────────────────────────────────────────────────
    {
        "label": "High-Energy Pop",
        "prefs": {
            "genre":        "pop",
            "mood":         "happy",
            "energy":       0.90,
            "valence":      0.85,
            "acousticness": 0.10,
            "studyability": 0.15,
            "niche_score":  0.20,
        },
    },
    {
        "label": "Chill Lofi",
        "prefs": {
            "genre":        "lofi",
            "mood":         "chill",
            "energy":       0.35,
            "valence":      0.60,
            "acousticness": 0.80,
            "studyability": 0.90,
            "niche_score":  0.60,
        },
    },
    {
        "label": "Deep Intense Rock",
        "prefs": {
            "genre":        "rock",
            "mood":         "intense",
            "energy":       0.92,
            "valence":      0.38,
            "acousticness": 0.08,
            "studyability": 0.10,
            "niche_score":  0.45,
        },
    },
    # ── Adversarial / edge-case profiles ────────────────────────────────────
    {
        "label": "[ADVERSARIAL] Conflicted Energy (energy=0.9, mood=sad)",
        "prefs": {
            "genre":        "pop",
            "mood":         "sad",       # no song in catalog has mood=sad → 0 mood bonus
            "energy":       0.90,        # pushes toward high-energy tracks
            "valence":      0.15,        # low valence (dark)
            "acousticness": 0.20,
            "studyability": 0.20,
            "niche_score":  0.30,
        },
    },
    {
        "label": "[ADVERSARIAL] Acoustic Metalhead (genre=metal, acousticness=0.95)",
        "prefs": {
            "genre":        "metal",     # only 1 metal song (Iron Cathedral, acoustic=0.06)
            "mood":         "angry",
            "energy":       0.95,
            "valence":      0.25,
            "acousticness": 0.95,        # wants acoustic, but metal songs are not acoustic
            "studyability": 0.05,
            "niche_score":  0.80,
        },
    },
    {
        "label": "[ADVERSARIAL] Blank Slate (all 0.5, no genre/mood)",
        "prefs": {
            "genre":        "",          # no categorical match possible
            "mood":         "",
            "energy":       0.50,
            "valence":      0.50,
            "acousticness": 0.50,
            "studyability": 0.50,
            "niche_score":  0.50,
        },
    },
]


def print_recommendations(label: str, user_prefs: dict, recommendations: list) -> None:
    genre_disp = user_prefs["genre"] or "(none)"
    mood_disp  = user_prefs["mood"]  or "(none)"

    print(f"\n{'━' * 72}")
    print(f"  PROFILE : {label}")
    print(f"  Genre: {genre_disp}  |  Mood: {mood_disp}  |  Energy: {user_prefs['energy']}")
    print(f"{'━' * 72}")

    rows = []
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        reasons_formatted = "\n".join(
            f"• {r}" for r in explanation.split("; ")
        )
        rows.append([
            f"#{rank}",
            song["title"],
            song["artist"],
            song["genre"],
            song["mood"],
            f"{score:.2f}",
            reasons_formatted,
        ])

    print(tabulate(
        rows,
        headers=["#", "Title", "Artist", "Genre", "Mood", "Score", "Why"],
        tablefmt="grid",
        maxcolwidths=[3, 22, 18, 12, 10, 6, 38],
    ))
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs from catalog.\n")

    for profile in PROFILES:
        recs = recommend_songs(profile["prefs"], songs, k=5)
        print_recommendations(profile["label"], profile["prefs"], recs)


if __name__ == "__main__":
    main()
