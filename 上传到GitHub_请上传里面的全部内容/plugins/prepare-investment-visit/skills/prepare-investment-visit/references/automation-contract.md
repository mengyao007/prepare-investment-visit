# Automation contract

Use this contract for CLI, bot, batch, or other file-backed runs.

## Preflight gate

Before any web search:

1. Confirm every declared input exists and is readable.
2. Confirm the Skill instructions and required references are readable.
3. Create the output directory, write a small probe file, read it back, and remove it.
4. Confirm the selected output filenames stay inside the assigned job directory.
5. Confirm the research depth and its query, source, time, and output-size ceilings.

If any check fails, stop immediately with `preflight_failed`. Do not continue public research without the supplied materials when the user expected those materials to be reviewed.

## Staged artifacts

For `standard` and `deep` file-backed runs, write these checkpoints:

- `research/material-claims.md` after reading supplied materials.
- `research/evidence-ledger.md` after core public research.
- `outputs/note.md` after drafting and validation.

Write a compact checkpoint rather than retaining all browsing text. A failed later stage should leave enough evidence to resume without repeating completed research.

## Stop conditions

Stop research and draft with labeled gaps when any condition is met:

- query, source, wall-time, or user-provided token ceiling;
- two distinct queries for a narrow claim yield no reliable result;
- remaining gaps are not decision-critical for the upcoming meeting;
- new results repeat already captured facts without improving source quality;
- required tools or files become unavailable.

## Structured status

Automation wrappers should distinguish:

- `complete`: requested files exist and validation ran;
- `needs_clarification`: company identity or another essential input is ambiguous;
- `preflight_failed`: files, output path, Skill resources, or sandbox are unavailable;
- `failed`: research or generation failed after preflight;
- `partial`: checkpoint artifacts exist but the final deliverable does not.

Never report `complete` solely because a final chat message was produced. Verify every declared output path exists.
