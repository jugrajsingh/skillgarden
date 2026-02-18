"""Application settings using Pydantic Settings + YAML.

Configuration priority:
    1. Environment variables (highest) - AWS__AWS_REGION=us-west-2
    2. YAML configuration file - local.env.yaml
    3. Default values (lowest) - Field(default="us-east-1")

Usage:
    from config.settings import settings

    region = settings.aws.aws_region
    db_host = settings.postgres.host
"""

from functools import lru_cache

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# =============================================================================
# Settings Sections (selected by user)
# =============================================================================


class PostgresSettings(BaseModel):
    """PostgreSQL connection settings."""

    host: str = Field(default="localhost")
    port: int = Field(default=5432)
    database: str = Field(default="app")
    user: str = Field(default="postgres")
    password: str = Field(default="")

    @property
    def dsn(self) -> str:
        """Generate connection string."""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    @property
    def async_dsn(self) -> str:
        """Generate async connection string."""
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class RedisSettings(BaseModel):
    """Redis connection settings."""

    host: str = Field(default="localhost")
    port: int = Field(default=6379)
    db: int = Field(default=0)
    password: str | None = Field(default=None)

    @property
    def url(self) -> str:
        """Generate Redis URL."""
        auth = f":{self.password}@" if self.password else ""
        return f"redis://{auth}{self.host}:{self.port}/{self.db}"


class AWSSettings(BaseModel):
    """AWS configuration."""

    aws_region: str = Field(default="us-east-1")
    endpoint_url: str | None = Field(default=None)
    access_key_id: str | None = Field(default=None)
    secret_access_key: str | None = Field(default=None)


class ElasticsearchSettings(BaseModel):
    """Elasticsearch cluster settings."""

    hosts: list[str] = Field(default_factory=lambda: ["http://localhost:9200"])
    username: str | None = Field(default=None)
    password: str | None = Field(default=None)
    verify_certs: bool = Field(default=True)


class SentrySettings(BaseModel):
    """Sentry error monitoring settings."""

    dsn: str | None = Field(default=None)
    environment: str | None = Field(default=None)
    traces_sample_rate: float = Field(default=0.1)


class LoggingSettings(BaseModel):
    """Logging configuration."""

    level: str = Field(default="INFO")
    format: str = Field(default="json")  # json or console
    show_timestamps: bool = Field(default=True)


class APISettings(BaseModel):
    """API server settings."""

    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    debug: bool = Field(default=False)
    cors_origins: list[str] = Field(default_factory=lambda: ["*"])


# =============================================================================
# Main Settings
# =============================================================================


class Settings(BaseSettings):
    """Application settings.

    Configuration is loaded from:
        1. Environment variables (use __ for nesting: POSTGRES__HOST)
        2. YAML file (local.env.yaml)
        3. Default values defined above

    Example environment variables:
        ENVIRONMENT=production
        POSTGRES__HOST=db.example.com
        POSTGRES__PASSWORD=secret
        AWS__AWS_REGION=us-west-2
    """

    environment: str = Field(default="local")
    debug: bool = Field(default=False)

    # Include selected sections (remove unused)
    postgres: PostgresSettings = Field(default_factory=PostgresSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    aws: AWSSettings = Field(default_factory=AWSSettings)
    elasticsearch: ElasticsearchSettings = Field(default_factory=ElasticsearchSettings)
    sentry: SentrySettings = Field(default_factory=SentrySettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    api: APISettings = Field(default_factory=APISettings)

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        yaml_file="local.env.yaml",
        yaml_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance.

    Settings are loaded once and cached for the lifetime of the application.
    To reload settings, clear the cache: get_settings.cache_clear()
    """
    return Settings()


# Convenience export
settings = get_settings()
