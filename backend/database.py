from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

from .config import settings


Base = declarative_base()


class JobCheck(Base):
    """SQLAlchemy model for jobs_checked table."""

    __tablename__ = "jobs_checked"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    prediction = Column(String(50), nullable=False)
    fraud_probability = Column(Float, nullable=False)
    rule_score = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


engine = create_engine(settings.database_url, echo=False, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Create database tables if they do not exist."""

    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency that provides a transactional database session."""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

