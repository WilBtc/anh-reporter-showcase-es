"""ANH Report models"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, Text, Float, JSON
import enum
from app.core.database import Base


class ReportStatus(str, enum.Enum):
    """Report status enumeration"""
    PENDING = "pending"
    GENERATING = "generating"
    VALIDATING = "validating"
    READY = "ready"
    UPLOADING = "uploading"
    UPLOADED = "uploaded"
    FAILED = "failed"


class ANHReport(Base):
    """ANH Daily Report"""
    __tablename__ = "anh_reports"

    id = Column(Integer, primary_key=True, index=True)
    report_date = Column(DateTime, nullable=False, index=True)
    status = Column(Enum(ReportStatus), default=ReportStatus.PENDING, nullable=False)

    # File information
    filename = Column(String, nullable=False)
    file_path = Column(String)
    file_size = Column(Integer)  # bytes

    # Content summary
    total_wells = Column(Integer)
    total_readings = Column(Integer)
    oil_production_total = Column(Float)  # barrels
    gas_production_total = Column(Float)  # KSCF
    water_production_total = Column(Float)  # barrels

    # Quality metrics
    data_quality_score = Column(Float)
    missing_samples = Column(Integer, default=0)
    validation_errors = Column(JSON)  # List of validation errors
    validation_warnings = Column(JSON)  # List of warnings

    # Upload information
    uploaded_at = Column(DateTime, nullable=True)
    upload_response = Column(Text)  # FTP server response

    # Metadata
    generated_at = Column(DateTime)
    generated_by = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<ANHReport date={self.report_date} status={self.status}>"
