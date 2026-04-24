from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split


def create_metadata_features(df: pd.DataFrame) -> np.ndarray:
    """Create additional metadata features."""

    description_length = df["description"].fillna("").apply(lambda x: len(str(x).split()))
    has_company_profile = df["company_profile"].fillna("").apply(lambda x: 1 if str(x).strip() else 0)
    salary_present = df["salary_range"].fillna("").apply(lambda x: 1 if str(x).strip() else 0)
    has_logo = df.get("has_company_logo", pd.Series([0] * len(df)))

    meta = np.vstack(
        [
            description_length.to_numpy(),
            has_company_profile.to_numpy(),
            salary_present.to_numpy(),
            has_logo.to_numpy(),
        ]
    ).T
    return meta


def vectorize_text(
    df: pd.DataFrame,
    max_features: int = 5000,
    ngram_range: Tuple[int, int] = (1, 2),
) -> Tuple[TfidfVectorizer, np.ndarray]:
    """Fit a TF-IDF vectorizer and transform full_text."""

    vectorizer = TfidfVectorizer(
        max_features=max_features,
        ngram_range=ngram_range,
        min_df=5,
    )
    X_text = vectorizer.fit_transform(df["full_text"].fillna(""))
    return vectorizer, X_text


def create_train_test_splits(
    df: pd.DataFrame,
    test_size: float = 0.2,
    random_state: int = 42,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Split dataframe into train and test sets."""

    train_df, test_df = train_test_split(
        df,
        test_size=test_size,
        random_state=random_state,
        stratify=df["fraudulent"],
    )
    return train_df, test_df

