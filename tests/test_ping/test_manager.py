from typing import Any
from pytest import mark
from application.ping.entities import HealthStatus
from application.ping.manager import PingManager


class TestPingManager:
    @mark.asyncio
    async def test_get_health_status(self, mocker: Any) -> None:
        mocker.patch.object(
            PingManager,
            "_perform_application_health_check",
            return_value=HealthStatus("application", True),
        )

        manager = PingManager()
        assert await manager.get_health_status() == [
            HealthStatus("application", True),
        ]
