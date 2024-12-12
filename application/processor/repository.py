from tortoise.exceptions import DoesNotExist

from application.processor.processors.entities import Token, SentimentAnalysis
from .models import (
    Assessment,
    ProcessRequest,
    ProcessRequestTokens,
    SentimentAnalysis as SentimentAnalysisModel,
    Token as TokenModel,
)


class ProcessorRepository:
    async def save_process_request(
        self, processor_name: str, language_code: str, client_id: str, text: str
    ) -> ProcessRequest:
        """Store the `ProcessRequest` in the DB

        Args:
            processor_name (str): The name of the processor
            language_code (str): The ISO 3166-1 alpha-2 of the text language
            client_id (str): UUID identifier
            text (str): Text to process

        Returns:
            ProcessRequest: The instance of the `ProcessRequest`
        """
        process_request = ProcessRequest(
            processor=processor_name,
            language_code=language_code,
            client_id=client_id,
            text=text,
        )
        await process_request.save()
        return process_request

    async def save_process_request_with_tokens(
        self,
        processed_tokens: list[Token],
        analysis: SentimentAnalysis,
        process_request: ProcessRequest,
    ) -> list[TokenModel]:
        """Store the `ProcessRequestTokes` in the DB

        Args:
            processed_tokens (list[Token]): The tokens to store
            process_request (ProcessRequest): The ProcessRequest to store

        Returns:
            list[TokenModel]: The stored tokens
        """
        tokens: list[TokenModel] = []

        for token in processed_tokens:
            try:
                if TokenModel.exists(word=token.text, tag=token.tag):
                    token_model = await TokenModel.get(word=token.text, tag=token.tag)
            except DoesNotExist:
                token_model = TokenModel(word=token.text, tag=token.tag)
                await token_model.save()
            finally:
                tokens.append(token_model)  # type: ignore

        sentiment_analysis = await SentimentAnalysisModel.create(
            text=analysis.text,
            mood=analysis.mood,
            bias=analysis.bias,
        )

        assessments_to_save: list[Assessment] = []
        for assessment in analysis.assessment:
            assessment_to_save = await Assessment.create(
                mood=assessment.mood, bias=assessment.bias
            )
            for assessment_token in assessment.tokens:
                for token in tokens:
                    if assessment_token == token.word:
                        await assessment_to_save.tokens.add(token)
                        await sentiment_analysis.assessments.add(assessment_to_save)
                        break
            assessments_to_save.append(assessment_to_save)

        process_request_tokens: list[ProcessRequestTokens] = []
        for token in tokens:
            process_request_tokens.append(
                ProcessRequestTokens(
                    process_request=process_request,
                    token=token,
                    sentiment_analysis=sentiment_analysis,
                )
            )
        await ProcessRequestTokens.bulk_create(process_request_tokens)

        return tokens
