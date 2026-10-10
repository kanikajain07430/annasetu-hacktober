from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: str = Field(..., pattern="^(farmer|vendor|ngo|admin)$")
    fullName: str = Field(..., min_length=2)
    phone: Optional[str] = None

class UserLogin(BaseModel):
    usernameOrEmail: str
    password: str

class TokenResponse(BaseModel):
    accessToken: str
    tokenType: str = "bearer"
    role: str
    username: str
    fullName: str
