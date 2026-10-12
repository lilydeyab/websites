from datetime import datetime
import uuid

from ..extensions import db


class Lead(db.Model):
    __tablename__ = "leads"

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

    customer_id = db.Column(
        db.String(36),
        db.ForeignKey("customers.id"),
        nullable=False,
        index=True,
    )

    source = db.Column(
        db.String(100),
        nullable=False,
    )

    source_reference = db.Column(
        db.String(255),
        nullable=True,
    )

    channel = db.Column(
        db.String(50),
        nullable=False,
    )

    status = db.Column(
        db.String(50),
        nullable=False,
        default="new",
        index=True,
    )

    intent = db.Column(
        db.String(255),
        nullable=True,
    )

    service_id = db.Column(
        db.String(36),
        db.ForeignKey("services.id"),
        nullable=True,
        index=True,
    )

    location_id = db.Column(
        db.String(36),
        db.ForeignKey("locations.id"),
        nullable=True,
        index=True,
    )

    urgency = db.Column(
        db.String(50),
        nullable=True,
    )

    qualification_status = db.Column(
        db.String(50),
        nullable=False,
        default="pending",
    )

    assigned_user_id = db.Column(
        db.String(36),
        db.ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True,
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    last_contacted_at = db.Column(
        db.DateTime,
        nullable=True,
    )

    __table_args__ = (
        db.Index(
            "ix_leads_company_status",
            "company_id",
            "status",
        ),
        db.Index(
            "ix_leads_company_created_at",
            "company_id",
            "created_at",
        ),
        db.Index(
            "ix_leads_company_customer",
            "company_id",
            "customer_id",
        ),
    )

    def __repr__(self):
        return f"<Lead {self.id}>"