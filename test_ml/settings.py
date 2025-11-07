from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    embed_model: str = "text-embedding-ada-002"
    embed_dim: int = 1536
    llm_model: str = "gpt-3.5-turbo"
    csv_file_path: str = "data/cocktails.csv"

    class Config:
        env_file = ".env"
