from __future__ import annotations

from typing import Dict, Any, Tuple, List

import numpy as np

from .model_loader import get_model, get_vectorizer
from .preprocessing import preprocess_text
from .fraud_rules import evaluate_rules
from .explainability import get_top_feature_explanations


def _build_metadata_features(
    text: str,
    company_profile: str,
    salary_text: str | None = None,
) -> np.ndarray:
    """Create simple metadata features."""

    description_length = len(text.split())
    has_company_profile = 1 if company_profile and company_profile.strip() else 0
    salary_present = 1 if salary_text and salary_text.strip() else 0
    has_logo = 0

    return np.array([[description_length, has_company_profile, salary_present, has_logo]])


def predict_single(
    title: str,
    description: str,
    company_profile: str,
    requirements: str,
) -> Tuple[Dict[str, Any], List[str]]:
    """Run full prediction pipeline for a single job posting."""

    # 🔹 Combine all text
    full_text_raw = " ".join(
        part
        for part in [
            description or "",
            requirements or "",
            company_profile or "",
        ]
        if part
    )

    # 🔹 Preprocess text
    cleaned_text = preprocess_text(full_text_raw)

    # 🔹 Load model & vectorizer
    vectorizer = get_vectorizer()
    model = get_model()

    # 🔹 Transform text
    text_vector = vectorizer.transform([cleaned_text])

    # 🔹 Metadata features
    metadata = _build_metadata_features(
        text=cleaned_text,
        company_profile=company_profile,
        salary_text=None,
    )

    # 🔹 Combine features
    from scipy.sparse import hstack

    final_features = hstack([text_vector, metadata])

    # 🔹 ML prediction
    proba = model.predict_proba(final_features)[0][1]

    # 🔹 Rule-based evaluation
    rule_score, rule_matches = evaluate_rules(full_text_raw)

    # 🔥 HYBRID DECISION LOGIC (MAIN FIX)

    if rule_score >= 2:
        prediction_label = "Fraud"
        proba = max(proba, 0.7)  # boost confidence

    elif proba >= 0.4:
        prediction_label = "Fraud"

    else:
        prediction_label = "Real"

    # 🔹 Explanation
    try:
        explanation_words = get_top_feature_explanations(
            model=model,
            vectorizer=vectorizer,
            text_vector=final_features,
            top_k=5,
        )
    except Exception:
        explanation_words = rule_matches

    # 🔹 Final response
    response = {
        "prediction": prediction_label,
        "fraud_probability": float(proba),
        "rule_score": int(rule_score),
        "explanation": explanation_words or rule_matches,
    }

    return response, rule_matches