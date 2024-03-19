import bcrypt
from .database import Base
from sqlalchemy import (Column, Integer, String,
                        DateTime, Float, ForeignKey)
from sqlalchemy.orm import relationship
from datetime import datetime


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=False, unique=True)
    email = Column(String, index=True, nullable=False, unique=True)
    role = Column(String, index=True, nullable=False)
    _password = Column("password", index=True, nullable=False)
    events = relationship("Event", back_populates="organizer")
    tickets = relationship("Ticket", back_populates="attendee")

    @property
    def password(self):
        raise AttributeError("Password: write-only field")
    
    @password.setter
    def password(self, password_input):
        self._password = bcrypt.hashpw(password_input.encode('utf-8'), bcrypt.gensalt()).decode()

    def check_password(self, password_input):
        return bcrypt.checkpw(password_input.encode('utf-8'), self._password.encode())

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, index=True, nullable=False)
    date = Column(DateTime, index=True, nullable=False)
    location = Column(String, index=True, nullable=False)
    price = Column(Float, index=True, nullable=False)
    tickets = Column(Integer, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    organizer = relationship("Users", back_populates="events")
    organizer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = relationship("Category", back_populates="events")
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    purchase_date = Column(DateTime, default=datetime.now, nullable=False)
    attendee = relationship("Users", back_populates="tickets")
    event = relationship("Event", back_populates="tickets")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, index=True, nullable=True)
    events = relationship("Event", back_populates="category")
