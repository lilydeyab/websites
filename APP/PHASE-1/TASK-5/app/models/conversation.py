from datetime import datetime
import uuid

from ..extensions import db


class Conversation(db.Model):
    __tablename__ = "conversations"

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

    channel = db.Column(
        db.String(50),
        nullable=False,
    )

    status = db.Column(
        db.String(50),
        nullable=False,
        default="active",
    )

    external_id = db.Column(
        db.String(255),
        nullable=True,
    )

    started_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    ended_at = db.Column(
        db.DateTime,
        nullable=True,
    )

    summary = db.Column(
        db.Text,
        nullable=True,
    )

    intent = db.Column(
        db.String(255),
        nullable=True,
    )

    outcome = db.Column(
        db.String(255),
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
            "external_id",
            name="uq_conversation_company_external",
        ),
    )

    def __repr__(self):
        return f"<Conversation {self.id}>"