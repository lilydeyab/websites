from datetime import datetime
import uuid

from ..extensions import db


class KnowledgeDocument(db.Model):
    __tablename__ = "knowledge_documents"

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

    title = db.Column(
        db.String(255),
        nullable=False,
    )

    content = db.Column(
        db.Text,
        nullable=False,
    )

    document_type = db.Column(
        db.String(100),
        nullable=False,
    )

    version = db.Column(
        db.Integer,
        nullable=False,
        default=1,
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
        return f"<KnowledgeDocument {self.title}>"