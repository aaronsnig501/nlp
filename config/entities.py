from dataclasses import dataclass


@dataclass
class ServerConfig:
    host: str
    port: int


@dataclass
class AWSConfig:
    aws_access_key: str
    aws_secret_key: str


@dataclass
class RedisConfig:
    uri: str
    channel: str


@dataclass
class DatabaseConfig:
    uri: str


@dataclass
class NlpConfig:
    url: str


@dataclass
class Config:
    server: ServerConfig
    aws: AWSConfig
    redis: RedisConfig
    database: DatabaseConfig
    nlp: NlpConfig
