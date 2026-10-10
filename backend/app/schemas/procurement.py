from pydantic import BaseModel, Field

class FarmerListingCreate(BaseModel):
    farmerName: str = Field(..., min_length=2, example="Ramesh Kumar")
    cropType: str = Field(..., example="Wheat (Lokwan)")
    quantityQuintals: float = Field(..., gt=0, le=10000, example=50.0)
    pricePerQuintal: float = Field(..., gt=100, example=2300.0)
    location: str = Field(..., min_length=2, example="Karnal, Haryana")
    whatsappAlerts: bool = Field(default=True)

class OrderStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(Pending|Matched|In-Transit|Completed)$")

class ProcurementOrderResponse(BaseModel):
    id: str
    farmer: str
    crop: str
    qty: str
    quantityQuintals: float
    pricePerQuintal: float
    location: str
    value: str
    numericValue: float
    status: str
    whatsappAlerts: bool
    createdAt: str
