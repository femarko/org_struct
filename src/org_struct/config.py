from functools import lru_cache
from pydantic import PostgresDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)



class Settings(BaseSettings):
    postgres_host: str
    db_port: int
    postgres_user: str
    postgres_password: str
    postgres_db: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    @property
    def db_url(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql",
                username=self.postgres_user,
                password=self.postgres_password,
                host=self.postgres_host,
                port=self.db_port,
                path=self.postgres_db
            )
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore
