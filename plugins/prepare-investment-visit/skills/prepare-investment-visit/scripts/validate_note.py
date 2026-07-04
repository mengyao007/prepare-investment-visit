#!/usr/bin/env python3
"""Structural validator for Markdown investment-visit notes."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SECTION_RULES = {
    "executive_summary": r"executive summary|执行摘要|核心结论|初步投决|投资判断",
    "company_or_product": r"公司(?:事实|概况|基本情况)|产品|技术",
    "industry": r"行业|市场|赛道",
    "competition": r"竞争|竞品|竞对|护城河|壁垒",
    "team": r"团队|创始人",
    "finance_or_funding": r"财务|融资|股权|cap table",
    "questions": r"问题清单|交流问题|必须回答|访谈问题",
    "sources": r"来源|证据|sources|references",
}

PROFILES = {
    "quick": {"min_urls": 3, "max_urls": 12, "min_questions": 8, "min_chars": 1200, "max_chars": 12000},
    "standard": {"min_urls": 8, "max_urls": 30, "min_questions": 10, "min_chars": 4000, "max_chars": 18000},
    "deep": {"min_urls": 15, "max_urls": 60, "min_questions": 12, "min_chars": 8000, "max_chars": 36000},
}

PROFILE_SECTION_RULES = {
    "quick": {},
    "standard": {"recent_developments": r"近期动态|最新动态|时间线|里程碑|recent developments"},
    "deep": {"recent_developments": r"近期动态|最新动态|时间线|里程碑|recent developments"},
}


def validate(text: str, profile: str, strict: bool) -> dict:
    limits = PROFILES[profile]
    headings = [line.strip("# ").strip() for line in text.splitlines() if line.startswith("#")]
    heading_blob = "\n".join(headings).lower()
    rules = {**SECTION_RULES, **PROFILE_SECTION_RULES[profile]}
    missing = [name for name, pattern in rules.items() if not re.search(pattern, heading_blob, re.I)]

    urls = re.findall(r"https?://[^\s)>]+", text)
    question_lines = [
        line for line in text.splitlines()
        if re.match(r"\s*(?:[-*]|\d+[.)、])\s*.*[？?]\s*$", line)
    ]
    has_cutoff = bool(re.search(r"研究(?:基准|截止)|信息截止|research cutoff|截至\s*20\d{2}", text, re.I))
    has_boundary = bool(re.search(r"不构成.*(?:尽调|建议)|证据边界|信息边界|非正式.*尽调", text, re.I))
    evidence_terms = len(re.findall(r"公司口径|公司称|待核验|未找到可靠公开披露|推测|推算|\[S\d+\]", text, re.I))

    warnings = []
    if len(question_lines) < limits["min_questions"]:
        warnings.append(
            f"Only {len(question_lines)} explicit question lines found; "
            f"{profile} target is at least {limits['min_questions']}."
        )
    if len(urls) < (limits["min_urls"] if strict else 1):
        warnings.append(f"Only {len(urls)} source URLs found.")
    if len(urls) > limits["max_urls"]:
        warnings.append(f"{len(urls)} source URLs exceed the {profile} target ceiling of {limits['max_urls']}.")
    if len(text) < limits["min_chars"]:
        warnings.append(f"Note is shorter than the {profile} target of {limits['min_chars']} characters.")
    if len(text) > limits["max_chars"]:
        warnings.append(f"Note exceeds the {profile} target ceiling of {limits['max_chars']} characters.")
    if evidence_terms < 3:
        warnings.append("Evidence-boundary labels appear sparse.")

    errors = []
    if missing:
        errors.append("Missing section families: " + ", ".join(missing))
    if not has_cutoff:
        errors.append("Missing research cutoff date.")
    if not has_boundary:
        errors.append("Missing evidence/due-diligence boundary statement.")

    return {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "stats": {
            "headings": len(headings),
            "urls": len(urls),
            "question_lines": len(question_lines),
            "characters": len(text),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("note", type=Path)
    parser.add_argument("--profile", choices=sorted(PROFILES), default="standard")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    text = args.note.read_text(encoding="utf-8")
    result = validate(text, args.profile, args.strict)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
