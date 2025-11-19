"""Seed data generator for demo/testing purposes"""
import random
from datetime import datetime, timedelta
from typing import List
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.telemetry import Field, Well, TelemetryReading
from app.models.alert import Alert, Anomaly, AlertSeverity, AlertType
from app.models.report import ANHReport, ReportStatus


async def seed_users(db: AsyncSession):
    """Create demo users"""
    users_data = [
        {
            "email": "admin@insaingenieria.com",
            "username": "admin",
            "full_name": "System Administrator",
            "password": "admin123",
            "role": UserRole.ADMIN
        },
        {
            "email": "engineer@insaingenieria.com",
            "username": "engineer",
            "full_name": "Field Engineer",
            "password": "engineer123",
            "role": UserRole.ENGINEER
        },
        {
            "email": "operator@insaingenieria.com",
            "username": "operator",
            "full_name": "Field Operator",
            "password": "operator123",
            "role": UserRole.OPERATOR
        }
    ]

    for user_data in users_data:
        # Check if user exists
        result = await db.execute(select(User).where(User.username == user_data["username"]))
        existing = result.scalar_one_or_none()

        if not existing:
            user = User(
                email=user_data["email"],
                username=user_data["username"],
                full_name=user_data["full_name"],
                hashed_password=get_password_hash(user_data["password"]),
                role=user_data["role"],
                is_active=True,
                is_verified=True
            )
            db.add(user)
            print(f"✓ Created user: {user_data['username']}")

    await db.commit()


async def seed_fields_and_wells(db: AsyncSession) -> List[Well]:
    """Create demo fields and wells"""

    fields_data = [
        {"name": "Campo Rubiales", "code": "RUB-001", "operator": "Meta Petroleum Corp", "location": "Meta"},
        {"name": "Campo Caño Limón", "code": "CL-002", "operator": "Occidental de Colombia", "location": "Arauca"},
        {"name": "Campo Cusiana", "code": "CUS-003", "operator": "Ecopetrol", "location": "Casanare"},
    ]

    wells_list = []

    for field_data in fields_data:
        # Check if field exists
        result = await db.execute(select(Field).where(Field.code == field_data["code"]))
        field = result.scalar_one_or_none()

        if not field:
            field = Field(**field_data)
            db.add(field)
            await db.flush()
            print(f"✓ Created field: {field_data['name']}")

        # Create wells for this field
        for i in range(1, 4):  # 3 wells per field
            well_name = f"{field.code}-W{i:02d}"
            result = await db.execute(select(Well).where(Well.api_number == well_name))
            existing_well = result.scalar_one_or_none()

            if not existing_well:
                well = Well(
                    name=well_name,
                    api_number=well_name,
                    field_id=field.id,
                    well_type="Producer",
                    status="Active",
                    latitude=4.5 + random.uniform(-1, 1),
                    longitude=-72.5 + random.uniform(-1, 1),
                    total_depth=2500 + random.uniform(-500, 500)
                )
                db.add(well)
                wells_list.append(well)
                print(f"  ✓ Created well: {well_name}")

    await db.commit()

    # Refresh wells to get IDs
    for well in wells_list:
        await db.refresh(well)

    return wells_list


async def seed_telemetry_data(db: AsyncSession, wells: List[Well], days: int = 7):
    """Generate realistic telemetry data"""
    print(f"\n🔄 Generating {days} days of telemetry data...")

    now = datetime.utcnow()
    samples_per_day = 144  # Every 10 minutes

    total_readings = 0

    for well in wells:
        # Base production rates for this well
        base_oil_rate = random.uniform(100, 500)
        base_gas_rate = random.uniform(500, 2000)
        base_water_rate = random.uniform(50, 200)

        for day in range(days):
            date = now - timedelta(days=days - day - 1)
            start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)

            batch = []

            for sample in range(samples_per_day):
                timestamp = start_of_day + timedelta(minutes=10 * sample)

                # Add some realistic variance
                oil_rate = max(0, base_oil_rate + random.gauss(0, 20))
                gas_rate = max(0, base_gas_rate + random.gauss(0, 100))
                water_rate = max(0, base_water_rate + random.gauss(0, 10))

                reading = TelemetryReading(
                    well_id=well.id,
                    timestamp=timestamp,
                    oil_rate=round(oil_rate, 2),
                    gas_rate=round(gas_rate, 2),
                    water_rate=round(water_rate, 2),
                    wellhead_pressure=round(random.uniform(800, 1200), 1),
                    tubing_pressure=round(random.uniform(600, 1000), 1),
                    casing_pressure=round(random.uniform(400, 800), 1),
                    wellhead_temperature=round(random.uniform(120, 180), 1),
                    flowline_temperature=round(random.uniform(100, 150), 1),
                    choke_size=round(random.uniform(16, 64)),
                    pump_status=True,
                    pump_speed=round(random.uniform(200, 400), 1),
                    data_quality_score=round(random.uniform(95, 100), 1),
                    is_validated=True,
                    source="SCADA_SIMULATOR"
                )
                batch.append(reading)

            db.add_all(batch)
            total_readings += len(batch)

        print(f"  ✓ Generated data for well {well.name}: {days * samples_per_day} readings")

    await db.commit()
    print(f"✅ Total telemetry readings created: {total_readings}")


