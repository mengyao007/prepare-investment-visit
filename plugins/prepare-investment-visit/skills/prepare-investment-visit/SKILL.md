---
name: prepare-investment-visit
description: Prepare evidence-backed pre-meeting research for private-market and venture-capital company visits. Use when an investor provides a company name, introduction, teaser, BP/pitch deck, website, founder or meeting-person name, or meeting plan and needs a professional PDF briefing, person profile, industry and competitor analysis, business/operating/financial/funding/ownership review, recent developments, red flags, tailored interview questions, a post-meeting data-request list, or an optional 5-10 minute podcast briefing.
---

# Prepare Investment Visit

Produce an investor-grade pre-meeting PDF whose facts are traceable and whose unknowns become useful meeting questions. Treat supplied company materials as claims to verify, not independent proof.

## Run the intake gate

Before any public research, confirm these three items in one concise message:

1. Who will the user meet? Ask for the person's name and role. Accept “待定” or “公司团队” when the user does not know.
2. Are there supplementary materials such as a BP, teaser, one-paragraph introduction, website, data room extract, or prior meeting note? Ask the user to attach or paste them; accept “没有”.
3. Should the final PDF also be adapted into a 5-10 minute single-host podcast audio? Accept “需要” or “不需要”.

If any item is missing, ask once and pause. Do not browse or draft before the answer. If all items are already present, do not ask again. Meeting date and special focus are optional follow-ups only when they materially change the research.

Resolve an ambiguous company with one discriminator such as website, location, legal entity, founder, or product. Never infer the target from an unreadable attachment.

## Select depth

Use standard unless the user chooses another depth.

| Depth | Public sources | Query ceiling | Working-note target |
|---|---:|---:|---:|
| quick | 4-8 | 8 | 1,500-3,000 Chinese characters |
| standard | 10-18 | 20 | 6,000-10,000 Chinese characters |
| deep | 20-35 | 40 | 12,000-20,000 Chinese characters |

Treat query ceilings as hard stops. Finish with labeled gaps rather than low-yield searching.

## Execute the workflow

1. For file-backed runs, perform [automation-contract.md](references/automation-contract.md).
2. Read every supplied file before browsing. Extract claims, metrics, dates, customers, team members, financing, legal entities, and contradictions with page or slide references. Stop and name any unreadable expected file.
3. Resolve the company, relevant legal entities, the meeting person, and same-name risks.
4. Research current public information with [research-method.md](references/research-method.md), record the cutoff date, and load only the relevant [sector-lenses.md](references/sector-lenses.md).
5. Maintain an evidence ledger. Label material statements as verified fact, company claim, third-party report, inference, or unknown, and grade sources A-D.
6. Reconcile supplied materials with public sources. Preserve meaningful contradictions and changes over time.
7. Form an investment view that separates market attractiveness, company quality, evidence quality, and current investability.
8. Draft the working note with [note-structure.md](references/note-structure.md). Lead with the meeting objective, decision view, key risks, and questions that can change the view.
9. Validate the working note, render the final PDF, and inspect the rendered pages using [pdf-output.md](references/pdf-output.md) and [quality-gates.md](references/quality-gates.md). The PDF is the default and required Note deliverable; Markdown is an internal intermediate only.
10. If podcast audio was selected, derive it only from the validated final note using [media-outputs.md](references/media-outputs.md). Do not add new facts during adaptation.

## Research rules

- Prioritize regulators, government records, filings, official documents, patents, standards, courts, procurement records, investor portfolio pages, and first-party talks.
- Use reputable media and industry bodies for triangulation. Treat aggregators, commercial databases, reposts, and anonymous content as leads.
- Search in Chinese and English when cross-border facts matter.
- After two materially different searches fail to verify a narrow claim, write “未找到可靠公开披露”, stop that search, and turn the gap into a question.
- Cite decision-relevant numbers, customers, financing events, roles, credentials, and recent events close to the claim.
- Distinguish contract value from revenue; capacity from output; registered capital from financing; logos from paid customers; pilots from binding orders; and design targets from measured performance.
- For people, corroborate identity, employment, education, and public statements. Do not infer personality, private life, or decision authority without evidence.
- Show assumptions and units for market sizing, cap-table estimates, and other calculations.

## Output rules

- Default to Chinese when the user writes Chinese.
- Deliver a polished PDF with clickable citations, page numbers, research cutoff, inputs used, and evidence boundary.
- Make the first two pages useful in under three minutes; place detailed analysis and sources later.
- Tailor questions to the meeting person, hypotheses, contradictions, and proof requests. Avoid generic founder questions.
- Do not present the output as legal, financial, tax, regulatory, medical, or technical due diligence.

## Degraded modes

If browsing is unavailable, produce a materials-only PDF and state that public verification is pending.

For podcast audio, prefer the official OpenAI speech Skill when installed and when the user has configured their own OPENAI_API_KEY. ChatGPT/Codex subscriptions do not supply this API credential. Without a key, use the bundled Windows offline renderer when available. If neither renderer works, still deliver the PDF and a production-ready podcast script, and report the exact audio failure.

If a required preflight fails, do not browse or pretend the missing input was reviewed. Return the failure and minimum corrective action.
