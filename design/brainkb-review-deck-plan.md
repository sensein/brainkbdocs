# BrainKB Review Deck Plan

Status: review preparation artifact  
Source design doc: `brainkb-architecture.md`  

## Source-Of-Truth Workflow

This markdown file is the core planning artifact. The review deck is a derivative output.

Future changes should follow this order:

1. Update `brainkb-architecture-deck-redesign.md`.
2. Rebuild the review deck from the markdown with `npm run build`.
3. Review the generated Reveal/HTML deck and PNG previews under `output/reveal/`.
4. If a PowerPoint export is needed, run `npm run build:pptx` as a secondary derivative.

Do not hand-edit generated decks as primary sources. If a slide needs to change, update the markdown first, then regenerate.

The preferred review artifact is now the structured Reveal-style HTML deck. It uses Mermaid source diagrams rendered to static SVG assets during the build so the review deck remains stable without live diagram rendering.

## Source Deck Disposition

| Original content | Slides | Decision for rebuild |
| --- | ---: | --- |
| Cover and motivation | 1-2 | Retain, rewrite as problem statement and target architecture promise. |
| Basal ganglia grounding case | 3 | Retain as the running example that ties identifiers, archives, papers, and claims together. |
| Knowledge review | 4 | Retain as Epic 01. |
| Hypothesis generation | 5 | Retain as Epic 02, explicitly marked as post-MVP unless core graph/search is present. |
| Methods and models | 6 | Retain as Epic 03. |
| Resource landscape | 7 | Retain as Epic 04. |
| Reading guide and L0-L4 architecture | 8-13 | Retain the five zooms, rename and clarify each level. |
| Polyglot persistence | 14 | Merge into L2 and L4, with RDF as canonical knowledge and Postgres/pgvector for operational state. |
| Sequence diagrams | 15-22 | Retain as appendix flows and link each flow to epic stories. |
| Deployment | 23 | Retain as deployment appendix and optional main-deck architecture proof. |
| Evolution/versioning | 24 | Retain and promote into L4 Knowledge/Data Model. |
| Agents and LLMs | 25 | Retain as platform boundary guidance and AI story support. |
| Operational and capability use cases | 26-31 | Retain as Epics 05-10. |
| Open questions | 32 | Retain as engineering decisions and next backlog candidates. |

## Reviewer-Driven Revision Principles

The review deck should now make the following principles visible before diving into detailed epics:

- Use one concrete basal ganglia competency fixture, not a purely schematic example.
- Treat hypothesis generation and assistant workflows as gated capabilities, not baseline promises.
- Define identifier, claim, provenance, graph-release, and projection contracts before implementation issues are written.
- Make deployment, ingest state, activation, observability, auth, backup, and external-service failure behavior reviewable.
- Keep RDF/named graphs as the canonical trust layer while allowing GraphQL/Postgres projections for efficient reads.
- Preserve the source-of-truth workflow: update this Markdown first, then regenerate the deck.

## Rebuilt Deck Outline

The rebuild should produce a concise engineering narrative first, with detail moved into appendices. Suggested structure:

### Main Deck

1. BrainKB target architecture: what we are building and why.
2. The federation problem: neuroscience knowledge is fragmented by resource, schema, archive, and paper.
3. MVP competency fixture: BG taxonomy atlas integration question, h5ad/assets, Patch-seq IDs, publications/claims, seed data bar, success criterion.
4. End-to-end evidence story: atlas/package plus archive file assets plus publication/preprint extraction to reviewed claim to entity page to provenance audit.
5. User story map: ten epics grouped into explore, curate, ingest, federate, reason, and audit.
6. MVP boundary and gated capabilities: what is reviewable now, what waits for more data/services.
7. Store/query strategy: canonical RDF/named graphs plus GraphQL/Postgres projections with parity rules.
8. Cache and agent memory strategy: cache service, memory service, memory horizons, promotion gates, and freshness/revalidation.
9. L0 Ecosystem: actors, external resources, agents, identity/policy boundaries, and upstream variability.
10. L1 Product/API Boundary: product workflows call one BrainKB API rather than many backend services.
11. L2 Minimal Deployable Slice: one UI, one API, one worker, connector adapters, stores, and future split points.
12. L3 Core Workflow Components: search, ingest state machine, projection sync, cache lifecycle, memory lifecycle, release activation, provenance, federation, assistant.
13. L4 Knowledge/Data Model: identifier policy, claim bundles, provenance, named graphs, release manifests, projection semantics, cache keys, and memory item semantics.
14. Operational readiness: deployment modes, job lifecycle, observability, auth scopes, backups, and external-service failure behavior.
15. Ontology alignment and FAIR: application profile, vocabulary versions, crosswalk provenance, validation, release metadata.
16. Traceability and engineering decisions: stories, contracts, architecture levels, and open choices.

