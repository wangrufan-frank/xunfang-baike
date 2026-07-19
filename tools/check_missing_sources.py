#!/usr/bin/env python3
"""Check for pages with no public sources and fail the build with a clear error.

Pages without public internet sources are a compliance risk. The public-content
policy (spec section 6.2) requires that every third-level page cite at least one
verifiable public web source, or be explicitly acknowledged as uncovered.

Usage:
    python tools/check_missing_sources.py          # check all modules
    python tools/check_missing_sources.py --module zhuangbei  # check one module
"""

from argparse import ArgumentParser
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = ROOT / "data" / "public-sources.json"

# Pages that have been verified to have no discoverable public internet sources.
# These are documented exceptions per the spec.
ACKNOWLEDGED_UNCOVERED: set[str] = set()


def main(argv=None):
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--module", help="Only check one module directory")
    parser.add_argument(
        "--acknowledge",
        action="append",
        default=[],
        help="Acknowledge a page as uncovered (may repeat). "
             "Format: module/slug.html",
    )
    args = parser.parse_args(argv)

    if not LEDGER_PATH.exists():
        print(f"ERROR: ledger not found at {LEDGER_PATH}", file=sys.stderr)
        return 1

    with LEDGER_PATH.open(encoding="utf-8") as stream:
        ledger = json.load(stream)

    acknowledged = set(args.acknowledge) | ACKNOWLEDGED_UNCOVERED

    uncovered = []
    for page in ledger.get("pages", []):
        path = page.get("path", "")
        if args.module and not path.startswith(f"{args.module}/"):
            continue
        source_ids = page.get("source_ids", [])
        # Also check point-level pages
        if not source_ids and page.get("points"):
            point_source_ids = set()
            for point in page["points"]:
                point_source_ids.update(point.get("source_ids", []))
            source_ids = list(point_source_ids)

        if not source_ids:
            uncovered.append(path)

    if not uncovered:
        print("PASS: All checked pages have at least one public source.")
        return 0

    acknowledged_uncovered = [p for p in uncovered if p in acknowledged]
    truly_uncovered = [p for p in uncovered if p not in acknowledged]

    if truly_uncovered:
        print(
            f"ERROR: {len(truly_uncovered)} page(s) have NO public internet sources:",
            file=sys.stderr,
        )
        for path in sorted(truly_uncovered):
            print(f"  - {path}", file=sys.stderr)

        print(
            "\nThese pages must either be assigned public sources in "
            "data/public-sources.json or be explicitly acknowledged as "
            "uncovered by adding their path to ACKNOWLEDGED_UNCOVERED "
            "in tools/check_missing_sources.py.\n"
            "\nTo search for a public source, try:\n"
            "  WebSearch for the equipment name + site:gov.cn or "
            "site:mil.cn\n",
            file=sys.stderr,
        )

    if acknowledged_uncovered:
        print(
            f"INFO: {len(acknowledged_uncovered)} page(s) acknowledged as uncovered:",
        )
        for path in sorted(acknowledged_uncovered):
            print(f"  - {path}")

    return 1 if truly_uncovered else 0


if __name__ == "__main__":
    sys.exit(main())
