from pydantic import BaseModel, Field
from typing import Optional

class SurplusDonationCreate(BaseModel):
    donorOrg: str = Field(..., min_length=2, example="Royal Palace Banquet")
    category: str = Field(..., example="Cooked Meals (Veg)")
    servings: int = Field(..., ge=5, le=50000, example=150)
    pickupWindowHours: str = Field(..., example="Next 3 Hours")
    locationZone: str = Field(..., example="North Sector 4")

class SurplusReserveRequest(BaseModel):
    ngoId: str = Field(..., example="Feeding Hope NGO - Registration #782")
    estimatedPickupTime: Optional[str] = Field(default="Within 45 Minutes")

class SurplusDonationResponse(BaseModel):
    id: str
    donor: str
    food: str
    servings: int
    window: str
    location: str
    isReserved: bool
    reservedByNGO: Optional[str] = None
    estimatedPickupTime: Optional[str] = None
    createdAt: str
