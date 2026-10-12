from datetime import datetime
import uuid

from ..extensions import db


class MessageTemplate(db.Model):
    __tablename__ = "message_templates"

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

    channel = db.Column(
        db.String(50),
        nullable=False,
    )

    content = db.Column(
        db.Text,
        nullable=False,
    )

    purpose = db.Column(
        db.String(100),
        nullable=False,
    )

    active = db.Column(
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
        return f"<MessageTemplate {self.name}>"