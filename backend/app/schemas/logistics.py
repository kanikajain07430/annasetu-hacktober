from pydantic import BaseModel, Field
from typing import Optional, List

class SmartMatchRequest(BaseModel):
    cropType: str = Field(..., example="Wheat (Lokwan)")
    quantity: float = Field(..., gt=0, example=120.0)
    originDistrict: str = Field(..., example="Karnal, Haryana")

class SmartMatchResponse(BaseModel):
    orderId: str
    matchFound: bool
    clusterOrigin: str
    destinationHub: str
    distanceKm: float
    estimatedDuration: str
    optimizedVehicle: str
    carbonReductionKg: float
    transitPassId: str
    routeCode: str
    qrHash: str
    logs: List[str]

class TransitPassResponse(BaseModel):
    passId: str
    orderId: Optional[str]
    commodity: str
    volume: str
    origin: str
    destination: str
    greenCorridorClearance: str
    qrHash: str
    vehicleType: str
    carbonReductionKg: float
    createdAt: str
