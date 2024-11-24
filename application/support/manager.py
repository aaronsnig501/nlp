from .models import Language


class SupportManager:

    async def get_supported_languages(self, service_name: str) -> dict[str, str]:
        """Get the supported languages for the given service

        Args:
            service_name (str): The name of the service to check for
        """
        languages = await Language.filter(
            nlp_service_languagess__service__name=service_name
        )

        supported_languages = {}
        supported_languages[service_name] = {}

        for language in languages:
            supported_languages[service_name][language.short_code] = language.name

        return supported_languages
