from datetime import datetime
import uuid

from sqlalchemy import JSON

from ..extensions import db


class AppointmentEvent(db.Model):
    __tablename__ = "appointment_events"

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
        nullable=False,
        index=True,
    )

    event_type = db.Column(
        db.String(100),
        nullable=False,
    )

    previous_status = db.Column(
        db.String(50),
        nullable=True,
    )

    new_status = db.Column(
        db.String(50),
        nullable=True,
    )

    actor_type = db.Column(
        db.String(50),
        nullable=False,
    )

    metadata = db.Column(
        JSON,
        nullable=True,
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True,
    )

    def __repr__(self):
        return f"<AppointmentEvent appointment={self.appointment_id} type={self.event_type}>"