# Automation contract

Use this contract for file-backed and batch runs.

## Preflight gate

Before public research:

1. Confirm intake has values for meeting person, supplementary-material status, and podcast choice.
2. Confirm every declared input exists and is readable.
3. Confirm the Skill, required references, and scripts are readable.
4. Create the assigned output directory, write/read/remove a probe file, and verify every output path remains inside it.
5. Confirm depth and query/source/time/size ceilings.
6. Confirm a Chinese font and PDF dependencies are available.

If any check fails, stop with preflight_failed. Do not continue as if supplied materials were reviewed.

## Staged artifacts

For standard and deep runs, keep:

- research/material-claims.md after reading supplied materials;
- research/evidence-ledger.md after core public research;
- outputs/note-source.md as the internal validated source;
- outputs/company-visit-note.pdf as the required final Note;
- outputs/podcast-script.txt and an audio file only when podcast was selected.

Do not deliver internal checkpoints unless requested.

## Stop conditions

Stop searching and draft with labeled gaps when:

- a query, source, time, or user-provided ceiling is reached;
- two distinct searches cannot verify a narrow claim;
- remaining gaps are not decision-critical;
- new results repeat captured facts without improving source quality;
- a required tool or input becomes unavailable.

## Structured status

- complete: PDF exists, working-note validation passed, PDF validation passed, and page images were inspected; requested audio also exists or its exact rendering failure is disclosed.
- needs_clarification: target company or another essential intake value remains ambiguous.
- preflight_failed: input, output path, font, Skill resource, or required dependency is unavailable.
- failed: research or generation failed after preflight.
- partial: checkpoints exist but the final PDF does not.

Never report complete based only on a chat response. Verify every declared artifact.
