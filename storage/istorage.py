from abc import ABC, abstractmethod


class IStorage(ABC):
    """
    Abstract base class that defines the interface for storage managers.
    """

    @abstractmethod
    def list_movies(self):
        """
        Retrieve a dictionary of all movies stored.
        """
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        """
        Add a new movie to the storage.
        """
        pass

    @abstractmethod
    def delete_movie(self, title):
        """
        Remove a movie from the storage by title.
        """
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        """
        Update the rating of a movie in the storage.
        """
        pass
