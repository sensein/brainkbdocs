"""Split a brainkb architecture design doc into a design doc and a deck plan.

Usage:
    python utils/split_design_doc.py original_source/brainkb-architecture-deck-redesign.md
"""

import argparse
import pathlib

DESIGN_SECTIONS = {
    "Revised Intent",
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
}

DECK_SECTIONS = {
    "Source-Of-Truth Workflow",
    "Source Deck Disposition",
    "Reviewer-Driven Revision Principles",
    "Rebuilt Deck Outline",
    "Authoring Guidance For The Later Deck",
    "Validation Checklist",
}


def parse_sections(lines):
    """Return list of (title, lines) tuples; preamble title is '__preamble__'."""
    sections = []
    current_title = None
    current_lines = []
    for line in lines:
        if line.startswith("## "):
            if current_title is not None:
                sections.append((current_title, current_lines))
            current_title = line[3:].strip()
            current_lines = [line]
        else:
            if current_title is None:
                current_title = "__preamble__"
            current_lines.append(line)
    if current_title is not None:
        sections.append((current_title, current_lines))
    return sections


def build_file(header_lines, sections, include):
    out = list(header_lines)
    for title, sec_lines in sections:
        if title in include:
            out.extend(sec_lines)
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=pathlib.Path,
                        help="Path to the source markdown file to split.")
    args = parser.parse_args()

    src = args.source.resolve()
    out_dir = src.parent.parent  # design/original_source -> design/

    lines = src.read_text().splitlines(keepends=True)
    sections = parse_sections(lines)

    design_header = [
        "# BrainKB Architecture\n\n",
        "Status: design document  \n",
        "Audience: engineering team  \n\n",
    ]
    deck_header = [
        "# BrainKB Review Deck Plan\n\n",
        "Status: review preparation artifact  \n",
        f"Source design doc: `original_source/{src.name}`  \n\n",
    ]

    design_lines = build_file(design_header, sections, DESIGN_SECTIONS)
    deck_lines = build_file(deck_header, sections, DECK_SECTIONS)

    out_design = out_dir / "brainkb-architecture.md"
    out_deck = out_dir / "brainkb-review-deck-plan.md"

    out_design.write_text("".join(design_lines))
    out_deck.write_text("".join(deck_lines))

    print(f"Written {len(design_lines)} lines -> {out_design.name}")
    print(f"Written {len(deck_lines)} lines  -> {out_deck.name}")

    unhandled = [t for t, _ in sections
                 if t not in DESIGN_SECTIONS and t not in DECK_SECTIONS and t != "__preamble__"]
    if unhandled:
        print(f"WARNING: unassigned sections: {unhandled}")


if __name__ == "__main__":
    main()
