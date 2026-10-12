from datetime import datetime
import uuid

from ..extensions import db


class FollowUp(db.Model):
    __tablename__ = "follow_ups"

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

    channel = db.Column(
        db.String(50),
        nullable=False,
    )

    template_id = db.Column(
        db.String(36),
        db.ForeignKey("message_templates.id"),
        nullable=True,
        index=True,
    )

    attempt_number = db.Column(
        db.Integer,
        nullable=False,
        default=1,
    )

    scheduled_at = db.Column(
        db.DateTime,
        nullable=False,
        index=True,
    )

    sent_at = db.Column(
        db.DateTime,
        nullable=True,
    )

    status = db.Column(
        db.String(50),
        nullable=False,
        default="scheduled",
        index=True,
    )

    stop_reason = db.Column(
        db.String(255),
        nullable=True,
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    def __repr__(self):
        return f"<FollowUp lead={self.lead_id} status={self.status}>"