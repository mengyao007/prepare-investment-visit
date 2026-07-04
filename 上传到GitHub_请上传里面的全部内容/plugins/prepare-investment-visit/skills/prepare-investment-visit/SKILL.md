---
name: prepare-investment-visit
description: Prepare evidence-backed pre-meeting research for private-market and venture-capital company visits. Use when an investor provides a company name, short introduction, teaser, BP/pitch deck, website, founder name, or meeting plan and needs a structured company briefing, founder profile, industry and competitor analysis, business/operating/financial/funding/ownership review, recent developments, red flags, tailored interview questions, or a post-meeting data-request list. Also use when the user explicitly requests a podcast/audio briefing or a video briefing derived from the research note.
---

# Prepare Investment Visit

Produce an investor-grade pre-meeting briefing whose facts can be traced and whose unknowns become useful questions. Treat company materials as claims to verify, not as independent evidence.

## Select scope

Determine two controls at intake:

- Research depth: `quick`, `standard` (default), or `deep`.
- Deliverable: `note` (default), `note+audio`, or `note+audio+video`.

Apply these default execution budgets unless the user explicitly requests otherwise:

| Depth | Public source target | Search-query ceiling | Note size target | Wall-time ceiling |
|---|---:|---:|---:|---:|
| `quick` | 4-8 | 8 | 1,500-3,000 Chinese characters | 5 minutes |
| `standard` | 10-18 | 20 | 5,000-9,000 Chinese characters | 12 minutes |
| `deep` | 20-35 | 40 | 10,000-18,000 Chinese characters | 30 minutes |

Treat ceilings as hard stop conditions for autonomous runs. When the ceiling is reached, finish with clearly labeled gaps instead of continuing low-yield searches. If usage data is available, target no more than roughly 25k, 60k, and 120k total model tokens for quick, standard, and deep modes respectively.

If the request names only an ambiguous company, ask for one discriminator such as location, website, legal entity, founder, or business description before researching. If the company is identifiable, proceed and state assumptions. Ask for the meeting person and meeting date when they will materially improve the output; do not block on them.

Confirm the target company before processing a newly attached teaser or BP when the identity is not explicit. Never expose confidential material beyond the user-authorized destination.

## Execute the workflow

1. In file-backed or automated runs, execute the preflight in [automation-contract.md](references/automation-contract.md). Stop before any public research if required inputs cannot be read or outputs cannot be written.
2. Inspect every supplied file and extract company claims, metrics, dates, customers, team members, financing, legal entities, and contradictions. Preserve page or slide references. If a supplied file cannot be read, stop and report the exact file failure; never continue as if it had been reviewed.
3. Resolve the company identity and related entities before broad searching. Distinguish brand, legal entity, subsidiaries, founder vehicles, and similarly named companies.
4. Build a bounded research plan from [research-method.md](references/research-method.md). Browse current public sources whenever browsing is available; record the research cutoff date.
5. Classify the business and load only the relevant parts of [sector-lenses.md](references/sector-lenses.md). Use sector metrics to sharpen the research, not to force irrelevant sections.
6. Maintain an evidence ledger while researching. Label material facts as `verified fact`, `company claim`, `third-party report`, `inference`, or `unknown`. Grade sources A-D using the research method. In file-backed runs, save the ledger before drafting the Note.
7. Reconcile inconsistencies across the BP, official records, company statements, and third-party reporting. Prefer the latest primary source, but preserve meaningful historical changes.
8. Form an investment view. Separate market attractiveness, company quality, evidence quality, and current investability. Do not convert missing data into a negative fact.
9. Draft the note using [note-structure.md](references/note-structure.md). Lead with the decision and the questions that can change it.
10. Run the checks in [quality-gates.md](references/quality-gates.md). For a Markdown deliverable, run `scripts/validate_note.py --profile <depth>`; fix structural failures before delivery.
11. If requested, derive audio or video strictly from the final note by following [media-outputs.md](references/media-outputs.md). The note remains the source of truth.

## Research behavior

- Prioritize primary sources: regulators and government, company filings and announcements, official websites, patents and standards, court records, procurement records, investor portfolio pages, and first-party talks.
- Use reputable media and industry bodies to triangulate. Treat commercial databases, aggregators, reposts, and anonymous social content as leads unless independently verified.
- Search in Chinese and English when the company, founder, technology, customers, or market has cross-border relevance.
- Stop searching a narrow claim after two materially different queries return no reliable evidence. Record the gap and turn it into a question.
- Do not exceed the selected query ceiling. Prioritize identity, product, customers, team, financing, recent events, and disconfirming evidence before background market statistics.
- Cite every decision-relevant number, customer, financing event, title, credential, and recent event close to the claim. Use direct links, document names, dates, and page/slide numbers when available.
- Distinguish contract value from recognized revenue; announced capacity from operating capacity; registered capital from financing; partner logos from paid customers; pilots or MOUs from binding orders; design targets from measured performance.
- For people, distinguish confirmed employment and education from same-name matches. Do not merge identities without corroboration.
- Treat cap-table estimates and market sizing as calculations. Show assumptions and label them as estimates.
- When current information cannot be verified, write `未找到可靠公开披露` and turn the gap into a meeting question or data request.

## Output rules

- Default to Chinese when the user writes Chinese; retain necessary English product and technical terms.
- Default to a structured Markdown note. Create DOCX, PDF, slides, audio, or video only when requested and when the corresponding tools are available.
- Make the executive section skimmable in three minutes. Put detailed evidence and sources later.
- Tailor questions to hypotheses and contradictions. Avoid generic prompts that any founder could answer.
- Include a concise confidentiality and evidence-boundary statement.
- Do not present the note as legal, financial, tax, regulatory, or technical due diligence.

## Degraded modes

If browsing is unavailable, produce a materials-only note and state that public verification remains pending. If speech or video rendering is unavailable, produce a production-ready narration script or storyboard rather than pretending that a media file was created.

If a required preflight fails, do not browse, infer from filenames, or spend the remaining research budget. Return the failure and the minimum corrective action.
