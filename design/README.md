# BrainKB Design Documents

## Documents

- **`brainkb-architecture.md`** — the architecture design document. Organized in six parts: Context (users, use cases), Architecture (L0–L4 zoom levels, key sequence flows), MVP (competency fixture, scope), Contracts (identifier governance, claim/provenance, graph release, operational readiness, ontology/FAIR), Strategy (store/query, API boundary, cache/memory), and Epics and Traceability.

## Document Structure

`brainkb-architecture.md` has six parts. Contracts say what the system must satisfy; strategies explain why it is shaped the way it is.

| Part | Sections | What it answers |
| --- | --- | --- |
| **Context** | Users and Actors · Use Cases | Who uses BrainKB and what they need to accomplish |
| **Architecture** | Five Architecture Zoom Levels · Key Sequence Flows | How the system is structured at every level of detail, and how data flows at runtime |
| **MVP** | MVP Competency Fixture · MVP Scope | The grounding fixture and capability boundary for the first release |
| **Contracts** | Identifier Governance · Claim and Provenance · Graph Release and Projection · Operational Readiness · Ontology Alignment and FAIR | Binding requirements the system must satisfy — each contract has a testable review question |
| **Strategy** | Store and Query · API Boundary and Service Decomposition · Cache and Agent Memory | Design decisions with rationale — explains the trade-offs behind the architecture |
| **Epics and Traceability** | Epic User Stories · Traceability Matrix · Contract Traceability Matrix | User-facing goals, bootstrap priority, and cross-references between epics, contracts, and architecture levels |


## `original_source/`

Contains the original document from which `brainkb-architecture.md` was derived. Kept for historical reference only — do not edit it.
