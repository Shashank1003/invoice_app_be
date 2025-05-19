from abc import ABC, abstractmethod


class DatabaseAbstractClientInterface(ABC):
    """Abstract base class for managing the database session."""

    @abstractmethod
    def get_db_session(self):
        """Get a new database session."""
        raise NotImplementedError

    @abstractmethod
    def get_current_db_session(self):
        """Get the current database session."""
        raise NotImplementedError

    @abstractmethod
    def create_all(self):
        """Create all database tables."""
        raise NotImplementedError

    @abstractmethod
    def get_base(self):
        """Returns Declarative Base"""
        raise NotImplementedError
