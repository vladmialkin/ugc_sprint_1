from pydantic import KafkaDsn, field_validator
from pydantic_core.core_schema import FieldValidationInfo

from app.settings.base import Settings


class KafkaSettings(Settings):
    KAFKA_HOST: str
    KAFKA_PORT: int
    # DSN: str | None = None

    # @field_validator("DSN", mode="before")
    # @classmethod
    # def assemble_dsn(cls, _: str | None, info: FieldValidationInfo) -> str:
    #     scheme = "kafka"
    #     host = info.data["KAFKA_HOST"]
    #     port = info.data["KAFKA_PORT"]
    #
    #     url = f"{host}:{port}"
    #     return KafkaDsn(url).unicode_string()


settings = KafkaSettings()
