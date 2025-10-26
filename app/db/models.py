"""SQLAlchemy database models"""
from enum import Enum
from sqlalchemy import Column, String, Boolean, DateTime, Integer
from datetime import datetime
from .base import Base


class ExperimentStatus(str, Enum):
    """Experiment status values"""
    ACTIVE = "active"
    COMPLETED = "completed"


class Variant(str, Enum):
    """Experiment variant labels"""
    A = "A"
    B = "B"


class ChampionPhrase(Base):
    """Store the current champion affirmation phrase"""
    __tablename__ = "champion_phrase"

    id = Column(Integer, primary_key=True, default=1)  # Always ID=1 (singleton)
    phrase = Column(String, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, nullable=False)

    def __repr__(self) -> str:
        return f"<ChampionPhrase(phrase={self.phrase})>"


class Experiment(Base):
    """Store A/B test experiments for finding better affirmation phrases"""
    __tablename__ = "experiments"

    id = Column(String, primary_key=True)  # UUID
    name = Column(String, nullable=False)
    variant_a_phrase = Column(String, nullable=False)
    variant_b_phrase = Column(String, nullable=False)
    status = Column(String, nullable=False)  # "active", "completed"
    target_runs = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    completed_at = Column(DateTime, nullable=True)

    # Results (calculated and stored at completion)
    winning_variant = Column(String, nullable=True)  # "A" or "B"
    variant_a_wins = Column(Integer, nullable=True)
    variant_b_wins = Column(Integer, nullable=True)
    variant_a_total = Column(Integer, nullable=True)
    variant_b_total = Column(Integer, nullable=True)

    def __repr__(self) -> str:
        return f"<Experiment(id={self.id}, name={self.name}, status={self.status})>"


class AffirmationResult(Base):
    """Store ferret affirmation results"""
    __tablename__ = "affirmation_results"

    affirmation_id = Column(String, primary_key=True, index=True)
    words_of_affirmation = Column(String, nullable=False)
    joy_sparked = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    callback_received_at = Column(DateTime, nullable=True)

    # Experiment tracking (optional, only set when part of an A/B test)
    experiment_id = Column(String, nullable=True)  # References experiments.id

    def __repr__(self) -> str:
        return f"<AffirmationResult(id={self.affirmation_id}, joy={self.joy_sparked})>"

