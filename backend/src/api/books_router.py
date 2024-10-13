from fastapi import APIRouter,Depends,UploadFile
from auth.auth import current_user
from schemas.schemas import BooksAddSchema
from .dependencies import books_service
from services.books_service import BooksServices
from models.models import User

router = APIRouter(
    tags=['books'],
    prefix='/books'
)


    

@router.post('')
async def create_book(
    file: UploadFile,
    name: str,
    deadline: int,
    motivations: str,
    user: User = Depends(current_user),
    book_service: BooksServices = Depends(books_service),
):
    book = {}
    book['book_name'] = name
    book['deadline'] = deadline
    book['motivation'] = motivations
    text = await book_service.add_books(book,file,user.id)
    return text