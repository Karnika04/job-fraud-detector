from typing import Dict, Tuple

import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)
from xgboost import XGBClassifier


def apply_smote(X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Balance classes using SMOTE."""

    smote = SMOTE(random_state=42)
    X_res, y_res = smote.fit_resample(X, y)
    return X_res, y_res


def train_models(
    X_train: np.ndarray,
    y_train: np.ndarray,
) -> Dict[str, object]:
    """Train Logistic Regression, Random Forest, and XGBoost models."""

    models: Dict[str, object] = {}

    lr = LogisticRegression(max_iter=1000, n_jobs=-1)
    lr.fit(X_train, y_train)
    models["logistic_regression"] = lr

    rf = RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        random_state=42,
        n_jobs=-1,
    )
    rf.fit(X_train, y_train)
    models["random_forest"] = rf

    xgb = XGBClassifier(
        n_estimators=300,
        learning_rate=0.1,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric="logloss",
        random_state=42,
        n_jobs=-1,
        use_label_encoder=False,
    )
    xgb.fit(X_train, y_train)
    models["xgboost"] = xgb

    return models


def evaluate_model(
    model: object,
    X_test: np.ndarray,
    y_test: np.ndarray,
) -> Dict[str, float]:
    """Evaluate a binary classification model."""

    y_pred = model.predict(X_test)
    if hasattr(model, "predict_proba"):
        y_proba = model.predict_proba(X_test)[:, 1]
    else:
        y_proba = y_pred

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1": f1_score(y_test, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, y_proba),
    }
    return metrics


def select_best_model(
    models: Dict[str, object],
    X_test: np.ndarray,
    y_test: np.ndarray,
) -> Tuple[str, object, Dict[str, Dict[str, float]]]:
    """Select best model based on F1-score."""

    all_metrics: Dict[str, Dict[str, float]] = {}
    best_name = ""
    best_model = None
    best_f1 = -1.0

    for name, model in models.items():
        metrics = evaluate_model(model, X_test, y_test)
        all_metrics[name] = metrics
        if metrics["f1"] > best_f1:
            best_f1 = metrics["f1"]
            best_name = name
            best_model = model

    return best_name, best_model, all_metrics

