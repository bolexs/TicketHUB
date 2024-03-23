import bcrypt
from .database import Base
from sqlalchemy import (Column, Integer, String,
                        DateTime, Float, ForeignKey)
from sqlalchemy.orm import relationship
from datetime import datetime
from utils.password_utils import hash_password, verify_password


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False, unique=True)
    email = Column(String, index=True, nullable=False, unique=True)
    role = Column(String, index=True, nullable=False)
    _password = Column("password", String, index=True, nullable=False)
    events = relationship("Event", back_populates="organizer")
    tickets = relationship("Ticket", back_populates="attendee")

    @property
    def password(self):
        raise AttributeError("Password: write-only field")
    
    @password.setter
    def password(self, password_input):
        self._password = hash_password(password_input)

    def verify_password(self, password_input):
        return verify_password(password_input, self._password)

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, index=True, nullable=False)
    date = Column(DateTime, index=True, nullable=False)
    location = Column(String, index=True, nullable=False)
    price = Column(Float, index=True, nullable=False)
    ticket_count = Column(Integer, index=True, nullable=False)
    tickets = relationship("Ticket", back_populates="event")
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    organizer = relationship("Users", back_populates="events")
    organizer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = relationship("Category", back_populates="events")
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quantity = Column(Integer, index=True, nullable=False, default=1)
    purchase_date = Column(DateTime, default=datetime.now, nullable=False)
    attendee = relationship("Users", back_populates="tickets")
    event = relationship("Event", back_populates="tickets")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, index=True, nullable=True)
    events = relationship("Event", back_populates="category")
