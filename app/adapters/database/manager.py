from .core import SQLAlchemyConnector
from .interface import DatabaseAbstractClientInterface


class DatabaseManager(DatabaseAbstractClientInterface):
    """Concrete implementation of the database session manager using SQLAlchemy."""

    __database_connector__ = SQLAlchemyConnector

    def __init__(self):
        self.session_manager = self.__database_connector__()

    def get_db_session(self):
        return self.session_manager.get_db_session()

    def get_current_db_session(self):
        return self.session_manager.get_current_db_session()

    def create_all(self, engine=None):
        self.session_manager.create_all(engine=engine)

    def get_base(self):
        return self.session_manager.get_base()


db_manager = DatabaseManager()
db_session = db_manager.get_db_session()
Base = db_manager.get_base()
