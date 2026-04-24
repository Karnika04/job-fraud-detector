from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

import joblib

from .config import settings


class ModelNotFoundError(RuntimeError):
    """Raised when the model or vectorizer file is missing."""


def _load_artifact(path: str) -> Any:
    """Load a joblib artifact from disk."""

    if not os.path.exists(path):
        raise ModelNotFoundError(f"Artifact not found at path: {path}")
    return joblib.load(path)


@lru_cache()
def get_model() -> Any:
    """Return the trained job fraud detection model."""

    return _load_artifact(settings.model_path)


@lru_cache()
def get_vectorizer() -> Any:
    """Return the TF-IDF vectorizer."""

    return _load_artifact(settings.vectorizer_path)

