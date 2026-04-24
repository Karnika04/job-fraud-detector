import os
from typing import Any, Dict

import joblib


def save_artifacts(
    model: Any,
    vectorizer: Any,
    metrics: Dict[str, Dict[str, float]],
    model_path: str = "models/job_fraud_model.pkl",
    vectorizer_path: str = "models/tfidf_vectorizer.pkl",
    metrics_path: str = "models/model_metrics.json",
) -> None:
    """Persist model, vectorizer and metrics to disk."""

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)

    import json

    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

