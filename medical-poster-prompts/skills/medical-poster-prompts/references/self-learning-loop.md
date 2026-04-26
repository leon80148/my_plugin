# Self-Learning Loop

This reference defines how `medical-poster-prompts` improves after real poster prompt work. Use it when a user says the generated image prompt produced a weak poster, when an output failed a medical-safety review, or when the same editing pattern appears across several cases.

## Observe

Record only concrete failures from actual use.

Case log fields:

- Date
- User topic
- Source type: article, guideline, note, transcript, pasted draft, URL summary
- Chosen style: clinical grid, friendly illustrated, emergency high-contrast, mechanism explainer, minimal myth-vs-fact, other
- Output issue
- Image-generation result if available
- Medical safety issue if any
- Publication issue if any
- User correction
- Final accepted pattern

## Common Failure Modes

1. Too much on-image text
   - Symptom: poster becomes unreadable on phone preview.
   - Candidate fix: tighten title to one message and move detail to caption.

2. Missing risk boundary
   - Symptom: prompt sounds like diagnosis, treatment, or guaranteed outcome.
   - Candidate fix: add disclaimer, "when to seek care", and non-promotional phrasing.

3. Style mismatch
   - Symptom: emergency topic looks soft and lifestyle-like, or prevention topic looks alarming.
   - Candidate fix: select style by reader action, not only disease category.

4. Source overclaim
   - Symptom: single study becomes broad recommendation.
   - Candidate fix: add evidence caveat and avoid population-wide certainty.

5. Generated text error
   - Symptom: image model distorts Chinese text or numbers.
   - Candidate fix: reduce exact text, ask for large typography, and instruct user to verify all text after generation.

6. Unsafe patient imagery
   - Symptom: real-looking patient, identifiable face, frightening symptom depiction, or stigmatizing body image.
   - Candidate fix: use schematic or non-identifiable illustration.

7. Weak alt text
   - Symptom: alt text describes decoration but not the health message.
   - Candidate fix: alt text should summarize the poster's main instruction and key warning.

## Hypothesize

Convert a repeated failure into a narrow rule:

- Bad: "make posters better"
- Good: "For any emergency symptom poster, force a bottom CTA bar with the action verb and phone number if supplied."
- Good: "For drug or supplement topics, require a compliance warning and remove all brand, price, discount, and cure framing."
- Good: "If the user supplies more than five claims, choose three for the poster and place the rest in caption text."

## Experiment

Run at least two different topics through the proposed rule:

- One low-risk public health topic
- One medium- or high-risk medical topic

Compare against the current skill using these binary checks:

- Main message is identifiable in five seconds.
- No unsupported medical claim is introduced.
- Poster text can fit on a 1080 x 1350 vertical canvas.
- The chosen style matches reader action and risk.
- Alt text communicates the same health message as the poster.

## Promote

Promote the rule into `SKILL.md` only when:

- It helps at least two different topics.
- It does not make the prompt longer without improving safety or usability.
- It does not create a rigid style that blocks legitimate variation.
- It has a clear counterexample or scope boundary.

Promote detailed style examples into `style-examples.md`.
Promote source or compliance references into `safety-sources.md`.
Promote workflow rules into `SKILL.md`.

## Reject

Do not promote:

- One-off user taste preferences.
- Claims that depend on a single unverified source.
- Visual trends that reduce readability or medical caution.
- Rules that rely on copyrighted brand layouts or protected logos.
- Rules that encourage fear, shame, stigma, or urgency without a medical reason.

## Skill-Auto-Sync Note

After a promoted rule changes this skill, let the repository's sync workflow commit and push, or make a manual commit with a clear scope such as:

```bash
git commit -m "docs(medical-poster-prompts): refine emergency poster rules"
```