### Appendix Slides

17. Epic 01 - Knowledge Review.
18. Epic 02 - Hypothesis Generation.
19. Epic 03 - Methods and Models.
20. Epic 04 - Resource Landscape.
21. Epic 05 - Entity Exploration.
22. Epic 06 - Curated Claim Ingest.
23. Epic 07 - Automated Partner Release Ingest.
24. Epic 08 - Cross-KB Federated Query.
25. Epic 09 - Grounded Assistant.
26. Epic 10 - Provenance Audit.
27. Sequence flow: search.
28. Sequence flow: ingest.
29. Sequence flow: release activation and projection readiness.
30. Sequence flow: cache invalidation and memory revalidation.
31. Sequence flow: drill-down/provenance.
32. Sequence flow: auth.
33. Sequence flow: federation.
34. Sequence flow: curator.
35. Sequence flow: assistant.
36. Deployment view.
37. Observability, backup, and restore appendix.
38. Open engineering backlog candidates.

## Authoring Guidance For The Later Deck

- Do not use the generated HTML/PPTXGen export as the long-term source of truth.
- Use the current PPTX and web export only to recover content, diagrams, and terminology.
- Keep the Markdown document as the deck source and generate review decks from it.
- Prefer the Reveal/HTML derivative for architecture review because it supports clearer sections and Mermaid diagrams.
- Treat PowerPoint as an optional export path, not the canonical authoring system.
- Keep the main deck understandable without appendix slides.
- Make every use-case slide trace to one architecture level and one sequence flow.
- Use the BG taxonomy atlas fixture consistently so architecture does not feel abstract and the services are visibly reusable beyond one domain.
- Keep cache and memory visible as platform services with different trust semantics: cache is performance; memory is workflow state; canonical graph writes require review.
- Avoid adding new technologies unless they clarify service boundaries or replace existing choices.

## Validation Checklist

- [x] The original ten major use cases are retained as cleaned epic stories.
- [x] Each epic uses actor, goal, value, trigger, preconditions, acceptance criteria, architecture dependencies, and suggested slides.
- [x] Each epic lists bootstrap assumptions and dependencies prioritized by ease of resolution.
- [x] All five architecture zoom levels are defined and distinct.
- [x] The triplestore strategy includes a GraphQL/Postgres projection variant and sync/update-cycle implications.
- [x] The browser-facing topology is minimized: `brainkb-ui` calls one `brainkb-api`, while internal modules and stores remain hidden from the UI.
- [x] L2 presents a minimal deployable slice before optional service splits.
- [x] Cache and agent memory are defined as platform services with lifecycle, freshness, retention, and promotion rules.
- [x] The MVP competency fixture defines a bounded BG taxonomy atlas integration question, including h5ad/source assets, Patch-seq IDs, file-level archive links, publication/claim/evidence graph, and seed-data bar.
- [x] Identifier, claim/provenance, graph-release, projection, operations, ontology-alignment, and FAIR contracts are explicit enough for review.
- [x] The traceability matrix maps stories to architecture levels, sequence flows, and capabilities.
- [x] Contract traceability maps reviewer concerns to epics, architecture levels, and review questions.
- [x] The rebuilt deck outline can be followed without opening the original 32-slide deck.
- [x] The default generated review deck is a Reveal-style HTML deck with Mermaid diagrams rendered as static SVG assets.
- [x] GitHub project boards and implementation issues are deferred until after design doc review.
