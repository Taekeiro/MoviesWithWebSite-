import json
from storage.istorage import IStorage


class StorageJson(IStorage):
    """
    JSON storage implementation of the IStorage interface.
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def _load_movies(self):
        """
        Load movies from the JSON file.
        """
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_movies(self, movies):
        """
        Save movies to the JSON file.
        """
        with open(self.file_path, 'w') as file:
            json.dump(movies, file, indent=4)

    def list_movies(self):
        """
        Retrieve a dictionary of all movies stored.
        """
        return self._load_movies()

    def add_movie(self, title, year, rating, poster):
        """
        Add a new movie to the storage.
        """
        movies = self._load_movies()
        if title in movies:
            raise ValueError(f"Movie '{title}' already exists.")
        movies[title] = {"year": year, "rating": rating, "poster": poster}
        self._save_movies(movies)

    def delete_movie(self, title):
        """
        Remove a movie from the storage by title.
        """
        movies = self._load_movies()
        if title not in movies:
            raise ValueError(f"Movie '{title}' not found.")
        del movies[title]
        self._save_movies(movies)

    def update_movie(self, title, rating):
        """
        Update the rating of a movie in the storage.
        """
        movies = self._load_movies()
        if title not in movies:
            raise ValueError(f"Movie '{title}' not found.")
        movies[title]['rating'] = rating
        self._save_movies(movies)

    def generate_website(self, output_file='movies.html'):
        """
        Generate a static HTML page for the movie collection.
        """
        movies = self.list_movies()
        if not movies:
            print("No movies available to generate the website.")
            return

        html_content = "<html><head><title>My Movie Collection</title></head><body>"
        html_content += "<h1>My Movie Collection</h1><ul>"

        for title, details in movies.items():
            html_content += f"<li>{title} ({details['year']}): {details['rating']}<br>"
            html_content += f"<img src='{details['poster']}' alt='{title} poster' style='width:100px'><br></li>"

        html_content += "</ul></body></html>"

        with open(output_file, 'w') as file:
            file.write(html_content)

        print(f"Website generated at {output_file}")
