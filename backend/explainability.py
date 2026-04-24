from __future__ import annotations

from typing import List, Any

import numpy as np
import shap


def get_top_feature_explanations(
    model: Any,
    vectorizer: Any,
    text_vector: np.ndarray,
    top_k: int = 5,
) -> List[str]:
    """Return top-k words contributing to the fraud prediction."""

    feature_names = np.array(vectorizer.get_feature_names_out())

    # Choose appropriate SHAP explainer based on model type
    if hasattr(model, "predict_proba") and "XGBClassifier" in type(model).__name__:
        explainer = shap.TreeExplainer(model)
    elif hasattr(model, "coef_"):
        explainer = shap.LinearExplainer(model, text_vector)
    else:
        explainer = shap.KernelExplainer(model.predict_proba, shap.sample(text_vector, 100))

    shap_values = explainer.shap_values(text_vector)

    # For binary classification shap_values is a list of length 2
    if isinstance(shap_values, list):
        shap_for_fraud = np.array(shap_values[1])[0]
    else:
        shap_for_fraud = np.array(shap_values)[0]

    # Get indices of top absolute SHAP values
    top_indices = np.argsort(-np.abs(shap_for_fraud))[:top_k]
    top_features = feature_names[top_indices]
    return top_features.tolist()

