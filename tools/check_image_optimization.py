"""Validate the image-optimization ledger without changing site files."""

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

DECISIONS = {"keep", "add", "replace", "no-image"}
VISUAL_TYPES = {"structure-label", "step-flow", "scene-zone", "comparison", "checklist", "legal-relationship"}
IMPLEMENTATION_STATUSES = {"not-started", "in-progress", "complete", "blocked"}
ACCEPTANCE_STATUSES = {"not-reviewed", "accepted", "blocked"}
ASSET_STATUSES = {"planned", "complete", "blocked"}
SOURCE_STATUSES = {"original", "external", "internal", "not-needed"}


def _load(root, relative):
    return json.loads((Path(root) / relative).read_text(encoding="utf-8"))


def _expected(inventory):
    return {article["path"]: article["module"] for module in inventory["modules"] for article in module["articles"]}


def validate_plan(root, module=None, require_complete=False):
    """Return ledger contract violations; an empty list is valid."""
    root = Path(root)
    errors = []
    try:
        plan = _load(root, "data/image-optimization-plan.json")
        expected = _expected(_load(root, "data/content-inventory.json"))
    except (OSError, json.JSONDecodeError) as exc:
        return [str(exc)]
    if plan.get("version") != 1 or plan.get("updated_at") != "2026-08-10":
        errors.append("invalid top-level version or updated_at")
    pages = plan.get("pages")
    if not isinstance(pages, list):
        return errors + ["pages must be a list"]
    paths = [page.get("path") for page in pages if isinstance(page, dict)]
    if len(paths) != len(expected) or set(paths) != set(expected) or len(set(paths)) != len(paths):
        errors.append("pages must cover inventory paths exactly once")
    for index, page in enumerate(pages):
        label = page.get("path", f"pages[{index}]") if isinstance(page, dict) else f"pages[{index}]"
        if not isinstance(page, dict):
            errors.append(f"{label}: page must be an object")
            continue
        path = page.get("path")
        if not isinstance(path, str) or not path.strip():
            errors.append(f"{label}: path must be a non-empty string")
            continue
        expected_module = expected.get(path)
        if page.get("module") != expected_module:
            errors.append(f"{label}: module does not match inventory")
        if module is not None and expected_module != module:
            continue
        current_images = page.get("current_images")
        if not isinstance(current_images, int) or isinstance(current_images, bool) or current_images < 0:
            errors.append(f"{label}: current_images must be a non-negative integer")
        else:
            html_path = root / path
            if not html_path.exists() or html_path.read_text(encoding="utf-8").count("<img") != current_images:
                errors.append(f"{label}: current_images does not match HTML")
        if page.get("decision") not in DECISIONS:
            errors.append(f"{label}: invalid decision")
        if page.get("implementation_status") not in IMPLEMENTATION_STATUSES:
            errors.append(f"{label}: invalid implementation_status")
        if page.get("acceptance_status") not in ACCEPTANCE_STATUSES:
            errors.append(f"{label}: invalid acceptance_status")
        if not isinstance(page.get("reason"), str) or not page["reason"].strip():
            errors.append(f"{label}: reason is required")
        for field in ("learning_targets", "visual_types", "insertion_points", "assets"):
            if not isinstance(page.get(field), list):
                errors.append(f"{label}: {field} must be a list")
        if any(kind not in VISUAL_TYPES for kind in page.get("visual_types", [])):
            errors.append(f"{label}: invalid visual type")
        assets = page.get("assets", [])
        if page.get("decision") in {"add", "replace"} and not assets:
            errors.append(f"{label}: {page.get('decision')} requires an asset")
        if page.get("decision") == "no-image" and assets:
            errors.append(f"{label}: no-image cannot have assets")
        for asset in assets:
            required = ("path", "kind", "purpose", "source_status", "source_url", "publisher", "accessed_at", "license", "status")
            if not isinstance(asset, dict) or any(not isinstance(asset.get(key), str) for key in required):
                errors.append(f"{label}: incomplete asset source fields")
                continue
            if asset["status"] not in ASSET_STATUSES:
                errors.append(f"{label}: invalid asset status")
            source_status = asset["source_status"]
            if source_status not in SOURCE_STATUSES:
                errors.append(f"{label}: invalid source_status")
                continue
            try:
                date.fromisoformat(asset["accessed_at"])
            except ValueError:
                errors.append(f"{label}: asset accessed_at must be ISO date")
            provenance = (asset["publisher"].strip(), asset["accessed_at"].strip(), asset["license"].strip())
            if source_status == "external":
                try:
                    parsed = urlparse(asset["source_url"])
                    valid_url = parsed.scheme in {"https", "http"} and bool(parsed.hostname)
                except ValueError:
                    valid_url = False
                if not valid_url or not all(provenance):
                    errors.append(f"{label}: external asset requires valid provenance")
            elif source_status in {"original", "internal"}:
                if asset["source_url"].strip() or not all(provenance):
                    errors.append(f"{label}: {source_status} asset requires local provenance without source_url")
            elif source_status == "not-needed" and any((asset["source_url"].strip(), *provenance)):
                errors.append(f"{label}: not-needed asset cannot claim provenance")
        if require_complete:
            terminal = ((page.get("implementation_status") == "complete" and page.get("acceptance_status") == "accepted") or
                        (page.get("implementation_status") == "blocked" and page.get("acceptance_status") == "blocked" and page.get("blocked_reason", "").strip()))
            if not terminal:
                errors.append(f"{label}: page is not in a terminal state")
            if page.get("implementation_status") == "blocked" and any(asset.get("status") == "complete" for asset in assets if isinstance(asset, dict)):
                errors.append(f"{label}: blocked page cannot contain complete new assets")
    return errors


