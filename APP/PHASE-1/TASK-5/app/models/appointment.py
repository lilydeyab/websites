from datetime import datetime
import uuid

from ..extensions import db


class Appointment(db.Model):
    __tablename__ = "appointments"

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

    location_id = db.Column(
        db.String(36),
        db.ForeignKey("locations.id"),
        nullable=True,
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

    external_id = db.Column(
        db.String(255),
        nullable=True,
    )

    start_time = db.Column(
        db.DateTime,
        nullable=False,
        index=True,
    )

    end_time = db.Column(
        db.DateTime,
        nullable=False,
        index=True,
    )

    status = db.Column(
        db.String(50),
        nullable=False,
        default="booked",
        index=True,
    )

    confirmation_status = db.Column(
        db.String(50),
        nullable=False,
        default="pending",
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
        return f"<Appointment {self.id} status={self.status}>"