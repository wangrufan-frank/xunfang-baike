"""Command-line entry point for validating and building learning modules."""

from __future__ import annotations

import argparse
from pathlib import Path

from learning_modules import build_pages, load_catalog, validate_catalog


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and build static learning pages")
    parser.add_argument("--check", action="store_true", help="validate without writing files")
    parser.add_argument("--catalog", type=Path, help="catalog path (defaults to data/learning-modules.json)")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    catalog_path = args.catalog or root / "data" / "learning-modules.json"
    catalog = load_catalog(catalog_path)
    errors = validate_catalog(catalog)
    if errors:
        print(f"目录校验失败（{len(errors)} 项）：")
        for error in errors:
            print(f"- {error}")
        return 1

    module_count = len(catalog["modules"])
    article_count = sum(len(module["articles"]) for module in catalog["modules"])
    if args.check:
        print(f"目录校验通过：{module_count} 个模块，{article_count} 篇文章，未写入文件。")
        return 0

    pages = build_pages(root, catalog)
    print(f"生成完成：{module_count} 个模块，{article_count} 篇文章，{len(pages)} 个页面。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
