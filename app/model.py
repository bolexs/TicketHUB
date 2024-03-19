from .database import Base
from sqlalchemy import (Column, Integer, String,
                        DateTime, Float, ForeignKey)
from sqlalchemy.orm import relationship
from datetime import datetime


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True)
    role = Column(String, index=True)
    events = relationship("Event", back_populates="organizer")
    tickets = relationship("Ticket", back_populates="attendee")

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    date = Column(DateTime, index=True)
    location = Column(String, index=True)
    price = Column(Float, index=True)
    tickets = Column(Integer, index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    organizer = relationship("Users", back_populates="events")
    organizer_id = Column(Integer, ForeignKey("users.id"))
    category = relationship("Category", back_populates="events")
    category_id = Column(Integer, ForeignKey("categories.id"))

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    purchase_date = Column(DateTime, default=datetime.now)
    attendee = relationship("Users", back_populates="tickets")
    event = relationship("Event", back_populates="tickets")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    events = relationship("Event", back_populates="category")
