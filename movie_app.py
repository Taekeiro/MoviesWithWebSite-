import random
import requests
import os


class MovieApp:
    """
    A class that manages the movie application logic.
    """

    def __init__(self, storage):
        """
        Initialize the MovieApp with a storage instance.
        :param storage: An instance of a class implementing IStorage.
        """
        self._storage = storage

    def _command_list_movies(self):
        """
        List all movies in the storage.
        """
        movies = self._storage.list_movies()
        if not movies:
            print("No movies found.")
        else:
            print("Movies in your collection:")
            for title, details in movies.items():
                print(f"- {title} ({details['year']}): {details['rating']}\n   Poster: {details['poster']}")

    def _command_add_movie(self):
        """
        Add a new movie by fetching details from OMDb API.
        """
        title = input("Enter the movie title: ").strip()
        self._storage.add_movie(title)

    def _command_delete_movie(self):
        """
        Delete a movie from the storage.
        """
        title = input("Enter the title of the movie to delete: ").strip()
        try:
            self._storage.delete_movie(title)
            print(f"Movie '{title}' deleted successfully.")
        except ValueError as e:
            print(e)

    def _command_random_movie(self):
        """
        Display a random movie from the collection.
        """
        movies = self._storage.list_movies()
        if not movies:
            print("No movies available.")
            return

        title, details = random.choice(list(movies.items()))
        print(f"Random Movie: {title} ({details['year']}): {details['rating']}\n   Poster: {details['poster']}")

    def _command_search_movie(self):
        """
        Search for movies by a partial title match.
        """
        search_query = input("Enter part of the movie title to search: ").strip().lower()
        movies = self._storage.list_movies()
        matching_movies = {
            title: details for title, details in movies.items()
            if search_query in title.lower()
        }

        if matching_movies:
            print("Matching movies:")
            for title, details in matching_movies.items():
                print(f"- {title} ({details['year']}): {details['rating']}\n   Poster: {details['poster']}")
        else:
            print("No matching movies found.")

    def _command_sort_by_year(self):
        """
        Sort and display movies by year.
        """
        movies = self._storage.list_movies()
        if not movies:
            print("No movies available.")
            return

        sorted_movies = sorted(movies.items(), key=lambda item: item[1]['year'])
        print("Movies sorted by year:")
        for title, details in sorted_movies:
            print(f"- {title} ({details['year']}): {details['rating']}\n   Poster: {details['poster']}")

    def _command_sort_by_rating(self):
        """
        Sort and display movies by rating.
        """
        movies = self._storage.list_movies()
        if not movies:
            print("No movies available.")
            return

        sorted_movies = sorted(movies.items(), key=lambda item: item[1]['rating'], reverse=True)
        print("Movies sorted by rating:")
        for title, details in sorted_movies:
            print(f"- {title} ({details['year']}): {details['rating']}\n   Poster: {details['poster']}")

    def _generate_website(self):
        """
        Generate a static website for the movie collection.
        """
        movies = self._storage.list_movies()
        if not movies:
            print("No movies available to generate the website.")
            return

        # Load template HTML
        with open('_static/index_template.html', 'r') as template_file:
            template_html = template_file.read()

        # Generate movie grid HTML
        movie_grid_html = ""
        for title, details in movies.items():
            movie_grid_html += f"""
                <li>
                    <div class='movie'>
                        <img class='movie-poster' src='{details['poster']}' alt='Poster for {title}' />
                        <div class='movie-title'>{title}</div>
                        <div class='movie-year'>{details['year']}</div>
                    </div>
                </li>
            """

        # Replace placeholders in template
        output_html = template_html.replace('__TEMPLATE_TITLE__', 'My Movie Collection')
        output_html = output_html.replace('__TEMPLATE_MOVIE_GRID__', movie_grid_html)

        # Write output HTML
        output_path = 'movies.html'
        with open(output_path, 'w') as output_file:
            output_file.write(output_html)

        print(f"Website generated successfully: {output_path}")

    def run(self):
        """
        Run the movie application.
        """
        while True:
            print("\nMenu:")
            print("1. List movies")
            print("2. Add a movie")
            print("3. Delete a movie")
            print("4. Random movie")
            print("5. Search movie")
            print("6. Sort movies by year")
            print("7. Sort movies by rating")
            print("8. Generate website")
            print("0. Exit")

            choice = input("Choose an option: ").strip()
            if choice == '1':
                self._command_list_movies()
            elif choice == '2':
                self._command_add_movie()
            elif choice == '3':
                self._command_delete_movie()
            elif choice == '4':
                self._command_random_movie()
            elif choice == '5':
                self._command_search_movie()
            elif choice == '6':
                self._command_sort_by_year()
            elif choice == '7':
                self._command_sort_by_rating()
            elif choice == '8':
                self._generate_website()
            elif choice == '0':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
