from utils.repository import SQLAlchemyRepository

from models.models import Books

class BooksRepository(SQLAlchemyRepository):

    model = Books