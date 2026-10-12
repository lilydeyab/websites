from dataclasses import dataclass
from typing import List, Dict
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s"
)

logger = logging.getLogger("data-system-needs")


@dataclass(frozen=True)
class DataEntity:
    name: str
    domain: str
    description: str
    fields: List[str]
    requires_company_id: bool = True


class DataSystemNeeds:
    """
    Machine-readable specification of all data required
    by the AI Revenue Recovery System.

    This is a DATA REQUIREMENTS layer.
    It does not create database tables yet.
    Database design belongs to Task 4.
    """

    DOMAINS = (
        "COMPANY",
        "CUSTOMER",
        "AI",
        "OPERATIONS",
        "REVENUE",
        "SYSTEM",
    )

    ENTITIES: Dict[str, DataEntity] = {

        # ==========================================
        # COMPANY DOMAIN
        # ==========================================

        "company": DataEntity(
            name="Company",
            domain="COMPANY",
            description="Customer business / tenant.",
            fields=[
                "company_id",
                "name",
                "legal_name",
                "business_type",
                "industry",
                "phone",
                "email",
                "website",
                "timezone",
                "currency",
                "status",
                "created_at",
                "updated_at",
            ],
        ),

        "user": DataEntity(
            name="User",
            domain="COMPANY",
            description="Authenticated company user.",
            fields=[
                "user_id",
                "company_id",
                "role",
                "permissions",
                "authentication_data",
                "last_login",
                "account_status",
                "created_at",
                "updated_at",
            ],
        ),

        "location": DataEntity(
            name="Location",
            domain="COMPANY",
            description="Physical business location.",
            fields=[
                "location_id",
                "company_id",
                "name",
                "address",
                "city",
                "state",
                "zip",
                "timezone",
                "phone",
                "status",
            ],
        ),

        "service": DataEntity(
            name="Service",
            domain="COMPANY",
            description="Service offered by the company.",
            fields=[
                "service_id",
                "company_id",
                "name",
                "description",
                "category",
                "duration",
                "pricing_information",
                "availability",
                "status",
            ],
        ),

        "service_area": DataEntity(
            name="Service Area",
            domain="COMPANY",
            description="Geographic area served by the company.",
            fields=[
                "service_area_id",
                "company_id",
                "location_id",
                "area",
                "zip_codes",
                "cities",
                "status",
            ],
        ),

        "business_rule": DataEntity(
            name="Business Rule",
            domain="COMPANY",
            description="Configurable commercial or operational rule.",
            fields=[
                "rule_id",
                "company_id",
                "rule_type",
                "rule_name",
                "configuration",
                "priority",
                "enabled",
                "created_at",
                "updated_at",
            ],
        ),

        "integration": DataEntity(
            name="Integration",
            domain="COMPANY",
            description="External system integration configuration.",
            fields=[
                "integration_id",
                "company_id",
                "provider",
                "integration_type",
                "credential_reference",
                "connection_status",
                "last_sync",
                "last_error",
                "created_at",
                "updated_at",
            ],
        ),

        # ==========================================
        # CUSTOMER DOMAIN
        # ==========================================

        "customer": DataEntity(
            name="Customer",
            domain="CUSTOMER",
            description="Customer identity and contact information.",
            fields=[
                "customer_id",
                "company_id",
                "first_name",
                "last_name",
                "phone",
                "email",
                "address",
                "city",
                "state",
                "zip",
                "created_at",
                "updated_at",
            ],
        ),

        "lead": DataEntity(
            name="Lead",
            domain="CUSTOMER",
            description="Primary revenue opportunity entity.",
            fields=[
                "lead_id",
                "company_id",
                "customer_id",
                "source",
                "source_reference",
                "status",
                "intent",
                "service",
                "urgency",
                "qualification_status",
                "assigned_user",
                "created_at",
                "updated_at",
            ],
        ),

        "lead_event": DataEntity(
            name="Lead Event",
            domain="CUSTOMER",
            description="Historical event associated with a lead.",
            fields=[
                "lead_event_id",
                "company_id",
                "lead_id",
                "event_type",
                "source",
                "metadata",
                "created_at",
            ],
        ),

        "conversation": DataEntity(
            name="Conversation",
            domain="CUSTOMER",
            description="Customer communication session.",
            fields=[
                "conversation_id",
                "company_id",
                "lead_id",
                "channel",
                "status",
                "started_at",
                "ended_at",
            ],
        ),

        "message": DataEntity(
            name="Message",
            domain="CUSTOMER",
            description="Individual communication message.",
            fields=[
                "message_id",
                "company_id",
                "conversation_id",
                "sender_type",
                "sender_id",
                "receiver",
                "content",
                "channel",
                "external_id",
                "timestamp",
                "direction",
                "status",
                "ai_generated",
                "ai_confidence",
                "metadata",
            ],
        ),

        "lead_history": DataEntity(
            name="Lead History",
            domain="CUSTOMER",
            description="Historical state changes of a lead.",
            fields=[
                "history_id",
                "company_id",
                "lead_id",
                "previous_value",
                "new_value",
                "changed_by",
                "reason",
                "source",
                "timestamp",
            ],
        ),

        # ==========================================
        # AI DOMAIN
        # ==========================================

        "ai_extraction": DataEntity(
            name="AI Extraction",
            domain="AI",
            description="Structured information extracted by AI.",
            fields=[
                "extraction_id",
                "company_id",
                "conversation_id",
                "lead_id",
                "field_name",
                "value",
                "source_message_id",
                "confidence",
                "created_at",
            ],
        ),

        "ai_decision": DataEntity(
            name="AI Decision",
            domain="AI",
            description="AI-generated decision or suggested next action.",
            fields=[
                "decision_id",
                "company_id",
                "lead_id",
                "conversation_id",
                "decision_type",
                "decision",
                "trigger",
                "reason",
                "confidence",
                "rules_evaluated",
                "outcome",
                "created_at",
            ],
        ),

        "knowledge_document": DataEntity(
            name="Knowledge Document",
            domain="AI",
            description="Company-specific knowledge available to the AI.",
            fields=[
                "document_id",
                "company_id",
                "title",
                "content",
                "document_type",
                "version",
                "status",
                "updated_at",
            ],
        ),

        "human_handoff": DataEntity(
            name="Human Handoff",
            domain="AI",
            description="Escalation from AI to a human employee.",
            fields=[
                "handoff_id",
                "company_id",
                "lead_id",
                "conversation_id",
                "reason",
                "summary",
                "qualification",
                "collected_data",
                "recommended_action",
                "assigned_user",
                "status",
                "resolution",
                "created_at",
                "resolved_at",
            ],
        ),

        # ==========================================
        # OPERATIONS DOMAIN
        # ==========================================

        "follow_up": DataEntity(
            name="Follow-up",
            domain="OPERATIONS",
            description="Scheduled lead recovery communication.",
            fields=[
                "follow_up_id",
                "company_id",
                "lead_id",
                "conversation_id",
                "trigger",
                "scheduled_at",
                "channel",
                "template_id",
                "message",
                "attempt_number",
                "status",
                "sent_at",
                "response",
                "stop_reason",
                "failure_reason",
            ],
        ),

        "appointment": DataEntity(
            name="Appointment",
            domain="OPERATIONS",
            description="Scheduled service appointment.",
            fields=[
                "appointment_id",
                "company_id",
                "lead_id",
                "customer_id",
                "location_id",
                "service_id",
                "scheduled_at",
                "start_time",
                "end_time",
                "status",
                "assigned_user",
                "booking_source",
                "confirmation",
                "cancellation",
                "calendar_event_id",
                "external_id",
                "created_at",
                "updated_at",
            ],
        ),

        "appointment_event": DataEntity(
            name="Appointment Event",
            domain="OPERATIONS",
            description="Appointment lifecycle event.",
            fields=[
                "appointment_event_id",
                "company_id",
                "appointment_id",
                "event_type",
                "previous_status",
                "new_status",
                "metadata",
                "created_at",
            ],
        ),

        "job": DataEntity(
            name="Job",
            domain="OPERATIONS",
            description="Actual service job resulting from an appointment.",
            fields=[
                "job_id",
                "company_id",
                "appointment_id",
                "lead_id",
                "customer_id",
                "service_id",
                "technician",
                "status",
                "completed_at",
                "job_value",
                "invoice_reference",
                "external_id",
                "outcome",
                "created_at",
                "updated_at",
            ],
        ),

        # ==========================================
        # REVENUE DOMAIN
        # ==========================================

        "revenue": DataEntity(
            name="Revenue Record",
            domain="REVENUE",
            description="Recorded revenue generated by a job.",
            fields=[
                "revenue_id",
                "company_id",
                "job_id",
                "customer_id",
                "amount",
                "currency",
                "source",
                "external_id",
                "status",
                "revenue_date",
                "recorded_at",
            ],
        ),

        "revenue_attribution": DataEntity(
            name="Revenue Attribution",
            domain="REVENUE",
            description="Links revenue to the recovered opportunity.",
            fields=[
                "attribution_id",
                "company_id",
                "revenue_id",
                "lead_id",
                "job_id",
                "attribution_type",
                "attributed_amount",
                "method",
                "confidence",
                "created_at",
            ],
        ),

        "recovery": DataEntity(
            name="Recovery",
            domain="REVENUE",
            description="Recovered revenue opportunity.",
            fields=[
                "recovery_id",
                "company_id",
                "lead_id",
                "recovery_type",
                "recovery_source",
                "trigger",
                "previous_state",
                "recovery_action",
                "result",
                "appointment_id",
                "job_id",
                "revenue_id",
                "recovered_amount",
                "status",
                "created_at",
            ],
        ),

        # ==========================================
        # SYSTEM DOMAIN
        # ==========================================

        "analytics_event": DataEntity(
            name="Analytics Event",
            domain="SYSTEM",
            description="Business or system performance event.",
            fields=[
                "analytics_event_id",
                "company_id",
                "event_type",
                "entity_type",
                "entity_id",
                "actor",
                "source",
                "metadata",
                "outcome",
                "timestamp",
            ],
        ),

        "audit_log": DataEntity(
            name="Audit Log",
            domain="SYSTEM",
            description="Trace of important system or user actions.",
            fields=[
                "audit_id",
                "company_id",
                "user_id",
                "action",
                "entity_type",
                "entity_id",
                "old_value",
                "new_value",
                "ip_address",
                "user_agent",
                "created_at",
            ],
        ),

        "system_error": DataEntity(
            name="System Error",
            domain="SYSTEM",
            description="Production system error record.",
            fields=[
                "error_id",
                "company_id",
                "service",
                "error_type",
                "message",
                "stack_reference",
                "request_id",
                "severity",
                "resolved",
                "created_at",
            ],
        ),

        "security_event": DataEntity(
            name="Security Event",
            domain="SYSTEM",
            description="Authentication and security event.",
            fields=[
                "security_event_id",
                "company_id",
                "user_id",
                "event_type",
                "ip_address",
                "user_agent",
                "metadata",
                "timestamp",
            ],
        ),
    }

    RELATIONSHIPS = [
        ("Company", "User"),
        ("Company", "Location"),
        ("Company", "Service"),
        ("Company", "Service Area"),
        ("Company", "Business Rule"),
        ("Company", "Integration"),

        ("Company", "Customer"),
        ("Customer", "Lead"),
        ("Lead", "Lead Event"),
        ("Lead", "Lead History"),
        ("Lead", "Conversation"),
        ("Conversation", "Message"),

        ("Conversation", "AI Extraction"),
        ("Lead", "AI Extraction"),
        ("Lead", "AI Decision"),
        ("Conversation", "AI Decision"),
        ("Company", "Knowledge Document"),
        ("Lead", "Human Handoff"),
        ("Conversation", "Human Handoff"),

        ("Lead", "Follow-up"),
        ("Lead", "Appointment"),
        ("Customer", "Appointment"),
        ("Appointment", "Appointment Event"),
        ("Appointment", "Job"),

        ("Job", "Revenue Record"),
        ("Revenue Record", "Revenue Attribution"),
        ("Lead", "Revenue Attribution"),
        ("Lead", "Recovery"),
        ("Appointment", "Recovery"),
        ("Job", "Recovery"),
        ("Revenue Record", "Recovery"),

        ("Company", "Analytics Event"),
        ("Company", "Audit Log"),
        ("Company", "System Error"),
        ("Company", "Security Event"),
    ]

    MULTI_TENANT_ENTITIES = {
        entity_name
        for entity_name, entity in ENTITIES.items()
        if entity.requires_company_id
    }

    REVENUE_CHAIN = [
        "Company",
        "Customer",
        "Lead",
        "Conversation",
        "Qualification",
        "Appointment",
        "Job",
        "Revenue",
        "Attribution",
        "Recovery",
    ]

    RECOVERY_TYPES = {
        "MISSED_CALL",
        "AFTER_HOURS",
        "FOLLOW_UP",
        "OLD_LEAD",
        "APPOINTMENT",
    }

    CHANNELS = {
        "PHONE",
        "SMS",
        "EMAIL",
        "OTHER",
    }

    USER_ROLES = {
        "OWNER",
        "ADMIN",
        "MANAGER",
        "STAFF",
    }

    @classmethod
    def get_entities_by_domain(cls, domain: str) -> List[DataEntity]:
        """Return all data entities belonging to a domain."""

        return [
            entity
            for entity in cls.ENTITIES.values()
            if entity.domain == domain
        ]

    @classmethod
    def get_entity(cls, entity_name: str) -> DataEntity:
        """Return one entity definition."""

        if entity_name not in cls.ENTITIES:
            raise KeyError(
                f"Unknown data entity: {entity_name}"
            )

        return cls.ENTITIES[entity_name]

    @classmethod
    def validate_structure(cls) -> bool:
        """
        Validate the data requirements specification itself.

        This checks requirements only.
        It does not validate a database.
        """

        logger.info("Validating data-system requirements...")

        if len(cls.DOMAINS) != 6:
            raise AssertionError(
                "Expected exactly 6 data domains"
            )

        for entity_name, entity in cls.ENTITIES.items():

            if not entity.name:
                raise AssertionError(
                    f"Entity {entity_name} has no name"
                )

            if entity.domain not in cls.DOMAINS:
                raise AssertionError(
                    f"Invalid domain for {entity_name}"
                )

            if not entity.fields:
                raise AssertionError(
                    f"Entity {entity_name} has no fields"
                )

            if entity.requires_company_id:
                if "company_id" not in entity.fields:
                    raise AssertionError(
                        f"Multi-tenant entity missing company_id: "
                        f"{entity_name}"
                    )

        logger.info(
            "PASS | %d entities across %d domains",
            len(cls.ENTITIES),
            len(cls.DOMAINS),
        )

        return True


