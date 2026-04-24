import re
import string
from typing import List

import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Ensure required NLTK resources are available
for resource in ["stopwords", "wordnet", "omw-1.4", "punkt"]:
    try:
        nltk.data.find(f"corpora/{resource}")
    except LookupError:
        nltk.download(resource)

STOPWORDS = set(stopwords.words("english"))
LEMMATIZER = WordNetLemmatizer()
PUNCT_TABLE = str.maketrans("", "", string.punctuation)


def strip_html(text: str) -> str:
    """Remove HTML tags from text."""
    if not text:
        return ""
    soup = BeautifulSoup(str(text), "html.parser")
    return soup.get_text(separator=" ")


def basic_cleanup(text: str) -> str:
    """Lowercase, remove punctuation and extra whitespace."""
    text = str(text).lower()
    text = text.translate(PUNCT_TABLE)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def remove_stopwords_and_lemmatize(tokens: List[str]) -> List[str]:
    """Remove stopwords and apply lemmatization."""
    cleaned_tokens: List[str] = []

    for token in tokens:
        if token in STOPWORDS or token.isdigit():
            continue

        lemma = LEMMATIZER.lemmatize(token)
        cleaned_tokens.append(lemma)

    return cleaned_tokens


def preprocess_text(text: str) -> str:
    """Full preprocessing pipeline for a single text string."""

    if not text:
        return ""

    text = strip_html(text)
    text = basic_cleanup(text)

    # Fast tokenization with NLTK instead of spaCy
    tokens = nltk.word_tokenize(text)

    tokens = remove_stopwords_and_lemmatize(tokens)

    return " ".join(tokens)


def build_full_text(description, requirements, company_profile, benefits):
    """Safely combine text columns even if NaN values exist."""

    parts = [description, requirements, company_profile, benefits]

    cleaned_parts = []
    for part in parts:
        if part is None:
            continue

        part = str(part)

        if part.lower() == "nan":
            continue

        cleaned_parts.append(part)

    return " ".join(cleaned_parts).strip()