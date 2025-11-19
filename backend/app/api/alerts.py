"""Alerts and Anomalies endpoints"""
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.alert import Alert, Anomaly, AlertSeverity, AlertType

router = APIRouter()


@router.get("/")
async def list_alerts(
    severity: Optional[AlertSeverity] = None,
    is_resolved: bool = False,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List alerts with filters"""

    query = select(Alert).where(Alert.is_resolved == is_resolved)

    if severity:
        query = query.where(Alert.severity == severity)

    query = query.order_by(Alert.created_at.desc()).offset(skip).limit(limit)

    result = await db.execute(query)
    alerts = result.scalars().all()

    return [
        {
            "id": alert.id,
            "type": alert.type,
            "severity": alert.severity,
            "title": alert.title,
            "description": alert.description,
            "well_id": alert.well_id,
            "value": alert.value,
            "threshold": alert.threshold,
            "is_resolved": alert.is_resolved,
            "created_at": alert.created_at
        }
        for alert in alerts
    ]


@router.get("/{alert_id}")
async def get_alert(
    alert_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get alert details"""

    result = await db.execute(select(Alert).where(Alert.id == alert_id))
    alert = result.scalar_one_or_none()

    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    return {
        "id": alert.id,
        "type": alert.type,
        "severity": alert.severity,
        "title": alert.title,
        "description": alert.description,
        "well_id": alert.well_id,
        "field_id": alert.field_id,
        "value": alert.value,
        "threshold": alert.threshold,
        "metric_name": alert.metric_name,
        "is_resolved": alert.is_resolved,
        "resolved_at": alert.resolved_at,
        "resolved_by": alert.resolved_by,
        "resolution_notes": alert.resolution_notes,
        "notification_sent": alert.notification_sent,
        "created_at": alert.created_at
    }


@router.post("/{alert_id}/resolve")
async def resolve_alert(
    alert_id: int,
    notes: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Resolve an alert"""

    result = await db.execute(select(Alert).where(Alert.id == alert_id))
    alert = result.scalar_one_or_none()

    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.is_resolved = True
    alert.resolved_at = datetime.utcnow()
    alert.resolved_by = current_user.get("sub")
    alert.resolution_notes = notes

    await db.commit()

    return {"message": "Alert resolved successfully", "alert_id": alert_id}


@router.get("/anomalies/")
async def list_anomalies(
    well_id: Optional[int] = None,
    is_confirmed: Optional[bool] = None,
    days: int = Query(default=7, ge=1, le=90),
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List detected anomalies"""

    start_date = datetime.utcnow() - timedelta(days=days)
    query = select(Anomaly).where(Anomaly.detected_at >= start_date)

    if well_id:
        query = query.where(Anomaly.well_id == well_id)
    if is_confirmed is not None:
        query = query.where(Anomaly.is_confirmed == is_confirmed)

    query = query.order_by(Anomaly.detected_at.desc()).offset(skip).limit(limit)

    result = await db.execute(query)
    anomalies = result.scalars().all()

    return [
        {
            "id": anomaly.id,
            "well_id": anomaly.well_id,
            "parameter": anomaly.parameter,
            "value": anomaly.value,
            "expected_value": anomaly.expected_value,
            "deviation": anomaly.deviation,
            "anomaly_score": anomaly.anomaly_score,
            "detection_method": anomaly.detection_method,
            "is_confirmed": anomaly.is_confirmed,
            "is_false_positive": anomaly.is_false_positive,
            "detected_at": anomaly.detected_at
        }
        for anomaly in anomalies
    ]
