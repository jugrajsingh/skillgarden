"""Application settings using Pydantic Settings + YAML.

Configuration priority:
    1. Init args (highest) - Settings(yaml_file="production.env.yaml")
    2. Environment variables - AWS__AWS_REGION=us-west-2
    3. YAML configuration files - discovered in order, last existing wins
    4. Default values (lowest) - Field(default="us-east-1")

YAML discovery order (last existing file wins, missing files silently skipped):
    env.yaml          — base config (deployed via ConfigMap/secret in k8s)
    local.env.yaml    — local dev overrides (gitignored)

Override at runtime for scripts:
    Settings(yaml_file="production.env.yaml")

Usage:
    from config.settings import settings

    region = settings.aws.aws_region
    db_host = settings.postgres.host
"""

from functools import lru_cache

from pydantic import BaseModel, Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

# Discoverable YAML files in priority order (last existing file wins).
# Missing files are silently skipped by YamlConfigSettingsSource.
YAML_CONFIG_FILES = ["env.yaml", "local.env.yaml"]


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

    Configuration is loaded from (highest to lowest priority):
        1. Init args — Settings(yaml_file="production.env.yaml")
        2. Environment variables (use __ for nesting: POSTGRES__HOST)
        3. YAML files — env.yaml then local.env.yaml (last wins)
        4. Default values defined above

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
        yaml_file=YAML_CONFIG_FILES,
        yaml_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,  # noqa: ARG003
        file_secret_settings: PydanticBaseSettingsSource,  # noqa: ARG003
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Priority: init > env > YAML > defaults.

        Supports ``Settings(yaml_file="production.env.yaml")`` to override
        the discoverable YAML file list at construction time. Useful for
        scripts that need to run against non-local environments.
        """
        yaml_override = init_settings.init_kwargs.pop("yaml_file", None)
        yaml_source = (
            YamlConfigSettingsSource(settings_cls, yaml_file=yaml_override)
            if yaml_override
            else YamlConfigSettingsSource(settings_cls)
        )
        return (init_settings, env_settings, yaml_source)


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance.

    Settings are loaded once and cached for the lifetime of the application.
    To reload settings, clear the cache: get_settings.cache_clear()
    """
    return Settings()


# Convenience export
settings = get_settings()
