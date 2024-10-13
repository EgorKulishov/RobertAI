from fastapi import FastAPI
import uvicorn

from auth.auth import auth_backend,fastapi_users
from auth.schemas import UserCreate,UserRead

from fastapi.middleware.cors import CORSMiddleware
from api.books_router import router as book_router



app = FastAPI(
    title='NeuroARK',
)



origins = [
    "http://127.0.0.1:5173",
    "http://127.0.0.1",
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:5173/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)






@app.get("/")
async def home():
    return "Hello World"



app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(book_router)





uvicorn.run(app)