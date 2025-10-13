"""Pydantic models for request/response validation"""
from pydantic import BaseModel, Field
from datetime import datetime


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

