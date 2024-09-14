from dataclasses import asdict

from sanic import Blueprint
from sanic.response import json
from sanic_ext import openapi

from .entities import HealthStatusResponse
from .manager import PingManager

bp = Blueprint("ping", url_prefix="/api")


@bp.get("/ping")
@openapi.summary("Perform health check")
@openapi.response(200, {"application/json": HealthStatusResponse})
async def ping(request, ping_manager: PingManager) -> dict[str, bool]:
    """Ping

    Ping endpoint to check the health of the application

    Example Usage:
        ```sh
        curl http://127.0.0.1:8000/api/ping | jq
        ```

    Example Response:
        ```json
        {
            "is_healthy": true,
            "status": [
                {
                    "name": "application",
                    "is_healthy": true
                }
            ]
        }
        ```
    """
    return json(
        asdict(HealthStatusResponse(True, await ping_manager.get_health_status()))
    )
