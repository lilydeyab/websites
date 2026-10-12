from datetime import datetime
import uuid

from ..extensions import db


class Service(db.Model):
    __tablename__ = "services"

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

    description = db.Column(
        db.Text,
        nullable=True,
    )

    category = db.Column(
        db.String(100),
        nullable=True,
    )

    duration = db.Column(
        db.Integer,
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
        return f"<Service {self.name}>"