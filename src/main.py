"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Full taste profile — all scoring features represented
    user_prefs = {
        "genre":         "lofi",   # preferred genre label
        "mood":          "chill",  # preferred mood label
        "energy":        0.38,     # low-key, background listening
        "valence":       0.60,     # mildly positive, not euphoric
        "acousticness":  0.80,     # strongly prefers organic/warm sound
        "studyability":  0.85,     # primarily studies to music
        "niche_score":   0.65,     # leans toward underground/non-mainstream
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
