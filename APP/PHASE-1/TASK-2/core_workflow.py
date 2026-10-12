from enum import Enum
import logging
from dataclasses import dataclass
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s"
)

logger = logging.getLogger("core-workflow")


class LeadState(str, Enum):
    NEW = "NEW"
    CONTACTED = "CONTACTED"
    UNDERSTANDING = "UNDERSTANDING"
    QUALIFYING = "QUALIFYING"
    QUALIFIED = "QUALIFIED"
    READY_TO_BOOK = "READY_TO_BOOK"
    BOOKING = "BOOKING"
    BOOKED = "BOOKED"
    RESCHEDULED = "RESCHEDULED"
    COMPLETED = "COMPLETED"
    REVENUE_ATTRIBUTED = "REVENUE_ATTRIBUTED"
    RECOVERED = "RECOVERED"

    UNQUALIFIED = "UNQUALIFIED"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    FOLLOW_UP = "FOLLOW_UP"
    NO_RESPONSE = "NO_RESPONSE"
    CANCELLED = "CANCELLED"
    NO_SHOW = "NO_SHOW"
    OLD_LEAD = "OLD_LEAD"
    REACTIVATION = "REACTIVATION"


class NextAction(str, Enum):
    ASK_QUESTION = "ASK_QUESTION"
    FOLLOW_UP = "FOLLOW_UP"
    BOOK_APPOINTMENT = "BOOK_APPOINTMENT"
    CONFIRM_APPOINTMENT = "CONFIRM_APPOINTMENT"
    RESCHEDULE = "RESCHEDULE"
    CANCEL = "CANCEL"
    ANSWER_FAQ = "ANSWER_FAQ"
    HANDOFF_HUMAN = "HANDOFF_HUMAN"
    REACTIVATE = "REACTIVATE"
    CLOSE_LEAD = "CLOSE_LEAD"


class EventType(str, Enum):
    INCOMING_CALL = "INCOMING_CALL"
    MISSED_CALL = "MISSED_CALL"
    INCOMING_SMS = "INCOMING_SMS"
    INCOMING_EMAIL = "INCOMING_EMAIL"
    AFTER_HOURS_LEAD = "AFTER_HOURS_LEAD"
    CRM_LEAD_CREATED = "CRM_LEAD_CREATED"
    APPOINTMENT_UPDATED = "APPOINTMENT_UPDATED"
    JOB_COMPLETED = "JOB_COMPLETED"


@dataclass
class InboundEvent:
    id: str
    company_id: str
    source: str
    event_type: EventType
    external_id: str
    timestamp: datetime
    payload: dict


class InvalidTransitionError(Exception):
    """Raised when an invalid lead-state transition is requested."""


ALLOWED_TRANSITIONS = {
    LeadState.NEW: {
        LeadState.CONTACTED,
        LeadState.OLD_LEAD,
    },

    LeadState.CONTACTED: {
        LeadState.UNDERSTANDING,
        LeadState.NO_RESPONSE,
        LeadState.HUMAN_REVIEW,
    },

    LeadState.UNDERSTANDING: {
        LeadState.QUALIFYING,
        LeadState.HUMAN_REVIEW,
        LeadState.FOLLOW_UP,
    },

    LeadState.QUALIFYING: {
        LeadState.QUALIFIED,
        LeadState.UNQUALIFIED,
        LeadState.HUMAN_REVIEW,
        LeadState.FOLLOW_UP,
    },

    LeadState.QUALIFIED: {
        LeadState.READY_TO_BOOK,
        LeadState.UNQUALIFIED,
        LeadState.HUMAN_REVIEW,
    },

    LeadState.READY_TO_BOOK: {
        LeadState.BOOKING,
        LeadState.FOLLOW_UP,
        LeadState.HUMAN_REVIEW,
    },

    LeadState.BOOKING: {
        LeadState.BOOKED,
        LeadState.FOLLOW_UP,
        LeadState.HUMAN_REVIEW,
    },

    LeadState.BOOKED: {
        LeadState.RESCHEDULED,
        LeadState.CANCELLED,
        LeadState.NO_SHOW,
        LeadState.COMPLETED,
    },

    LeadState.RESCHEDULED: {
        LeadState.BOOKED,
        LeadState.CANCELLED,
    },

    LeadState.COMPLETED: {
        LeadState.REVENUE_ATTRIBUTED,
    },

    LeadState.REVENUE_ATTRIBUTED: {
        LeadState.RECOVERED,
    },

    LeadState.NO_RESPONSE: {
        LeadState.FOLLOW_UP,
    },

    LeadState.FOLLOW_UP: {
        LeadState.UNDERSTANDING,
        LeadState.NO_RESPONSE,
        LeadState.HUMAN_REVIEW,
    },

    LeadState.OLD_LEAD: {
        LeadState.REACTIVATION,
    },

    LeadState.REACTIVATION: {
        LeadState.QUALIFYING,
        LeadState.HUMAN_REVIEW,
        LeadState.FOLLOW_UP,
    },

    LeadState.UNQUALIFIED: set(),

    LeadState.HUMAN_REVIEW: set(),

    LeadState.CANCELLED: set(),

    LeadState.NO_SHOW: {
        LeadState.FOLLOW_UP,
    },

    LeadState.RECOVERED: set(),
}


class CoreWorkflow:
    def __init__(self, company_id: str):
        if not company_id:
            raise ValueError("company_id is required")

        self.company_id = company_id

        logger.info(
            "Core Workflow initialized | company_id=%s",
            company_id
        )

    def transition(
        self,
        current_state: LeadState,
        next_state: LeadState
    ) -> LeadState:

        allowed_states = ALLOWED_TRANSITIONS.get(
            current_state,
            set()
        )

        if next_state not in allowed_states:
            logger.error(
                "Invalid transition | %s -> %s",
                current_state.value,
                next_state.value
            )

            raise InvalidTransitionError(
                f"Invalid transition: "
                f"{current_state.value} -> {next_state.value}"
            )

        logger.info(
            "State transition | %s -> %s",
            current_state.value,
            next_state.value
        )

        return next_state

    def process_event(self, event: InboundEvent) -> LeadState:

        if event.company_id != self.company_id:
            raise ValueError(
                "Event company_id does not match workflow company_id"
            )

        logger.info(
            "Processing inbound event | "
            "event_id=%s | type=%s",
            event.id,
            event.event_type.value
        )

        if event.event_type == EventType.MISSED_CALL:
            return self.transition(
                LeadState.NEW,
                LeadState.CONTACTED
            )

        if event.event_type in {
            EventType.INCOMING_CALL,
            EventType.INCOMING_SMS,
            EventType.INCOMING_EMAIL,
            EventType.AFTER_HOURS_LEAD,
            EventType.CRM_LEAD_CREATED,
        }:
            return self.transition(
                LeadState.NEW,
                LeadState.CONTACTED
            )

        if event.event_type == EventType.APPOINTMENT_UPDATED:
            return LeadState.BOOKED

        if event.event_type == EventType.JOB_COMPLETED:
            return LeadState.COMPLETED

        raise ValueError(
            f"Unsupported event type: {event.event_type}"
        )