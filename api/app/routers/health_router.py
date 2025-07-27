from fastapi import APIRouter

from ..models.domain_model import HealthCheckResponse

health_router = APIRouter(prefix="/health", tags=["health"])


@health_router.get("", response_model=HealthCheckResponse, include_in_schema=False)
def health_check() -> HealthCheckResponse:
    return HealthCheckResponse(status="ok")
