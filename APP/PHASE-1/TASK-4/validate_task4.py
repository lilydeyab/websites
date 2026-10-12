"""
TASK 4 - Database Design Validator

Validates the final 28-table database architecture for the
AI Revenue Recovery System.

Run:
    python validate_task4.py
"""

from database_design import DatabaseDesign


db = DatabaseDesign()

PASS_COUNT = 0
FAIL_COUNT = 0


def log_pass(message):
    global PASS_COUNT
    PASS_COUNT += 1
    print(f"INFO | PASS | {message}")


def log_fail(message):
    global FAIL_COUNT
    FAIL_COUNT += 1
    print(f"ERROR | FAIL | {message}")


def require(condition, message):
    if condition:
        log_pass(message)
    else:
        log_fail(message)


def get_table(name):
    try:
        return db.get_table(name)
    except KeyError:
        return None


# ============================================================
# 1. DOMAINS
# ============================================================

def test_domains():
    expected = {
        "COMPANY",
        "CUSTOMER",
        "AI",
        "OPERATIONS",
        "REVENUE",
        "SYSTEM",
    }

    actual = set(db.DOMAINS)

    require(
        actual == expected,
        "domains"
    )


# ============================================================
# 2. REQUIRED TABLES
# ============================================================

def test_required_tables():
    expected = {
        # COMPANY
        "companies",
        "users",
        "company_users",
        "locations",
        "services",
        "service_areas",
        "business_rules",
        "integrations",

        # CUSTOMER
        "customers",
        "leads",
        "lead_events",
        "conversations",
        "messages",

        # AI
        "ai_extractions",
        "ai_decisions",
        "knowledge_documents",
        "human_handoffs",

        # OPERATIONS
        "follow_ups",
        "message_templates",
        "appointments",
        "appointment_events",
        "jobs",

        # REVENUE
        "revenue_records",
        "revenue_attributions",
        "recoveries",

        # SYSTEM
        "analytics_events",
        "audit_logs",
        "system_errors",
    }

    actual = set(db.table_names())

    require(
        actual == expected,
        "required tables"
    )


# ============================================================
# 3. TABLE COUNT
# ============================================================

def test_table_count():
    require(
        len(db.TABLES) == 28,
        "table count = 28"
    )


# ============================================================
# 4. TABLE INTEGRITY
# ============================================================

def test_table_integrity():
    valid = True

    for name, table in db.TABLES.items():

        if table.name != name:
            valid = False
            log_fail(
                f"table name mismatch: key={name}, table.name={table.name}"
            )

        primary_keys = [
            column
            for column in table.columns
            if column.primary_key
        ]

        if len(primary_keys) != 1:
            valid = False
            log_fail(
                f"{name} must have exactly one primary key"
            )

    if valid:
        log_pass("table integrity")


# ============================================================
# 5. DOMAIN DISTRIBUTION
# ============================================================

def test_domain_distribution():
    expected = {
        "COMPANY": 8,
        "CUSTOMER": 5,
        "AI": 4,
        "OPERATIONS": 5,
        "REVENUE": 3,
        "SYSTEM": 3,
    }

    actual = {}

    for table in db.TABLES.values():
        actual[table.domain] = actual.get(table.domain, 0) + 1

    require(
        actual == expected,
        f"domain distribution = {actual}"
    )


# ============================================================
# 6. TENANT COMPANY_ID COVERAGE
# ============================================================

def test_company_id_coverage():
    valid = True

    for name, table in db.TABLES.items():

        if name in {"companies", "users"}:
            continue

        columns = {column.name for column in table.columns}

        if "company_id" not in columns:
            valid = False
            log_fail(
                f"{name} missing company_id"
            )

    if valid:
        log_pass("tenant company_id coverage")


# ============================================================
# 7. COMPANY USER ISOLATION
# ============================================================

def test_company_user_isolation():
    table = get_table("company_users")

    if table is None:
        log_fail("company_users table missing")
        return

    names = {column.name for column in table.columns}

    require(
        {"company_id", "user_id", "role", "status"} <= names,
        "company_users isolation fields"
    )

    require(
        ("company_id", "user_id") in table.unique_constraints,
        "company_users UNIQUE(company_id,user_id)"
    )


# ============================================================
# 8. CUSTOMER INDEXES
# ============================================================

def test_customer_indexes():
    table = get_table("customers")

    require(
        ("company_id", "phone") in table.indexes,
        "customer phone index"
    )

    require(
        ("company_id", "email") in table.indexes,
        "customer email index"
    )


# ============================================================
# 9. LEAD INDEXES
# ============================================================

def test_lead_indexes():
    table = get_table("leads")

    require(
        ("company_id", "status") in table.indexes,
        "lead status index"
    )

    require(
        ("company_id", "created_at") in table.indexes,
        "lead created_at index"
    )

    require(
        ("company_id", "customer_id") in table.indexes,
        "lead customer index"
    )


# ============================================================
# 10. LEAD STRUCTURE
# ============================================================

