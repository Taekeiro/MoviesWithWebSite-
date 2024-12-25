import csv
import requests
from storage.istorage import IStorage

class StorageCsv(IStorage):
    """
    CSV storage implementation of the IStorage interface.
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.api_key = "537f950f"
        self.api_url = "http://www.omdbapi.com/"

    def list_movies(self):
        movies = {}
        try:
            with open(self.file_path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    title = row['title']
                    movies[title] = {
                        'rating': float(row['rating']),
                        'year': int(row['year']),
                        'poster': row.get('poster', None)
                    }
        except FileNotFoundError:
            pass
        return movies

    def add_movie(self, title):
        response = requests.get(self.api_url, params={"t": title, "apikey": self.api_key})
        if response.status_code != 200:
            print("Error: Unable to reach the API. Please check your connection.")
            return

        data = response.json()
        if data.get("Response") != "True":
            print(f"Error: Movie '{title}' not found in the database.")
            return

        movie_data = {
            "title": data.get("Title"),
            "year": int(data.get("Year")),
            "rating": float(data.get("imdbRating")),
            "poster": data.get("Poster")
        }

        movies = self.list_movies()
        if movie_data['title'] in movies:
            print(f"Movie '{movie_data['title']}' already exists.")
            return

        with open(self.file_path, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['title', 'year', 'rating', 'poster'])
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(movie_data)

        print(f"Movie '{movie_data['title']}' added successfully.")

    def delete_movie(self, title):
        movies = self.list_movies()
        if title not in movies:
            raise ValueError(f"Movie '{title}' not found.")
        del movies[title]

        with open(self.file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['title', 'year', 'rating', 'poster'])
            writer.writeheader()
            for title, details in movies.items():
                writer.writerow({'title': title, 'year': details['year'], 'rating': details['rating'], 'poster': details['poster']})

    def update_movie(self, title, rating):
        movies = self.list_movies()
        if title not in movies:
            raise ValueError(f"Movie '{title}' not found.")
        movies[title]['rating'] = rating

        with open(self.file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['title', 'year', 'rating', 'poster'])
            writer.writeheader()
            for title, details in movies.items():
                writer.writerow({'title': title, 'year': details['year'], 'rating': details['rating'], 'poster': details['poster']})
