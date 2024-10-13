from services.user_services import UserServices
from repositories.user_repo import UserRepository
from repositories.books_repo import BooksRepository
from services.books_service import BooksServices

def user_service() -> UserServices:
    return UserServices(UserRepository)

def books_service() -> UserServices:
    return BooksServices(BooksRepository)