# Audio and video outputs

Create media only after the note passes its quality gates. Do not add new facts during adaptation.

## Audio briefing

Default to an 8-12 minute Chinese briefing unless the user specifies otherwise. Use either one narrator or a two-host discussion. Cover:

1. What the company does and why now
2. Product and business model
3. Industry and competition
4. Team and financing
5. What is verified, what is claimed, and the main risks
6. The five questions to remember before entering the meeting

Write for listening: short sentences, explain acronyms once, round non-critical numbers, and verbally distinguish facts from company claims. Put links and detailed sourcing in the accompanying note, not in spoken narration.

If a speech-synthesis tool is available, render the final approved script and return the audio file. Otherwise return a production-ready script with speaker labels, pauses, pronunciation notes, and estimated duration. Never claim an audio file exists when only a script was produced.

## Video briefing

Default to 5-8 minutes. Produce a scene-by-scene storyboard containing duration, narration, on-screen text, visual source or generation instruction, and citation. Prefer diagrams, timelines, value-chain maps, product flows, competitor maps, and a final meeting-question card.

Use source-backed charts and properly licensed or user-provided images. Label AI-generated technical visuals as schematics; never present them as the company's actual product, facility, customer, or measured result. Keep speculative future states visually distinct.

If all rendering tools are available and the user requested a rendered video, create the visuals, narration, captions, and final video. Otherwise return the storyboard, narration, shot list, and asset manifest needed for production.

## Cost control

- `quick`: 4-6 minute audio; no rendered video, only a six-scene outline.
- `standard`: 8-12 minute audio; 5-8 minute storyboard or rendered video when tools permit.
- `deep`: 12-18 minute audio; expanded technical explainer and appendix scenes.

Tell the user before any high-cost rendering step that requires a paid external API or substantial generation. Research and note creation should not wait on media generation.