def test_lead_structure():
    table = get_table("leads")

    required = {
        "company_id",
        "customer_id",
        "source",
        "channel",
        "status",
        "intent",
        "service_id",
        "location_id",
        "qualification_status",
        "assigned_user_id",
        "created_at",
        "updated_at",
    }

    names = {column.name for column in table.columns}

    require(
        required <= names,
        "lead core structure"
    )


# ============================================================
# 11. LEAD EVENTS
# ============================================================

def test_lead_events():
    table = get_table("lead_events")

    required = {
        "company_id",
        "lead_id",
        "event_type",
        "previous_status",
        "new_status",
        "actor_type",
        "metadata",
        "created_at",
    }

    names = {column.name for column in table.columns}

    require(
        required <= names,
        "lead timeline structure"
    )


# ============================================================
# 12. CONVERSATION INTEGRITY
# ============================================================

def test_conversations():
    table = get_table("conversations")

    names = {column.name for column in table.columns}

    require(
        {
            "company_id",
            "lead_id",
            "channel",
            "status",
            "external_id",
        } <= names,
        "conversation core structure"
    )

    require(
        ("company_id", "external_id") in table.unique_constraints,
        "conversation UNIQUE(company_id,external_id)"
    )


# ============================================================
# 13. MESSAGE TIMELINE
# ============================================================

def test_messages():
    table = get_table("messages")

    require(
        ("company_id", "conversation_id", "timestamp")
        in table.indexes,
        "message timeline index"
    )


# ============================================================
# 14. AI EXTRACTION TRACEABILITY
# ============================================================

def test_ai_extractions():
    table = get_table("ai_extractions")

    names = {column.name for column in table.columns}

    required = {
        "conversation_id",
        "lead_id",
        "message_id",
        "field_name",
        "field_value",
        "source",
        "confidence",
        "created_at",
    }

    require(
        required <= names,
        "AI extraction traceability"
    )


# ============================================================
# 15. AI DECISIONS
# ============================================================

def test_ai_decisions():
    table = get_table("ai_decisions")

    names = {column.name for column in table.columns}

    required = {
        "conversation_id",
        "lead_id",
        "decision_type",
        "trigger",
        "confidence",
        "business_rule_result",
        "created_at",
    }

    require(
        required <= names,
        "AI decision traceability"
    )


# ============================================================
# 16. AI DECISION TYPES
# ============================================================

def test_ai_decision_types():
    expected = {
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
    }

    require(
        set(db.AI_DECISION_TYPES) == expected,
        "AI decision types"
    )


# ============================================================
# 17. INTEGRATION SECURITY
# ============================================================

def test_integrations():
    table = get_table("integrations")

    names = {
        column.name.lower()
        for column in table.columns
    }

    forbidden = {
        "password",
        "secret",
        "secret_key",
        "api_key",
        "access_token",
        "refresh_token",
        "private_key",
    }

    exposed = names & forbidden

    require(
        not exposed,
        "integration security - no plaintext secret columns"
    )

    require(
        (
            "company_id",
            "provider",
            "external_account_id",
        ) in table.unique_constraints,
        "integration uniqueness"
    )


# ============================================================
# 18. APPOINTMENT STRUCTURE
# ============================================================

def test_appointments():
    table = get_table("appointments")

    names = {column.name for column in table.columns}

    required = {
        "company_id",
        "lead_id",
        "customer_id",
        "location_id",
        "service_id",
        "assigned_user_id",
        "start_time",
        "end_time",
        "status",
        "confirmation_status",
    }

    require(
        required <= names,
        "appointment structure"
    )


# ============================================================
# 19. APPOINTMENT STATUSES
# ============================================================

def test_appointment_statuses():
    expected = {
        "BOOKED",
        "CONFIRMED",
        "RESCHEDULED",
        "CANCELLED",
        "NO_SHOW",
        "COMPLETED",
    }

    require(
        set(db.APPOINTMENT_STATUSES) == expected,
        "appointment statuses"
    )


# ============================================================
# 20. APPOINTMENT EVENTS
# ============================================================

def test_appointment_events():
    table = get_table("appointment_events")

    names = {column.name for column in table.columns}

    required = {
        "company_id",
        "appointment_id",
        "event_type",
        "previous_status",
        "new_status",
        "actor_type",
        "created_at",
    }

    require(
        required <= names,
        "appointment event history"
    )


# ============================================================
# 21. JOB SEPARATION
# ============================================================

def test_jobs():
    table = get_table("jobs")

    names = {column.name for column in table.columns}

    required = {
        "appointment_id",
        "lead_id",
        "customer_id",
        "service_id",
        "job_value",
        "status",
    }

    require(
        required <= names,
        "job structure - appointment separated from job"
    )


# ============================================================
# 22. REVENUE CHAIN
# ============================================================

def test_revenue_chain():
    expected = [
        "companies",
        "customers",
        "leads",
        "conversations",
        "appointments",
        "jobs",
        "revenue_records",
        "revenue_attributions",
        "recoveries",
    ]

    actual = [
        name
        for name in expected
        if name in db.TABLES
    ]

    require(
        actual == expected,
        "revenue chain"
    )


# ============================================================
# 23. REVENUE RECORDS
# ============================================================

