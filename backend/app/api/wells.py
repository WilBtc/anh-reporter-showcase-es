"""Wells and Fields management endpoints"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.telemetry import Well, Field
from app.schemas.telemetry import (
    WellCreate,
    WellResponse,
    FieldCreate,
    FieldResponse
)

router = APIRouter()


@router.post("/fields", response_model=FieldResponse, status_code=status.HTTP_201_CREATED)
async def create_field(
    field_data: FieldCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new field"""
    new_field = Field(**field_data.model_dump())
    db.add(new_field)
    await db.commit()
    await db.refresh(new_field)
    return new_field


@router.get("/fields", response_model=List[FieldResponse])
async def list_fields(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List all fields"""
    result = await db.execute(
        select(Field).where(Field.is_active == True).offset(skip).limit(limit)
    )
    fields = result.scalars().all()
    return fields


@router.get("/fields/{field_id}", response_model=FieldResponse)
async def get_field(
    field_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get field by ID"""
    result = await db.execute(select(Field).where(Field.id == field_id))
    field = result.scalar_one_or_none()

    if not field:
        raise HTTPException(status_code=404, detail="Field not found")

    return field


@router.post("/", response_model=WellResponse, status_code=status.HTTP_201_CREATED)
async def create_well(
    well_data: WellCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new well"""
    new_well = Well(**well_data.model_dump())
    db.add(new_well)
    await db.commit()
    await db.refresh(new_well)
    return new_well


@router.get("/", response_model=List[WellResponse])
async def list_wells(
    skip: int = 0,
    limit: int = 100,
    field_id: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List all wells"""
    query = select(Well).where(Well.is_active == True)

    if field_id:
        query = query.where(Well.field_id == field_id)

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    wells = result.scalars().all()
    return wells


@router.get("/{well_id}", response_model=WellResponse)
async def get_well(
    well_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get well by ID"""
    result = await db.execute(select(Well).where(Well.id == well_id))
    well = result.scalar_one_or_none()

    if not well:
        raise HTTPException(status_code=404, detail="Well not found")

    return well
