from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

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
    """Reads a CSV file and returns a list of song dicts with typed numeric values."""
    import csv

    int_fields = {"id"}
    float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(dict(row))
    return songs

def score_song(user_prefs: Dict, song: Dict) -> float:
    """
    Scores a single song against a user preference profile.
    Recipe (max 4.0):
      +2.0  genre match
      +1.0  mood match
      +0-1  energy similarity: 1.0 - abs(song.energy - target_energy)
    """
    score = 0.0
    if song["genre"] == user_prefs["favorite_genre"]:
        score += 2.0
    if song["mood"] == user_prefs["favorite_mood"]:
        score += 1.0
    score += 1.0 - abs(song["energy"] - user_prefs["target_energy"])
    return score

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [(song, score_song(user_prefs, song)) for song in songs]
    scored.sort(key=lambda x: x[1], reverse=True)
    results = []
    for song, score in scored[:k]:
        reasons = []
        if song["genre"] == user_prefs["favorite_genre"]:
            reasons.append("genre match (+2.0)")
        if song["mood"] == user_prefs["favorite_mood"]:
            reasons.append("mood match (+1.0)")
        energy_points = 1.0 - abs(song["energy"] - user_prefs["target_energy"])
        reasons.append(f"energy similarity +{energy_points:.2f} (song: {song['energy']}, target: {user_prefs['target_energy']})")
        explanation = " | ".join(reasons)
        results.append((song, score, explanation))
    return results
