from datetime import datetime
import uuid

from ..extensions import db


class CompanyUser(db.Model):
    __tablename__ = "company_users"

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

    user_id = db.Column(
        db.String(36),
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    role = db.Column(
        db.String(50),
        nullable=False,
    )

    status = db.Column(
        db.String(50),
        nullable=False,
        default="active",
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
            "user_id",
            name="uq_company_user",
        ),
    )

    def __repr__(self):
        return f"<CompanyUser company={self.company_id} user={self.user_id}>"