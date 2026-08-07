from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    DATABASE_URL: str

    SECRET_KEY: str

    ALGORITHM: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int

    NEWS_API_KEY: str

    GNEWS_API_KEY: str
    GEMINI_API_KEY: str
    GUARDIAN_API_KEY: str

    GROQ_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