async def seed_alerts(db: AsyncSession, wells: List[Well]):
    """Create sample alerts"""
    alert_types = [
        ("High Pressure Alert", "Wellhead pressure exceeded threshold", AlertSeverity.WARNING),
        ("Low Production", "Oil production below expected rate", AlertSeverity.CRITICAL),
        ("Pump Failure", "Pump stopped unexpectedly", AlertSeverity.CRITICAL),
        ("Data Quality Issue", "Missing telemetry samples detected", AlertSeverity.WARNING),
    ]

    for well in wells[:3]:  # Create alerts for first 3 wells
        for i, (title, desc, severity) in enumerate(alert_types[:2]):
            alert = Alert(
                type=AlertType.EQUIPMENT if "Pump" in title else AlertType.ANOMALY,
                severity=severity,
                title=title,
                description=desc,
                well_id=well.id,
                value=random.uniform(1000, 1500),
                threshold=1200.0,
                metric_name="wellhead_pressure",
                is_resolved=i == 0,  # First alert is resolved
                notification_sent=True
            )
            db.add(alert)

    await db.commit()
    print("✓ Created sample alerts")


async def seed_reports(db: AsyncSession):
    """Create sample ANH reports"""
    now = datetime.utcnow()

    for days_ago in range(7):
        report_date = now - timedelta(days=days_ago)

        report = ANHReport(
            report_date=report_date.date(),
            status=ReportStatus.UPLOADED if days_ago > 0 else ReportStatus.READY,
            filename=f"ANH_REPORT_{report_date.strftime('%Y%m%d')}.json",
            file_path=f"/data/exports/ANH_REPORT_{report_date.strftime('%Y%m%d')}.json",
            file_size=random.randint(50000, 150000),
            total_wells=9,
            total_readings=9 * 144,
            oil_production_total=round(random.uniform(2000, 4000), 2),
            gas_production_total=round(random.uniform(10000, 18000), 2),
            water_production_total=round(random.uniform(500, 1500), 2),
            data_quality_score=round(random.uniform(98, 100), 1),
            missing_samples=random.randint(0, 5),
            validation_errors=[],
            validation_warnings=[],
            generated_at=report_date.replace(hour=6, minute=0),
            uploaded_at=report_date.replace(hour=6, minute=50) if days_ago > 0 else None,
            generated_by="1"
        )
        db.add(report)

    await db.commit()
    print("✓ Created sample ANH reports")


async def main():
    """Run all seed functions"""
    print("\n" + "=" * 60)
    print("🌱 ANH Reporter - Seeding Database")
    print("=" * 60 + "\n")

    async with AsyncSessionLocal() as db:
        try:
            print("📝 Creating users...")
            await seed_users(db)

            print("\n🏭 Creating fields and wells...")
            wells = await seed_fields_and_wells(db)

            if wells:
                print(f"\n📊 Generating telemetry data for {len(wells)} wells...")
                await seed_telemetry_data(db, wells, days=7)

                print("\n⚠️  Creating alerts...")
                await seed_alerts(db, wells)

            print("\n📄 Creating ANH reports...")
            await seed_reports(db)

            print("\n" + "=" * 60)
            print("✅ Database seeding completed successfully!")
            print("=" * 60)
            print("\n📋 Demo Credentials:")
            print("   Admin:    admin / admin123")
            print("   Engineer: engineer / engineer123")
            print("   Operator: operator / operator123")
            print("\n")

        except Exception as e:
            print(f"\n❌ Error during seeding: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(main())
