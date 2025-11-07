import os
import openai
import logging
from typing import Any
from cv_app.models import CV
from cv_app.services.translation.prompt_service import build_translation_prompt

logger = logging.getLogger(__name__)

class OpenAITranslator:

    def __init__(self, api_key: str | None = None) -> None:
        key = api_key or os.getenv("OPENAI_API_KEY")
        if not key:
            logger.error("OPENAI_API_KEY is not set")
            raise RuntimeError("OPENAI_API_KEY is not set")
        openai.api_key = key
        logger.debug("OpenAI API key loaded")

    def translate(self, cv: CV, target_language: str) -> str:
        prompt = build_translation_prompt(cv, target_language)
        response: Any = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional translator. Preserve formatting and lists."
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        text = response.choices[0].message.content.strip()
        return text
