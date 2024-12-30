from storage.storage_json import StorageJson
from movie_app import MovieApp


def main():
    """
    Main entry point for the movie application.
    """
    print("Welcome to the Movie App!")
    print("Your movies will be stored in a file named after you.")
    print("If it's your first time, a new file will be created.")
    user_name = input("Enter your name: ").strip().lower()

    # Create a storage file for the user
    storage_file = f"data/{user_name}.json"
    print(f"Using storage file: {storage_file}")

    # Initialize JSON storage
    storage = StorageJson(storage_file)

    # Start the app
    app = MovieApp(storage)
    app.run()


if __name__ == "__main__":
    main()
