from typing import Any

from pydantic import AmqpDsn, BaseSettings, Field, HttpUrl, validator


class Settings(BaseSettings):
    kafka_server: str
    kafka_topic: str
    source_key_map: dict[str, str] = Field(default_factory=dict)
    policies: set[tuple[str, str]] = Field(default_factory=set)

    broker_server: str = "localhost"
    broker_port: str = "5672"
    broker_user: str = "guest"
    broker_pass: str = "guest"

    opensearch_scheme: str = "http"
    opensearch_host: str = "localhost"
    opensearch_port: str = "9200"
    opensearch_username: str = "admin"
    opensearch_password: str = "admin"

    broker_uri: AmqpDsn | None = None
    opensearch_uri: HttpUrl | None = None

    @validator("broker_uri", pre=True)
    def assemble_broker_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return AmqpDsn.build(
            scheme="amqp",
            host=values.get("broker_server"),
            user=values.get("broker_user"),
            password=values.get("broker_pass"),
            port=values.get("broker_port"),
        )

    @validator("opensearch_uri", pre=True)
    def assemble_opensearch_connection(
        cls,
        v: str | None,
        values: dict[str, Any],
    ) -> Any:
        if isinstance(v, str):
            return v
        return HttpUrl.build(
            scheme=values.get("opensearch_scheme"),
            host=values.get("opensearch_host"),
            port=values.get("opensearch_port"),
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
