from enum import Enum


class Mood(str, Enum):
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    POSITIVE = "positive"


class Bias(str, Enum):
    OBJECTIVE = "objective"
    SUBJECTIVE = "subjective"


def map_mood(value: float) -> Mood:
    if value >= 0.25:
        return Mood.POSITIVE
    elif value <= -0.25:
        return Mood.NEGATIVE

    return Mood.NEUTRAL


def map_bias(value: float) -> Bias:
    if value > 0.5:
        return Bias.SUBJECTIVE
    return Bias.OBJECTIVE
