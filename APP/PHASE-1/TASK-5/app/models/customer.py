from datetime import datetime
import uuid

from ..extensions import db


class Customer(db.Model):
    __tablename__ = "customers"

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

    first_name = db.Column(
        db.String(100),
        nullable=False,
    )

    last_name = db.Column(
        db.String(100),
        nullable=False,
    )

    phone = db.Column(
        db.String(50),
        nullable=True,
    )

    email = db.Column(
        db.String(255),
        nullable=True,
    )

    address = db.Column(
        db.String(500),
        nullable=True,
    )

    city = db.Column(
        db.String(100),
        nullable=True,
    )

    state = db.Column(
        db.String(100),
        nullable=True,
    )

    zip = db.Column(
        db.String(20),
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
        db.Index(
            "ix_customers_company_phone",
            "company_id",
            "phone",
        ),
        db.Index(
            "ix_customers_company_email",
            "company_id",
            "email",
        ),
    )

    def __repr__(self):
        return f"<Customer {self.first_name} {self.last_name}>"