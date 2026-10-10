from pydantic import BaseModel
from typing import List

class CropVolumeBreakdown(BaseModel):
    crop: str
    percentage: float
    tons: float

class AnalyticsStatsResponse(BaseModel):
    connectedFarmers: int
    tonsProcured: float
    mealsSaved: int
    activeMandis: int
    procurementVolumeByCrop: List[CropVolumeBreakdown]
    foodSurplusEfficiencyPercent: float
    directIncomeUpliftPercent: float
    settlementWindowHours: int
