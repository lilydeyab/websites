"""
TASK 4 - Database Design
AI Revenue Recovery System

Production-oriented database structure based on:
Architecture + Final Task 4 Structure
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Column:
    name: str
    data_type: str
    nullable: bool = True
    primary_key: bool = False
    foreign_key: Optional[str] = None
    unique: bool = False
    indexed: bool = False


@dataclass
class Table:
    name: str
    domain: str
    columns: list
    indexes: list
    unique_constraints: list


class DatabaseDesign:

    # ============================================================
    # CONSTANTS
    # ============================================================

    DOMAINS = [
        "COMPANY",
        "CUSTOMER",
        "AI",
        "OPERATIONS",
        "REVENUE",
        "SYSTEM",
    ]

    USER_ROLES = [
        "OWNER",
        "ADMIN",
        "MANAGER",
        "STAFF",
    ]

    AI_DECISION_TYPES = [
        "ASK_QUESTION",
        "FOLLOW_UP",
        "BOOK_APPOINTMENT",
        "CONFIRM_APPOINTMENT",
        "RESCHEDULE",
        "CANCEL",
        "ANSWER_FAQ",
        "HANDOFF_HUMAN",
        "REACTIVATE",
        "CLOSE_LEAD",
    ]

    APPOINTMENT_STATUSES = [
        "BOOKED",
        "CONFIRMED",
        "RESCHEDULED",
        "CANCELLED",
        "NO_SHOW",
        "COMPLETED",
    ]

    RECOVERY_TYPES = [
        "MISSED_CALL",
        "AFTER_HOURS",
        "FOLLOW_UP",
        "OLD_LEAD",
        "APPOINTMENT",
    ]

    # ============================================================
    # DATABASE TABLES
    # ============================================================

    TABLES = {

        # ========================================================
        # COMPANY DOMAIN
        # ========================================================

        "companies": Table(
            name="companies",
            domain="COMPANY",
            columns=[
                Column("id", "UUID", primary_key=True),
                Column("name", "VARCHAR", nullable=False),
                Column("legal_name", "VARCHAR"),
                Column("business_type", "VARCHAR"),
                Column("industry", "VARCHAR"),
                Column("phone", "VARCHAR"),
                Column("email", "VARCHAR"),
                Column("website", "VARCHAR"),
                Column("timezone", "VARCHAR"),
                Column("default_currency", "VARCHAR"),
                Column("status", "VARCHAR"),
                Column("onboarding_status", "VARCHAR"),
                Column("primary_location_id", "UUID"),
                Column("created_at", "TIMESTAMP"),
                Column("updated_at", "TIMESTAMP"),
            ],
            indexes=[
                ("name",),
                ("email",),
            ],
            unique_constraints=[
                ("email",),
            ],
        ),

        "users": Table(
            name="users",
            domain="COMPANY",
            columns=[
                Column("id", "UUID", primary_key=True),
                Column("email", "VARCHAR", nullable=False, unique=True),
                Column("password_hash", "VARCHAR", nullable=False),
                Column("first_name", "VARCHAR"),
                Column("last_name", "VARCHAR"),
                Column("status", "VARCHAR"),
                Column("last_login_at", "TIMESTAMP"),
                Column("created_at", "TIMESTAMP"),
                Column("updated_at", "TIMESTAMP"),
            ],
            indexes=[
                ("email",),
            ],
            unique_constraints=[
                ("email",),
            ],
        ),

        "company_users": Table(
            name="company_users",
            domain="COMPANY",
            columns=[
                Column("id", "UUID", primary_key=True),
                Column(
                    "company_id",
                    "UUID",
                    nullable=False,
                    foreign_key="companies.id",
                    indexed=True,
                ),
                Column(
                    "user_id",
                    "UUID",
                    nullable=False,
                    foreign_key="users.id",
                    indexed=True,
                ),
                Column("role", "VARCHAR", nullable=False),
                Column("status", "VARCHAR"),
                Column("created_at", "TIMESTAMP"),
                Column("updated_at", "TIMESTAMP"),
            ],
            indexes=[
                ("company_id", "user_id"),
            ],
            unique_constraints=[
                ("company_id", "user_id"),
            ],
        ),

        "locations": Table(
            name="locations",
            domain="COMPANY",
            columns=[
                Column("id", "UUID", primary_key=True),
                Column(
                    "company_id",
                    "UUID",
                    nullable=False,
                    foreign_key="companies.id",
                    indexed=True,
                ),
                Column("name", "VARCHAR", nullable=False),
                Column("address", "VARCHAR"),
                Column("city", "VARCHAR"),
                Column("state", "VARCHAR"),
                Column("zip", "VARCHAR"),
                Column("latitude", "DECIMAL"),
                Column("longitude", "DECIMAL"),
                Column("timezone", "VARCHAR"),
                Column("phone", "VARCHAR"),
                Column("status", "VARCHAR"),
                Column("created_at", "TIMESTAMP"),
                Column("updated_at", "TIMESTAMP"),
            ],
            indexes=[
                ("company_id",),
                ("company_id", "city"),
            ],
            unique_constraints=[],
        ),

        "services": Table(
            name="services",
            domain="COMPANY",
            columns=[
                Column("id", "UUID", primary_key=True),
                Column(
                    "company_id",
                    "UUID",
                    nullable=False,
                    foreign_key="companies.id",
                    indexed=True,
                ),
                Column("name", "VARCHAR", nullable=False),
                Column("description", "TEXT"),
                Column("category", "VARCHAR"),
                Column("duration", "INTEGER"),
                Column("status", "VARCHAR"),
                Column("created_at", "TIMESTAMP"),
                Column("updated_at", "TIMESTAMP"),
            ],
            indexes=[
                ("company_id",),
            ],
            unique_constraints=[],
        ),

        "service_areas": Table(
            name="service_areas",
            domain="COMPANY",
            columns=[
                Column("id", "UUID", primary_key=True),
                Column(
                    "company_id",
                    "UUID",
                    nullable=False,
                    foreign_key="companies.id",
                    indexed=True,
                ),
                Column(
                    "location_id",
                    "UUID",
                    nullable=False,
                    foreign_key="locations.id",
                    indexed=True,
                ),
                Column("area", "VARCHAR"),
                Column("zip_code", "VARCHAR"),
                Column("city", "VARCHAR"),
                Column("state", "VARCHAR"),
                Column("status", "VARCHAR"),
                Column("created_at", "TIMESTAMP"),
                Column("updated_at", "TIMESTAMP"),
            ],
            indexes=[
                ("company_id",),
                ("company_id", "zip_code"),
            ],
            unique_constraints=[],
        ),

        "business_rules": Table(
            name="business_rules",
            domain="COMPANY",
            columns=[
                Column("id", "UUID", primary_key=True),
                Column(
                    "company_id",
                    "UUID",
                    nullable=False,
                    foreign_key="companies.id",
                    indexed=True,
                ),
                Column("rule_type", "VARCHAR"),
                Column("rule_name", "VARCHAR"),
                Column("configuration", "JSON"),
                Column("priority", "INTEGER"),
                Column("enabled", "BOOLEAN"),
                Column("created_at", "TIMESTAMP"),
                Column("updated_at", "TIMESTAMP"),
            ],
            indexes=[
                ("company_id",),
                ("company_id", "enabled"),
            ],
            unique_constraints=[],
        ),

        "integrations": Table(
            name="integrations",
            domain="COMPANY",
            columns=[
                Column("id", "UUID", primary_key=True),
                Column(
                    "company_id",
                    "UUID",
                    nullable=False,
                    foreign_key="companies.id",
                    indexed=True,
                ),
                Column("integration_type", "VARCHAR"),
                Column("provider", "VARCHAR"),
                Column("status", "VARCHAR"),
                Column("external_account_id", "VARCHAR"),
                Column("configuration", "JSON"),
                Column("last_sync_at", "TIMESTAMP"),
                Column("created_at", "TIMESTAMP"),
                Column("updated_at", "TIMESTAMP"),
            ],
            indexes=[
                ("company_id",),
            ],
            unique_constraints=[
                ("company_id", "provider", "external_account_id"),
            ],
        ),

        # ========================================================
        # CUSTOMER DOMAIN
        # ========================================================

        "customers": Table(
            name="customers",
            domain="CUSTOMER",
            columns=[
                Column("id", "UUID", primary_key=True),
                Column(
                    "company_id",
                    "UUID",
                    nullable=False,
                    foreign_key="companies.id",
                    indexed=True,
                ),
                Column("first_name", "VARCHAR"),
                Column("last_name", "VARCHAR"),
                Column("phone", "VARCHAR"),
                Column("email", "VARCHAR"),
                Column("address", "VARCHAR"),
                Column("city", "VARCHAR"),
                Column("state", "VARCHAR"),
                Column("zip", "VARCHAR"),
                Column("created_at", "TIMESTAMP"),
                Column("updated_at", "TIMESTAMP"),
            ],
            indexes=[
                ("company_id", "phone"),
                ("company_id", "email"),
            ],
            unique_constraints=[],
        ),

        "leads": Table(
            name="leads",
            domain="CUSTOMER",
            columns=[
                Column("id", "UUID", primary_key=True),
                Column(
                    "company_id",
                    "UUID",
                    nullable=False,
                    foreign_key="companies.id",
                    indexed=True,
                ),
                Column(
                    "customer_id",
                    "UUID",
                    foreign_key="customers.id",
                    indexed=True,
                ),
                Column("source", "VARCHAR"),
                Column("source_reference", "VARCHAR"),
                Column("channel", "VARCHAR"),
                Column("status", "VARCHAR"),
                Column("intent", "VARCHAR"),
                Column(
                    "service_id",
                    "UUID",
                    foreign_key="services.id",
                ),
                Column(
                    "location_id",
                    "UUID",
                    foreign_key="locations.id",
                ),
                Column("urgency", "VARCHAR"),
                Column("qualification_status", "VARCHAR"),
                Column(
                    "assigned_user_id",
                    "UUID",
                    foreign_key="users.id",
                ),
                Column("created_at", "TIMESTAMP"),
                Column("updated_at", "TIMESTAMP"),
                Column("last_contacted_at", "TIMESTAMP"),
            ],
            indexes=[
                ("company_id", "status"),
                ("company_id", "created_at"),
                ("company_id", "customer_id"),
            ],
            unique_constraints=[],
        ),

        "lead_events": Table(
            name="lead_events",
            domain="CUSTOMER",
            columns=[
                Column("id", "UUID", primary_key=True),
                Column(
                    "company_id",
                    "UUID",
                    nullable=False,
                    foreign_key="companies.id",
                    indexed=True,
                ),
                Column(
                    "lead_id",
                    "UUID",
                    nullable=False,
                    foreign_key="leads.id",
                    indexed=True,
                ),
                Column("event_type", "VARCHAR"),
                Column("previous_status", "VARCHAR"),
                Column("new_status", "VARCHAR"),
                Column("actor_type", "VARCHAR"),
                Column("actor_id", "UUID"),
                Column("metadata", "JSON"),
                Column("created_at", "TIMESTAMP"),
            ],
            indexes=[
                ("company_id", "lead_id"),
                ("company_id", "created_at"),
            ],
            unique_constraints=[],
        ),

        "conversations": Table(
            name="conversations",
            domain="CUSTOMER",
            columns=[
                Column("id", "UUID", primary_key=True),
                Column(
                    "company_id",
                    "UUID",
                    nullable=False,
                    foreign_key="companies.id",
                    indexed=True,
                ),
                Column(
                    "lead_id",
                    "UUID",
                    nullable=False,
                    foreign_key="leads.id",
                    indexed=True,
                ),
                Column("channel", "VARCHAR"),
                Column("status", "VARCHAR"),
                Column("external_id", "VARCHAR"),
                Column("started_at", "TIMESTAMP"),
                Column("ended_at", "TIMESTAMP"),
                Column("summary", "TEXT"),
                Column("intent", "VARCHAR"),
                Column("outcome", "VARCHAR"),
                Column("created_at", "TIMESTAMP"),
                Column("updated_at", "TIMESTAMP"),
            ],
            indexes=[
                ("company_id", "lead_id"),
            ],
            unique_constraints=[
                ("company_id", "external_id"),
            ],
        ),

        "messages": Table(
            name="messages",
            domain="CUSTOMER",
            columns=[
                Column("id", "UUID", primary_key=True),
                Column(
                    "company_id",
                    "UUID",
                    nullable=False,
                    foreign_key="companies.id",
                    indexed=True,
                ),
                Column(
                    "conversation_id",
                    "UUID",
                    nullable=False,
                    foreign_key="conversations.id",
                    indexed=True,
                ),
                Column("sender_type", "VARCHAR"),
                Column("sender_id", "UUID"),
                Column("direction", "VARCHAR"),
                Column("content", "TEXT"),
                Column("message_type", "VARCHAR"),
                Column("delivery_status", "VARCHAR"),
                Column("ai_generated", "BOOLEAN"),
                Column("external_id", "VARCHAR"),
                Column("timestamp", "TIMESTAMP"),
                Column("metadata", "JSON"),
                Column("created_at", "TIMESTAMP"),
            ],
            indexes=[
                ("company_id", "conversation_id", "timestamp"),
            ],
            unique_constraints=[],
        ),

        # ========================================================
        # AI DOMAIN
        # ========================================================

        "ai_extractions": Table(
            name="ai_extractions",
            domain="AI",
            columns=[
                Column("id", "UUID", primary_key=True),
                Column(
                    "company_id",
                    "UUID",
                    nullable=False,
                    foreign_key="companies.id",
                    indexed=True,
                ),
                Column(
                    "conversation_id",
                    "UUID",
                    foreign_key="conversations.id",
                ),
                Column(
                    "lead_id",
                    "UUID",
                    foreign_key="leads.id",
                ),
                Column(
                    "message_id",
                    "UUID",
                    foreign_key="messages.id",
                ),
                Column("field_name", "VARCHAR"),
                Column("field_value", "TEXT"),
                Column("source", "VARCHAR"),
                Column("confidence", "DECIMAL"),
                Column("created_at", "TIMESTAMP"),
            ],
            indexes=[
                ("company_id", "lead_id"),
                ("company_id", "conversation_id"),
            ],
            unique_constraints=[],
        ),

        "ai_decisions": Table(
            name="ai_decisions",
            domain="AI",
            columns=[
                Column("id", "UUID", primary_key=True),
                Column(
                    "company_id",
                    "UUID",
                    nullable=False,
                    foreign_key="companies.id",
                    indexed=True,
                ),
                Column(
                    "conversation_id",
                    "UUID",
                    foreign_key="conversations.id",
                ),
                Column(
                    "lead_id",
                    "UUID",
                    foreign_key="leads.id",
                ),
                Column("decision_type", "VARCHAR"),
                Column("trigger", "VARCHAR"),
                Column("confidence", "DECIMAL"),
                Column("business_rule_result", "JSON"),
                Column("metadata", "JSON"),
                Column("created_at", "TIMESTAMP"),
            ],
            indexes=[
                ("company_id", "lead_id"),
                ("company_id", "created_at"),
            ],
            unique_constraints=[],
        ),

        "knowledge_documents": Table(
            name="knowledge_documents",
            domain="AI",
            columns=[
                Column("id", "UUID", primary_key=True),
                Column(
                    "company_id",
                    "UUID",
                    nullable=False,
                    foreign_key="companies.id",
                    indexed=True,
                ),
                Column("title", "VARCHAR"),
                Column("content", "TEXT"),
                Column("document_type", "VARCHAR"),
                Column("version", "INTEGER"),
                Column("active", "BOOLEAN"),
                Column("created_at", "TIMESTAMP"),
                Column("updated_at", "TIMESTAMP"),
            ],
            indexes=[
                ("company_id",),
            ],
            unique_constraints=[],
        ),

        "human_handoffs": Table(
            name="human_handoffs",
            domain="AI",
            columns=[
                Column("id", "UUID", primary_key=True),
                Column(
                    "company_id",
                    "UUID",
                    nullable=False,
                    foreign_key="companies.id",
                    indexed=True,
                ),
                Column(
                    "lead_id",
                    "UUID",
                    foreign_key="leads.id",
                ),
                Column(
                    "conversation_id",
                    "UUID",
                    foreign_key="conversations.id",
                ),
                Column("reason", "TEXT"),
                Column("summary", "TEXT"),
                Column("qualification_data", "JSON"),
                Column("recommended_action", "VARCHAR"),
                Column(
                    "assigned_user_id",
                    "UUID",
                    foreign_key="users.id",
                ),
                Column("status", "VARCHAR"),
                Column("created_at", "TIMESTAMP"),
                Column("resolved_at", "TIMESTAMP"),
            ],
            indexes=[
                ("company_id", "lead_id"),
                ("company_id", "status"),
            ],
            unique_constraints=[],
        ),

        # ========================================================
        # OPERATIONS DOMAIN
        # ========================================================

        "follow_ups": Table(
            name="follow_ups",
            domain="OPERATIONS",
            columns=[
                Column("id", "UUID", primary_key=True),
                Column(
                    "company_id",
                    "UUID",
                    nullable=False,
                    foreign_key="companies.id",
                    indexed=True,
                ),
                Column(
                    "lead_id",
                    "UUID",
                    foreign_key="leads.id",
                ),
                Column(
                    "conversation_id",
                    "UUID",
                    foreign_key="conversations.id",
                ),
                Column("channel", "VARCHAR"),
                Column(
                    "template_id",
                    "UUID",
                    foreign_key="message_templates.id",
                ),
                Column("attempt_number", "INTEGER"),
                Column("scheduled_at", "TIMESTAMP"),
                Column("sent_at", "TIMESTAMP"),
                Column("status", "VARCHAR"),
                Column("stop_reason", "VARCHAR"),
                Column("created_at", "TIMESTAMP"),
            ],
            indexes=[
                ("company_id", "scheduled_at"),
                ("company_id", "lead_id"),
            ],
            unique_constraints=[],
        ),

        "message_templates": Table(
            name="message_templates",
            domain="OPERATIONS",
            columns=[
                Column("id", "UUID", primary_key=True),
                Column(
                    "company_id",
                    "UUID",
                    nullable=False,
                    foreign_key="companies.id",
                    indexed=True,
                ),
                Column("name", "VARCHAR"),
                Column("channel", "VARCHAR"),
                Column("content", "TEXT"),
                Column("purpose", "VARCHAR"),
                Column("active", "BOOLEAN"),
                Column("created_at", "TIMESTAMP"),
                Column("updated_at", "TIMESTAMP"),
            ],
            indexes=[
                ("company_id",),
            ],
            unique_constraints=[],
        ),

        "appointments": Table(
            name="appointments",
            domain="OPERATIONS",
            columns=[
                Column("id", "UUID", primary_key=True),
                Column(
                    "company_id",
                    "UUID",
                    nullable=False,
                    foreign_key="companies.id",
                    indexed=True,
                ),
                Column(
                    "lead_id",
                    "UUID",
                    foreign_key="leads.id",
                ),
                Column(
                    "customer_id",
                    "UUID",
                    foreign_key="customers.id",
                ),
                Column(
                    "location_id",
                    "UUID",
                    foreign_key="locations.id",
                ),
                Column(
                    "service_id",
                    "UUID",
                    foreign_key="services.id",
                ),
                Column(
                    "assigned_user_id",
                    "UUID",
                    foreign_key="users.id",
                ),
                Column("external_id", "VARCHAR"),
                Column("start_time", "TIMESTAMP"),
                Column("end_time", "TIMESTAMP"),
                Column("status", "VARCHAR"),
                Column("confirmation_status", "VARCHAR"),
                Column("created_at", "TIMESTAMP"),
                Column("updated_at", "TIMESTAMP"),
            ],
            indexes=[
                ("company_id", "start_time"),
                ("company_id", "lead_id"),
            ],
            unique_constraints=[],
        ),

        "appointment_events": Table(
            name="appointment_events",
            domain="OPERATIONS",
            columns=[
                Column("id", "UUID", primary_key=True),
                Column(
                    "company_id",
                    "UUID",
                    nullable=False,
                    foreign_key="companies.id",
                    indexed=True,
                ),
                Column(
                    "appointment_id",
                    "UUID",
                    nullable=False,
                    foreign_key="appointments.id",
                    indexed=True,
                ),
                Column("event_type", "VARCHAR"),
                Column("previous_status", "VARCHAR"),
                Column("new_status", "VARCHAR"),
                Column("actor_type", "VARCHAR"),
                Column("metadata", "JSON"),
                Column("created_at", "TIMESTAMP"),
            ],
            indexes=[
                ("company_id", "appointment_id"),
            ],
            unique_constraints=[],
        ),

        "jobs": Table(
            name="jobs",
            domain="OPERATIONS",
            columns=[
                Column("id", "UUID", primary_key=True),
                Column(
                    "company_id",
                    "UUID",
                    nullable=False,
                    foreign_key="companies.id",
                    indexed=True,
                ),
                Column(
                    "appointment_id",
                    "UUID",
                    foreign_key="appointments.id",
                ),
                Column(
                    "lead_id",
                    "UUID",
                    foreign_key="leads.id",
                ),
                Column(
                    "customer_id",
                    "UUID",
                    foreign_key="customers.id",
                ),
                Column(
                    "service_id",
                    "UUID",
                    foreign_key="services.id",
                ),
                Column(
                    "assigned_user_id",
                    "UUID",
                    foreign_key="users.id",
                ),
                Column("status", "VARCHAR"),
                Column("completed_at", "TIMESTAMP"),
                Column("job_value", "DECIMAL"),
                Column("currency", "VARCHAR"),
                Column("created_at", "TIMESTAMP"),
                Column("updated_at", "TIMESTAMP"),
            ],
            indexes=[
                ("company_id", "appointment_id"),
                ("company_id", "customer_id"),
            ],
            unique_constraints=[],
        ),

        # ========================================================
        # REVENUE DOMAIN
        # ========================================================

        "revenue_records": Table(
            name="revenue_records",
            domain="REVENUE",
            columns=[
                Column("id", "UUID", primary_key=True),
                Column(
                    "company_id",
                    "UUID",
                    nullable=False,
                    foreign_key="companies.id",
                    indexed=True,
                ),
                Column(
                    "lead_id",
                    "UUID",
                    foreign_key="leads.id",
                ),
                Column(
                    "job_id",
                    "UUID",
                    foreign_key="jobs.id",
                ),
                Column(
                    "customer_id",
                    "UUID",
                    foreign_key="customers.id",
                ),
                Column("amount", "DECIMAL"),
                Column("currency", "VARCHAR"),
                Column("revenue_date", "DATE"),
                Column("source", "VARCHAR"),
                Column("external_id", "VARCHAR"),
                Column("status", "VARCHAR"),
                Column("created_at", "TIMESTAMP"),
                Column("updated_at", "TIMESTAMP"),
            ],
            indexes=[
                ("company_id", "revenue_date"),
                ("company_id", "lead_id"),
                ("company_id", "job_id"),
            ],
            unique_constraints=[],
        ),

        "revenue_attributions": Table(
            name="revenue_attributions",
            domain="REVENUE",
            columns=[
                Column("id", "UUID", primary_key=True),
                Column(
                    "company_id",
                    "UUID",
                    nullable=False,
                    foreign_key="companies.id",
                    indexed=True,
                ),
                Column(
                    "revenue_id",
                    "UUID",
                    nullable=False,
                    foreign_key="revenue_records.id",
                ),
                Column(
                    "lead_id",
                    "UUID",
                    foreign_key="leads.id",
                ),
                Column(
                    "job_id",
                    "UUID",
                    foreign_key="jobs.id",
                ),
                Column("attribution_type", "VARCHAR"),
                Column("attribution_confidence", "DECIMAL"),
                Column("attributed_amount", "DECIMAL"),
                Column("method", "VARCHAR"),
                Column("created_at", "TIMESTAMP"),
            ],
            indexes=[
                ("company_id", "revenue_id"),
                ("company_id", "lead_id"),
            ],
            unique_constraints=[],
        ),

        "recoveries": Table(
            name="recoveries",
            domain="REVENUE",
            columns=[
                Column("id", "UUID", primary_key=True),
                Column(
                    "company_id",
                    "UUID",
                    nullable=False,
                    foreign_key="companies.id",
                    indexed=True,
                ),
                Column(
                    "lead_id",
                    "UUID",
                    foreign_key="leads.id",
                ),
                Column("recovery_type", "VARCHAR"),
                Column("trigger", "VARCHAR"),
                Column("action", "VARCHAR"),
                Column("result", "VARCHAR"),
                Column(
                    "appointment_id",
                    "UUID",
                    foreign_key="appointments.id",
                ),
                Column(
                    "job_id",
                    "UUID",
                    foreign_key="jobs.id",
                ),
                Column(
                    "revenue_id",
                    "UUID",
                    foreign_key="revenue_records.id",
                ),
                Column("recovered_at", "TIMESTAMP"),
                Column("metadata", "JSON"),
            ],
            indexes=[
                ("company_id", "lead_id"),
                ("company_id", "recovered_at"),
            ],
            unique_constraints=[],
        ),

        # ========================================================
        # SYSTEM DOMAIN
        # ========================================================

        "analytics_events": Table(
            name="analytics_events",
            domain="SYSTEM",
            columns=[
                Column("id", "UUID", primary_key=True),
                Column(
                    "company_id",
                    "UUID",
                    nullable=False,
                    foreign_key="companies.id",
                    indexed=True,
                ),
                Column(
                    "lead_id",
                    "UUID",
                    foreign_key="leads.id",
                ),
                Column("event_type", "VARCHAR"),
                Column("source", "VARCHAR"),
                Column("metadata", "JSON"),
                Column("created_at", "TIMESTAMP"),
            ],
            indexes=[
                ("company_id", "created_at"),
                ("company_id", "lead_id"),
            ],
            unique_constraints=[],
        ),

        "audit_logs": Table(
            name="audit_logs",
            domain="SYSTEM",
            columns=[
                Column("id", "UUID", primary_key=True),
                Column(
                    "company_id",
                    "UUID",
                    nullable=False,
                    foreign_key="companies.id",
                    indexed=True,
                ),
                Column(
                    "user_id",
                    "UUID",
                    foreign_key="users.id",
                ),
                Column("action", "VARCHAR"),
                Column("entity_type", "VARCHAR"),
                Column("entity_id", "UUID"),
                Column("old_values", "JSON"),
                Column("new_values", "JSON"),
                Column("ip_address", "VARCHAR"),
                Column("created_at", "TIMESTAMP"),
            ],
            indexes=[
                ("company_id", "created_at"),
                ("company_id", "entity_type", "entity_id"),
            ],
            unique_constraints=[],
        ),

        "system_errors": Table(
            name="system_errors",
            domain="SYSTEM",
            columns=[
                Column("id", "UUID", primary_key=True),
                Column(
                    "company_id",
                    "UUID",
                    nullable=False,
                    foreign_key="companies.id",
                    indexed=True,
                ),
                Column("service", "VARCHAR"),
                Column("error_type", "VARCHAR"),
                Column("message", "TEXT"),
                Column("severity", "VARCHAR"),
                Column("metadata", "JSON"),
                Column("resolved", "BOOLEAN"),
                Column("created_at", "TIMESTAMP"),
                Column("resolved_at", "TIMESTAMP"),
            ],
            indexes=[
                ("company_id", "created_at"),
                ("company_id", "resolved"),
            ],
            unique_constraints=[],
        ),
    }

    # ============================================================
    # HELPER METHODS
    # ============================================================

    @classmethod
    def get_table(cls, table_name):
        """Return a table by its exact name."""
        return cls.TABLES[table_name]

    @classmethod
    def get_all_tables(cls):
        """Return all database tables."""
        return cls.TABLES

    @classmethod
    def table_names(cls):
        """Return all table names."""
        return list(cls.TABLES.keys())

    @classmethod
    def tables_by_domain(cls, domain):
        """Return tables belonging to one domain."""
        return {
            name: table
            for name, table in cls.TABLES.items()
            if table.domain == domain
        }


# ================================================================
# DEFAULT DATABASE DESIGN OBJECT
# ================================================================

db = DatabaseDesign()


# ================================================================
# BASIC SELF-CHECK
# ================================================================

if __name__ == "__main__":
    print(f"Database tables: {len(DatabaseDesign.TABLES)}")

    for domain in DatabaseDesign.DOMAINS:
        tables = DatabaseDesign.tables_by_domain(domain)
        print(f"{domain}: {len(tables)} tables")