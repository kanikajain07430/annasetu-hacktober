from pydantic import BaseModel, Field
from typing import Optional

class GrievanceCreate(BaseModel):
    name: str = Field(..., min_length=2, example="Gurpreet Singh")
    category: str = Field(..., example="Payment Delay")
    issueDetails: str = Field(..., min_length=5, example="Delay in Direct Benefit transfer for Order ORD-8821.")

class GrievanceResponse(BaseModel):
    ticketId: str
    name: str
    category: str
    issueDetails: str
    status: str
    resolutionNotes: Optional[str] = None
    createdAt: str
