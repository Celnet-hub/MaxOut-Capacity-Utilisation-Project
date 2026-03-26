from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional


# Telemetry Schemas (For the /telemetry endpoint)
class TelemetryCreate(BaseModel):
    """
    This defines the EXACT JSON payload we expect from the Netboss Simulator.
    """
    circuit_id: str = Field(..., description="The unique CID of the customer product", example="CIR-10023")
    pop: str = Field(..., description="describes the POP the customer is connecting to", example="Barnet")
    network_device: str = Field(..., description="The switch the customer connecting from", example="GB-BARNET-SW-001")
    utilization_mbps: float = Field(..., description="Current bandwidth utilization in Mbps", ge=0.0, example=95.5)
    timestamp: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc), 
        description="Time the metric was recorded"
    )

    class Config:
        from_attributes = True

class TelemetryResponse(BaseModel):
    """
    This defines what our API sends BACK to the simulator after successful ingestion.
    """
    status: str = Field(default="success", example="success")
    message: str = Field(..., example="Telemetry ingested successfully")
    recorded_utilization: float


# Event Schemas (For future dashboard endpoints)
# class MaxOutEventResponse(BaseModel):
#     id: int
#     product_id: int
#     notification_sent: bool
#     timestamp: datetime
    
#     class Config:
#         from_attributes = True