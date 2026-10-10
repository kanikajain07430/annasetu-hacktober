from pydantic import BaseModel, Field

class MandiRateBase(BaseModel):
    crop: str = Field(..., example="Wheat (Lokwan)")
    district: str = Field(..., example="Karnal, Haryana")
    msp: float = Field(..., gt=0, example=2275.0)
    marketRate: float = Field(..., gt=0, example=2380.0)
    trend: str = Field(default="up", pattern="^(up|down)$")

class MandiRateCreate(MandiRateBase):
    pass

class MandiRateResponse(MandiRateBase):
    id: int
    updated_at: str
