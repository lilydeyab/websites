from datetime import datetime
import uuid

from ..extensions import db


class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    company_id = db.Column(
        db.String(36),
        db.ForeignKey("companies.id"),
        nullable=False,
        index=True,
    )

    appointment_id = db.Column(
        db.String(36),
        db.ForeignKey("appointments.id"),
        nullable=True,
        index=True,
    )

    lead_id = db.Column(
        db.String(36),
        db.ForeignKey("leads.id"),
        nullable=False,
        index=True,
    )

    customer_id = db.Column(
        db.String(36),
        db.ForeignKey("customers.id"),
        nullable=False,
        index=True,
    )

    service_id = db.Column(
        db.String(36),
        db.ForeignKey("services.id"),
        nullable=True,
        index=True,
    )

    assigned_user_id = db.Column(
        db.String(36),
        db.ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    status = db.Column(
        db.String(50),
        nullable=False,
        default="scheduled",
        index=True,
    )

    completed_at = db.Column(
        db.DateTime,
        nullable=True,
    )

    job_value = db.Column(
        db.Numeric(12, 2),
        nullable=True,
    )

    currency = db.Column(
        db.String(3),
        nullable=False,
        default="USD",
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    def __repr__(self):
        return f"<Job {self.id} status={self.status}>"