def test_revenue_records():
    table = get_table("revenue_records")

    names = {column.name for column in table.columns}

    required = {
        "company_id",
        "lead_id",
        "job_id",
        "customer_id",
        "amount",
        "currency",
        "revenue_date",
        "source",
        "status",
    }

    require(
        required <= names,
        "revenue record structure"
    )


# ============================================================
# 24. REVENUE ATTRIBUTION
# ============================================================

def test_revenue_attribution():
    table = get_table("revenue_attributions")

    names = {column.name for column in table.columns}

    required = {
        "company_id",
        "revenue_id",
        "lead_id",
        "job_id",
        "attribution_type",
        "attribution_confidence",
        "attributed_amount",
        "method",
    }

    require(
        required <= names,
        "revenue attribution structure"
    )


# ============================================================
# 25. RECOVERY TYPES
# ============================================================

def test_recovery_types():
    expected = {
        "MISSED_CALL",
        "AFTER_HOURS",
        "FOLLOW_UP",
        "OLD_LEAD",
        "APPOINTMENT",
    }

    require(
        set(db.RECOVERY_TYPES) == expected,
        "recovery types"
    )


# ============================================================
# 26. RECOVERY LINKS
# ============================================================

def test_recovery_links():
    table = get_table("recoveries")

    names = {column.name for column in table.columns}

    required = {
        "company_id",
        "lead_id",
        "recovery_type",
        "trigger",
        "action",
        "result",
        "appointment_id",
        "job_id",
        "revenue_id",
        "recovered_at",
    }

    require(
        required <= names,
        "recovery links"
    )


# ============================================================
# 27. AUDITABILITY
# ============================================================

def test_audit_logs():
    table = get_table("audit_logs")

    names = {column.name for column in table.columns}

    required = {
        "company_id",
        "user_id",
        "action",
        "entity_type",
        "entity_id",
        "old_values",
        "new_values",
        "created_at",
    }

    require(
        required <= names,
        "auditability"
    )


# ============================================================
# 28. SYSTEM ERRORS
# ============================================================

def test_system_errors():
    table = get_table("system_errors")

    names = {column.name for column in table.columns}

    required = {
        "company_id",
        "service",
        "error_type",
        "message",
        "severity",
        "resolved",
        "created_at",
        "resolved_at",
    }

    require(
        required <= names,
        "system error tracking"
    )


# ============================================================
# 29. USER ROLES
# ============================================================

def test_user_roles():
    expected = {
        "OWNER",
        "ADMIN",
        "MANAGER",
        "STAFF",
    }

    require(
        set(db.USER_ROLES) == expected,
        "user roles"
    )


# ============================================================
# 30. FOREIGN KEY TARGETS
# ============================================================

def test_foreign_key_targets():
    valid = True

    for table in db.TABLES.values():

        for column in table.columns:

            if not column.foreign_key:
                continue

            target_table, target_column = column.foreign_key.split(".")

            if target_table not in db.TABLES:
                valid = False
                log_fail(
                    f"{table.name}.{column.name} references missing table "
                    f"{target_table}"
                )
                continue

            target = get_table(target_table)

            target_columns = {
                c.name
                for c in target.columns
            }

            if target_column not in target_columns:
                valid = False
                log_fail(
                    f"{table.name}.{column.name} references missing column "
                    f"{column.foreign_key}"
                )

    if valid:
        log_pass("foreign key targets")


# ============================================================
# 31. DATABASE ARCHITECTURE
# ============================================================

def test_database_architecture():
    require(
        len(db.TABLES) == 28
        and set(db.DOMAINS) == {
            "COMPANY",
            "CUSTOMER",
            "AI",
            "OPERATIONS",
            "REVENUE",
            "SYSTEM",
        },
        "database architecture"
    )


# ============================================================
# RUN ALL TESTS
# ============================================================

def run_all_tests():

    tests = [
        test_domains,
        test_required_tables,
        test_table_count,
        test_table_integrity,
        test_domain_distribution,
        test_company_id_coverage,
        test_company_user_isolation,
        test_customer_indexes,
        test_lead_indexes,
        test_lead_structure,
        test_lead_events,
        test_conversations,
        test_messages,
        test_ai_extractions,
        test_ai_decisions,
        test_ai_decision_types,
        test_integrations,
        test_appointments,
        test_appointment_statuses,
        test_appointment_events,
        test_jobs,
        test_revenue_chain,
        test_revenue_records,
        test_revenue_attribution,
        test_recovery_types,
        test_recovery_links,
        test_audit_logs,
        test_system_errors,
        test_user_roles,
        test_foreign_key_targets,
        test_database_architecture,
    ]

    for test in tests:
        try:
            test()
        except Exception as error:
            log_fail(
                f"{test.__name__} crashed: {error}"
            )

    print()
    print("=" * 60)
    print(f"TOTAL PASSED: {PASS_COUNT}")
    print(f"TOTAL FAILED: {FAIL_COUNT}")
    print("=" * 60)

    if FAIL_COUNT == 0:
        print("INFO | TASK 4 VALIDATION PASSED")
    else:
        print("ERROR | TASK 4 VALIDATION FAILED")


if __name__ == "__main__":
    run_all_tests()