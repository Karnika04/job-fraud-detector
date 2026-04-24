from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = "running"


class PredictRequest(BaseModel):
    title: str = Field("", description="Job title")
    description: str = Field("", description="Job description")
    company_profile: str = Field("", description="Company profile")
    requirements: str = Field("", description="Job requirements")


class PredictResponse(BaseModel):
    prediction: str
    fraud_probability: float
    rule_score: int
    explanation: List[str]


class JobHistoryItem(BaseModel):
    id: int
    title: str
    description: str
    prediction: str
    fraud_probability: float
    rule_score: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class JobHistoryList(BaseModel):
    items: List[JobHistoryItem]
    total: int