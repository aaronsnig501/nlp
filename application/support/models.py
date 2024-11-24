from tortoise import Model
from tortoise.fields import (
    IntField, CharField, ForeignKeyField, ManyToManyField, CASCADE
)


class Domain(Model):
    id = IntField(primary_key=True)
    name = CharField(max_length=25, null=False, blank=False)
    display_name = CharField(max_length=50, null=False, blank=False)
    services = ForeignKeyField(
        "models.Service", "services", on_delete=CASCADE, null=False, blank=False
    )

    class Meta: # type: ignore
        table = "nlp_domains"

    def __str__(self) -> str:
        return self.name


class Service(Model):
    id = IntField(primary_key=True)
    name = CharField(max_length=25, null=False, blank=False)
    display_name = CharField(max_length=50, null=False, blank=False)
    languages = ManyToManyField(
        "models.Language", related_name="langauges", through="ServiceLanguage"
    )

    class Meta: # type: ignore
        table = "nlp_services"

    def __str__(self) -> str:
        return self.name


class ServiceLanguage(Model):
    id = IntField(primary_key=True)
    service = ForeignKeyField("models.Service")
    language = ForeignKeyField("models.Language")

    class Meta: # type: ignore
        table = "nlp_service_languages"


class Language(Model):
    id = IntField(primary_key=True)
    name = CharField(max_length=25, null=False, blank=False)
    short_code = CharField(max_length=2, null=False, blank=False)
    long_code = CharField(max_length=8, null=False, blank=False)

    class Meta: # type: ignore
        table = "nlp_languages"

    def __str__(self) -> str:
        return f"{self.name} - {self.short_code} ({self.long_code})"