def validate_runtime(root, module=None, require_complete=False):
    """Check assets only for pages whose implementation is complete."""
    root = Path(root)
    try:
        pages = _load(root, "data/image-optimization-plan.json").get("pages", [])
        expected = _expected(_load(root, "data/content-inventory.json"))
    except (OSError, json.JSONDecodeError) as exc:
        return [str(exc)]
    errors = []
    for page in pages:
        if not isinstance(page, dict):
            errors.append("runtime page must be an object")
            continue
        path = page.get("path")
        if not isinstance(path, str) or not path.strip():
            errors.append("runtime page path must be a non-empty string")
            continue
        expected_module = expected.get(path)
        if page.get("module") != expected_module:
            errors.append(f"{path}: module does not match inventory")
        if module is not None and expected_module != module:
            continue
        if require_complete:
            terminal = (
                page.get("implementation_status") == "complete"
                and page.get("acceptance_status") == "accepted"
            ) or (
                page.get("implementation_status") == "blocked"
                and page.get("acceptance_status") == "blocked"
                and bool(page.get("blocked_reason", "").strip())
            )
            if not terminal:
                errors.append(f"{page.get('path', 'runtime page')}: page is not in a terminal state")
        if page.get("implementation_status") != "complete":
            continue
        html_path = root / path
        html = html_path.read_text(encoding="utf-8") if html_path.exists() else ""
        for asset in page.get("assets", []):
            if asset.get("status") != "complete":
                continue
            asset_path = root / asset["path"]
            if not asset_path.exists():
                errors.append(f"{page['path']}: missing asset {asset['path']}")
                continue
            if asset["path"] not in html:
                errors.append(f"{page['path']}: asset is not referenced in HTML")
            if asset.get("kind") == "svg":
                try:
                    svg = asset_path.read_text(encoding="utf-8")
                    node = ET.fromstring(svg)
                    if not node.get("viewBox") or not any(child.tag.endswith("title") for child in node) or not any(child.tag.endswith("desc") for child in node):
                        errors.append(f"{page['path']}: SVG needs viewBox, title and desc")
                    if "http://" in svg or "https://" in svg or "href=" in svg:
                        errors.append(f"{page['path']}: SVG contains an external reference")
                except (OSError, ET.ParseError) as exc:
                    errors.append(f"{page['path']}: invalid SVG ({exc})")
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", choices=("zhuangbei", "qinwu", "xunlian", "jingqing", "fagui", "zoufang"))
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[1]
    errors = list(dict.fromkeys(
        validate_plan(root, module=args.module, require_complete=args.require_complete)
        + validate_runtime(root, module=args.module, require_complete=args.require_complete)
    ))
    all_pages = _load(root, "data/image-optimization-plan.json").get("pages", [])
    expected = _expected(_load(root, "data/content-inventory.json"))
    pages = sum(
        1
        for page in all_pages
        if args.module is None or expected.get(page.get("path")) == args.module
    )
    print(f"{pages} pages checked")
    print(f"{len(errors)} validation errors")
    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
