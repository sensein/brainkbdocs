"""Merge two split design doc files back into a single file.

Usage:
    python utils/merge_design_doc.py brainkb-architecture.md brainkb-review-deck-plan.md
    python utils/merge_design_doc.py brainkb-architecture.md brainkb-review-deck-plan.md \\
        --original original_source/brainkb-architecture-deck-redesign.md
"""

import argparse
import difflib
import pathlib

# Original section order (must match the order in the source file)
ORIGINAL_ORDER = [
    "Source-Of-Truth Workflow",
    "Revised Intent",
    "Source Deck Disposition",
    "Reviewer-Driven Revision Principles",
    "MVP Competency Fixture",
    "MVP Capability Boundaries",
    "Identifier Governance Contract",
    "Claim And Provenance Contract",
    "Graph Release And Projection Contract",
    "Operational Readiness Contract",
    "Ontology Alignment And FAIR Contract",
    "Store And Query Strategy",
    "API Boundary And Technical Burden",
    "Cache And Agent Memory Strategy",
    "Cleaned Epic User Stories",
    "Five Architecture Zoom Levels",
    "Traceability Matrix",
    "Contract Traceability Matrix",
    "Rebuilt Deck Outline",
    "Authoring Guidance For The Later Deck",
    "Validation Checklist",
]

ORIGINAL_PREAMBLE = (
    "# BrainKB Architecture Deck Redesign\n"
    "\n"
    "Status: review-ready planning artifact  \n"
    "Audience: engineering team  \n"
    "Source material: `/Users/satra/Downloads/brainkb-ui-arch.pptx` and companion web export  \n"
    "Canonical deliverable: this Markdown design doc  \n"
    "Derivative deliverable: generated review deck under `output/`\n"
    "\n"
)


def parse_sections(lines):
    """Return dict of title -> lines (including the ## heading line)."""
    sections = {}
    current_title = None
    current_lines = []
    for line in lines:
        if line.startswith("## "):
            if current_title is not None:
                sections[current_title] = current_lines
            current_title = line[3:].strip()
            current_lines = [line]
        else:
            if current_title is not None:
                current_lines.append(line)
    if current_title is not None:
        sections[current_title] = current_lines
    return sections


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("architecture", type=pathlib.Path,
                        help="Path to the architecture design doc (e.g. brainkb-architecture.md).")
    parser.add_argument("deck_plan", type=pathlib.Path,
                        help="Path to the review deck plan (e.g. brainkb-review-deck-plan.md).")
    parser.add_argument("--original", type=pathlib.Path, default=None,
                        help="Optional path to the original source file to verify against.")
    args = parser.parse_args()

    arch_sections = parse_sections(args.architecture.read_text().splitlines(keepends=True))
    deck_sections = parse_sections(args.deck_plan.read_text().splitlines(keepends=True))
    all_sections  = {**arch_sections, **deck_sections}

    missing = [t for t in ORIGINAL_ORDER if t not in all_sections]
    if missing:
        print(f"ERROR: missing sections: {missing}")
        return

    merged = list(ORIGINAL_PREAMBLE)
    for title in ORIGINAL_ORDER:
        merged.extend(all_sections[title])

    out = args.architecture.parent / (args.architecture.stem + "-merged.md")
    out.write_text("".join(merged))
    print(f"Written -> {out}")

    if args.original is None:
        return

    if not args.original.exists():
        print(f"WARNING: original file not found at {args.original}, skipping diff check.")
        return

    original_text = args.original.read_text()
    merged_text   = "".join(merged)

    if original_text == merged_text:
        print("OK: merged file is identical to the original.")
    else:
        diff = list(difflib.unified_diff(
            original_text.splitlines(keepends=True),
            merged_text.splitlines(keepends=True),
            fromfile="original",
            tofile="merged",
            n=3,
        ))
        print(f"DIFF: {len(diff)} lines differ from original:")
        print("".join(diff[:60]))
        if len(diff) > 60:
            print(f"... ({len(diff) - 60} more lines)")


if __name__ == "__main__":
    main()
