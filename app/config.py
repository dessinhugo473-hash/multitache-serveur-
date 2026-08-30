from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration de l'application, lue depuis les variables d'environnement (.env)."""

    redis_url: str = "redis://redis:6379/0"
    app_name: str = "multitask-server"
    log_level: str = "info"

    class Config:
        env_file = ".env"


settings = Settings()
