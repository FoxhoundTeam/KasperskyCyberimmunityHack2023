from pydantic import BaseSettings


class Settings(BaseSettings):
    kafka_server: str
    kafka_topic: str
    private_key: str
    monitor_topic: str = "monitor"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
