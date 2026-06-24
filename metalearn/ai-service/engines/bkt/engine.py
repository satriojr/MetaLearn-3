"""
Bayesian Knowledge Tracing (BKT) Engine.

Estimates student mastery probability for each knowledge component
using a simplified Bayesian model:

P(mastery) = P(mastery|correct) or P(mastery|incorrect)

With parameters:
- p_learn: probability of learning from one opportunity
- p_guess: probability of guessing correctly without knowledge
- p_slip: probability of slipping (wrong despite knowing)
- p_init: initial probability of mastery
"""

from typing import Optional


class BKTEngine:
    DEFAULT_PARAMS = {
        "p_learn": 0.15,
        "p_guess": 0.10,
        "p_slip": 0.05,
        "p_init": 0.20,
    }

    def __init__(self, params: Optional[dict] = None):
        self.params = {**self.DEFAULT_PARAMS, **(params or {})}

    def update_mastery(
        self,
        prior_mastery: float,
        is_correct: bool,
    ) -> float:
        p_init = prior_mastery
        p_learn = self.params["p_learn"]
        p_guess = self.params["p_guess"]
        p_slip = self.params["p_slip"]

        if is_correct:
            p_correct = p_init * (1 - p_slip) + (1 - p_init) * p_guess
            if p_correct == 0:
                return p_init
            p_mastery_given_correct = (p_init * (1 - p_slip)) / p_correct
            return p_mastery_given_correct + (1 - p_mastery_given_correct) * p_learn
        else:
            p_incorrect = p_init * p_slip + (1 - p_init) * (1 - p_guess)
            if p_incorrect == 0:
                return p_init
            p_mastery_given_incorrect = (p_init * p_slip) / p_incorrect
            return p_mastery_given_incorrect + (1 - p_mastery_given_incorrect) * p_learn

    def estimate_mastery(
        self,
        correct_count: int,
        total_count: int,
        streak: int = 0,
    ) -> float:
        if total_count == 0:
            return self.params["p_init"]

        mastery = self.params["p_init"]
        # Simulate sequence: we don't know the order, so use a simplified estimate
        for _ in range(total_count - streak):
            mastery = self.update_mastery(mastery, is_correct=False)
        for _ in range(streak):
            mastery = self.update_mastery(mastery, is_correct=True)

        avg_correct = correct_count / total_count
        for _ in range(total_count):
            mastery = self.update_mastery(mastery, is_correct=avg_correct > 0.5)

        return min(max(mastery, 0.0), 1.0)

    def should_remediate(self, mastery: float, threshold: float = 0.80) -> bool:
        return mastery < threshold

    def get_difficulty_adjustment(self, mastery: float) -> str:
        if mastery < 0.4:
            return "beginner"
        elif mastery < 0.7:
            return "intermediate"
        else:
            return "advanced"
