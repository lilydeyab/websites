from datetime import datetime
import uuid

from ..extensions import db


class AIExtraction(db.Model):
    __tablename__ = "ai_extractions"

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

    message_id = db.Column(
        db.String(36),
        db.ForeignKey("messages.id"),
        nullable=True,
        index=True,
    )

    field_name = db.Column(
        db.String(100),
        nullable=False,
    )

    field_value = db.Column(
        db.Text,
        nullable=True,
    )

    source = db.Column(
        db.String(100),
        nullable=False,
    )

    confidence = db.Column(
        db.Float,
        nullable=True,
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True,
    )

    def __repr__(self):
        return f"<AIExtraction {self.field_name}>"