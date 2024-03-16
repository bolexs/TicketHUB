from fastapi import FastAPI, Request
from app.database import engine, get_db # noqa: F401


# Application initialization
app = FastAPI(title="TicketHUB", version="1.0.0")