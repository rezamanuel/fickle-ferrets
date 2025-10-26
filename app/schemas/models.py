"""Pydantic models for request/response validation"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal


class Message(BaseModel):
    """Generic message response"""
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)


class ChampionPhraseResponse(BaseModel):
    """Current champion phrase"""
    phrase: str
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AffirmationResponse(BaseModel):
    """Response when affirmation is shared with ferrets"""
    affirmation_id: str = Field(..., description="Unique affirmation identifier")
    message: str = Field(..., description="Status message")


class FerretJoyResult(BaseModel):
    """Response from Spark API indicating if ferrets felt joy"""
    joy_sparked: bool


class WebhookCallback(BaseModel):
    """Webhook callback payload with ferret joy result"""
    affirmation_id: str = Field(..., description="Affirmation identifier")
    joy_sparked: bool = Field(..., description="Whether the words sparked joy in our fickle ferrets")
    timestamp: datetime = Field(default_factory=datetime.now)


class AffirmationHistoryItem(BaseModel):
    """History item for affirmations stored in database"""
    affirmation_id: str = Field(..., description="Unique affirmation identifier")
    words_of_affirmation: str = Field(..., description="The words shared with the ferrets")
    joy_sparked: bool = Field(..., description="Whether joy was sparked")
    created_at: datetime = Field(..., description="When the affirmation was created")
    callback_received_at: datetime | None = Field(None, description="When the callback was received")
    
    class Config:
        from_attributes = True  # Enables compatibility with SQLAlchemy models


class ExperimentCreate(BaseModel):
    """Request model for creating a new A/B test experiment"""
    name: str = Field(..., description="Name/description of the experiment")
    variant_b_phrase: str = Field(..., description="New phrase to test against current champion")
    target_runs: int = Field(default=100, ge=1, description="Number of affirmations to run for this experiment")


class ExperimentResponse(BaseModel):
    """Response model for experiment data with calculated win rates"""
    id: str
    name: str
    variant_a_phrase: str
    variant_b_phrase: str
    status: Literal["active", "completed"]
    target_runs: int
    created_at: datetime
    completed_at: datetime | None
    winning_variant: Literal["A", "B"] | None
    variant_a_wins: int | None
    variant_b_wins: int | None
    variant_a_total: int | None
    variant_b_total: int | None
    variant_a_win_rate: float | None
    variant_b_win_rate: float | None

