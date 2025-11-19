"""Telemetry models for oil & gas data"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Index, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class Field(Base):
    """Oil & Gas Field"""
    __tablename__ = "fields"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    code = Column(String, unique=True, nullable=False)  # ANH field code
    operator = Column(String, nullable=False)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    wells = relationship("Well", back_populates="field")

    def __repr__(self):
        return f"<Field {self.name}>"


class Well(Base):
    """Oil & Gas Well"""
    __tablename__ = "wells"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    api_number = Column(String, unique=True, nullable=False)  # Unique well identifier
    field_id = Column(Integer, ForeignKey("fields.id"), nullable=False)
    well_type = Column(String)  # Producer, Injector, Observation
    status = Column(String)  # Active, Shut-in, Abandoned
    latitude = Column(Float)
    longitude = Column(Float)
    total_depth = Column(Float)  # meters
    spud_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    field = relationship("Field", back_populates="wells")
    telemetry = relationship("TelemetryReading", back_populates="well")

    def __repr__(self):
        return f"<Well {self.name}>"


class TelemetryReading(Base):
    """Telemetry reading from SCADA/DCS system"""
    __tablename__ = "telemetry_readings"

    id = Column(Integer, primary_key=True, index=True)
    well_id = Column(Integer, ForeignKey("wells.id"), nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)

    # Production data
    oil_rate = Column(Float)  # barrels/day
    gas_rate = Column(Float)  # KSCF/day
    water_rate = Column(Float)  # barrels/day
    oil_cumulative = Column(Float)  # total barrels
    gas_cumulative = Column(Float)  # total KSCF
    water_cumulative = Column(Float)  # total barrels

    # Pressure data
    wellhead_pressure = Column(Float)  # PSI
    tubing_pressure = Column(Float)  # PSI
    casing_pressure = Column(Float)  # PSI
    line_pressure = Column(Float)  # PSI

    # Temperature data
    wellhead_temperature = Column(Float)  # °F
    flowline_temperature = Column(Float)  # °F

    # Well status
    choke_size = Column(Float)  # 64ths of an inch
    pump_status = Column(Boolean)
    pump_speed = Column(Float)  # RPM
    pump_strokes_per_minute = Column(Float)

    # Power & Equipment
    motor_current = Column(Float)  # Amps
    motor_voltage = Column(Float)  # Volts
    power_consumption = Column(Float)  # kW

    # Separator data
    separator_pressure = Column(Float)  # PSI
    separator_temperature = Column(Float)  # °F
    separator_level = Column(Float)  # percentage

    # Quality metrics
    data_quality_score = Column(Float, default=100.0)
    is_validated = Column(Boolean, default=False)
    is_anomaly = Column(Boolean, default=False)

    # Metadata
    source = Column(String)  # OPC-UA, Modbus, MQTT, Manual
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    well = relationship("Well", back_populates="telemetry")

    # Indexes for performance
    __table_args__ = (
        Index('idx_telemetry_well_timestamp', 'well_id', 'timestamp'),
        Index('idx_telemetry_timestamp', 'timestamp'),
    )

    def __repr__(self):
        return f"<TelemetryReading well={self.well_id} time={self.timestamp}>"
