from application.shared.clients.decyphr.types import (
    NlpResponseDict,
    SentimentAnalysisResponseDict,
    TagsResponseDict,
)
from application.processor.processors.entities import (
    NormalisedNlp,
    Token,
    Assessment,
    SentimentAnalysis,
)
from application.processor.processors.glossary import GLOSSARY
from application.processor.processors.sentiments import map_mood, map_bias


class DecyphrNlpNormaliser:
    def _normalise_tokens(self, tags: list[TagsResponseDict]) -> list[Token]:
        tokens = [
            Token(
                text=tag["token"],
                tag=tag["tag"],
                display_name=GLOSSARY[tag["tag"]],
            )
            for tag in tags
        ]
        return tokens

    # def _convert_assessment_tokens_to_tokens

    def _normalise_sentiment_analysis(
        self, analysis: SentimentAnalysisResponseDict
    ) -> SentimentAnalysis:
        assessments = [
            Assessment(
                tokens=assessment["tokens"],
                mood=map_mood(assessment["polarity"]),
                bias=map_bias(assessment["subjectivity"]),
            )
            for assessment in analysis["assessment"]
        ]

        return SentimentAnalysis(
            text=analysis["text"],
            mood=map_mood(analysis["polarity"]),
            bias=map_bias(analysis["subjectivity"]),
            assessment=assessments,
        )

    def normalise(self, data: NlpResponseDict) -> NormalisedNlp:
        tokens = self._normalise_tokens(data["tags"])
        analysis = self._normalise_sentiment_analysis(data["analysis"])
        return NormalisedNlp(tokens=tokens, analysis=analysis)