def validate_task3_architecture():
    logger.info("========================================")
    logger.info("TASK 3 ARCHITECTURE VALIDATION")
    logger.info("========================================")

    # 1. Validate domains
    expected_domains = {
        "COMPANY",
        "CUSTOMER",
        "AI",
        "OPERATIONS",
        "REVENUE",
        "SYSTEM",
    }

    assert set(DataSystemNeeds.DOMAINS) == expected_domains

    logger.info("PASS | Six data domains")


    # 2. Validate required entities
    required_entities = {
        "company",
        "user",
        "location",
        "service",
        "service_area",
        "business_rule",
        "integration",

        "customer",
        "lead",
        "lead_event",
        "conversation",
        "message",
        "lead_history",

        "ai_extraction",
        "ai_decision",
        "knowledge_document",
        "human_handoff",

        "follow_up",
        "appointment",
        "appointment_event",
        "job",

        "revenue",
        "revenue_attribution",
        "recovery",

        "analytics_event",
        "audit_log",
        "system_error",
        "security_event",
    }

    assert set(DataSystemNeeds.ENTITIES) == required_entities

    logger.info(
        "PASS | All required data entities present | count=%d",
        len(required_entities),
    )


    # 3. Validate all entities have a valid domain
    for entity in DataSystemNeeds.ENTITIES.values():
        assert entity.domain in DataSystemNeeds.DOMAINS
        assert entity.fields

    logger.info("PASS | Entity/domain integrity")


    # 4. Multi-tenant validation
    for entity_name in DataSystemNeeds.MULTI_TENANT_ENTITIES:
        entity = DataSystemNeeds.get_entity(entity_name)

        assert entity.requires_company_id is True
        assert "company_id" in entity.fields

    logger.info(
        "PASS | Multi-tenant company isolation requirements"
    )


    # 5. AI extraction requirements
    extraction = DataSystemNeeds.get_entity("ai_extraction")

    required_extraction_fields = {
        "value",
        "source_message_id",
        "confidence",
        "created_at",
    }

    assert required_extraction_fields.issubset(
        set(extraction.fields)
    )

    logger.info(
        "PASS | AI extraction traceability requirements"
    )


    # 6. Integration security requirement
    integration = DataSystemNeeds.get_entity("integration")

    assert "credential_reference" in integration.fields
    assert "connection_status" in integration.fields

    logger.info(
        "PASS | Integration credential reference requirement"
    )


    # 7. Revenue chain validation
    expected_revenue_chain = [
        "Company",
        "Customer",
        "Lead",
        "Conversation",
        "Qualification",
        "Appointment",
        "Job",
        "Revenue",
        "Attribution",
        "Recovery",
    ]

    assert DataSystemNeeds.REVENUE_CHAIN == expected_revenue_chain

    logger.info("PASS | Revenue chain")


    # 8. Recovery types
    expected_recovery_types = {
        "MISSED_CALL",
        "AFTER_HOURS",
        "FOLLOW_UP",
        "OLD_LEAD",
        "APPOINTMENT",
    }

    assert DataSystemNeeds.RECOVERY_TYPES == expected_recovery_types

    logger.info("PASS | Recovery types")


    # 9. Communication channels
    expected_channels = {
        "PHONE",
        "SMS",
        "EMAIL",
        "OTHER",
    }

    assert DataSystemNeeds.CHANNELS == expected_channels

    logger.info("PASS | Communication channels")


    # 10. User roles
    expected_roles = {
        "OWNER",
        "ADMIN",
        "MANAGER",
        "STAFF",
    }

    assert DataSystemNeeds.USER_ROLES == expected_roles

    logger.info("PASS | User roles")


    # 11. Appointment and Job must remain separate
    appointment = DataSystemNeeds.get_entity("appointment")
    job = DataSystemNeeds.get_entity("job")

    assert appointment.name != job.name
    assert "appointment_id" in job.fields

    logger.info(
        "PASS | Appointment / Job separation"
    )


    # 12. Revenue must connect to Job
    revenue = DataSystemNeeds.get_entity("revenue")

    assert "job_id" in revenue.fields

    logger.info(
        "PASS | Revenue linked to actual Job"
    )


    # 13. Attribution must connect revenue to lead/job
    attribution = DataSystemNeeds.get_entity(
        "revenue_attribution"
    )

    assert "revenue_id" in attribution.fields
    assert "lead_id" in attribution.fields
    assert "job_id" in attribution.fields
    assert "attributed_amount" in attribution.fields
    assert "method" in attribution.fields
    assert "confidence" in attribution.fields

    logger.info(
        "PASS | Revenue attribution requirements"
    )


    # 14. Auditability
    audit = DataSystemNeeds.get_entity("audit_log")

    required_audit_fields = {
        "user_id",
        "action",
        "entity_type",
        "entity_id",
        "old_value",
        "new_value",
        "created_at",
    }

    assert required_audit_fields.issubset(
        set(audit.fields)
    )

    logger.info(
        "PASS | Audit trail requirements"
    )


    # 15. System reliability data
    system_error = DataSystemNeeds.get_entity(
        "system_error"
    )

    required_error_fields = {
        "service",
        "error_type",
        "message",
        "request_id",
        "severity",
        "resolved",
    }

    assert required_error_fields.issubset(
        set(system_error.fields)
    )

    logger.info(
        "PASS | System error tracking requirements"
    )


    # 16. Required relationships
    required_relationships = {
        ("Company", "User"),
        ("Company", "Location"),
        ("Company", "Service"),
        ("Company", "Service Area"),
        ("Company", "Business Rule"),
        ("Company", "Integration"),
        ("Company", "Customer"),
        ("Customer", "Lead"),
        ("Lead", "Conversation"),
        ("Conversation", "Message"),
        ("Lead", "Appointment"),
        ("Appointment", "Job"),
        ("Job", "Revenue"),
        ("Revenue Record", "Revenue Attribution"),
        ("Lead", "Recovery"),
        ("Company", "Analytics Event"),
        ("Company", "Audit Log"),
        ("Company", "System Error"),
        ("Company", "Security Event"),
    }

    actual_relationships = set(
        DataSystemNeeds.RELATIONSHIPS
    )

    assert required_relationships.issubset(
        actual_relationships
    )

    logger.info(
        "PASS | Required data relationships"
    )


    # 17. Base specification validation
    assert DataSystemNeeds.validate_structure() is True

    logger.info(
        "PASS | Base data specification"
    )

    logger.info("========================================")
    logger.info("TASK 3 ARCHITECTURE VALIDATION PASSED")
    logger.info("========================================")


if __name__ == "__main__":
    logger.info("========================================")
    logger.info("TASK 3 DATA SYSTEM NEEDS START")
    logger.info("========================================")

    validate_task3_architecture()

    for domain in DataSystemNeeds.DOMAINS:
        entities = DataSystemNeeds.get_entities_by_domain(
            domain
        )

        logger.info(
            "%s | %d entities",
            domain,
            len(entities)
        )

    logger.info(
        "Total entities | %d",
        len(DataSystemNeeds.ENTITIES)
    )

    logger.info(
        "Revenue chain length | %d",
        len(DataSystemNeeds.REVENUE_CHAIN)
    )

    logger.info("========================================")
    logger.info("TASK 3 DATA SYSTEM NEEDS READY")
    logger.info("========================================")