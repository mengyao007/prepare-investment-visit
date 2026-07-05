#!/usr/bin/env python3
"""Structural validator for the Markdown source used to render visit-note PDFs."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SECTION_RULES = {
    "investment_brief": r"投资简报|执行摘要|核心结论|投资判断",
    "meeting_person": r"交流对象|会谈对象|人物画像|meeting person",
    "company_product": r"公司与产品|公司概况|产品与技术",
    "market_competition": r"市场与竞争|行业与竞争|竞争格局",
    "commercial_operations": r"商业与运营|商业模式|经营验证|运营验证",
    "team_capital": r"团队.*资本|团队.*融资|财务|融资|股权|治理",
    "recent_risks": r"近期动态|时间线|风险|红旗|矛盾",
    "meeting_plan": r"会谈计划|交流问题|核心问题|访谈问题",
    "sources": r"来源|证据台账|参考资料|sources|references",
}

PROFILES = {
    "quick": {"min_urls": 3, "max_urls": 15, "min_questions": 8, "min_chars": 1200, "max_chars": 14000},
    "standard": {"min_urls": 8, "max_urls": 35, "min_questions": 10, "min_chars": 5000, "max_chars": 22000},
    "deep": {"min_urls": 15, "max_urls": 70, "min_questions": 12, "min_chars": 10000, "max_chars": 42000},
}


def validate(text: str, profile: str, strict: bool) -> dict:
    limits = PROFILES[profile]
    headings = [line.strip("# ").strip() for line in text.splitlines() if line.startswith("#")]
    heading_blob = "\n".join(headings).lower()
    missing = [name for name, pattern in SECTION_RULES.items() if not re.search(pattern, heading_blob, re.I)]
    urls = re.findall(r"https?://[^\s)>]+", text)
    questions = [
        line for line in text.splitlines()
        if re.match(r"\s*(?:[-*]|\d+[.)、])\s*.*[？?]\s*$", line)
    ]
    checks = {
        "cutoff": bool(re.search(r"研究(?:基准|截止)|信息截止|research cutoff|截至\s*20\d{2}", text, re.I)),
        "boundary": bool(re.search(r"不构成.*(?:尽调|建议)|证据边界|信息边界|非正式.*尽调", text, re.I)),
        "inputs": bool(re.search(r"输入材料|使用材料|材料来源|inputs used", text, re.I)),
        "meeting_person": bool(re.search(r"交流对象|会谈对象|meeting person", text, re.I)),
        "current_action": bool(re.search(r"当前建议|当前行动|优先跟进|继续交流|观察|暂缓", text, re.I)),
    }
    evidence_terms = len(re.findall(r"公司口径|公司称|待核验|未找到可靠公开披露|推断|推算|已验证事实|\[S\d+\]", text, re.I))

    warnings: list[str] = []
    if len(questions) < limits["min_questions"]:
        warnings.append(f"Only {len(questions)} explicit question lines found; target is {limits['min_questions']}.")
    if len(urls) < (limits["min_urls"] if strict else 1):
        warnings.append(f"Only {len(urls)} source URLs found.")
    if len(urls) > limits["max_urls"]:
        warnings.append(f"{len(urls)} source URLs exceed the {profile} target ceiling.")
    if len(text) < limits["min_chars"]:
        warnings.append(f"Note is shorter than the {profile} target of {limits['min_chars']} characters.")
    if len(text) > limits["max_chars"]:
        warnings.append(f"Note exceeds the {profile} target ceiling of {limits['max_chars']} characters.")
    if evidence_terms < 5:
        warnings.append("Evidence-boundary labels appear sparse.")

    errors: list[str] = []
    if missing:
        errors.append("Missing section families: " + ", ".join(missing))
    failed_checks = [name for name, passed in checks.items() if not passed]
    if failed_checks:
        errors.append("Missing required front-matter/content checks: " + ", ".join(failed_checks))

    return {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "stats": {
            "headings": len(headings),
            "urls": len(urls),
            "question_lines": len(questions),
            "characters": len(text),
            "evidence_labels": evidence_terms,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("note", type=Path)
    parser.add_argument("--profile", choices=sorted(PROFILES), default="standard")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    result = validate(args.note.read_text(encoding="utf-8"), args.profile, args.strict)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
