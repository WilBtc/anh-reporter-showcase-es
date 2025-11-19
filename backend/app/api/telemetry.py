"""Telemetry data endpoints"""
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.telemetry import TelemetryReading, Well
from app.schemas.telemetry import (
    TelemetryReadingCreate,
    TelemetryReadingResponse,
    TelemetryBatch,
    TelemetryStats
)

router = APIRouter()


@router.post("/", response_model=TelemetryReadingResponse, status_code=201)
async def create_telemetry_reading(
    reading_data: TelemetryReadingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a single telemetry reading"""

    # Verify well exists
    result = await db.execute(select(Well).where(Well.id == reading_data.well_id))
    well = result.scalar_one_or_none()

    if not well:
        raise HTTPException(status_code=404, detail="Well not found")

    # Create reading
    new_reading = TelemetryReading(**reading_data.model_dump())
    db.add(new_reading)
    await db.commit()
    await db.refresh(new_reading)

    return new_reading


@router.post("/batch", status_code=201)
async def create_telemetry_batch(
    batch: TelemetryBatch,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create multiple telemetry readings in batch"""

    readings = [TelemetryReading(**reading.model_dump()) for reading in batch.readings]
    db.add_all(readings)
    await db.commit()

    return {
        "message": f"Successfully created {len(readings)} telemetry readings",
        "count": len(readings)
    }


@router.get("/", response_model=List[TelemetryReadingResponse])
async def list_telemetry_readings(
    well_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 144,  # Default to one day of readings
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List telemetry readings with filters"""

    query = select(TelemetryReading)

    filters = []
    if well_id:
        filters.append(TelemetryReading.well_id == well_id)
    if start_date:
        filters.append(TelemetryReading.timestamp >= start_date)
    if end_date:
        filters.append(TelemetryReading.timestamp <= end_date)

    if filters:
        query = query.where(and_(*filters))

    query = query.order_by(TelemetryReading.timestamp.desc()).offset(skip).limit(limit)

    result = await db.execute(query)
    readings = result.scalars().all()

    return readings


@router.get("/stats/{well_id}", response_model=TelemetryStats)
async def get_telemetry_stats(
    well_id: int,
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get statistical summary of telemetry data for a well"""

    # Default to last 24 hours if no dates provided
    if not end_date:
        end_date = datetime.utcnow()
    if not start_date:
        start_date = end_date - timedelta(days=1)

    # Query aggregated statistics
    result = await db.execute(
        select(
            func.count(TelemetryReading.id).label('total_readings'),
            func.avg(TelemetryReading.oil_rate).label('avg_oil_rate'),
            func.avg(TelemetryReading.gas_rate).label('avg_gas_rate'),
            func.avg(TelemetryReading.water_rate).label('avg_water_rate'),
            func.sum(TelemetryReading.oil_rate).label('total_oil'),
            func.sum(TelemetryReading.gas_rate).label('total_gas'),
            func.sum(TelemetryReading.water_rate).label('total_water'),
            func.avg(TelemetryReading.data_quality_score).label('data_quality_avg')
        ).where(
            and_(
                TelemetryReading.well_id == well_id,
                TelemetryReading.timestamp >= start_date,
                TelemetryReading.timestamp <= end_date
            )
        )
    )

    stats = result.one()

    return TelemetryStats(
        well_id=well_id,
        start_date=start_date,
        end_date=end_date,
        total_readings=stats.total_readings or 0,
        avg_oil_rate=float(stats.avg_oil_rate) if stats.avg_oil_rate else None,
        avg_gas_rate=float(stats.avg_gas_rate) if stats.avg_gas_rate else None,
        avg_water_rate=float(stats.avg_water_rate) if stats.avg_water_rate else None,
        total_oil=float(stats.total_oil) if stats.total_oil else None,
        total_gas=float(stats.total_gas) if stats.total_gas else None,
        total_water=float(stats.total_water) if stats.total_water else None,
        data_quality_avg=float(stats.data_quality_avg) if stats.data_quality_avg else 0.0
    )


@router.get("/{reading_id}", response_model=TelemetryReadingResponse)
async def get_telemetry_reading(
    reading_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get a specific telemetry reading"""

    result = await db.execute(
        select(TelemetryReading).where(TelemetryReading.id == reading_id)
    )
    reading = result.scalar_one_or_none()

    if not reading:
        raise HTTPException(status_code=404, detail="Telemetry reading not found")

    return reading
