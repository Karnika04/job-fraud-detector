from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class FraudRule:
    """Represents a simple keyword-based fraud rule."""

    phrase: str
    weight: int


DEFAULT_RULES: List[FraudRule] = [
    FraudRule("registration fee", 2),
    FraudRule("earn money fast", 2),
    FraudRule("no experience required", 1),
    FraudRule("work from home high salary", 2),
    FraudRule("urgent hiring", 1),
    FraudRule("quick money", 1),
    FraudRule("limited seats", 1),
]


def evaluate_rules(text: str, rules: List[FraudRule] | None = None) -> Tuple[int, List[str]]:
    """Evaluate fraud rules on given text and return score and matched phrases."""

    if not text:
        return 0, []

    if rules is None:
        rules = DEFAULT_RULES

    text_lower = text.lower()
    score = 0
    matches: List[str] = []

    for rule in rules:
        if rule.phrase in text_lower:
            score += rule.weight
            matches.append(rule.phrase)

    return score, matches

