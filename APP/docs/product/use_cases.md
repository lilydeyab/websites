# Core Use Cases

The system is built around one Core Engine with multiple scenarios.

The 12 use cases do not represent 12 independent systems.

They are scenarios processed through the same core workflow.

---

## UC-01 — Missed Call Recovery

Missed Call
→ Detect
→ Create / Resolve Lead
→ Contact Customer
→ Understand Need
→ Qualify
→ Book / Handoff

---

## UC-02 — After-Hours Recovery

After-hours inquiry
→ Lead Intake
→ Conversation
→ Qualification
→ Follow-up / Booking

---

## UC-03 — Lead Qualification

Incoming Lead
→ Extract Information
→ Apply Business Rules
→ Qualified / Unqualified / Human Review

---

## UC-04 — Follow-Up Recovery

Lead
→ No Response / No Booking
→ Follow-up Sequence
→ Customer Response
→ Resume Core Workflow

---

## UC-05 — Appointment Conversion

Qualified Lead
→ Check Availability
→ Customer Selects Slot
→ Create Appointment
→ Confirm Appointment

---

## UC-06 — Appointment Recovery

Booked Appointment
→ Cancellation / No-show / Reschedule
→ Recovery Workflow
→ Alternative Appointment

---

## UC-07 — FAQ / Objection Handling

Customer Question
→ Understand Intent
→ Knowledge Lookup
→ Answer
→ Continue Core Workflow

---

## UC-08 — Old Lead Reactivation

Old Lead
→ Reactivation
→ Conversation
→ Qualification
→ Booking

---

## UC-09 — Incoming Conversation Handling

All supported communication channels enter the Core Engine.

Phone
SMS
Email
Other Integration
→ Core Engine

---

## UC-10 — Human Handoff

When the AI should not continue:

AI
→ Handoff Decision
→ Human Handoff Packet

The packet should contain:

- Lead
- Intent
- Conversation Summary
- Collected Data
- Qualification Status
- Reason for Escalation
- Recommended Next Action

---

## UC-11 — Revenue Attribution

Lead
→ Appointment
→ Job
→ Revenue
→ Attribution

The system should determine which recovered opportunity generated attributable revenue.

---

## UC-12 — Recovery Analytics

The system should expose recovery metrics including:

- Leads Recovered
- Qualified Leads
- Appointments
- Completed Jobs
- Attributed Revenue
- Recovery Revenue
- ROI

---

#
# Core Engine Principle

All use cases enter and interact with the same Core Engine.

Core Engine:

Lead Flow
+ Conversation
+ Qualification
+ Next Action
+ Follow-up
+ Booking
+ Human Handoff
+ Job Outcome
+ Revenue Attribution
+ Recovery Analytics

This prevents the product from becoming twelve independent systems.