#!/usr/bin/env python3
"""Validate the structural integrity of an investment-visit PDF."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

from pypdf import PdfReader


PAGE_TARGETS = {"quick": (2, 7), "standard": (5, 18), "deep": (10, 35)}
REQUIRED_TERMS = [
    ("meeting_person", ["交流对象", "会谈对象", "Meeting person"]),
    ("investment_view", ["投资判断", "当前建议", "核心结论"]),
    ("company_product", ["公司与产品", "公司概况", "产品与技术"]),
    ("market_competition", ["市场与竞争", "行业与竞争", "竞争格局"]),
    ("risk", ["风险", "红旗", "矛盾"]),
    ("questions", ["核心问题", "交流问题", "会谈问题"]),
    ("sources", ["来源", "证据台账", "参考资料"]),
    ("cutoff", ["研究截止", "信息截止", "研究基准"]),
]


def validate(pdf: Path, profile: str) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    reader = PdfReader(str(pdf))
    page_texts = [(page.extract_text() or "").strip() for page in reader.pages]
    text = "\n".join(page_texts)
    if not reader.pages:
        errors.append("PDF contains no pages.")
    empty_pages = [index + 1 for index, value in enumerate(page_texts) if len(value) < 20]
    if empty_pages:
        errors.append(f"Pages with little or no extractable text: {empty_pages}")
    if "�" in text:
        errors.append("PDF contains Unicode replacement characters.")
    if len(text) < 1000:
        errors.append("Extracted PDF text is unexpectedly short.")
    missing = [name for name, alternatives in REQUIRED_TERMS if not any(term.lower() in text.lower() for term in alternatives)]
    if missing:
        errors.append("Missing required content families: " + ", ".join(missing))
    minimum, maximum = PAGE_TARGETS[profile]
    if len(reader.pages) < minimum:
        warnings.append(f"{profile} PDF has only {len(reader.pages)} pages; target starts at {minimum}.")
    if len(reader.pages) > maximum:
        warnings.append(f"{profile} PDF has {len(reader.pages)} pages; target ceiling is {maximum}.")
    annotations = sum(len(page.get("/Annots") or []) for page in reader.pages)
    if annotations == 0:
        warnings.append("No PDF link annotations found; verify citations are clickable.")
    metadata = reader.metadata or {}
    if not metadata.get("/Title"):
        warnings.append("PDF title metadata is missing.")
    return {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "stats": {"pages": len(reader.pages), "characters": len(text), "link_annotations": annotations, "bytes": pdf.stat().st_size},
    }


def render_pages(pdf: Path, output_dir: Path) -> list[str]:
    executable = shutil.which("pdftoppm")
    if not executable:
        raise RuntimeError("pdftoppm is not available for visual QA.")
    executable_path = Path(executable)
    if executable_path.suffix.lower() in {".cmd", ".bat"}:
        bundled_exe = (
            executable_path.parent.parent
            / "native"
            / "poppler"
            / "Library"
            / "bin"
            / "pdftoppm.exe"
        )
        if bundled_exe.is_file():
            executable = str(bundled_exe)
    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = output_dir / pdf.stem
    subprocess.run([executable, "-png", "-r", "130", str(pdf), str(prefix)], check=True, capture_output=True, text=True)
    return [str(path) for path in sorted(output_dir.glob(f"{pdf.stem}-*.png"))]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--profile", choices=sorted(PAGE_TARGETS), default="standard")
    parser.add_argument("--render-dir", type=Path)
    args = parser.parse_args()
    if not args.pdf.is_file():
        raise SystemExit(f"PDF not found: {args.pdf}")
    result = validate(args.pdf, args.profile)
    if args.render_dir:
        try:
            images = render_pages(args.pdf, args.render_dir)
            result["rendered_pages"] = images
            if len(images) != result["stats"]["pages"]:
                result["errors"].append("Rendered page count does not match PDF page count.")
                result["ok"] = False
        except Exception as exc:
            result["errors"].append(str(exc))
            result["ok"] = False
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
