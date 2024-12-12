from tortoise import Model
from tortoise.fields import (
    IntField,
    CharField,
    TextField,
    ForeignKeyField,
    ManyToManyField,
)


class ProcessRequest(Model):
    id = IntField(primary_key=True)
    processor = CharField(max_length=15)
    language_code = CharField(max_length=5)
    client_id = CharField(max_length=50)
    text = TextField()
    tokens = ManyToManyField(
        "models.Token",
        related_name="process_requests",
        through="process_request_tokens",
    )

    class Meta:  # type: ignore
        table = "process_request"

    def __str__(self):
        return f"{self.client_id}: {self.processor}-{self.language_code}"


class Token(Model):
    id = IntField(primary_key=True)
    word = CharField(max_length=50)
    tag = CharField(max_length=50)

    class Meta:  # type: ignore
        table = "token"
        unique_together = ("word", "tag")

    def __str__(self) -> str:
        return f"{self.word}: {self.tag}"


class ProcessRequestTokens(Model):
    process_request = ForeignKeyField("models.ProcessRequest")
    token = ForeignKeyField("models.Token")
    sentiment_analysis = ForeignKeyField(
        "models.SentimentAnalysis", blank=True, null=True
    )

    class Meta:  # type: ignore
        table = "process_request_tokens"


class AssessmentToken(Model):
    id = IntField(primary_key=True)
    token = ForeignKeyField("models.Token")
    assessment = ForeignKeyField("models.Assessment")

    class Meta:  # type: ignore
        table = "assessment_token"


class Assessment(Model):
    id = IntField(primary_key=True)
    mood = CharField(max_length=25)
    bias = CharField(max_length=25)
    tokens = ManyToManyField(
        "models.Token", related_name="assessments", through="assessment_token"
    )

    class Meta:  # type: ignore
        table = "assessment"


class SentimentAnalysisAssessment(Model):
    id = IntField(primary_key=True)
    sentiment_analysis = ForeignKeyField("models.SentimentAnalysis")
    assessment = ForeignKeyField("models.Assessment")

    class Meta:  # type: ignore
        table = "sentiment_analysis_assessment"


class SentimentAnalysis(Model):
    id = IntField(primary_key=True)
    text = TextField()
    mood = CharField(max_length=25)
    bias = CharField(max_length=25)
    assessments = ManyToManyField(
        "models.Assessment",
        related_name="sentiment_analysis",
        through="sentiment_analysis_assessment",
    )

    class Meta:  # type: ignore
        table = "sentiment_analysis"
