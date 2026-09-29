from pydantic import BaseModel, ConfigDict, EmailStr, Field

class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class HomeRequest(BaseModel):
    budget: float = Field(gt=0)
    room_type: str = Field(min_length=2, max_length=80)
    style: str = Field(default="Modern", max_length=80)
    items: str = Field(default="lights, ceiling fan, table", max_length=500)

class PartyRequest(BaseModel):
    budget: float = Field(gt=0)
    guests: int = Field(gt=0, le=10000)
    event_type: str = Field(min_length=2, max_length=80)
    venue: str = Field(default="Home", max_length=100)
    preferences: str = Field(default="", max_length=500)

class RecommendationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    planner_type: str
    recommendations: list[dict]
    budget: float
    summary: str
