from application.shared.clients.decyphr.types import NlpTaggingResponse
from application.processor.processors.entities import Token, Tokens


class DecyphrNlpNormaliser:
    def normalise(self, data: NlpTaggingResponse) -> Tokens:
        return Tokens(
            tokens=[Token(text=tag["token"], tag=tag["tag"]) for tag in data["tags"]]
        )
