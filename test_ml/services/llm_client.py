# services/llm_client.py
import openai


class LLMClientService:
    
    def __init__(
            self,
            openai_api_key: str,
            model: str
    ):
        openai.api_key = openai_api_key
        self.model = model

    def generate_answer(
            self,
            prompt: str
    ) -> str:
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful cocktail assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=300
        )
        answer = response["choices"][0]["message"]["content"]
        return answer.strip()
