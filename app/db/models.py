"""SQLAlchemy database models"""
from sqlalchemy import Column, String, Boolean, DateTime, Integer
from datetime import datetime
from .base import Base


class ChampionPhrase(Base):
    """Store the current champion affirmation phrase"""
    __tablename__ = "champion_phrase"
    
    id = Column(Integer, primary_key=True, default=1)  # Always ID=1 (singleton)
    phrase = Column(String, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, nullable=False)
    
    def __repr__(self) -> str:
        return f"<ChampionPhrase(phrase={self.phrase})>"


class AffirmationResult(Base):
    """Store ferret affirmation results"""
    __tablename__ = "affirmation_results"
    
    affirmation_id = Column(String, primary_key=True, index=True)
    words_of_affirmation = Column(String, nullable=False)
    joy_sparked = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    callback_received_at = Column(DateTime, nullable=True)
    
    def __repr__(self) -> str:
        return f"<AffirmationResult(id={self.affirmation_id}, joy={self.joy_sparked})>"

