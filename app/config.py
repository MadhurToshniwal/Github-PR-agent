from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """Application configuration settings"""
    
    # API Keys
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    GITHUB_TOKEN: str = ""
    
    # LLM Provider (openai, groq, anthropic)
    LLM_PROVIDER: str = "groq"
    
    # Application
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    APP_NAME: str = "PR Review Agent"
    APP_VERSION: str = "1.0.0"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_ENABLED: bool = False
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # PR Review Settings
    MAX_PR_SIZE: int = 1000
    MAX_FILE_SIZE_KB: int = 500
    SUPPORTED_LANGUAGES: str = "python,javascript,typescript,java,go,rust"
    REVIEW_TIMEOUT_SECONDS: int = 300
    
    # Agent Configuration
    DEFAULT_LLM_MODEL: str = "llama-3.1-70b-versatile"  # Groq model (or gpt-4-turbo-preview for OpenAI)
    TEMPERATURE: float = 0.1
    MAX_TOKENS: int = 2000
    
    # Webhook
    WEBHOOK_SECRET: str = ""
    WEBHOOK_ENABLED: bool = False
    
    # Monitoring
    SENTRY_DSN: str = ""
    SENTRY_ENABLED: bool = False
    
    # Database
    DATABASE_URL: str = "sqlite:///./pr_review.db"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported programming languages"""
        return [lang.strip() for lang in self.SUPPORTED_LANGUAGES.split(",")]


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


settings = get_settings()
