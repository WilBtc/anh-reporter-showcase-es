"""ANH Report management endpoints"""
from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.core.database import get_db
from app.core.security import get_current_user, check_permission
from app.models.report import ANHReport, ReportStatus

router = APIRouter()


@router.post("/generate", status_code=202)
async def generate_report(
    report_date: datetime,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(check_permission("operator"))
):
    """Generate ANH report for a specific date"""

    # Check if report already exists
    result = await db.execute(
        select(ANHReport).where(
            and_(
                ANHReport.report_date == report_date.date(),
                ANHReport.status.in_([ReportStatus.READY, ReportStatus.UPLOADED])
            )
        )
    )
    existing_report = result.scalar_one_or_none()

    if existing_report:
        return {
            "message": "Report already exists",
            "report_id": existing_report.id,
            "status": existing_report.status
        }

    # Create new report record
    filename = f"ANH_REPORT_{report_date.strftime('%Y%m%d')}.json"
    new_report = ANHReport(
        report_date=report_date,
        status=ReportStatus.PENDING,
        filename=filename,
        generated_by=current_user.get("sub")
    )

    db.add(new_report)
    await db.commit()
    await db.refresh(new_report)

    # In production, this would trigger actual report generation
    # background_tasks.add_task(generate_anh_report_task, new_report.id)

    return {
        "message": "Report generation started",
        "report_id": new_report.id,
        "status": new_report.status
    }


@router.get("/", response_model=List[dict])
async def list_reports(
    skip: int = 0,
    limit: int = 30,
    status: ReportStatus = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List ANH reports"""

    query = select(ANHReport).order_by(ANHReport.report_date.desc())

    if status:
        query = query.where(ANHReport.status == status)

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    reports = result.scalars().all()

    return [
        {
            "id": report.id,
            "report_date": report.report_date,
            "status": report.status,
            "filename": report.filename,
            "total_wells": report.total_wells,
            "total_readings": report.total_readings,
            "data_quality_score": report.data_quality_score,
            "uploaded_at": report.uploaded_at,
            "created_at": report.created_at
        }
        for report in reports
    ]


@router.get("/{report_id}")
async def get_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get report details"""

    result = await db.execute(
        select(ANHReport).where(ANHReport.id == report_id)
    )
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    return {
        "id": report.id,
        "report_date": report.report_date,
        "status": report.status,
        "filename": report.filename,
        "file_size": report.file_size,
        "total_wells": report.total_wells,
        "total_readings": report.total_readings,
        "oil_production_total": report.oil_production_total,
        "gas_production_total": report.gas_production_total,
        "water_production_total": report.water_production_total,
        "data_quality_score": report.data_quality_score,
        "missing_samples": report.missing_samples,
        "validation_errors": report.validation_errors,
        "validation_warnings": report.validation_warnings,
        "uploaded_at": report.uploaded_at,
        "generated_at": report.generated_at,
        "created_at": report.created_at
    }


@router.post("/{report_id}/upload", status_code=202)
async def upload_report(
    report_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(check_permission("operator"))
):
    """Upload report to ANH FTP server"""

    result = await db.execute(
        select(ANHReport).where(ANHReport.id == report_id)
    )
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    if report.status != ReportStatus.READY:
        raise HTTPException(
            status_code=400,
            detail=f"Report must be in READY status to upload (current: {report.status})"
        )

    # Update status
    report.status = ReportStatus.UPLOADING
    await db.commit()

    # In production, trigger FTP upload
    # background_tasks.add_task(upload_report_to_ftp, report_id)

    return {
        "message": "Report upload started",
        "report_id": report_id,
        "status": report.status
    }
