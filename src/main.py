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
    print(f"Loaded songs: {len(songs)}")

    # pop/happy profile — high energy, upbeat, mainstream
    user_prefs = {
        "genre":        "pop",
        "mood":         "happy",
        "energy":       0.80,
        "valence":      0.82,
        "acousticness": 0.20,
        "studyability": 0.30,
        "niche_score":  0.25,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    width = 60
    print("\n" + "=" * width)
    print("  🎵  TOP RECOMMENDATIONS")
    print(f"  Genre: {user_prefs['genre']}  |  Mood: {user_prefs['mood']}  |  Energy: {user_prefs['energy']}")
    print("=" * width)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']} — {song['artist']}")
        print(f"       Score : {score:.2f} / 6.25")
        print(f"       Genre : {song['genre']}  |  Mood: {song['mood']}")
        print(f"       Why   :")
        for reason in explanation.split("; "):
            print(f"               • {reason}")

    print("\n" + "=" * width)


if __name__ == "__main__":
    main()
