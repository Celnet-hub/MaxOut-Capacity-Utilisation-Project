from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from middleware.config.db import get_db
from middleware.schemas.netboss_network import TelemetryCreate, TelemetryResponse
from middleware.models.database import CustomerProduct

router = APIRouter(tags=["Telemetry"])


@router.post("/telemetry", response_model=TelemetryResponse, status_code=status.HTTP_201_CREATED)
def ingest_telemetry(payload: TelemetryCreate, db: Session = Depends(get_db)):
    """
    Ingests simulated network telemetry data from the Netboss Mock.
    """
    # Validate the Circuit ID against our database
    product = db.query(CustomerProduct).filter(
        CustomerProduct.cid == payload.circuit_id).first()

    if not product:
        # If the simulator sends a fake CID, reject it immediately
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Circuit ID {payload.circuit_id} not found in database."
        )

    threshold = product.provisioned_bandwidth_mbps * 0.95
    if payload.utilization_mbps >= threshold:
        print(
            f"⚠️ WARNING: {payload.circuit_id} is maxing out! ({payload.utilization_mbps} Mbps / {product.provisioned_bandwidth_mbps} Mbps)")

    return TelemetryResponse(
        message="Telemetry ingested successfully",
        recorded_utilization=payload.utilization_mbps
    )
