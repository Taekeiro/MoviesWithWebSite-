from storage.storage_csv import StorageCsv
from movie_app import MovieApp

def main():
    """
    Main function to run the movie application.
    """
    # Initialize CSV storage
    storage = StorageCsv('data/movies.csv')

    # Initialize MovieApp with CSV storage
    app = MovieApp(storage)

    # Run the MovieApp
    app.run()


if __name__ == "__main__":
    main()