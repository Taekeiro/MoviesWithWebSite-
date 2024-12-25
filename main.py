from storage.storage_csv import StorageCsv
from movie_app import MovieApp


def main():
    """
    Main entry point for the movie application.
    """
    storage = StorageCsv('data/movies.csv')  # Use CSV storage
    app = MovieApp(storage)
    app.run()


if __name__ == "__main__":
    main()
