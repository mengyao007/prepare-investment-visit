# PDF output

The user-facing Note is always a PDF. Keep Markdown only as a working intermediate.

## File workflow

1. Save the validated working note as outputs/note-source.md.
2. Run scripts/validate_note.py against the working note.
3. Render it with scripts/render_note_pdf.py:

    python scripts/render_note_pdf.py outputs/note-source.md outputs/company-visit-note.pdf

4. Run scripts/validate_pdf.py against the PDF.
5. Render every page to PNG with Poppler and visually inspect all pages:

    pdftoppm -png outputs/company-visit-note.pdf tmp/pdfs/company-visit-note

6. Fix layout defects and repeat validation and visual inspection.
7. Deliver the PDF. Do not deliver the Markdown intermediate unless the user explicitly requests it.

## Writing conventions for the renderer

- Use one H1 title.
- Use H2 for numbered main sections and H3 for subsections.
- Use short paragraphs, bullets, numbered questions, blockquotes for key callouts, and pipe tables for compact comparisons.
- Use Markdown links for citations. Keep raw URLs in the source ledger only when needed.
- Use the literal marker <!-- pagebreak --> only before a deliberate major-section page break.
- Keep tables to six columns or fewer; split dense tables instead of shrinking them until unreadable.

## Visual specification

- A4 portrait, restrained navy/blue palette, generous margins, and consistent hierarchy.
- Cover contains company, subtitle, meeting person, date/cutoff, confidentiality, and inputs used.
- Header identifies the report; footer contains page number and evidence-boundary reminder.
- First two pages remain decision-first and scannable.
- Long source links wrap without clipping.
- Tables repeat headers across pages where supported.

## Font handling

The renderer searches common Chinese fonts on Windows, macOS, and Linux. The user may set INVESTMENT_VISIT_FONT and INVESTMENT_VISIT_BOLD_FONT to explicit font paths. If no Chinese font is available, stop with a precise font error rather than emitting broken glyphs.
