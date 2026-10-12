from datetime import datetime
import uuid

from ..extensions import db


class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    name = db.Column(db.String(255), nullable=False)
    legal_name = db.Column(db.String(255), nullable=True)
    business_type = db.Column(db.String(100), nullable=True)
    industry = db.Column(db.String(100), nullable=True)

    phone = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    website = db.Column(db.String(500), nullable=True)

    timezone = db.Column(
        db.String(100),
        nullable=False,
        default="America/New_York",
    )

    default_currency = db.Column(
        db.String(3),
        nullable=False,
        default="USD",
    )

    status = db.Column(
        db.String(50),
        nullable=False,
        default="active",
    )

    onboarding_status = db.Column(
        db.String(50),
        nullable=False,
        default="pending",
    )

    primary_location_id = db.Column(
        db.String(36),
        nullable=True,
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
        return f"<Company {self.name}>"