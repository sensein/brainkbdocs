# BrainKB Architecture

Status: design document  
Audience: engineering team  

## Revised Intent

The rebuilt deck should be an engineering reference for building BrainKB. It should explain what the platform must let people do, what system capabilities those workflows require, and how the architecture supports them.

The current deck has the right ingredients: provenance, federation, versioned named graphs, use-case packages, core services, concrete containers, deployment, and LLM/agent boundaries. The rebuild should make those ingredients easier to act on by organizing the story in this order:

1. Why BrainKB exists: neuroscience knowledge is fragmented across resources, schemas, papers, archives, and tools.
2. Who uses it: researchers, curators, pipelines, reviewers, agents, and application services.
3. What they need to do: ten epic-level stories with clear acceptance criteria.
4. What the platform must provide: stable identifiers, claim provenance, named graph versioning, federated reads, validated ingest, review workflows, and grounded AI.
5. How the architecture supports this: five zoom levels that move from ecosystem to data model.

The deck should stop feeling like a collection of architecture diagrams plus scattered examples. It should become a traceable argument: user stories drive capabilities, capabilities drive service boundaries, and service boundaries drive data/model choices.

After informatics, operations, and neuroscience review, the next revision should also make three contracts explicit enough for engineering discussion:

1. What minimum seed knowledge is enough to make the researcher workflows credible.
2. What trust primitives make identifiers, claims, provenance, graph releases, and projections auditable.
3. What operational behaviors make ingest, deployment, auth, backup, external calls, and rollback safe enough to build against.

## MVP Competency Fixture

Purpose: prove that BrainKB can answer a bounded neuroscience evidence-review question with enough concrete data to expose identity, provenance, versioning, source disagreement, projection behavior, file-level lineage, literature-derived claims, and reusable platform services.

Primary competency question:

> For a basal ganglia taxonomy atlas class, Patch-seq cell, gene, gene set, or related preprint, can BrainKB show the taxonomy assignment, BICAN model/release context, h5ad/source assets, gene and gene-set evidence, Patch-seq cell IDs, file-level archive artifacts, related publications, people, resources, claims, estimated analysis graphs, support/conflict/silence states, and graph version as of a selected date?

BG integration fixture scope:

- Atlas and taxonomy package:
  - Use the ABC Atlas / Human-Mammalian Brain Atlas Basal Ganglia package as the running seed resource.
  - Capture the BICAN model or application profile used by the atlas package.
  - Represent taxonomy release/version, class IDs, labels, aliases, hierarchy, crosswalks, species, anatomical region, assay/modality, and lifecycle state.
  - Preserve links to h5ad assets, expression matrices, metadata tables, spatial assets, gene expression matrices, marker genes, gene sets, and Patch-seq component references.
- Cell and specimen identity:
  - Represent gene names with stable gene identifiers and explicit source vocabulary/version.
  - Represent Patch-seq cell IDs, specimen IDs, taxonomy assignments, mapping method, mapping confidence, and quality-control state.
  - Resolve associated archive assets at file/asset level when available, not only dataset-level metadata.
  - Store dataset ID, asset/path/file ID, checksum or version, modality, format such as NWB or h5ad, and cell/specimen-level linkage.
- Publication and claim network:
  - Represent bioRxiv/preprint/publication records where the taxonomy was created, described, reused, or cited.
  - Extract or curate people, organizations, affiliations, resource mentions, dataset/tool/atlas references, and relevant identifiers.
  - Represent claims and evidence from text, figures, tables, notebooks, and estimated analysis graphs as reviewable claim bundles.
  - Preserve support, conflict, "not stated", inferred, superseded, and replaced states with graph release/as-of context.
- Reusable platform and tooling:
  - Build the fixture with adapters and transforms that are reusable outside BG: ABC Atlas adapter, h5ad metadata extractor, gene/gene-set resolver, Patch-seq cell mapper, DANDI/BIL/NeMO-style asset resolver, publication/NER/claim extractor, analysis-graph/evidence packager, provenance exporter, release manifest builder, projection parity checks, cache invalidation, and memory revalidation.
  - Treat BG as an integration test for shared platform capabilities, not as a one-off hardcoded demo.

Competency tasks:

- Given a BG taxonomy class, show marker genes/gene sets, species/region/modality qualifiers, BICAN model/release context, h5ad cells/assets, Patch-seq cells, source publications, and evidence state.
- Given a Patch-seq cell ID, show taxonomy class assignment, mapping method/confidence, source h5ad or NWB/file assets, archive asset links, related publications, and evidence graph.
- Given a gene or gene set, show related BG taxonomy classes, marker/evidence claims, source assets, source releases, and conflict/silence states.
- Given a paper or preprint, show detected people, organizations, resources, datasets, tools, atlas mentions, claims, source fragments, figures/tables when available, and links to taxonomy/assets.
- Given an as-of date, show which taxonomy classes, assets, claims, publications, mappings, and release manifests were active, superseded, deprecated, or unavailable.

Required graph object types:

- `TaxonomyRelease`, `TaxonClass`, `Cell`, `Specimen`, `Gene`, `GeneSet`, `Dataset`, `FileAsset`, `Publication`, `Preprint`, `Person`, `Organization`, `Resource`, `Claim`, `Evidence`, `AnalysisGraph`, `Notebook`, `WorkflowRun`, `ModelProfile`, `IdentifierMapping`, and `ReleaseManifest`.

Required identifier rule:

- Every seed entity must have a canonical BrainKB IRI before review.
- Every seed entity should carry at least one resolvable external identifier or source-specific accession when one exists.
- Placeholder identifiers may be used only in internal fixture drafts; they must not appear on review slides as if they were real external IDs.
- Cross-resource equivalence must state its relation type: exact match, close match, broad/narrow match, related match, or unresolved candidate.
- Patch-seq cell/specimen IDs and file assets must remain queryable as first-class identifiers, even when the public-facing researcher question starts from a taxonomy class, gene, or paper.

Example claim table shape:

| Field | Required meaning |
| --- | --- |
| `claim_id` | Stable claim identifier exposed in RDF and projections. |
| `subject_iri` | Canonical BrainKB entity IRI. |
| `predicate_iri` | Predicate from the application profile. |
| `object_iri_or_value` | Object entity IRI or literal value. |
| `species_id` | Taxon identifier, such as `NCBITaxon:10090` or `NCBITaxon:9606`. |
| `region_id` | Anatomical region identifier when available. |
| `assay_or_modality` | Experimental modality or assay context. |
| `source_id` | Publication, dataset, release, or upstream resource identifier. |
| `evidence_id` | Evidence node or source fragment backing the claim. |
| `support_state` | Supported, conflicting, refuted, not stated, inferred, or pending review. |
| `evidence_grade` | Lightweight confidence/evidence-strength label, not a claim of scientific certainty. |
| `graph_uri` | Named graph containing the claim. |
| `release_id` | Immutable graph release identifier. |
| `as_of` | Date or timestamp used for as-of query behavior. |
| `lifecycle_state` | Draft, active, superseded, deprecated, or withdrawn. |

Acceptance expansion:

- Entity pages must exist for taxonomy classes, Patch-seq cells/specimens, genes, gene sets, file assets, datasets, papers/preprints, people, organizations, resources, claims, and evidence.
- The UI must expose file-level lineage and source asset links, not just top-level dataset metadata.
- Publication-derived claims must show whether they were manually curated, NER/extraction-derived, inferred from an analysis graph, or imported from a source package.
- Reusable adapters and derived artifacts must be named in release manifests so other domains can reuse the same services and tooling.

