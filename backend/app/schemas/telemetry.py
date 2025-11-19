"""Telemetry schemas for API requests/responses"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class WellBase(BaseModel):
    name: str
    api_number: str
    field_id: int
    well_type: Optional[str] = "Producer"
    status: Optional[str] = "Active"


class WellCreate(WellBase):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    total_depth: Optional[float] = None


class WellResponse(WellBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class FieldBase(BaseModel):
    name: str
    code: str
    operator: str


class FieldCreate(FieldBase):
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class FieldResponse(FieldBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TelemetryReadingBase(BaseModel):
    well_id: int
    timestamp: datetime

    # Production
    oil_rate: Optional[float] = None
    gas_rate: Optional[float] = None
    water_rate: Optional[float] = None

    # Pressures
    wellhead_pressure: Optional[float] = None
    tubing_pressure: Optional[float] = None
    casing_pressure: Optional[float] = None

    # Temperatures
    wellhead_temperature: Optional[float] = None
    flowline_temperature: Optional[float] = None

    # Equipment
    choke_size: Optional[float] = None
    pump_status: Optional[bool] = None
    pump_speed: Optional[float] = None


class TelemetryReadingCreate(TelemetryReadingBase):
    source: str = "API"


class TelemetryReadingResponse(TelemetryReadingBase):
    id: int
    data_quality_score: float
    is_validated: bool
    is_anomaly: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TelemetryBatch(BaseModel):
    """Batch of telemetry readings for bulk upload"""
    readings: list[TelemetryReadingCreate]


class TelemetryStats(BaseModel):
    """Statistical summary of telemetry data"""
    well_id: int
    start_date: datetime
    end_date: datetime
    total_readings: int
    avg_oil_rate: Optional[float] = None
    avg_gas_rate: Optional[float] = None
    avg_water_rate: Optional[float] = None
    total_oil: Optional[float] = None
    total_gas: Optional[float] = None
    total_water: Optional[float] = None
    data_quality_avg: float
