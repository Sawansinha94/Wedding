from typing import Literal
from pydantic import BaseModel, Field
class ChatIn(BaseModel):
    question: str = Field(min_length=1,max_length=500)
    language: str = "en"
class WishIn(BaseModel):
    name: str = Field(default="",max_length=80)
    tone: str = "heartfelt"
    language: str = "en"

class Turn(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(max_length=1500)
class AgentChatIn(BaseModel):
    question: str = Field(min_length=1, max_length=1000)
    language: str = "en"
    history: list[Turn] = Field(default_factory=list, max_length=20)
    visitor_name: str = Field(default="", max_length=80)
    family_confirmation: str = Field(default="", max_length=100)
    verification_token: str = Field(default="", max_length=2000)

class PublicWish(BaseModel):
    name: str = Field(min_length=1,max_length=80)
    message: str = Field(min_length=1,max_length=1200)

class RSVPIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    attendance: str
    event: str
    guests: int = Field(ge=1, le=20)
    message: str = Field(default='', max_length=2000)

RSVP_ATTENDANCE = {'Joyfully accepts', 'Regretfully declines'}
RSVP_EVENTS = {'Wedding Ceremony', 'Reception & Blessings', 'Both events'}

