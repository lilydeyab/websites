import json
import logging
from pathlib import Path


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s"
)

logger = logging.getLogger("task1-validator")


ROOT = Path(__file__).resolve().parents[2]
PRODUCT_DOCS = ROOT / "docs" / "product"

REQUIRED_FILES = [
    "target_customer.md",
    "use_cases.md",
    "qualification_criteria.md",
    "task1_definition.json",
]

EXPECTED_USE_CASE_COUNT = 12


def validate_required_files():
    logger.info("Checking Task 1 documentation files...")

    missing = []

    for filename in REQUIRED_FILES:
        path = PRODUCT_DOCS / filename

        if path.exists():
            logger.info("FOUND | %s", filename)
        else:
            logger.error("MISSING | %s", filename)
            missing.append(filename)

    assert not missing, f"Missing required files: {missing}"


def load_definition():
    path = PRODUCT_DOCS / "task1_definition.json"

    logger.info("Loading machine-readable Task 1 definition...")

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def validate_task_metadata(data):
    logger.info("Validating task metadata...")

    task = data["task"]

    assert task["id"] == "PHASE1-TASK1"
    assert task["name"] == "Target Customer & Use Cases"
    assert task["status"] == "implemented"

    logger.info("PASS | Task metadata")


def validate_market(data):
    logger.info("Validating market definition...")

    market = data["market_reference"]

    assert market["naics"] == "238220"
    assert market["us_establishments_2023"] == 111207
    assert market["employees_20_plus"] == 12601
    assert market["employees_50_plus"] == 4217
    assert market["premium_proxy_is_not_actual_tam"] is True

    logger.info("PASS | Market definition")


def validate_architecture(data):
    logger.info("Validating core architecture decision...")

    architecture = data["architecture"]

    assert architecture["model"] == "one_core_engine_multiple_scenarios"
    assert architecture["independent_system_per_use_case"] is False

    logger.info("PASS | One Core Engine / Multiple Scenarios")


def validate_use_cases(data):
    logger.info("Validating use cases...")

    use_cases = data["use_cases"]

    assert len(use_cases) == EXPECTED_USE_CASE_COUNT

    ids = [use_case["id"] for use_case in use_cases]

    expected_ids = [
        f"UC-{number:02d}"
        for number in range(1, EXPECTED_USE_CASE_COUNT + 1)
    ]

    assert ids == expected_ids

    names = [use_case["name"] for use_case in use_cases]

    assert "Missed Call Recovery" in names
    assert "After-Hours Recovery" in names
    assert "Lead Qualification" in names
    assert "Follow-Up Recovery" in names
    assert "Appointment Conversion" in names
    assert "Appointment Recovery" in names
    assert "FAQ / Objection Handling" in names
    assert "Old Lead Reactivation" in names
    assert "Incoming Conversation Handling" in names
    assert "Human Handoff" in names
    assert "Revenue Attribution" in names
    assert "Recovery Analytics" in names

    logger.info("PASS | %d use cases", len(use_cases))


def validate_document_content():
    logger.info("Validating documentation content...")

    target_customer = (
        PRODUCT_DOCS / "target_customer.md"
    ).read_text(encoding="utf-8")

    use_cases = (
        PRODUCT_DOCS / "use_cases.md"
    ).read_text(encoding="utf-8")

    qualification = (
        PRODUCT_DOCS / "qualification_criteria.md"
    ).read_text(encoding="utf-8")

    required_target_terms = [
        "Primary Market",
        "Initial Vertical",
        "Core Business Problem",
        "Economic-Fit Signals",
        "Economic-Fit Principle",
    ]

    required_use_case_terms = [
        "UC-01",
        "UC-02",
        "UC-03",
        "UC-04",
        "UC-05",
        "UC-06",
        "UC-07",
        "UC-08",
        "UC-09",
        "UC-10",
        "UC-11",
        "UC-12",
        "Core Engine Principle",
    ]

    required_qualification_terms = [
        "Inbound Lead Volume",
        "Missed Opportunities",
        "Follow-Up Leakage",
        "Appointment Leakage",
        "Average Job Value",
        "Recoverable Revenue",
        "Operational Capacity",
        "Required Integrations",
    ]

    for term in required_target_terms:
        assert term in target_customer, (
            f"Missing target-customer section: {term}"
        )

    for term in required_use_case_terms:
        assert term in use_cases, (
            f"Missing use-case section: {term}"
        )

    for term in required_qualification_terms:
        assert term in qualification, (
            f"Missing qualification section: {term}"
        )

    logger.info("PASS | Documentation content")


def main():
    logger.info("========================================")
    logger.info("TASK 1 VALIDATION START")
    logger.info("========================================")

    validate_required_files()

    data = load_definition()

    validate_task_metadata(data)
    validate_market(data)
    validate_architecture(data)
    validate_use_cases(data)
    validate_document_content()

    logger.info("========================================")
    logger.info("TASK 1 VALIDATION PASSED")
    logger.info("========================================")


if __name__ == "__main__":
    main()