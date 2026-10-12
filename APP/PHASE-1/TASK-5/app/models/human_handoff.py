from datetime import datetime
import uuid

from sqlalchemy import JSON

from ..extensions import db


class HumanHandoff(db.Model):
    __tablename__ = "human_handoffs"

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
        nullable=False,
        index=True,
    )

    conversation_id = db.Column(
        db.String(36),
        db.ForeignKey("conversations.id"),
        nullable=True,
        index=True,
    )

    reason = db.Column(
        db.String(255),
        nullable=False,
    )

    summary = db.Column(
        db.Text,
        nullable=True,
    )

    qualification_data = db.Column(
        JSON,
        nullable=True,
    )

    recommended_action = db.Column(
        db.String(255),
        nullable=True,
    )

    assigned_user_id = db.Column(
        db.String(36),
        db.ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    status = db.Column(
        db.String(50),
        nullable=False,
        default="pending",
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True,
    )

    resolved_at = db.Column(
        db.DateTime,
        nullable=True,
    )

    def __repr__(self):
        return f"<HumanHandoff lead={self.lead_id} status={self.status}>"