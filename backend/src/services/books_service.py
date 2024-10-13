from utils.repository import AbstractRepository
import aiohttp
import asyncio
from gemini import request_to_model


class BooksServices:

    def __init__(self,books_repo: AbstractRepository) -> None:
        self.books_repo = books_repo()

    async def add_books(self,book,file,user_id):

        
        book['user_id'] = user_id

        text = file.read()

        promtt = f'''{text} твоя задача сделать выжимку данного текста чтобы его было можно прочитать за данное количество дней, если каждый день человек читает по 2 часа, а в час он прочитывает 9000 слов, если что его точно можно прочитать за данное количество дней
        количество дней={book['deadline']}
        '''

        text_new = await request_to_model(promtt,0)
        book['text'] = text_new
        book_id = await self.books_repo.add_one(book)
        return text_new

