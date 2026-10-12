from datetime import datetime
import uuid

from ..extensions import db


class RevenueRecord(db.Model):
    __tablename__ = "revenue_records"

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
        nullable=True,
        index=True,
    )

    job_id = db.Column(
        db.String(36),
        db.ForeignKey("jobs.id"),
        nullable=True,
        index=True,
    )

    customer_id = db.Column(
        db.String(36),
        db.ForeignKey("customers.id"),
        nullable=True,
        index=True,
    )

    amount = db.Column(
        db.Numeric(12, 2),
        nullable=False,
    )

    currency = db.Column(
        db.String(3),
        nullable=False,
        default="USD",
    )

    revenue_date = db.Column(
        db.DateTime,
        nullable=False,
        index=True,
    )

    source = db.Column(
        db.String(100),
        nullable=False,
    )

    external_id = db.Column(
        db.String(255),
        nullable=True,
    )

    status = db.Column(
        db.String(50),
        nullable=False,
        default="recorded",
        index=True,
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
        return f"<RevenueRecord {self.id} amount={self.amount}>"