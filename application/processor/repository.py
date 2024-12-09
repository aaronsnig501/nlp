from application.processor.processors.entities import Token
from .models import (
    ProcessRequest,
    ProcessRequestTokens,
    Token as TokenModel,
)


class ProcessorRepository:
    async def save_process_request(
        self, processor_name: str, language_code: str, client_id: str
    ) -> ProcessRequest:
        process_request = ProcessRequest(
            processor=processor_name, language_code=language_code, client_id=client_id
        )
        await process_request.save()
        return process_request

    async def save_process_request_with_tokens(
        self, processed_tokens: list[Token], process_request: ProcessRequest
    ) -> list[TokenModel]:
        tokens: list[TokenModel] = []
        process_request_tokens: list[ProcessRequestTokens] = []
        for token in processed_tokens:
            token = TokenModel(word=token.text, tag=token.tag)
            await token.save()
            tokens.append(token)

        for token in tokens:
            process_request_tokens.append(
                ProcessRequestTokens(process_request=process_request, token=token)
            )
        await ProcessRequestTokens.bulk_create(process_request_tokens)

        return tokens
