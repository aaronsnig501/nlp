from enum import Enum


class Mood(str, Enum):
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    POSITIVE = "positive"


class Bias(str, Enum):
    OBJECTIVE = "objective"
    SUBJECTIVE = "subjective"


def map_mood(value: float) -> Mood:
    """Provide a text value for the analysis score given to the sentiment anaylsis

    Args:
        value (float): The score

    Returns:
        Mood: The mood
    """
    if value >= 0.25:
        return Mood.POSITIVE
    elif value <= -0.25:
        return Mood.NEGATIVE

    return Mood.NEUTRAL


def map_bias(value: float) -> Bias:
    """Provide a text value for the subjectivity score given to the sentiment anaylsis

    Args:
        value (float): The score

    Returns:
        Bias: The bias
    """
    if value > 0.5:
        return Bias.SUBJECTIVE
    return Bias.OBJECTIVE
