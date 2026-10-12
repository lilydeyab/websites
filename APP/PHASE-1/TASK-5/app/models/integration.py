from datetime import datetime
import uuid

from sqlalchemy import JSON

from ..extensions import db


class Integration(db.Model):
    __tablename__ = "integrations"

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

    integration_type = db.Column(
        db.String(100),
        nullable=False,
    )

    provider = db.Column(
        db.String(100),
        nullable=False,
    )

    status = db.Column(
        db.String(50),
        nullable=False,
        default="inactive",
    )

    external_account_id = db.Column(
        db.String(255),
        nullable=True,
    )

    configuration = db.Column(
        JSON,
        nullable=False,
        default=dict,
    )

    last_sync_at = db.Column(
        db.DateTime,
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

    __table_args__ = (
        db.UniqueConstraint(
            "company_id",
            "provider",
            "external_account_id",
            name="uq_company_provider_external_account",
        ),
    )

    def __repr__(self):
        return f"<Integration {self.provider}>"