Architecture stress points:

- L0 external resources: ABC Atlas/GitHub package, BICAN model/profile, DANDI/BIL/NeMO-style archives, bioRxiv, PubMed/Semantic Scholar-style metadata, ontology/gene services, repository/notebook artifacts, and partner KBs.
- L1 product/API: evidence review, taxonomy/cell/file lookup, paper/preprint curation, release/as-of view, saved workspace, and optional assistant evidence expansion behind one `brainkb-api`.
- L2 containers/stores: `brainkb-ui`, `brainkb-api`, `brainkb-worker`, connector adapters, object storage, Postgres/GraphQL projections, canonical graph store, cache, and memory.
- L3 workflows: atlas ingest, h5ad metadata extraction, Patch-seq mapping ingest, archive asset resolution, publication NER/claim extraction, analysis-graph provenance packaging, projection parity, cache invalidation, and memory revalidation.
- L4 model: identifiers, taxonomy/model profile, cell/specimen/file asset lineage, claim/evidence bundles, named graphs, release manifests, provenance activities, mappings, lifecycle states, and derived/workflow-state contract.

Source anchors to verify before fixture implementation:

- [ABC Atlas access repository](https://github.com/AllenInstitute/abc_atlas_access) and [ABC Atlas data access docs](https://alleninstitute.github.io/abc_atlas_access/intro.html).
- [HMBA-BG notebooks](https://alleninstitute.github.io/abc_atlas_access/descriptions/HMBA-BG_notebooks.html) and data descriptions, including taxonomy/clustering, h5ad/gene expression, spatial, and Patch-seq components.
- Archive mappings from Patch-seq cell/specimen IDs to DANDI/BIL/NeMO-style assets and files. Exact DANDI/BIL/NeMO asset identifiers should be validated before becoming fixture facts.
- Publication/preprint corpus where the taxonomy was created, reused, cited, or discussed.

Researcher success criterion:

- A neuroscientist can start from a BG taxonomy class, Patch-seq cell ID, gene/gene set, file asset, or bioRxiv/preprint record and reach taxonomy context, supporting evidence, source files, people/resources/claims, and release/as-of state in less than five minutes.

## MVP Capability Boundaries

The MVP should be framed as a trustable evidence-review and ingest slice, not a broad discovery assistant.

MVP capabilities:

- Search by label, synonym, identifier, and fixture-specific source accession.
- Entity detail pages with source-attributed properties and evidence badges.
- Claim-level provenance drilldown with source, contributor, activity, graph, schema, release, and lifecycle state.
- Curated claim ingest from fixture data or manually authored paper-derived claims.
- Named graph release creation, validation, projection readiness, activation, and rollback.
- Optional GraphQL/Postgres projections for high-traffic read views, provided parity checks against canonical RDF pass.
- Local/self-hosted demonstration with reproducible fixtures and external services disabled, mocked, or clearly marked optional.

Post-MVP or gated capabilities:

- Hypothesis generation over broad neuroscience knowledge.
- Grounded assistant answers beyond the seeded fixture.
- General cross-KB federation across heterogeneous live sources.
- Automated ingestion from many partner release practices.
- Evidence-strength scoring across heterogeneous claims at production scale.
- Broad methods/models recommendation beyond a small structured catalog.

Hypothesis and assistant guardrails:

- Initial outputs should be framed as candidate gap surfacing, triage, or evidence expansion, not discovery of new biological facts.
- The system should expose sparse-graph bias, literature-retrieval bias, ontology-mapping uncertainty, correlation-versus-mechanism limits, and species/modality transfer risk.
- A generated suggestion should not be written to the canonical graph without curator or reviewer action.
- If local evidence coverage is low, the product should fall back to search, external evidence expansion, or "insufficient evidence" rather than over-answering.

## Identifier Governance Contract

BrainKB needs explicit identifier governance because almost every epic depends on stable identity and explainable cross-resource alignment.

Canonical IRI policy:

- BrainKB may mint canonical IRIs for platform-owned entities, claims, graph releases, activities, and fixture records.
- Canonical IRIs should follow stable, documented patterns by entity class; generated IDs must not encode mutable labels.
- Source-specific identifiers must be preserved as cross-references, not discarded after canonicalization.
- The resolver should return labels, type, lifecycle state, equivalent identifiers, graph/release context, and deprecation or supersession metadata.

Equivalence policy:

- Use `owl:sameAs` only for very strong identity equivalence.
- Prefer SKOS-style mapping relations for most cross-resource alignments: exact match, close match, broad match, narrow match, related match, and candidate match.
- Each xref or mapping must have provenance: source, method, contributor or service, date, confidence, and graph/release context.

Merge, split, and deprecation lifecycle:

- Merges should create explicit replacement edges and preserve old IRIs as resolvable deprecated identifiers.
- Splits should preserve the historical entity and point to replacement entities with rationale.
- Deprecated or superseded identifiers must remain queryable for as-of and provenance workflows.
- Projections must carry canonical IRI, source xrefs, mapping confidence, and lifecycle state so UI reads do not hide identity uncertainty.

## Claim And Provenance Contract

The unit of knowledge should not be an unqualified triple. BrainKB should represent each user-visible assertion as a qualified claim bundle.

Claim bundle requirements:

- Stable `claim_id`.
- Subject, predicate, object/value, and optional qualifiers such as species, region, modality, developmental stage, assay, and context.
- Evidence node linking to publication, dataset, release, source fragment, table, figure, archive file, or upstream assertion.
- Provenance activity: imported, extracted, inferred, curated, reviewed, activated, superseded, or withdrawn.
- Agent: curator, reviewer, service principal, external resource, extraction model, or transform job.
- Graph and release context: named graph URI, schema version, application profile version, release ID, and as-of timestamp.
- Review and lifecycle state: draft, pending review, active, superseded, deprecated, rejected, or withdrawn.
- Evidence status: supports, refutes, conflicts with, not stated by, or insufficient evidence.
- Confidence/evidence grade with a documented interpretation and no implication of absolute biological truth.

Modeling direction:

- Use named graphs to preserve source/release/contribution boundaries.
- Consider a nanopublication-like or RDF-star-compatible representation for qualified statements, but do not require the deck to choose syntax before modeling requirements are agreed.
- PROV-O should express activity, agent, entity, derivation, generation time, and source lineage.
- SHACL or equivalent validation should enforce required provenance fields before activation.

Researcher-facing evidence UX:

- Default views should first answer: what is the claim, what supports/refutes it, which paper/dataset/release says so, which species/region/modality applies, and whether the assertion is curated, imported, inferred, extracted, or superseded.
- Full PROV-O lineage should be one drilldown away, not the first thing a scientist must parse.

## Graph Release And Projection Contract

Automated ingest and GraphQL/Postgres projections require a release contract that makes activation observable and reversible.

Release manifest requirements:

- Immutable `release_id`.
- Named graph URI or graph set URI.
- Source resource, upstream release identifier, source checksum, and retrieved-at timestamp.
- Transform code version, container digest or workflow digest, and configuration hash.
- Application profile/schema version and validation report pointer.
- Graph diff pointer against the previous active release.
- Projection schema version and projection validation report.
- Activation timestamp, activated-by agent, previous active release, and rollback target.
- External dependencies and connector versions used during build.

Activation rule:

- The active release pointer changes only after graph validation, projection build, projection parity checks, and readiness checks pass.
- From the user's perspective, RDF reads and GraphQL/Postgres projection reads must expose the same active release or clearly report a stale/unready projection state.
- If projection readiness fails, the previous active release remains visible and the failed release remains inspectable.

Ingest and activation state machine:

`submitted -> staged -> transformed -> validated -> graph_written -> projected -> projection_validated -> ready_to_activate -> active`

Failure and control states:

`failed`, `cancelled`, `retrying`, `quarantined`, `rolled_back`, `superseded`

Operational rules:

- Ingest submissions must be idempotent by source, release, graph URI, and payload checksum.
- Validation failures should produce actionable reports, not just job failure states.
- Retry behavior should distinguish transient connector errors from deterministic schema failures.
- Dead-letter or quarantine queues should preserve failed payloads and logs for review.
- Rollback should move the active pointer back to the previous successful release without deleting the failed or superseded graph.

Projection parity requirements:

- GraphQL objects and Postgres read models must expose canonical IRI, claim ID, graph URI, release ID, schema version, evidence links, lifecycle/as-of state, and projection freshness.
- Parity tests should compare a small set of canonical RDF/SPARQL answers against GraphQL/Postgres responses for the fixture competency questions.
- Projection schema evolution must be versioned and tied to release manifests.

## Operational Readiness Contract

The deck should make deployability and operations reviewable rather than leaving them as implied implementation detail.

Deployment targets:

- Local fixture mode: Docker Compose or equivalent local stack with Oxigraph, Postgres, Redis if needed, seed fixtures, mocked connectors, disabled or stubbed LLM calls, and deterministic rebuild.
- Self-hosted mode: documented volumes, migrations, secrets, TLS/proxy expectations, backup locations, and upgrade path.
- Production mode: Kubernetes or equivalent deployment with health checks, readiness checks, persistent volumes, service accounts, and controlled activation jobs.

Ingest/job requirements:

- Jobs expose state, progress, current phase, input manifest, validation report, retry count, cancellation state, activation readiness, projection freshness, and final release ID.
- Long-running jobs support cancellation before activation.
- Backpressure and queue depth should be visible so partner releases or extraction jobs do not overwhelm the system.

Observability requirements:

- Metrics: ingest duration, validation failure rate, queue depth, projection lag, activation failures, stale reads, cache hit/miss/stale rates, cache invalidation failures, memory promotion/rejection counts, embedding freshness, connector latency/error rate, external rate-limit hits, LLM call count/cost/error rate, auth failures, backup freshness, and restore-test age.
- Logs: request ID, job ID, release ID, graph URI, actor/service principal, connector name, upstream source, and error category.
- Traces: `brainkb-api` is the trace root for browser workflows and propagates request ID, user/session/project, release/as-of context, job ID, projection freshness, cache status, partial-result status, and downstream service/module spans for ingest, projection, cache lookup/fill/invalidation, memory read/write/promotion, search, provenance lookup, federation, and assistant retrieval.
- SLO candidates: read availability, search latency, cache freshness, memory retrieval latency, projection lag after activation, ingest success rate for fixture packages, and restore time.

Auth and scope matrix:

| Role | Read | Draft | Validate | Activate | Administer | External calls |
| --- | --- | --- | --- | --- | --- | --- |
| Anonymous reader | Public graph only | No | No | No | No | No |
| Authenticated researcher | Public and permitted graphs | Saved collections only | No | No | No | Optional, user-scoped |
| Curator | Permitted graphs | Yes | Yes | No | No | Via approved connectors |
| Reviewer | Permitted graphs | Yes | Yes | Approve within scope | No | Via approved connectors |
| Service principal | Scoped graph/package access | Yes | Yes | Scoped activation | No | Scoped, audited |
| Admin | All | Yes | Yes | Yes | Yes | Yes, audited |
| Connector operator | Operational metadata | No | No | No | Connector config only | Yes, audited |

Browser-facing auth rule:

- `brainkb-ui` authenticates with `brainkb-api` only. `brainkb-api` enforces the user/session/project/release policy and calls internal modules with service identity plus propagated user and scope claims.

Backup and restore:

- Define RPO/RTO targets before production implementation.
- Back up Postgres, triplestore/named graph snapshots, release manifests, validation reports, durable connector caches, project/task memory, vector indexes or their rebuild manifests, and object/artifact storage.
- Treat Redis or queue state as non-durable unless configured otherwise.
- Run restore drills using the basal ganglia fixture and at least one superseded release.
- Preserve rollback targets for active graph releases.

External service boundaries:

- Connectors own credentials, rate limits, caching, attribution, retry policy, privacy/data-egress checks, and outage behavior.
- The UI should distinguish local evidence, cached external evidence, live external evidence, memory-derived context, and unavailable sources.
- External failures should produce partial-result states where appropriate, not silent empty answers.

## Ontology Alignment And FAIR Contract

Ontology and schema alignment should be a named workstream, not a hidden data-cleaning task.

Application profile:

- Define the minimal BrainKB application profile for the MVP fixture: entity classes, predicates, claim qualifiers, provenance fields, release fields, and validation shapes.
- Version the application profile and tie each graph release to the profile version used for validation.

Ontology import and alignment:

- State which versions of BICAN, openMINDS, NIMP, BIDS, NWB, UBERON, CL, NCBITaxon, biolink, and other vocabularies are imported or referenced.
- Preserve crosswalk provenance, mapping confidence, mapping method, and mapping lifecycle.
- Validate term usage across the MVP fixture before presenting a claim as active.
- Track term deprecation, replacement, and unresolved mapping candidates.

FAIR and export metadata:

- Each graph release should expose machine-readable metadata for citation, license/access constraints, source attribution, schema/profile version, checksums, and provenance.
- Consider RO-Crate, DataCite, and schema.org-style metadata for release packages.
- Exportable snapshots should include enough manifest and provenance metadata to reproduce the fixture review without relying on hidden local state.

## Store And Query Strategy

The current deck frames the triplestore as the canonical knowledge store. The rebuild should preserve that as the conceptual model, but also surface a practical variant: GraphQL backed by Postgres projections for efficient UI and application reads.

Baseline decision:

- RDF/named graphs remain the canonical model for claims, provenance, source boundaries, versioning, and federation semantics.
- `brainkb-api` is the single browser-facing API/BFF. It owns the product API contract, auth/session enforcement, release/as-of context, trace roots, and routing to internal modules.
- The graph/knowledge module behind `brainkb-api` owns writes, validation, and canonical query semantics regardless of the backing implementation.
- Postgres already stores operational state; it may also hold denormalized read models for common entity, evidence, search, dashboard, task-memory, and agent-memory views.
- Caches and memory stores improve performance and workflow continuity, but they do not become canonical knowledge unless a reviewed promotion writes through the standard claim/provenance path.
- `brainkb-ui` and browser-based agents should call only `brainkb-api`; they should not call graph, ingest, job, cache, memory, connector, or store APIs directly.

GraphQL/Postgres variant:

- Add a GraphQL read mode on `brainkb-api`, or a GraphQL module behind it, backed by Postgres tables or materialized projections derived from canonical RDF/named graphs.
- Use GraphQL for high-traffic UI patterns that are awkward or slow to express directly as SPARQL: entity detail pages, nested evidence views, faceted search, timelines, review queues, and dashboard summaries.
- Keep SPARQL/RDF available for graph-native queries, federation, provenance audits, schema/version operations, and expert workflows.
- Treat GraphQL objects as read models with explicit semantics, not as a second source of truth.
- Expose canonical IRI, claim ID, graph URI, release ID, schema/profile version, evidence links, lifecycle/as-of state, and projection freshness on relevant GraphQL objects.

Required sync and lifecycle rules:

- Ingestion/update cycles must include projection updates after validation and named graph activation.
- Projection records must preserve canonical IRIs, claim IDs, graph URIs, source IDs, schema version, evidence node IDs, lifecycle state, and activation/as-of timestamps.
- Graph activation must be atomic from the user's perspective: a graph release and its Postgres/GraphQL projection are either both visible or both still pending.
- Projection lag and cache freshness must be observable through job status, sync timestamps, stale/readiness flags, and invalidation logs.
- No application write should bypass canonical validation just because a GraphQL/Postgres view exists.
- Projection parity tests must cover the MVP competency questions and compare canonical RDF/SPARQL answers against GraphQL/Postgres responses.
- If RDF and projection versions disagree, the API must return release/freshness metadata and either block the stale view or clearly label it as stale.

Architecture impact:

- L1 should show one BrainKB API boundary between products/workflows and backend modules.
- L2 should show a minimal deployable slice first: `brainkb-ui`, `brainkb-api`, `brainkb-worker`, connector adapters, and stores.
- L2 should show the triplestore plus an optional GraphQL/Postgres read projection as a deliberate performance boundary, not as an accidental duplicate source of truth.
- L2 should keep GraphQL, jobs, ingest, cache, memory, and auth as internal modules or future split points unless scale or ownership requires separate deployables.
- L3 ingest flows should include projection refresh, projection validation, cache invalidation, and rollback/stale-state handling.
- L4 should explain which semantics must survive projection, caching, and memory retrieval: provenance, versioning, named graph membership, identifier stability, auth scope, and release context.

## API Boundary And Technical Burden

The first build should minimize frontend and operational coupling. BrainKB can preserve the important trust contracts without starting as many browser-facing microservices.

MVP API topology:

- `brainkb-ui` talks to one public surface: `brainkb-api`.
- `brainkb-api` may be implemented as a BFF/gateway, as a module around the graph/knowledge API, or as a single `brainkb-api` service. The architectural boundary matters more than the initial packaging.
- `brainkb-api` exposes product-shaped operations: search, entity detail, evidence/provenance views, release/as-of context, saved collections, task workspace, curator review, ingest status, and admin/release status.
- Internal modules behind `brainkb-api` handle graph reads/writes, GraphQL projection reads, auth/policy, jobs, ingest submission, memory reads/writes, cache lookup/fill, and connector orchestration.
- `brainkb-worker` handles long-running ingest, validation, graph writes, projection build, parity checks, release activation, rollback preparation, cache invalidation, and memory revalidation.
- Connector adapters should start as an internal library or sidecar boundary. Split them into a separate `connector-api` only when credential isolation, rate limiting, scaling, or ownership requires it.

Services that should not be directly browser-facing:

- Triplestore, Postgres/pgvector, Redis, object storage, release workers, connector adapters, cache internals, memory stores, and external LLM/search/archive endpoints.
- `jobs-api`, `ingest-api`, `cache-api`, `memory-api`, `auth-api`, and `graphql-api` are useful names for internal modules or future split points, but the deck should not require them as day-one deployables.

Single invariant:

- Canonical facts live in RDF/named graphs. Projections, cache, memory, vectors, connector responses, and assistant outputs are derived or workflow state unless promoted through review, validation, named graph write, and release activation.

## Cache And Agent Memory Strategy

BrainKB should treat caching and agent memory as related but distinct platform capabilities. Cache is a performance and resilience boundary. Memory is workflow state for researchers and agents. Neither should silently create facts in the canonical graph.

Cache service:

- The cache module, exposed internally and split later as `cache-api` only if needed, provides a deterministic cache facade for entity hydration, provenance lookup, release readiness, connector responses, federated subquery results, search facets, projection materialization status, and expensive LLM/tool-call intermediates.
- Cache keys must include the relevant `release_id`, `graph_uri`, `as_of` date or active pointer, application profile/schema version, source/resource ID, query template version, connector version, tenant/project, and auth scope.
- Cache entries must expose status metadata: hit, miss, stale, negative cache, upstream source, source timestamp, cache timestamp, TTL, invalidation reason, and replay/recompute pointer when available.
- Graph release activation should namespace or invalidate cache entries by release and schema version rather than mutating old results in place.
- Redis can back hot short-TTL cache; Postgres or object storage can back durable connector/result caches when replay, rate-limit protection, reproducibility, or offline review matter.
- Cache misses, stale reads, invalidation failures, negative-cache rates, and upstream retry behavior must be observable.

Agent memory components:

- Ephemeral working memory: current conversation/task context, selected entities, active filters, retrieved evidence, tool results, and UI state. It is user/session scoped, short TTL, resumable within a session, and discarded unless promoted.
- Short-term task memory: active research workspace with query plans, candidate hypotheses, scratch collections, rejected suggestions, retrieval traces, and partial review state. It is user/project scoped, expires or archives, and can support multi-step agent work.
- Long-term project/user memory: saved collections, reviewed claims, reusable query templates, trusted-source preferences, vocabulary choices, researcher goals, and explicit "remember this" notes. It requires user-visible control and should be exportable.
- Institutional/platform memory: curated ontology mappings, release validation outcomes, connector reliability history, benchmark results, answer-quality evaluations, and reusable workflow templates. It is admin or reviewer governed.
- Semantic/vector memory: embeddings for entities, claims, papers, datasets, tools, workflows, and memory items. Vector entries are derived indexes that must point back to canonical IDs, evidence, release context, and embedding model version.
- Provenance/audit memory: prompts, model/provider metadata, tool calls, retrieval sets, source snippets, generated drafts, and reviewer decisions when they influence user-visible answers or candidate claims.

Memory lifecycle and promotion rules:

- The memory module, exposed internally and split later as `memory-api` only if needed, owns memory reads, writes, retention, promotion, and deletion; UI code and agents should not write directly to store tables.
- Every memory item should carry owner, scope, source, created_at, updated_at, expires_at, release context, graph URI or active-release pointer, auth policy, privacy class, retrieval score, decay policy, and revalidation status.
- Promotion path is explicit: ephemeral memory can become task memory; task memory can become project memory; project memory can propose candidate claims; candidate claims enter the canonical graph only through review, validation, named graph write, and release activation.
- Memory can bias retrieval and workflow continuity, but it cannot replace evidence. Agent answers must cite canonical entities, claims, papers, datasets, or explicitly labeled external results.
- Stale memory must be revalidated when graph releases, ontology mappings, projection schemas, or connector versions change.
- Private user/project memory must not be used as institutional memory or model-training/evaluation input without explicit policy and consent.

## Cleaned Epic User Stories

Each story uses the same template so the later deck can turn it into slides, issues, or implementation slices without reinterpreting intent.

Bootstrap dependency priority uses ease of resolution, not importance:

- Easy: can be seeded from existing deck content, a small curated fixture, public metadata exports, or simple adapters.
- Medium: needs schema alignment, repeated curation, service integration, or a reliable sync/update process.
- Hard: depends on substantial KB coverage, external search/retrieval services, model evaluation, cross-resource agreement, or sustained curator/researcher feedback.

### Epic 01 - Knowledge Review

Actor: researcher or reviewer

Goal: review everything BrainKB knows about an entity or claim, including agreement and conflict across sources.

Value: users can evaluate the field's state of knowledge without flattening contradictory evidence into a single asserted fact.

Trigger: a user searches for an entity, opens a property, or asks "what do we know about this?"

Preconditions:

- Entities have stable identifiers or resolvable cross-references.
- Claims are stored with source, contributor, timestamp, and schema version.
- Named graphs preserve source boundaries.

Acceptance criteria:

- Entity views group assertions by predicate and source.
- Conflicting claims are visible together, not silently collapsed.
- Each claim links to evidence, source resource, contributor, and graph/version metadata.
- Users can filter or compare by source, version, and as-of date.

Architecture dependencies: L0 external resources, L1 evidence review workflow, L2 brainkb-api and canonical graph store, L3 entity search/detail and provenance lookup, L4 named graphs and PROV-O.

Suggested slides: "Why evidence review matters", "Epic story card", "Evidence/provenance interaction flow", "L4 provenance model".

Bootstrap assumptions and dependencies, ordered easiest to hardest:

- Easy: seed a small entity set from the BG taxonomy atlas fixture with stable IRIs, labels, synonyms, source links, BICAN model/profile context, and a few manually curated claims.
- Easy: include a minimal set of taxonomy classes, h5ad assets, gene/gene-set evidence, Patch-seq cell IDs, file assets, and source papers/preprints so the UI can traverse from any entry point.
- Easy: require every seed claim to include source, contributor placeholder, timestamp, schema version, and named graph URI.
- Medium: curate enough overlapping claims across at least two sources to demonstrate agreement, disagreement, and "not stated" states.
- Medium: build or project common entity/evidence views into Postgres/GraphQL if direct SPARQL reads are too slow for UI iteration.
- Hard: assign defensible evidence-strength scores across heterogeneous sources without overclaiming scientific certainty.

### Epic 02 - Hypothesis Generation

Actor: researcher

Goal: surface plausible hypotheses from graph structure, gaps, analogies, contradictions, and similarity.

Value: BrainKB helps users discover candidate ideas while keeping generated suggestions grounded and reviewable.

Trigger: a user starts from an entity, region, species, marker set, or graph pattern and asks what might be implied.

Preconditions:

- Core graph search and entity hydration are available.
- Similarity signals exist for entities, claims, or documents.
- The system can cite graph nodes behind any generated suggestion.
- Task memory can retain query plans, rejected ideas, retrieved evidence, and candidate drafts without treating them as graph facts.

Acceptance criteria:

- Suggested hypotheses are labeled as candidates, not facts.
- Each suggestion includes supporting evidence, missing evidence, and possible counterevidence.
- The system exposes the source nodes, paths, or neighbors used to create the suggestion.
- Users can save, reject, or send a suggestion to curator review without committing it to the canonical graph.
- Saved or rejected suggestions are stored as task/project memory with release context and can be revalidated when the graph changes.

Architecture dependencies: L1 gated assistant/hypothesis workflow, L2 brainkb-api, connector adapters, internal memory module, Postgres/pgvector, L3 LLM-assisted query, memory promotion, and graph hydration, L4 identifiers, claim provenance, and workflow-state semantics.

Suggested slides: "Hypothesis as a user story", "Grounded suggestion flow", "AI boundary rules".

Bootstrap assumptions and dependencies, ordered easiest to hardest:

- Easy: limit initial hypotheses to "candidate connections" over the seed graph, such as shared markers, shared regions, missing evidence, or source disagreement.
- Easy: expose the underlying graph paths and retrieved nodes before attempting polished natural-language synthesis.
- Easy: store candidate, saved, and rejected suggestions as scoped task memory so users can resume exploration and review what the agent already tried.
- Medium: populate enough claims, entity embeddings, and paper/dataset metadata to make similarity results useful rather than trivial.
- Medium: integrate external discovery services such as PubMed, Semantic Scholar, Google Scholar-like search, repositories, or archive APIs as evidence expansion sources.
- Hard: produce scientifically useful hypothesis suggestions, because this depends on KB coverage, external literature retrieval quality, model behavior, and researcher feedback loops.

### Epic 03 - Methods and Models Catalog

Actor: methodologist or analyst

Goal: find tools, models, and pipelines that fit a dataset and understand when they fail.

Value: tool selection becomes a query over applicability, benchmark evidence, and failure modes instead of a manual literature search.

Trigger: a user describes a dataset signature, task, modality, species, scale, or noise regime.

Preconditions:

- Tools and models are represented as first-class graph entities.
- Applicability conditions and benchmark evidence are structured.
- Dataset metadata uses aligned vocabularies.

Acceptance criteria:

- Users can query for methods compatible with a dataset signature.
- Results show works-when, breaks-when, benchmark evidence, and source provenance.
- Incompatible tools are excluded or shown with clear contraindications.
- Tool versions, owners, inputs, and outputs are visible.

Architecture dependencies: L0 tools and registries, L1 methods/catalog workflow, L2 brainkb-api and canonical graph store, L3 query planning, L4 tool/model schema and provenance.

Suggested slides: "Methods are graph entities", "Tool compatibility story", "Schema requirements".

Bootstrap assumptions and dependencies, ordered easiest to hardest:

- Easy: seed a short catalog of tools/models from known project context with inputs, outputs, modality, species, scale, owner, version, and links.
- Easy: represent applicability conditions as structured metadata even before full ontology alignment is complete.
- Medium: add benchmark and failure-mode evidence from papers, docs, or curated notes for enough tools to make comparison meaningful.
- Medium: align dataset signatures to controlled terms so compatibility queries are not just keyword matching.
- Hard: maintain trustworthy failure-mode and benchmark claims across tool versions and heterogeneous datasets.

### Epic 04 - Resource Landscape

Actor: planner, new entrant, or infrastructure lead

Goal: understand which neuroscience resources exist, how they relate, and how their lifecycle changes over time.

Value: BrainKB becomes a time-aware map of resources, schemas, ontologies, archives, and initiatives.

Trigger: a user asks for active resources for a topic as of a date or across a time window.

Preconditions:

- Resources are first-class graph entities.
- Releases, lifecycle states, supersession, dependencies, and dates are captured.
- As-of graph selection is supported.

Acceptance criteria:

- Users can view resources by topic, status, date, and relationship.
- The UI shows active, superseded, deprecated, and retired resources.
- Version history and replacement edges are visible.
- The same lifecycle vocabulary applies to taxonomies, schemas, datasets, and tools.

Architecture dependencies: L0 resource ecosystem, L1 resource landscape workflow, L2 brainkb-api and canonical graph store, L3 as-of query support, L4 lifecycle vocabulary and named graph versioning.

Suggested slides: "Resource lifecycle story", "As-of resource query", "Versioned named graph model".

Bootstrap assumptions and dependencies, ordered easiest to hardest:

- Easy: seed a resource registry for the resources already named in the source deck and BG fixture: BICAN, ABC Atlas/HMBA-BG, DANDI, BIL, NeMO, Allen Brain Atlas, NeuroMorpho, EBRAINS, BIDS, NWB, openMINDS, bioRxiv, PubMed/Semantic Scholar-style metadata, and relevant ontologies.
- Easy: capture minimal lifecycle metadata: active/superseded/deprecated/retired, homepage, API endpoint, release URL, and last checked date.
- Medium: add version edges, replaces/extends/dependency relations, and topic tags for a bounded neuroscience area.
- Medium: implement as-of graph selection or projection filters for a few versioned resources.
- Hard: keep the registry current across many independent resources without automated monitoring and review ownership.

### Epic 05 - Entity Exploration

Actor: neuroscientist or researcher

Goal: search for a cell type, dataset, region, paper, method, or claim and see the full connected picture.

Value: read-only exploration works without requiring users to know SPARQL, RDF, or source-specific identifiers.

Trigger: a user enters a name, synonym, identifier, or natural-language phrase.

Preconditions:

- Search indexes cover labels, synonyms, identifiers, and selected claim text.
- Entity detail pages can hydrate graph neighborhoods.
- External links and federated attributes are clearly attributed.

Acceptance criteria:

- Search resolves synonyms and cross-references to canonical entity pages.
- Entity pages show definitions, properties, related entities, source links, file-level assets, and evidence badges.
- BG fixture exploration works from taxonomy class, Patch-seq cell/specimen ID, gene, gene set, file asset, dataset, paper/preprint, person, resource, or claim.
- Read-only exploration works without login.
- Logged-in users can save searches or collections if identity is enabled.

Architecture dependencies: L1 search/detail workflow, L2 brainkb-ui, brainkb-api, canonical graph store, Postgres/pgvector projections, L3 search and drill-down flows, L4 identifiers and ontology mappings.

Suggested slides: "Entity exploration story", "Search to detail flow", "L3 search/drill-down components".

Bootstrap assumptions and dependencies, ordered easiest to hardest:

- Easy: choose the BG taxonomy atlas fixture and populate canonical entities, labels, synonyms, definitions, source links, file assets, and a few relationship types.
- Easy: build search over labels, synonyms, and identifiers before adding semantic search.
- Medium: add enough cross-references and ontology mappings to make synonym, Patch-seq cell/specimen, gene, gene-set, and file-asset resolution credible across resources.
- Medium: project entity detail read models into Postgres/GraphQL if direct graph traversal creates slow or brittle UI reads.
- Hard: provide a "full connected picture" across modalities and species without broad ingestion from archives, atlases, and papers.

### Epic 06 - Curated Claim Ingest

Actor: curator or domain expert

Goal: extract candidate claims from a paper or preprint, review them, and publish approved claims into the graph.

Value: experts can add structured knowledge without writing RDF by hand, while preserving human review and provenance.

Trigger: a curator uploads or references a publication and starts an extraction/review job.

Preconditions:

- Document parsing produces structured text and offsets.
- Extraction creates candidate entities and relations.
- Review state can persist before publication.
- Approved claims can be validated against schema.

Acceptance criteria:

- Candidate claims include source document, offsets, model/prompt metadata when relevant, and confidence.
- Curators can approve, edit, reject, or batch publish candidates.
- Approved triples are written through the standard ingest path.
- Published claims land in a named graph tied to the source and curator.

Architecture dependencies: L1 curator review workflow, L2 brainkb-api, brainkb-worker, connector adapters, Postgres, canonical graph store, L3 curator and ingest flows, L4 schema validation and provenance.

Suggested slides: "Curator review story", "Draft-to-publish lifecycle", "Ingest and provenance components".

Bootstrap assumptions and dependencies, ordered easiest to hardest:

- Easy: start with manually authored candidate claims from one or two BG taxonomy papers/preprints instead of requiring automated extraction on day one.
- Easy: store draft review state in Postgres with links to source document, offsets where available, and target graph/schema version.
- Medium: integrate one PDF/text parser and one entity extraction path behind connector adapters or an app service boundary, with NER for people, organizations, resources, datasets, tools, atlas references, genes, and cell classes.
- Medium: represent figure/table/notebook-derived or estimated analysis-graph evidence as structured evidence nodes before writing canonical claims.
- Medium: define a minimal claim schema and SHACL validation path so approved claims can be written consistently.
- Hard: reach high-quality automated extraction across neuroscience papers, figures, tables, and terminology without sustained model and curator evaluation.

### Epic 07 - Automated Partner Release Ingest

Actor: pipeline, bot, or service principal

Goal: ingest a new upstream dataset, taxonomy, or schema release automatically and replace the previous active graph atomically.

Value: BrainKB can stay current with partner resources while preserving reproducibility and history.

Trigger: upstream release tag, scheduled job, webhook, or CI pipeline.

Preconditions:

- Machine credentials and scoped write tokens exist.
- Incoming data can be validated locally and by BrainKB.
- Versioned graph URIs and supersession policy exist.

Acceptance criteria:

- Pipelines can submit idempotent ingest jobs through a headless API.
- Validation reports and graph diffs are available before activation.
- New releases become active without deleting old releases.
- Failures leave the previous active graph untouched and produce actionable logs.

Architecture dependencies: L1 ingestion/release workflow, L2 brainkb-api, brainkb-worker, canonical graph store, Postgres/Redis if needed, L3 auth and ingest flows, L4 named graph lifecycle.

Suggested slides: "Automated ingest story", "Atomic release replace", "Deployment and operational state".

Bootstrap assumptions and dependencies, ordered easiest to hardest:

- Easy: support file-based or fixture-based release ingest for the ABC Atlas/HMBA-BG package before building full upstream automation.
- Easy: require each ingest package to declare source, release ID, graph URI, schema version, and expected activation behavior.
- Medium: add validation reports, graph diffs, file-asset manifests, h5ad metadata summaries, and projection sync checks to the job lifecycle.
- Medium: add a repeatable Patch-seq-to-archive asset resolution step so cell/specimen-level file links update with the release.
- Medium: implement scoped service credentials for machine ingest.
- Hard: build reliable automated polling/webhooks and transforms for multiple partner resources with different release practices.

### Epic 08 - Cross-KB Federated Query

Actor: analyst or advanced researcher

Goal: ask one question whose answer spans local BrainKB knowledge and partner resources.

Value: BrainKB handles identity alignment, query planning, source attribution, and partial results so users do not export and join data by hand.

Trigger: a user builds a query that combines properties owned by different resources.

Preconditions:

- Equivalent entities are mapped to canonical identifiers or cross-references.
- External resources expose SPARQL, REST, file, or adapter-accessible interfaces.
- The system tracks latency, failure, and source attribution per external call.

Acceptance criteria:

- The query service can plan local and federated subqueries.
- Results reconcile by canonical URI and preserve per-cell provenance.
- Slow or unavailable sources degrade gracefully with visible status.
- REST-backed resources can be lifted into temporary graph-like results through connectors.

Architecture dependencies: L0 partner resources, L1 federated query workflow, L2 brainkb-api, connector adapters, and cache module, L3 federation flow, L4 identity mapping and source attribution.

Suggested slides: "Federation story", "Query planning flow", "Connector boundary".

Bootstrap assumptions and dependencies, ordered easiest to hardest:

- Easy: demonstrate federation with one local graph and one mocked or stable external endpoint/adapter such as ABC Atlas metadata, archive asset lookup, or publication metadata.
- Easy: preserve source attribution per result cell even when the first query plan is hand-authored.
- Easy: cache connector responses with source, TTL, auth scope, and stale/partial-result status so repeated demos do not depend on live upstream behavior.
- Medium: align canonical identifiers or cross-references across two or three real resources such as ABC Atlas/HMBA-BG, DANDI/BIL/NeMO-style archives, bioRxiv/PubMed/Semantic Scholar-style publication metadata, and gene/ontology services.
- Medium: add timeout, partial result, and stale cache behavior so external failures are visible rather than mysterious.
- Hard: generalize query planning across heterogeneous SPARQL, REST, file, and repository sources with predictable performance.

### Epic 09 - Grounded Assistant

Actor: researcher

Goal: ask a plain-language question and receive a readable answer with citations to graph nodes, claims, papers, or datasets.

Value: natural-language interaction broadens access while keeping the answer grounded in BrainKB evidence.

Trigger: a user asks a question in an assistant panel or invokes a query-generation workflow.

Preconditions:

- Retrieval can return candidate entities and claims by semantic and graph context.
- The answer generator can hydrate retrieved IRIs through `brainkb-api`.
- LLM providers are routed through connector adapters behind `brainkb-api` or a single AI service boundary.
- Memory retrieval can supply user/project context while still respecting auth, release, and provenance constraints.

Acceptance criteria:

- Answers cite retrieved graph nodes, claims, papers, or datasets.
- The generated query or retrieval basis is inspectable.
- The assistant refuses or falls back to search when evidence is insufficient.
- Provider, prompt, model, and trace metadata are captured for provenance where outputs become draft claims.
- The assistant separates canonical evidence, external cached evidence, and memory-derived context in the answer trace.

Architecture dependencies: L1 gated assistant workflow, L2 brainkb-api, connector adapters, cache/memory modules, Postgres/pgvector, L3 cache-aware retrieval and LLM-assisted query flow, L4 claim/evidence and workflow-state contracts.

Suggested slides: "Grounded assistant story", "RAG over the graph", "LLM/agent boundary".

Bootstrap assumptions and dependencies, ordered easiest to hardest:

- Easy: start with answer synthesis over the BG fixture and force citations to retrieved IRIs, claims, file assets, papers/preprints, and release manifests.
- Easy: fall back to entity search when retrieval confidence or evidence coverage is low.
- Easy: keep session/task memory for active questions, selected entities, and prior retrieval traces so agent follow-ups are useful but auditable.
- Medium: add embeddings for entities, claims, papers, and resource descriptions, with hydration through `brainkb-api`.
- Medium: route PubMed/Semantic Scholar/repository expansion through connector adapters when local evidence is insufficient.
- Hard: deliver reliable answers for broad neuroscience questions without hallucination when the KB is sparse or external retrieval is noisy.

### Epic 10 - Provenance Audit

Actor: reviewer, curator, scientist, or compliance user

Goal: inspect the full lineage of a single claim or property.

Value: trust is built into the platform because there is no no-provenance mode.

Trigger: a user clicks a provenance badge, conflict indicator, or evidence link.

Preconditions:

- Claims are addressable and connected to evidence nodes.
- Source URIs, contributor IDs, schema versions, ingest timestamps, and graph versions are stored.
- Old assertions remain queryable after updates.

Acceptance criteria:

- Every visible claim has an accessible provenance view.
- Provenance views show source, contributor, schema version, graph URI, ingest time, and supersession status.
- Users can navigate from claim to publication, dataset, curator action, and previous versions.
- Updates create new versions or supersession edges, not silent edits.

Architecture dependencies: L1 evidence/provenance workflow, L2 brainkb-api and canonical graph store, L3 provenance lookup, L4 PROV-O, named graphs, identifiers, and lifecycle vocabulary.

Suggested slides: "Provenance audit story", "Claim lineage model", "Evidence chain UX".

Bootstrap assumptions and dependencies, ordered easiest to hardest:

- Easy: make provenance mandatory in seed data and fixture ingest, even if contributor values initially use placeholders.
- Easy: define a compact provenance card model: source URI, contributor, schema version, graph URI, ingest time, and supersession state.
- Medium: support claim-level IDs and evidence-node lookup in both RDF and any GraphQL/Postgres projection.
- Medium: preserve old assertions during updates and expose supersession history in the UI.
- Hard: show complete provenance chains across federated resources when upstream systems have incomplete or incompatible metadata.

## Five Architecture Zoom Levels

### L0 - Ecosystem

Question answered: who and what does BrainKB connect?

L0 should show BrainKB as a federating platform in the neuroscience ecosystem, not as a replacement for every source system.

In scope at L0:

- Human actors: researchers, curators, reviewers, methodologists, infrastructure operators, and anonymous readers.
- Machine actors: ingest pipelines, partner release bots, external agents, service principals, extraction models, and assistant/LLM providers.
- External knowledge sources: papers/preprints, PubMed/Semantic Scholar/Google Scholar-like search, ABC Atlas/HMBA-BG-style atlas packages, DANDI/BIL/NeMO/Allen/BICAN-style archives and atlases, h5ad/NWB/source files, ontologies, schemas, tool registries, repositories, and partner knowledge bases.
- Governance boundaries: identity providers, access policies, data-use terms, rate limits, licenses, citation rules, and privacy/data-egress constraints.

Out of scope at L0:

- Internal service names, store choices, queue details, and schema tables.

The diagram should make one point: BrainKB sits between actors, external resources, and governance constraints in an ecosystem whose data quality and availability vary. It should not introduce internal services or schema mechanics; those belong to L2-L4.

### L1 - Product/API Boundary

Question answered: what product workflows call the BrainKB platform, and through what stable boundary?

L1 should show the product/API boundary, not backend deployment detail.

Products and workflows:

- Evidence review: entity search/detail, claim comparison, conflict/silence states, provenance drilldown.
- Curation: candidate claim review, structured edits, batch publish request, validation report review.
- Release/as-of administration: graph release visibility, activation status, rollback target, projection readiness.
- Research workspace: saved searches, collections, task context, and explicit memory controls.
- Gated later: grounded assistant, broad live federation, long-term project memory, and hypothesis generation beyond the fixture.

Single public API boundary:

- `brainkb-ui` calls `brainkb-api`, not individual graph, job, ingest, memory, cache, or connector APIs.
- `brainkb-api` exposes product-shaped operations: search, evidence, provenance, ingest status, release context, collections, task workspace, and admin/review actions.
- `brainkb-api` can route internally to REST handlers, GraphQL read mode, graph queries, job state, memory, cache, and connector orchestration without exposing that topology to the UI.

Backend capability modules behind the boundary:

- Graph and claims: canonical graph reads/writes, identifier resolution, claim/evidence/provenance hydration.
- Ingest and release: staged submissions, validation, projection build, activation, rollback, and readiness.
- Projection and search: GraphQL/read models, facets, entity pages, and vector/search indexes.
- Connector adapters: LLMs, parsers, external search, archives, partner KBs, credentials, retries, and rate limits.
- Cache and memory policy: cache freshness, stale/partial-result states, memory retention, revalidation, and promotion gates.

Out of scope at L1:

- Service deployment choices, store names, table schemas, queue phases, and exact cache/memory key fields.

The diagram should make one point: products call one BrainKB API. Backend modules can evolve without turning the UI into a service orchestrator.

### L2 - Service Containers / Minimal Deployable Slice

Question answered: what is the smallest useful deployable topology?

L2 should show a minimal deployable slice first, with future split points named but not required.

Day-one deployables:

- `brainkb-ui`: web UI only. It calls `brainkb-api` and does not orchestrate internal services.
- `brainkb-api`: public BFF/API facade for REST/GraphQL reads, auth/policy enforcement, search, entity/evidence/provenance views, release/as-of context, saved collections, task workspace, ingest submission, and job status.
- `brainkb-worker`: asynchronous worker for ingest, validation, canonical graph writes, projection build, parity checks, release activation, rollback prep, cache invalidation, memory revalidation, and export jobs.
- Connector adapters: internal library or sidecar for LLMs, parsers, ontology services, external search, archives, and partner KBs.

Stores:

- Canonical graph store: RDF/named graphs and release-scoped graph state. Oxigraph is a plausible first choice; Fuseki or GraphDB remain alternatives.
- Postgres + pgvector: users, scopes, jobs, drafts, review state, GraphQL/read projections, vector indexes, durable memory, and durable connector/result cache.
- Object/artifact storage: source packages, validation reports, graph diffs, extraction artifacts, release manifests, and export snapshots.
- Redis, optional: queue broker, locks, and short-lived hot cache only if the chosen worker/cache approach needs it.

Future split points:

- Split GraphQL/read projection, jobs, ingest, connector, cache, memory, auth, or observability into dedicated services only when scale, security, ownership, deployment cadence, or isolation requires it.
- Keep internal interfaces clean enough that these splits are possible, but do not present them as the default operational burden.

Out of scope at L2:

- Product story details and graph schema semantics that belong at L1 or L4.

The diagram should make one point: BrainKB can start as one UI, one API, one worker, connector adapters, and a few stores while preserving the trust boundary. Products never write directly to graph stores, memory tables, caches, or external services.

### L3 - Core Workflow Components

Question answered: how do the key workflows move through the system?

L3 should not be a generic module dump. It should show internals only for the workflows the deck promises:

- Search and entity detail: UI config, `brainkb-api` route, query template, graph/projection read, entity hydration, evidence badges.
- Ingest: submit job, stage, transform, validate, write named graph, build projection, validate projection, activate or fail safely.
- Projection sync: after graph activation, update Postgres/GraphQL read models, verify sync status, expose stale projection warnings, and invalidate release-scoped caches.
- Provenance audit: claim lookup, evidence node hydration, source/contributor/schema/version rendering.
- Federation: plan subqueries, call partner endpoints or adapters, reconcile by canonical URI, annotate source.
- Assistant: retrieve scoped memory, retrieve IRIs, hydrate claims, consult connector/cache for external expansion if needed, call LLM boundary, return cited answer or fallback.
- Release activation: validate manifest, compare graph diff, run SHACL and projection parity checks, move active pointer, record activation ledger, retain rollback target.

Cross-cutting annotations on those workflows:

- Cache lifecycle: compute scoped key, lookup, return freshness metadata, fill, negative-cache where appropriate, invalidate by release/schema/source/auth scope, and record cache traces.
- Agent memory lifecycle: capture working context, write task memory, retrieve scoped memory, hydrate canonical evidence, decay or expire stale memory, and promote only through explicit review gates.
- Job control: expose state, progress, retries, cancellation, quarantine, and final release/projection identifiers.

Out of scope at L3:

- Full ontology/class design and full deployment topology.

The diagram should make one point: each workflow uses the same core primitives: stable identifiers, scoped access, named graphs, validation, provenance, release context, cache freshness, and memory promotion rules.

### L4 - Knowledge/Data Model

Question answered: what data model makes trust and evolution possible?

L4 should explain the model in layers:

- Identity: stable IRIs, ORCID, DOI, dataset IDs, file/asset IDs, Patch-seq cell/specimen IDs, gene IDs, repository commits, cross-references.
- Domain model: BICAN, openMINDS, NIMP, taxonomy releases, cell/specimen/file assets, tool/model entities, datasets, claims.
- Standards: LinkML, SHACL, BIDS, NWB, schema versions.
- Reference vocabularies: UBERON, CL, NCBITaxon, biolink categories.
- Provenance: PROV-O, source, contributor, generated-by, derived-from, timestamp.
- Versioning: named graphs per source/release/contribution, supersession edges, lifecycle states, as-of queries.
- Claim bundles: stable claim IDs, qualifiers, evidence nodes, activity/agent/source lineage, confidence/evidence labels, and review lifecycle state.
- Release manifests: immutable release ID, source checksum, transform digest, validation report, projection schema version, activation timestamp, previous release, and rollback target.
- Projection contract: any GraphQL/Postgres read model must preserve IRIs, claim IDs, graph membership, evidence links, schema versions, and lifecycle/as-of state.
- Derived/index/workflow-state contract: cache keys, memory items, vector entries, connector responses, and assistant traces must carry release context, auth scope, source, freshness/revalidation status, and pointers back to canonical entities/claims/evidence where applicable.

Out of scope at L4:

- UI layouts, product grouping, and container deployment diagrams.

The diagram should make one point: provenance, versioning, release context, projection semantics, cache freshness, and memory lifecycle are not add-ons. They are the data model that keeps BrainKB usable by humans and agents.

## Traceability Matrix

| Epic | Primary architecture levels | Sequence flows | Required platform capabilities |
| --- | --- | --- | --- |
| 01 Knowledge Review | L1, L3, L4 | Search, drill-down, provenance | Entity hydration, named graph aggregation, BG taxonomy/asset/claim traversal, conflict display, evidence scoring. |
| 02 Hypothesis Generation | L1, L2, L3, L4 | Search, LLM-assisted query, memory promotion | Graph patterns, similarity retrieval, task memory, grounded suggestions, reviewable drafts. |
| 03 Methods and Models | L0, L1, L4 | Search, drill-down | Tool/model entities, applicability schema, benchmarks, failure-mode provenance. |
| 04 Resource Landscape | L0, L1, L4 | Search, federation | Resource lifecycle model, version edges, as-of queries, timeline/supersession UI. |
| 05 Entity Exploration | L1, L2, L3, L4 | Search, drill-down, federation | Canonical identifiers, synonym search, taxonomy/cell/gene/file/paper entity pages, evidence badges, source links. |
| 06 Curated Claim Ingest | L1, L2, L3, L4 | Curator, ingest, auth | Document parsing, NER/extraction drafts, analysis-graph evidence, review queue, schema validation, named graph write. |
| 07 Automated Partner Release Ingest | L2, L3, L4 | Auth, ingest | Service credentials, idempotent atlas/package jobs, file manifests, validation reports, graph diff, atomic activation. |
| 08 Cross-KB Federated Query | L0, L2, L3, L4 | Federation, search, cache lookup | Query planning, atlas/archive/publication/gene connectors, connector/result cache, source attribution, partial results, URI reconciliation. |
| 09 Grounded Assistant | L1, L2, L3, L4 | LLM-assisted query, search, memory retrieval | pgvector retrieval, cache-aware graph hydration, scoped memory, citations to claims/assets/papers, provider boundary, fallback behavior. |
| 10 Provenance Audit | L1, L3, L4 | Provenance, drill-down | Evidence nodes, PROV-O paths, schema/version metadata, supersession history. |

## Contract Traceability Matrix

| Contract | Primary epics | Architecture levels | Required review question |
| --- | --- | --- | --- |
| MVP competency fixture | 01, 05, 06, 07, 08, 09, 10 | L0, L1, L2, L3, L4 | Can a neuroscientist start from a BG taxonomy class, Patch-seq cell, gene/gene set, file asset, or preprint and explain taxonomy, files, evidence, claims, support/conflict/silence, and as-of state? |
| Identifier governance | 01, 03, 04, 05, 08, 10 | L0, L3, L4 | Can every visible entity and mapping explain its canonical IRI, source xrefs, mapping type, confidence, and lifecycle state? |
| Claim/provenance bundle | 01, 06, 09, 10 | L1, L3, L4 | Can every user-visible assertion identify its evidence, source, activity, agent, graph, release, schema, and review state? |
| Graph release and projection | 04, 05, 07, 10 | L2, L3, L4 | Can a release activate atomically, expose projection freshness, and roll back without losing history? |
| Ops readiness | 06, 07, 08, 09 | L1, L2, L3 | Can the stack be deployed locally and operated with observable ingest, projection, auth, backup, restore, and connector behavior? |
| Ontology alignment and FAIR | 03, 04, 05, 08 | L0, L4 | Can the fixture state vocabulary versions, crosswalk provenance, validation profile, citation, license, and export metadata? |
| Cache and agent memory | 02, 05, 08, 09, 10 | L1, L2, L3, L4 | Can agents reuse context and cached work while respecting release freshness, provenance, auth scope, retention, and promotion gates? |

