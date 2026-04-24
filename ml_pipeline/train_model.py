import os

import numpy as np

from scipy.sparse import hstack

from .preprocessing import run_preprocessing_pipeline, PROCESSED_DATA_PATH
from .feature_engineering import (
    vectorize_text,
    create_metadata_features,
    create_train_test_splits,
)
from .model_training import apply_smote, train_models, select_best_model
from .evaluation import plot_metric_comparison
from .save_model import save_artifacts


def run_training() -> None:
    """Run end-to-end model training pipeline."""

    df, processed_path = run_preprocessing_pipeline(
        input_path=os.path.join("data", "raw_dataset.csv"),
        output_path=PROCESSED_DATA_PATH,
    )

    train_df, test_df = create_train_test_splits(df)

    vectorizer, X_train_text = vectorize_text(train_df)
    X_train_meta = create_metadata_features(train_df)

    X_train = hstack([X_train_text, X_train_meta])
    y_train = train_df["fraudulent"].to_numpy()

    X_test_text = vectorizer.transform(test_df["full_text"].fillna(""))
    X_test_meta = create_metadata_features(test_df)
    X_test = hstack([X_test_text, X_test_meta])
    y_test = test_df["fraudulent"].to_numpy()

    X_train_balanced, y_train_balanced = apply_smote(X_train, y_train)

    models = train_models(X_train_balanced, y_train_balanced)
    best_name, best_model, metrics = select_best_model(models, X_test, y_test)

    os.makedirs("models", exist_ok=True)
    plot_metric_comparison(metrics, os.path.join("models", "model_comparison.png"))

    save_artifacts(
        model=best_model,
        vectorizer=vectorizer,
        metrics=metrics,
        model_path=os.path.join("models", "job_fraud_model.pkl"),
        vectorizer_path=os.path.join("models", "tfidf_vectorizer.pkl"),
        metrics_path=os.path.join("models", "model_metrics.json"),
    )

    print(f"Training completed. Best model: {best_name}")


if __name__ == "__main__":
    run_training()

