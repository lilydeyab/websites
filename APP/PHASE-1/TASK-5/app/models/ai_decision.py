from datetime import datetime
import uuid

from sqlalchemy import JSON

from ..extensions import db


class AIDecision(db.Model):
    __tablename__ = "ai_decisions"

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

    conversation_id = db.Column(
        db.String(36),
        db.ForeignKey("conversations.id"),
        nullable=False,
        index=True,
    )

    lead_id = db.Column(
        db.String(36),
        db.ForeignKey("leads.id"),
        nullable=False,
        index=True,
    )

    decision_type = db.Column(
        db.String(100),
        nullable=False,
    )

    trigger = db.Column(
        db.String(255),
        nullable=False,
    )

    confidence = db.Column(
        db.Float,
        nullable=True,
    )

    business_rule_result = db.Column(
        JSON,
        nullable=True,
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
        return f"<AIDecision {self.decision_type}>"