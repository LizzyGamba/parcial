from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from Backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    reviews = relationship(
        "Review",
        back_populates="author",
        cascade="all, delete-orphan"
    )

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    producto = Column(String(100), index=True, nullable=False)
    texto_resena = Column(Text, nullable=False)
    sentimiento = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    author = relationship("User", back_populates="reviews")