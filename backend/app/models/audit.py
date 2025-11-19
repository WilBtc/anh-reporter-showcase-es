"""Audit log model for tracking all system actions"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class AuditLog(Base):
    """Audit log for tracking user actions and system events"""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String, nullable=False, index=True)  # login, create, update, delete, etc.
    resource = Column(String, nullable=False)  # user, report, well, etc.
    resource_id = Column(String)  # ID of the affected resource

    # Details
    details = Column(JSON)  # Additional context
    ip_address = Column(String)
    user_agent = Column(String)

    # Status
    success = Column(Integer, default=True)
    error_message = Column(String)

    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="audit_logs")

    def __repr__(self):
        return f"<AuditLog {self.action} on {self.resource}>"
