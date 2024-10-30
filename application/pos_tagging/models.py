from sanic_motor import BaseModel


class PartOfSpeechTags(BaseModel):

    __coll__ = "part_of_speech_tags"
    __unique_fields__ = ["language", "text"]
