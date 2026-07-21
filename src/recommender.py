from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from operator import itemgetter

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

DEFAULT_TASTE_PROFILE = UserProfile(
    favorite_genre="pop",
    favorite_mood="happy",
    target_energy=0.8,
    likes_acoustic=False,
)

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv
    print(f"Loading songs from {csv_path}...")
    songs = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numeric columns to float
                song = {
                    'id': int(row['id']),
                    'title': row['title'],
                    'artist': row['artist'],
                    'genre': row['genre'],
                    'mood': row['mood'],
                    'energy': float(row['energy']),
                    'tempo_bpm': float(row['tempo_bpm']),
                    'valence': float(row['valence']),
                    'danceability': float(row['danceability']),
                    'acousticness': float(row['acousticness']),
                }
                songs.append(song)
        print(f"Successfully loaded {len(songs)} songs.")
    except FileNotFoundError:
        print(f"Error: File '{csv_path}' not found.")
    except Exception as e:
        print(f"Error loading songs: {e}")
    
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences using point-weighting strategy.
    
    Scoring breakdown:
    - +2.0 points for genre match
    - +1.0 point for mood match
    - +0.0 to +1.5 points for energy similarity
    - +0.5 bonus for acousticness preference
    
    Max possible score: 5.0 points (normalized to 1.0)
    
    Expected return format: (score, reasons)
    """
    total_points = 0
    reasons = []
    
    # Genre match: +2.0 points
    if song['genre'].lower() == user_prefs['genre'].lower():
        total_points += 2.0
        reasons.append(f"Genre match: {song['genre']}")
    
    # Mood match: +1.0 point
    if song['mood'].lower() == user_prefs['mood'].lower():
        total_points += 1.0
        reasons.append(f"Mood match: {song['mood']}")
    
    # Energy similarity: +0.0 to +1.5 points
    # Perfect match (distance = 0) gives 1.5 points
    # Worst match (distance = 1.0) gives 0 points
    energy_distance = abs(song['energy'] - user_prefs['energy'])
    energy_points = max(0, 1.5 * (1 - energy_distance))
    total_points += energy_points
    reasons.append(f"Energy alignment: {energy_points:.2f} pts (target: {user_prefs['energy']}, song: {song['energy']})")
    
    # Acousticness preference: +0.0 to +0.5 bonus
    # If user prefers acoustic, reward high acousticness; otherwise reward low acousticness
    if user_prefs['likes_acoustic']:
        acoustic_score = song['acousticness'] * 0.5
        total_points += acoustic_score
        reasons.append(f"Acousticness bonus: {acoustic_score:.2f} pts")
    else:
        # Penalize acoustic tracks slightly, reward non-acoustic
        acoustic_penalty = (1 - song['acousticness']) * 0.5
        total_points += acoustic_penalty
        reasons.append(f"Non-acoustic preference: {acoustic_penalty:.2f} pts")
    
    # Normalize score to 0-1 range (max possible is 5.0 points)
    max_possible_score = 2.0 + 1.0 + 1.5 + 0.5  # 5.0
    normalized_score = min(total_points / max_possible_score, 1.0)
    
    return normalized_score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Scores all songs and returns the top k recommendations.
    
    Expected return format: (song_dict, score, explanation)
    """
    scored_songs = []

    # Score each song
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = " | ".join(reasons)
        scored_songs.append((song, score, explanation))

    # Sort by score (descending) and return top k
    return sorted(scored_songs, key=itemgetter(1), reverse=True)[:k]
