import logging
from datetime import datetime

from core_workflow import (
    ALLOWED_TRANSITIONS,
    CoreWorkflow,
    EventType,
    InboundEvent,
    InvalidTransitionError,
    LeadState,
)


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s"
)

logger = logging.getLogger("task2-validator")


def test_workflow_initialization():
    logger.info("Testing workflow initialization...")

    workflow = CoreWorkflow("company-001")

    assert workflow.company_id == "company-001"

    logger.info("PASS | Workflow initialization")


def test_valid_state_transitions():
    logger.info("Testing valid state transitions...")

    workflow = CoreWorkflow("company-001")

    state = workflow.transition(
        LeadState.NEW,
        LeadState.CONTACTED
    )

    assert state == LeadState.CONTACTED

    state = workflow.transition(
        LeadState.CONTACTED,
        LeadState.UNDERSTANDING
    )

    assert state == LeadState.UNDERSTANDING

    state = workflow.transition(
        LeadState.UNDERSTANDING,
        LeadState.QUALIFYING
    )

    assert state == LeadState.QUALIFYING

    state = workflow.transition(
        LeadState.QUALIFYING,
        LeadState.QUALIFIED
    )

    assert state == LeadState.QUALIFIED

    state = workflow.transition(
        LeadState.QUALIFIED,
        LeadState.READY_TO_BOOK
    )

    assert state == LeadState.READY_TO_BOOK

    logger.info("PASS | Valid state transitions")


def test_invalid_transition():
    logger.info("Testing invalid state transition rejection...")

    workflow = CoreWorkflow("company-001")

    try:
        workflow.transition(
            LeadState.NEW,
            LeadState.BOOKED
        )

    except InvalidTransitionError:
        logger.info("PASS | Invalid transition rejected")
        return

    raise AssertionError(
        "Invalid transition was not rejected"
    )


def test_follow_up_loop():
    logger.info("Testing follow-up loop...")

    workflow = CoreWorkflow("company-001")

    state = workflow.transition(
        LeadState.NO_RESPONSE,
        LeadState.FOLLOW_UP
    )

    assert state == LeadState.FOLLOW_UP

    state = workflow.transition(
        LeadState.FOLLOW_UP,
        LeadState.UNDERSTANDING
    )

    assert state == LeadState.UNDERSTANDING

    logger.info("PASS | Follow-up loop")


def test_booking_recovery_loop():
    logger.info("Testing booking recovery loop...")

    workflow = CoreWorkflow("company-001")

    state = workflow.transition(
        LeadState.BOOKED,
        LeadState.RESCHEDULED
    )

    assert state == LeadState.RESCHEDULED

    state = workflow.transition(
        LeadState.RESCHEDULED,
        LeadState.BOOKED
    )

    assert state == LeadState.BOOKED

    logger.info("PASS | Booking recovery loop")


def test_old_lead_reactivation():
    logger.info("Testing old-lead reactivation flow...")

    workflow = CoreWorkflow("company-001")

    state = workflow.transition(
        LeadState.OLD_LEAD,
        LeadState.REACTIVATION
    )

    assert state == LeadState.REACTIVATION

    state = workflow.transition(
        LeadState.REACTIVATION,
        LeadState.QUALIFYING
    )

    assert state == LeadState.QUALIFYING

    logger.info("PASS | Old-lead reactivation")


def test_inbound_event_processing():
    logger.info("Testing inbound event processing...")

    workflow = CoreWorkflow("company-001")

    event = InboundEvent(
        id="event-001",
        company_id="company-001",
        source="phone",
        event_type=EventType.MISSED_CALL,
        external_id="call-001",
        timestamp=datetime.now(),
        payload={
            "phone": "+15550000000"
        }
    )

    state = workflow.process_event(event)

    assert state == LeadState.CONTACTED

    logger.info("PASS | Inbound event processing")


def test_company_isolation():
    logger.info("Testing company isolation...")

    workflow = CoreWorkflow("company-001")

    event = InboundEvent(
        id="event-002",
        company_id="company-002",
        source="sms",
        event_type=EventType.INCOMING_SMS,
        external_id="sms-001",
        timestamp=datetime.now(),
        payload={
            "message": "I need a plumber"
        }
    )

    try:
        workflow.process_event(event)

    except ValueError:
        logger.info("PASS | Cross-company event rejected")
        return

    raise AssertionError(
        "Cross-company event was not rejected"
    )


