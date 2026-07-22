"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


PROFILES = [
    # Three distinct "core" tastes
    ("High-Energy Pop", {"genre": "pop", "mood": "happy", "energy": 0.85, "likes_acoustic": False}),
    ("Chill Lofi", {"genre": "lofi", "mood": "chill", "energy": 0.30, "likes_acoustic": True}),
    ("Deep Intense Rock", {"genre": "rock", "mood": "intense", "energy": 0.95, "likes_acoustic": False}),
    # Adversarial / edge cases
    ("Adversarial: Sad but High-Energy", {"genre": "soul", "mood": "sad", "energy": 0.95, "likes_acoustic": False}),
    ("Adversarial: Genre Not In Catalog", {"genre": "metal", "mood": "intense", "energy": 0.9, "likes_acoustic": False}),
    ("Adversarial: No Genre Preference", {"mood": "chill", "energy": 0.5}),
]


def print_recommendations(label: str, user_prefs: dict, songs: list) -> None:
    print(f"\n=== {label} ===")
    print(f"user_prefs = {user_prefs}\n")
    for song, score, explanation in recommend_songs(user_prefs, songs, k=5):
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for label, user_prefs in PROFILES:
        print_recommendations(label, user_prefs, songs)


if __name__ == "__main__":
    main()
