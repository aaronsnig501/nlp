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
        """Normalise tokens

        Normalise and format the syntax token data from the NLP provider

        Args:
            tags (list[TagsResponseDict]): The token syntax data from the provider

        Returns:
            list[Token]: The Token data
        """
        tokens = [
            Token(
                text=tag["token"],
                tag=tag["tag"],
                display_name=GLOSSARY[tag["tag"]],
            )
            for tag in tags
        ]
        return tokens

    def _normalise_sentiment_analysis(
        self, analysis: SentimentAnalysisResponseDict
    ) -> SentimentAnalysis:
        """Normalise sentiment analysis

        Normalise and format the data sentiment analysis data from the NLP provider

        Args:
            analysis (SentimentAnalysisResponseDict):   The sentiment analysis data from
                                                        from the provider

        Returns:
            SentimentAnalysis: The SentimentAnalysis data
        """
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
        """Normalise and post process data

        Perform the post processing on the data that is returned from the NLP provider
        to ensure that the data is normalised

        Args:
            data (NlpResponseDict): The data from the NLP provider

        Returns:
            NormalisedNlp: The normalised data
        """
        tokens = self._normalise_tokens(data["tags"])
        analysis = self._normalise_sentiment_analysis(data["analysis"])
        return NormalisedNlp(tokens=tokens, analysis=analysis)