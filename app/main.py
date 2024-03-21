from fastapi import FastAPI, Request
from app.database import engine, get_db # noqa: F401
from fastapi.middleware.cors import CORSMiddleware
from app import model
from app.router import users, auth_user

model.Base.metadata.create_all(bind=engine)

# Application initialization
app = FastAPI(title="TicketHUB", version="1.0.0")

app.include_router(users.router)
app.include_router(auth_user.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)