from datetime import datetime
import uuid

from sqlalchemy import JSON

from ..extensions import db


class Message(db.Model):
    __tablename__ = "messages"

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

    sender_type = db.Column(
        db.String(50),
        nullable=False,
    )

    sender_id = db.Column(
        db.String(36),
        nullable=True,
    )

    direction = db.Column(
        db.String(20),
        nullable=False,
    )

    content = db.Column(
        db.Text,
        nullable=False,
    )

    message_type = db.Column(
        db.String(50),
        nullable=False,
        default="text",
    )

    delivery_status = db.Column(
        db.String(50),
        nullable=True,
    )

    ai_generated = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )

    external_id = db.Column(
        db.String(255),
        nullable=True,
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True,
    )

    metadata = db.Column(
        JSON,
        nullable=True,
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    def __repr__(self):
        return f"<Message {self.id}>"