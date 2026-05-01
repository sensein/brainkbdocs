# BrainKB Design Documents

## Documents

**Edit these files directly:**

- **`brainkb-architecture.md`** — primary document; contracts, epic user stories, architecture zoom levels, traceability matrices
- **`brainkb-review-deck-plan.md`** — review deck preparation; slide outline, authoring guidance, validation checklist

## Directory Structure

```
design/
  brainkb-architecture.md          # <-- edit this
  brainkb-review-deck-plan.md      # <-- edit this
  original_source/
    brainkb-architecture-deck-redesign.md   # historical reference; do not edit
  utils/
    split_design_doc.py            # one-time split utility (already run)
    merge_design_doc.py            # combines both docs for review/export
    README.md
```

## `original_source/`

Contains `brainkb-architecture-deck-redesign.md` — the original combined document from which the two working files were derived via `utils/split_design_doc.py`.  Do not edit it; all ongoing work happens in the split files above.

## Merging for review or export

To produce a single combined document:

```bash
cd design/
python utils/merge_design_doc.py brainkb-architecture.md brainkb-review-deck-plan.md
```

Output: `brainkb-architecture-merged.md` (written alongside `brainkb-architecture.md`)
