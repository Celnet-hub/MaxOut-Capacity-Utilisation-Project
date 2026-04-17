from fastapi import APIRouter, status
from fastapi import APIRouter, status, BackgroundTasks
from middleware.schemas.netboss_network import TelemetryCreate, TelemetryResponse
from middleware.services.alerts import async_processing

router = APIRouter(tags=["Telemetry"])


@router.post("/telemetry", response_model=TelemetryResponse, status_code=status.HTTP_201_CREATED)
def ingest_telemetry(payload: TelemetryCreate, background_tasks: BackgroundTasks):

    """
    Ingests telemetry. Instantly returns ACK to prevent Netboss from blocking.
    Actual processing happens in the background.
    """

    # Hand the raw data off to background worker
    background_tasks.add_task(
        async_processing, 
        circuit_id=payload.circuit_id, 
        current_utilization=payload.utilization_mbps
    )

    return TelemetryResponse(
        message="Alert ingested successfully",
        recorded_utilization=payload.utilization_mbps
    )
