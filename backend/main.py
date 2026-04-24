from __future__ import annotations

from typing import List

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import schemas
from .config import settings
from .database import init_db, get_db, JobCheck, Base, engine
from .predictor import predict_single


app = FastAPI(title="Online Job Fraud Detection Platform")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin, "http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    """Initialize resources on startup."""

    init_db()

    # Ensure database tables exist
    Base.metadata.create_all(bind=engine)


@app.get("/health", response_model=schemas.HealthResponse)
def health_check() -> schemas.HealthResponse:
    """Health check endpoint."""

    return schemas.HealthResponse()


@app.post("/predict", response_model=schemas.PredictResponse)
def predict_job(
    payload: schemas.PredictRequest,
    db: Session = Depends(get_db),
) -> schemas.PredictResponse:
    """Predict whether a job is fraudulent or real."""

    result, rule_matches = predict_single(
        title=payload.title,
        description=payload.description,
        company_profile=payload.company_profile,
        requirements=payload.requirements,
    )

    job_record = JobCheck(
        title=payload.title,
        description=payload.description,
        prediction=result["prediction"],
        fraud_probability=result["fraud_probability"],
        rule_score=result["rule_score"],
    )

    try:
        db.add(job_record)
        db.commit()
        db.refresh(job_record)
    except Exception as e:
        print("DB ERROR:", e)

    return schemas.PredictResponse(
        prediction=result["prediction"],
        fraud_probability=result["fraud_probability"],
        rule_score=result["rule_score"],
        explanation=result["explanation"] or rule_matches,
    )


@app.get("/history", response_model=schemas.JobHistoryList)
def get_history(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
) -> schemas.JobHistoryList:
    """Return paginated history of checked jobs."""

    query = db.query(JobCheck).order_by(JobCheck.created_at.desc())
    total = query.count()
    items: List[JobCheck] = query.offset(skip).limit(limit).all()

    return schemas.JobHistoryList(items=items, total=total)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=True,
    )