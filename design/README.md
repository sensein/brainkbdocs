# BrainKB Design Documents

## Documents

**Edit these files directly:**

- **`brainkb-architecture.md`** — primary architecture design document, organized in six parts: Context (users, use cases), Architecture (L0–L4 zoom levels, key sequence flows), MVP (competency fixture, scope), Contracts (identifier governance, claim/provenance, graph release, operational readiness, ontology/FAIR), Strategy (store/query, API boundary, cache/memory), and Epics and Traceability

## Directory Structure

```
design/
  brainkb-architecture.md          # <-- edit this
  original_source/
    brainkb-architecture-deck-redesign.md   # historical reference; do not edit
  utils/
    split_design_doc.py            # one-time split utility (already run)
    merge_design_doc.py            # combines both docs for review/export
    README.md
```

## `original_source/`

Contains `brainkb-architecture-deck-redesign.md` — the original combined document from which the two working files were derived via `utils/split_design_doc.py`.  Do not edit it; all ongoing work happens in the split files above.

