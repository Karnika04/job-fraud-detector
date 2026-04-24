import os
from typing import Tuple

import pandas as pd

from backend.preprocessing import preprocess_text, build_full_text


RAW_DATA_PATH = os.path.join("data", "raw_dataset.csv")
PROCESSED_DATA_PATH = os.path.join("data", "processed_dataset.csv")


def load_raw_dataset(path: str = RAW_DATA_PATH) -> pd.DataFrame:
    """Load the EMSCAD dataset."""

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Raw dataset not found at {path}. Please place the EMSCAD CSV there."
        )
    return pd.read_csv(path)


def clean_and_combine_text(df: pd.DataFrame) -> pd.DataFrame:
    """Create full_text column and preprocess it."""

    text_parts = ["description", "requirements", "company_profile", "benefits"]
    for col in text_parts:
        if col not in df.columns:
            df[col] = ""

    df["full_text_raw"] = df.apply(
        lambda row: build_full_text(
            description=row.get("description", ""),
            requirements=row.get("requirements", ""),
            company_profile=row.get("company_profile", ""),
            benefits=row.get("benefits", ""),
        ),
        axis=1,
    )

    df["full_text"] = df["full_text_raw"].astype(str).apply(preprocess_text)
    return df


def save_processed_dataset(df: pd.DataFrame, path: str = PROCESSED_DATA_PATH) -> None:
    """Save processed dataset to CSV."""

    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)


def run_preprocessing_pipeline(
    input_path: str = RAW_DATA_PATH,
    output_path: str = PROCESSED_DATA_PATH,
) -> Tuple[pd.DataFrame, str]:
    """Execute preprocessing pipeline end-to-end."""

    df = load_raw_dataset(input_path)
    df = clean_and_combine_text(df)
    save_processed_dataset(df, output_path)
    return df, output_path


if __name__ == "__main__":
    run_preprocessing_pipeline()

