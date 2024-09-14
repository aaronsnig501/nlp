from dataclasses import dataclass


@dataclass
class HealthStatus:
    name: str
    is_healthy: bool


@dataclass
class HealthStatusResponse:
    is_healthy: bool
    status: list[HealthStatus]
