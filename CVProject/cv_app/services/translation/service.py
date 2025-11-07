from cv_app.models import CV
from cv_app.services.translation.translator import OpenAITranslator


class TranslationService:

    def __init__(self) -> None:
        self.translator = OpenAITranslator()

    def translate(self, cv_pk: int, target_language: str) -> str:
        cv = (
            CV.objects
              .only("id", "firstname", "lastname", "bio", "skills", "projects", "contacts")
              .get(pk=cv_pk)
        )
        return self.translator.translate(cv, target_language)
