from pydantic import BaseModel,EmailStr,Field,FileUrl
from fastapi import UploadFile
from enum import Enum
from typing import Optional



class UserReadSchema(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

class BooksAddSchema(BaseModel):
    name: str
    deadline: int
    motivations: str

