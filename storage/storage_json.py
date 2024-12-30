import json
from storage.istorage import IStorage
import requests


class StorageJson(IStorage):
    """
    JSON storage implementation of the IStorage interface.
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.api_key = "537f950f"
        self.api_url = "http://www.omdbapi.com/"

    def _load_movies(self):
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_movies(self, movies):
        with open(self.file_path, 'w') as file:
            json.dump(movies, file, indent=4)

    def list_movies(self):
        return self._load_movies()

    def add_movie(self, title):
        response = requests.get(self.api_url, params={"t": title, "apikey": self.api_key})
        if response.status_code != 200:
            print("Error: Unable to reach the API. Please check your connection.")
            return

        data = response.json()
        if data.get("Response") != "True":
            print(f"Error: Movie '{title}' not found in the database.")
            return

        movies = self._load_movies()
        if title in movies:
            print(f"Movie '{title}' already exists.")
            return

        # Handle non-numeric year
        try:
            year = int(data.get("Year", "0").split("–")[0].strip())
        except ValueError:
            year = 0  # Default year if parsing fails

        # Handle non-numeric or missing rating
        try:
            rating = float(data.get("imdbRating", "0").replace("N/A", "0"))
        except ValueError:
            rating = 0.0

        movies[title] = {
            "year": year,
            "rating": rating,
            "poster": data.get("Poster")
        }
        self._save_movies(movies)
        print(f"Movie '{title}' added successfully.")

    def delete_movie(self, title):
        movies = self._load_movies()
        if title not in movies:
            raise ValueError(f"Movie '{title}' not found.")
        del movies[title]
        self._save_movies(movies)

    def update_movie(self, title, rating):
        movies = self._load_movies()
        if title not in movies:
            raise ValueError(f"Movie '{title}' not found.")
        movies[title]["rating"] = rating
        self._save_movies(movies)
