# Design Doc Utilities

## `merge_design_doc.py`

Combines `brainkb-architecture.md` and `brainkb-review-deck-plan.md` into a single file.
Run from the `design/` directory.

```bash
python utils/merge_design_doc.py brainkb-architecture.md brainkb-review-deck-plan.md
```

Output: `brainkb-architecture-merged.md` (written alongside the architecture file)

Optionally verify the result matches the original source:

```bash
python utils/merge_design_doc.py brainkb-architecture.md brainkb-review-deck-plan.md \
    --original original_source/brainkb-architecture-deck-redesign.md
```

## `split_design_doc.py`

One-time utility used to split the original source into the two working documents.
Not needed for normal editing — kept for reference.

```bash
python utils/split_design_doc.py original_source/brainkb-architecture-deck-redesign.md
```
