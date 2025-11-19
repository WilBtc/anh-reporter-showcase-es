"""Alert and Anomaly models"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, Float, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base


class AlertSeverity(str, enum.Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AlertType(str, enum.Enum):
    """Alert type enumeration"""
    ANOMALY = "anomaly"
    DATA_QUALITY = "data_quality"
    SYSTEM = "system"
    COMPLIANCE = "compliance"
    EQUIPMENT = "equipment"


class Alert(Base):
    """System alerts"""
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(AlertType), nullable=False, index=True)
    severity = Column(Enum(AlertSeverity), nullable=False, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)

    # Related entities
    well_id = Column(Integer, ForeignKey("wells.id"), nullable=True)
    field_id = Column(Integer, ForeignKey("fields.id"), nullable=True)

    # Alert data
    value = Column(Float)  # Measured value that triggered alert
    threshold = Column(Float)  # Threshold that was exceeded
    metric_name = Column(String)  # Name of the metric

    # Status
    is_resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime, nullable=True)
    resolved_by = Column(String)
    resolution_notes = Column(Text)

    # Notification
    notification_sent = Column(Boolean, default=False)
    notification_sent_at = Column(DateTime, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Alert {self.type} - {self.severity}>"


class Anomaly(Base):
    """Detected anomalies in telemetry data"""
    __tablename__ = "anomalies"

    id = Column(Integer, primary_key=True, index=True)
    well_id = Column(Integer, ForeignKey("wells.id"), nullable=False)
    telemetry_id = Column(Integer, ForeignKey("telemetry_readings.id"), nullable=True)

    # Anomaly details
    parameter = Column(String, nullable=False)  # Which parameter is anomalous
    value = Column(Float, nullable=False)  # Anomalous value
    expected_value = Column(Float)  # Expected value
    deviation = Column(Float)  # Percent deviation
    anomaly_score = Column(Float, nullable=False)  # ML model confidence (0-1)

    # Detection method
    detection_method = Column(String)  # IsolationForest, LSTM, SPC, etc.
    model_version = Column(String)

    # Classification
    is_confirmed = Column(Boolean, default=False)  # Manually confirmed
    is_false_positive = Column(Boolean, default=False)
    confirmed_by = Column(String)
    confirmed_at = Column(DateTime, nullable=True)
    notes = Column(Text)

    # Metadata
    detected_at = Column(DateTime, default=datetime.utcnow, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Anomaly well={self.well_id} param={self.parameter}>"
