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
    from src.recommender import DEFAULT_TASTE_PROFILE, load_songs, recommend_songs
except ModuleNotFoundError:
    # Works when run directly from inside src/: python main.py
    from recommender import DEFAULT_TASTE_PROFILE, load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Specific taste profile used for comparisons:
    # prefers pop/happy songs with high energy and avoids acoustic tracks.
    user_prefs = {
        "genre": DEFAULT_TASTE_PROFILE.favorite_genre,
        "mood": DEFAULT_TASTE_PROFILE.favorite_mood,
        "energy": DEFAULT_TASTE_PROFILE.target_energy,
        "likes_acoustic": DEFAULT_TASTE_PROFILE.likes_acoustic,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print_recommendations(recommendations)


def print_recommendations(recommendations) -> None:
    """Print recommendations in a clean, ranked terminal layout."""
    width = 60
    print()
    print("=" * width)
    print("TOP RECOMMENDATIONS".center(width))
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
