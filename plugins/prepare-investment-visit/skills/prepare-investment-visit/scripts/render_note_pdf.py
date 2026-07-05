#!/usr/bin/env python3
"""Render a constrained Markdown investment briefing as a polished Chinese PDF."""

from __future__ import annotations

import argparse
import html
import os
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import HRFlowable, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


NAVY = colors.HexColor("#17365D")
BLUE = colors.HexColor("#2F75B5")
PALE_BLUE = colors.HexColor("#EAF2F8")
LIGHT = colors.HexColor("#F5F7FA")
MID = colors.HexColor("#D8DEE9")
TEXT = colors.HexColor("#1F2937")
MUTED = colors.HexColor("#64748B")


def _first_existing(candidates: list[str | None]) -> str | None:
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return str(Path(candidate))
    return None


def register_fonts() -> tuple[str, str]:
    regular = _first_existing([
        os.getenv("INVESTMENT_VISIT_FONT"),
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
        r"C:\Windows\Fonts\simsun.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    ])
    if not regular:
        raise SystemExit("No Chinese font found. Set INVESTMENT_VISIT_FONT to a readable TTF/TTC font path.")
    bold = _first_existing([
        os.getenv("INVESTMENT_VISIT_BOLD_FONT"),
        r"C:\Windows\Fonts\msyhbd.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
        "/System/Library/Fonts/PingFang.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
    ]) or regular
    pdfmetrics.registerFont(TTFont("VisitSans", regular, subfontIndex=0))
    pdfmetrics.registerFont(TTFont("VisitSansBold", bold, subfontIndex=0))
    pdfmetrics.registerFontFamily("VisitSans", normal="VisitSans", bold="VisitSansBold", italic="VisitSans", boldItalic="VisitSansBold")
    return "VisitSans", "VisitSansBold"


def inline_markup(value: str) -> str:
    escaped = html.escape(value.strip(), quote=True)
    escaped = re.sub(
        r"\[([^\]]+)\]\((https?://[^\s)]+)\)",
        lambda match: f'<a href="{match.group(2)}" color="#1D4ED8"><u>{match.group(1)}</u></a>',
        escaped,
    )
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escaped)
    escaped = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", escaped)
    return escaped


def parse_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_separator(line: str) -> bool:
    cells = parse_cells(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def build_styles(font: str, bold_font: str):
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("CoverTitle", parent=styles["Title"], fontName=bold_font, fontSize=25, leading=34, textColor=NAVY, alignment=TA_LEFT, spaceAfter=12 * mm))
    styles.add(ParagraphStyle("H2CN", parent=styles["Heading2"], fontName=bold_font, fontSize=16, leading=23, textColor=NAVY, spaceBefore=6 * mm, spaceAfter=3 * mm, keepWithNext=True))
    styles.add(ParagraphStyle("H3CN", parent=styles["Heading3"], fontName=bold_font, fontSize=12, leading=18, textColor=BLUE, spaceBefore=4 * mm, spaceAfter=2 * mm, keepWithNext=True))
    styles.add(ParagraphStyle("BodyCN", parent=styles["BodyText"], fontName=font, fontSize=9.5, leading=16, textColor=TEXT, alignment=TA_LEFT, wordWrap="CJK", spaceAfter=2.5 * mm))
    styles.add(ParagraphStyle("BulletCN", parent=styles["BodyText"], fontName=font, fontSize=9.3, leading=15, textColor=TEXT, leftIndent=6 * mm, firstLineIndent=-4 * mm, wordWrap="CJK", spaceAfter=1.5 * mm))
    styles.add(ParagraphStyle("SmallCN", parent=styles["BodyText"], fontName=font, fontSize=7.8, leading=11, textColor=TEXT, wordWrap="CJK"))
    styles.add(ParagraphStyle("TableHeaderCN", parent=styles["BodyText"], fontName=bold_font, fontSize=7.8, leading=11, textColor=colors.white, wordWrap="CJK"))
    styles.add(ParagraphStyle("CalloutCN", parent=styles["BodyText"], fontName=font, fontSize=10, leading=16, textColor=NAVY, wordWrap="CJK"))
    return styles


def render(markdown_path: Path, output_path: Path) -> None:
    font, bold_font = register_fonts()
    styles = build_styles(font, bold_font)
    lines = markdown_path.read_text(encoding="utf-8").splitlines()
    title = next((line[2:].strip() for line in lines if line.startswith("# ")), markdown_path.stem)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=20 * mm,
        bottomMargin=18 * mm,
        title=title,
        author="prepare-investment-visit",
        subject="一级市场访前研究",
    )
    story = []
    paragraph_lines: list[str] = []
    seen_title = False
    first_h2 = True

    def flush_paragraph() -> None:
        if paragraph_lines:
            story.append(Paragraph(inline_markup(" ".join(paragraph_lines)), styles["BodyCN"]))
            paragraph_lines.clear()

    index = 0
    while index < len(lines):
        stripped = lines[index].strip()
        if not stripped:
            flush_paragraph()
            index += 1
            continue
        if stripped == "<!-- pagebreak -->":
            flush_paragraph()
            story.append(PageBreak())
            index += 1
            continue
        if stripped in {"---", "***"}:
            flush_paragraph()
            story.append(HRFlowable(width="100%", thickness=0.7, color=MID))
            story.append(Spacer(1, 2 * mm))
            index += 1
            continue
        if stripped.startswith("# "):
            flush_paragraph()
            seen_title = True
            story.append(Spacer(1, 20 * mm))
            story.append(Paragraph(inline_markup(stripped[2:]), styles["CoverTitle"]))
            story.append(HRFlowable(width="34%", thickness=3, color=BLUE, hAlign="LEFT"))
            story.append(Spacer(1, 8 * mm))
            index += 1
            continue
        if stripped.startswith("## "):
            flush_paragraph()
            if seen_title and first_h2:
                story.append(PageBreak())
                first_h2 = False
            story.append(Paragraph(inline_markup(stripped[3:]), styles["H2CN"]))
            index += 1
            continue
        if stripped.startswith("### "):
            flush_paragraph()
            story.append(Paragraph(inline_markup(stripped[4:]), styles["H3CN"]))
            index += 1
            continue
        if stripped.startswith(">"):
            flush_paragraph()
            callout = Paragraph(inline_markup(stripped.lstrip("> ")), styles["CalloutCN"])
            table = Table([[callout]], colWidths=[doc.width])
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), PALE_BLUE),
                ("BOX", (0, 0), (-1, -1), 0.5, BLUE),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]))
            story.append(table)
            story.append(Spacer(1, 3 * mm))
            index += 1
            continue
        if "|" in stripped and index + 1 < len(lines) and is_separator(lines[index + 1]):
            flush_paragraph()
            rows = [parse_cells(stripped)]
            index += 2
            while index < len(lines) and "|" in lines[index] and lines[index].strip():
                rows.append(parse_cells(lines[index]))
                index += 1
            column_count = max(len(row) for row in rows)
            rows = [row + [""] * (column_count - len(row)) for row in rows]
            data = [
                [
                    Paragraph(
                        inline_markup(cell),
                        styles["TableHeaderCN"] if row_index == 0 else styles["SmallCN"],
                    )
                    for cell in row
                ]
                for row_index, row in enumerate(rows)
            ]
            table = Table(data, colWidths=[doc.width / column_count] * column_count, repeatRows=1, hAlign="LEFT")
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), bold_font),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
                ("GRID", (0, 0), (-1, -1), 0.35, MID),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]))
            story.append(table)
            story.append(Spacer(1, 3 * mm))
            continue
        bullet = re.match(r"^[-*]\s+(.+)$", stripped)
        numbered = re.match(r"^(\d+)[.)、]\s*(.+)$", stripped)
        if bullet or numbered:
            flush_paragraph()
            prefix = "•" if bullet else f"{numbered.group(1)}."
            body = bullet.group(1) if bullet else numbered.group(2)
            story.append(Paragraph(f"{prefix} {inline_markup(body)}", styles["BulletCN"]))
            index += 1
            continue
        paragraph_lines.append(stripped)
        index += 1
    flush_paragraph()

    def draw_page(canvas, pdf_doc):
        canvas.saveState()
        width, height = A4
        canvas.setStrokeColor(MID)
        canvas.setLineWidth(0.4)
        canvas.line(18 * mm, height - 13 * mm, width - 18 * mm, height - 13 * mm)
        canvas.setFont(font, 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(18 * mm, height - 10 * mm, "一级市场访前研究")
        canvas.drawRightString(width - 18 * mm, 10 * mm, f"第 {pdf_doc.page} 页 | 非正式尽调材料")
        canvas.restoreState()

    doc.build(story, onFirstPage=draw_page, onLaterPages=draw_page)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("markdown", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if not args.markdown.is_file():
        raise SystemExit(f"Markdown source not found: {args.markdown}")
    render(args.markdown, args.output)
    if not args.output.is_file() or args.output.stat().st_size < 1024:
        raise SystemExit("PDF rendering did not produce a valid non-empty file.")
    print(f"PDF_OK\t{args.output.resolve()}\t{args.output.stat().st_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