def test_required_transitions_exist():
    logger.info("Testing required workflow branches...")

    required_branches = [
        (LeadState.NEW, LeadState.CONTACTED),
        (LeadState.QUALIFIED, LeadState.READY_TO_BOOK),
        (LeadState.READY_TO_BOOK, LeadState.BOOKING),
        (LeadState.BOOKING, LeadState.BOOKED),
        (LeadState.BOOKED, LeadState.RESCHEDULED),
        (LeadState.RESCHEDULED, LeadState.BOOKED),
        (LeadState.COMPLETED, LeadState.REVENUE_ATTRIBUTED),
        (LeadState.REVENUE_ATTRIBUTED, LeadState.RECOVERED),
        (LeadState.OLD_LEAD, LeadState.REACTIVATION),
        (LeadState.REACTIVATION, LeadState.QUALIFYING),
    ]

    for current_state, next_state in required_branches:
        assert next_state in ALLOWED_TRANSITIONS[current_state]

    logger.info("PASS | Required workflow branches")


# =========================
# DEBUGGING / EDGE CASES
# =========================

def test_empty_company_id():
    logger.info("Testing empty company_id rejection...")

    try:
        CoreWorkflow("")

    except ValueError:
        logger.info("PASS | Empty company_id rejected")
        return

    raise AssertionError(
        "Empty company_id was not rejected"
    )


def test_final_state_cannot_continue():
    logger.info("Testing final-state protection...")

    workflow = CoreWorkflow("company-001")

    try:
        workflow.transition(
            LeadState.RECOVERED,
            LeadState.BOOKED
        )

    except InvalidTransitionError:
        logger.info("PASS | Final state protected")
        return

    raise AssertionError(
        "Final state accepted an invalid transition"
    )


def test_unsupported_event():
    logger.info("Testing unsupported event rejection...")

    workflow = CoreWorkflow("company-001")

    class FakeEventType:
        value = "UNSUPPORTED_EVENT"

    event = InboundEvent(
        id="event-invalid",
        company_id="company-001",
        source="test",
        event_type=FakeEventType(),
        external_id="external-invalid",
        timestamp=datetime.now(),
        payload={}
    )

    try:
        workflow.process_event(event)

    except ValueError:
        logger.info("PASS | Unsupported event rejected")
        return

    raise AssertionError(
        "Unsupported event was not rejected"
    )


def test_terminal_states():
    logger.info("Testing terminal states...")

    terminal_states = [
        LeadState.UNQUALIFIED,
        LeadState.HUMAN_REVIEW,
        LeadState.CANCELLED,
        LeadState.RECOVERED,
    ]

    workflow = CoreWorkflow("company-001")

    for state in terminal_states:
        assert ALLOWED_TRANSITIONS[state] == set()

    logger.info("PASS | Terminal states protected")


def test_cross_company_workflow_protection():
    logger.info("Testing cross-company workflow protection...")

    workflow = CoreWorkflow("company-A")

    event_from_b = InboundEvent(
        id="event-cross-company",
        company_id="company-B",
        source="sms",
        event_type=EventType.INCOMING_SMS,
        external_id="sms-cross-company",
        timestamp=datetime.now(),
        payload={
            "message": "Hello"
        }
    )

    try:
        workflow.process_event(event_from_b)

    except ValueError:
        logger.info(
            "PASS | Cross-company workflow access rejected"
        )
        return

    raise AssertionError(
        "Cross-company workflow access was not rejected"
    )


def main():
    logger.info("========================================")
    logger.info("TASK 2 VALIDATION START")
    logger.info("========================================")

    test_workflow_initialization()
    test_valid_state_transitions()
    test_invalid_transition()
    test_follow_up_loop()
    test_booking_recovery_loop()
    test_old_lead_reactivation()
    test_inbound_event_processing()
    test_company_isolation()
    test_required_transitions_exist()

    # Debugging / Edge-case checkpoint
    test_empty_company_id()
    test_final_state_cannot_continue()
    test_unsupported_event()
    test_terminal_states()
    test_cross_company_workflow_protection()

    logger.info("========================================")
    logger.info("TASK 2 VALIDATION PASSED")
    logger.info("========================================")


if __name__ == "__main__":
    main()