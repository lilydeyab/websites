from datetime import datetime
import uuid

from ..extensions import db


class Location(db.Model):
    __tablename__ = "locations"

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

    name = db.Column(
        db.String(255),
        nullable=False,
    )

    address = db.Column(
        db.String(500),
        nullable=False,
    )

    city = db.Column(
        db.String(100),
        nullable=False,
    )

    state = db.Column(
        db.String(100),
        nullable=False,
    )

    zip = db.Column(
        db.String(20),
        nullable=False,
    )

    latitude = db.Column(
        db.Float,
        nullable=True,
    )

    longitude = db.Column(
        db.Float,
        nullable=True,
    )

    timezone = db.Column(
        db.String(100),
        nullable=False,
        default="America/New_York",
    )

    phone = db.Column(
        db.String(50),
        nullable=True,
    )

    status = db.Column(
        db.String(50),
        nullable=False,
        default="active",
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
        return f"<Location {self.name}>"