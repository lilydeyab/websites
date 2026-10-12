import logging

from data_system_needs import DataSystemNeeds


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s"
)

logger = logging.getLogger("task3-validator")


def test_domains():
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


def test_required_entities():
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
        len(required_entities)
    )


def test_entity_integrity():
    for entity_name, entity in DataSystemNeeds.ENTITIES.items():
        assert entity.name
        assert entity.domain in DataSystemNeeds.DOMAINS
        assert entity.fields

    logger.info("PASS | Entity/domain integrity")


def test_multi_tenant_isolation():
    for entity_name in DataSystemNeeds.MULTI_TENANT_ENTITIES:
        entity = DataSystemNeeds.get_entity(entity_name)

        assert entity.requires_company_id is True
        assert "company_id" in entity.fields

    logger.info(
        "PASS | Multi-tenant company isolation requirements"
    )


def test_ai_extraction_traceability():
    extraction = DataSystemNeeds.get_entity(
        "ai_extraction"
    )

    required_fields = {
        "value",
        "source_message_id",
        "confidence",
        "created_at",
    }

    assert required_fields.issubset(
        set(extraction.fields)
    )

    logger.info(
        "PASS | AI extraction traceability requirements"
    )


def test_ai_decision_requirements():
    decision = DataSystemNeeds.get_entity(
        "ai_decision"
    )

    required_fields = {
        "decision_type",
        "decision",
        "reason",
        "confidence",
        "rules_evaluated",
        "created_at",
    }

    assert required_fields.issubset(
        set(decision.fields)
    )

    logger.info(
        "PASS | AI decision requirements"
    )


def test_integration_security():
    integration = DataSystemNeeds.get_entity(
        "integration"
    )

    assert "credential_reference" in integration.fields
    assert "connection_status" in integration.fields

    logger.info(
        "PASS | Integration credential reference requirement"
    )


def test_revenue_chain():
    expected_chain = [
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

    assert DataSystemNeeds.REVENUE_CHAIN == expected_chain

    logger.info("PASS | Revenue chain")


def test_recovery_types():
    expected_recovery_types = {
        "MISSED_CALL",
        "AFTER_HOURS",
        "FOLLOW_UP",
        "OLD_LEAD",
        "APPOINTMENT",
    }

    assert (
        DataSystemNeeds.RECOVERY_TYPES
        == expected_recovery_types
    )

    logger.info("PASS | Recovery types")


def test_channels():
    expected_channels = {
        "PHONE",
        "SMS",
        "EMAIL",
        "OTHER",
    }

    assert DataSystemNeeds.CHANNELS == expected_channels

    logger.info("PASS | Communication channels")


def test_user_roles():
    expected_roles = {
        "OWNER",
        "ADMIN",
        "MANAGER",
        "STAFF",
    }

    assert DataSystemNeeds.USER_ROLES == expected_roles

    logger.info("PASS | User roles")


def test_appointment_job_separation():
    appointment = DataSystemNeeds.get_entity(
        "appointment"
    )

    job = DataSystemNeeds.get_entity(
        "job"
    )

    assert appointment.name != job.name
    assert "appointment_id" in job.fields

    logger.info(
        "PASS | Appointment / Job separation"
    )


def test_revenue_linked_to_job():
    revenue = DataSystemNeeds.get_entity(
        "revenue"
    )

    assert "job_id" in revenue.fields

    logger.info(
        "PASS | Revenue linked to actual Job"
    )


def test_revenue_attribution():
    attribution = DataSystemNeeds.get_entity(
        "revenue_attribution"
    )

    required_fields = {
        "revenue_id",
        "lead_id",
        "job_id",
        "attributed_amount",
        "method",
        "confidence",
    }

    assert required_fields.issubset(
        set(attribution.fields)
    )

    logger.info(
        "PASS | Revenue attribution requirements"
    )


def test_recovery_requirements():
    recovery = DataSystemNeeds.get_entity(
        "recovery"
    )

    required_fields = {
        "lead_id",
        "recovery_type",
        "recovery_source",
        "recovery_action",
        "appointment_id",
        "job_id",
        "revenue_id",
        "recovered_amount",
        "status",
        "created_at",
    }

    assert required_fields.issubset(
        set(recovery.fields)
    )

    logger.info(
        "PASS | Recovery data requirements"
    )


def test_audit_trail():
    audit = DataSystemNeeds.get_entity(
        "audit_log"
    )

    required_fields = {
        "user_id",
        "action",
        "entity_type",
        "entity_id",
        "old_value",
        "new_value",
        "created_at",
    }

    assert required_fields.issubset(
        set(audit.fields)
    )

    logger.info(
        "PASS | Audit trail requirements"
    )


def test_system_error_tracking():
    system_error = DataSystemNeeds.get_entity(
        "system_error"
    )

    required_fields = {
        "service",
        "error_type",
        "message",
        "request_id",
        "severity",
        "resolved",
    }

    assert required_fields.issubset(
        set(system_error.fields)
    )

    logger.info(
        "PASS | System error tracking requirements"
    )


def test_required_relationships():
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
        ("Job", "Revenue Record"),
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


def test_base_structure():
    assert DataSystemNeeds.validate_structure() is True

    logger.info(
        "PASS | Base data specification"
    )


def run_validation():
    logger.info("========================================")
    logger.info("TASK 3 VALIDATION START")
    logger.info("========================================")

    test_domains()
    test_required_entities()
    test_entity_integrity()
    test_multi_tenant_isolation()
    test_ai_extraction_traceability()
    test_ai_decision_requirements()
    test_integration_security()
    test_revenue_chain()
    test_recovery_types()
    test_channels()
    test_user_roles()
    test_appointment_job_separation()
    test_revenue_linked_to_job()
    test_revenue_attribution()
    test_recovery_requirements()
    test_audit_trail()
    test_system_error_tracking()
    test_required_relationships()
    test_base_structure()

    logger.info("========================================")
    logger.info("TASK 3 VALIDATION PASSED")
    logger.info("========================================")


if __name__ == "__main__":
    run_validation()