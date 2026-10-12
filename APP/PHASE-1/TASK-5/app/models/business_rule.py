from datetime import datetime
import uuid

from sqlalchemy import JSON

from ..extensions import db


class BusinessRule(db.Model):
    __tablename__ = "business_rules"

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

    rule_type = db.Column(
        db.String(100),
        nullable=False,
    )

    rule_name = db.Column(
        db.String(255),
        nullable=False,
    )

    configuration = db.Column(
        JSON,
        nullable=False,
        default=dict,
    )

    priority = db.Column(
        db.Integer,
        nullable=False,
        default=0,
    )

    enabled = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
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
        return f"<BusinessRule {self.rule_name}>"