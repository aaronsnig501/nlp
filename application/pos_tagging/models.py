from tortoise import Model
from tortoise.fields import IntField, CharField, ForeignKeyField, ManyToManyField


class ProcessRequest(Model):

    id = IntField(primary_key=True)
    processor = CharField(max_length=15)
    language_code = CharField(max_length=5)
    client_id = CharField(max_length=50)
    tokens = ManyToManyField(
        "models.Token",
        related_name="tokens",
        through="ProcessRequestTokens"
    )

    class Meta: # type: ignore
        table = "process_request"

    def __str__(self):
        return f"{self.client_id}: {self.processor}-{self.language_code}"


class Token(Model):

    id = IntField(primary_key=True)
    word = CharField(max_length=50)
    tag = CharField(max_length=50)

    class Meta: # type: ignore
        table = "token"
        unique_together = ("word", "tag")

    def __str__(self) -> str:
        return f"{self.word}: {self.tag}"


class ProcessRequestTokens(Model):
    process_request = ForeignKeyField("models.ProcessRequest")
    token = ForeignKeyField("models.Token")

    class Meta: # type: ignore
        table = "process_request_tokens"
