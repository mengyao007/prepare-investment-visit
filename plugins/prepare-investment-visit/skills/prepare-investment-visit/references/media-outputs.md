# Podcast output

Create audio only after the PDF passes all quality gates. The final note is the source of truth.

## Editorial adaptation

Write a new 5-10 minute single-host professional investment briefing; do not read the note verbatim. Target roughly 1,800-2,800 Chinese characters and cover:

1. What the company does and why the meeting matters.
2. Product, buyer, business model, and proof of adoption.
3. Market and competitive position.
4. The meeting person: verified background, role, and relevant public views.
5. What is verified, what is company claim, and the decisive risks.
6. The five questions to remember before entering the meeting.

Use short spoken sentences, transitions, and one coherent narrative arc. Explain acronyms once, round non-critical numbers, and verbally label claims and inferences. Do not speak URLs, long source lists, tables, disclaimers, or appendix detail. Include a brief statement that the voice is AI-generated.

Save the internal UTF-8 script as plain text without Markdown links.

## Preferred renderer: official speech Skill

When the OpenAI curated speech Skill is installed and OPENAI_API_KEY is configured, invoke it with:

- one single-host job;
- Chinese language input;
- voice cedar unless the user requests another built-in voice;
- MP3 output;
- composed, analytical, neutral tone;
- brisk but clear pacing.

The API key and API billing belong to the user and are separate from the ChatGPT/Codex subscription. Never ask the user to paste a key into chat.

## No-key Windows fallback

When no API key is available, run the bundled offline renderer:

    powershell -ExecutionPolicy Bypass -File scripts/render_audio.ps1
      -InputTextPath outputs/podcast-script.txt
      -OutputPath outputs/company-visit-podcast.wav

This path needs no API key but may sound less natural. It still uses the adapted podcast script, not the full note.

## Verification

- Confirm the audio exists and is non-empty.
- Check duration is 5-10 minutes, or explain a justified exception.
- Spot-check the beginning, meeting-person segment, and final five questions for pronunciation and factual fidelity.
- Confirm the audio introduces no fact absent from the final note.
- If rendering fails, deliver the PDF and podcast script, state the exact failure, and never claim an audio file exists.
