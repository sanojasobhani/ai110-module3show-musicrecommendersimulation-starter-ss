"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    # Works when run as a module from the project root: python -m src.main
    from src.recommender import load_songs, recommend_songs
except ModuleNotFoundError:
    # Works when run directly from inside src/: python main.py
    from recommender import load_songs, recommend_songs


# Three distinct user taste profiles used to compare recommendations.
# Each dict matches the keys expected by recommender.score_song:
# genre, mood, energy (0.0-1.0), and likes_acoustic (bool).
USER_PROFILES = {
    # Upbeat pop fan: loud, happy, high-energy, no acoustic tracks.
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.9,
        "likes_acoustic": False,
    },
    # Laid-back listener: mellow lofi for focus, low energy, acoustic-friendly.
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.3,
        "likes_acoustic": True,
    },
    # Hard-hitting rock fan: aggressive, high-energy, electric (non-acoustic).
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.85,
        "likes_acoustic": False,
    },
}


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Generate and print recommendations for each taste profile so the
    # differences between profiles are easy to compare in the terminal.
    for profile_name, user_prefs in USER_PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(recommendations, profile_name)


def print_recommendations(recommendations, profile_name: str = "") -> None:
    """Print recommendations in a clean, ranked terminal layout."""
    width = 60
    title = f"TOP RECOMMENDATIONS - {profile_name}" if profile_name else "TOP RECOMMENDATIONS"
    print()
    print("=" * width)
    print(title.center(width))
    print("=" * width)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        header = f"{rank}. {song['title']} - {song['artist']}"
        print(f"\n{header}")
        print(f"   Score: {score:.2f} / 1.00")
        print("   Reasons:")
        for reason in explanation.split(" | "):
            print(f"     - {reason}")

    print("\n" + "=" * width)


if __name__ == "__main__":
    main()
