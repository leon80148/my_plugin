# Safety Sources

Consult these official or primary sources when medical accuracy, advertising risk, accessibility, or publication hygiene affects the poster prompt.

## Prompt Pattern Reference

- YouMind-OpenLab `awesome-gpt-image-2`: use its structured prompt patterns as inspiration, especially explicit `type`, `subject`, `style`, `layout`, labels, footer, and replaceable parameters. Do not copy community prompts verbatim unless the user requests attribution-safe adaptation.
  - https://github.com/YouMind-OpenLab/awesome-gpt-image-2
- YouMind commit history: check this when the user explicitly wants current examples or "latest" style inspiration.
  - https://github.com/YouMind-OpenLab/awesome-gpt-image-2/commits/main/

Observed useful pattern families from the library:

- Product exploded-view posters: strong for mechanism explainers and anatomy callouts.
- Hand-drawn map infographics: strong for patient journeys and daily habit routes.
- Dense explanatory slides: useful only for professional audiences; simplify for public posters.
- Clean commercial product infographics: useful for polished clinical grids, but remove sales framing.
- Isometric micro-world cross-sections: useful for environmental health, clinic flow, household safety, and community prevention.
- Reference-sheet grids: useful for step sequences, rehab movements, inhaler technique, or exercise demonstrations when reviewed.
- UI overlay mockups: useful for LINE/app/patient portal workflows, not disease facts.

When adapting these patterns, keep the medical poster's one-message rule above visual novelty. A trendy style is rejected if it creates crowded text, fake authority, or weaker risk boundaries.

## Health Communication

- CDC Clear Communication Index: one main message, actionability, audience understanding, and visuals that support the message.
  - https://www.cdc.gov/ccindex/
- NIH Clear & Simple: plain words, limited concepts, logical sequence, uncluttered visuals, helpful captions.
  - https://www.nih.gov/institutes-nih/nih-office-director/office-communications-public-liaison/clear-communication/clear-simple

Use these sources when the issue is not whether a statement is medically true, but whether the public will understand the poster:

- Is there exactly one main message?
- Is the next action visible without reading a caption?
- Are headings close to the text they explain?
- Are visuals directly related to the message?
- Are unfamiliar terms defined or replaced with everyday words?
- Does the poster avoid unnecessary concepts?

## Advertising and Claims

- FTC Health Products Compliance Guidance: health-related advertising claims must be truthful, not misleading, and backed by competent scientific evidence.
  - https://www.ftc.gov/business-guidance/resources/health-products-compliance-guidance
- FDA Basics of Drug Ads: prescription drug benefit claims require balanced risk presentation.
  - https://www.fda.gov/drugs/prescription-drug-advertising/basics-drug-ads
- Taiwan MOHW social media medical advertising note: medical institution social media content must follow medical advertising rules.
  - https://www.mohw.gov.tw/cp-2704-21236-1.html
- Taiwan TFDA food labeling and advertising: food labeling, promotion, and advertising must not be false, exaggerated, misleading, or claim medical efficacy.
  - https://www.fda.gov.tw/TC/siteContent.aspx?sid=12345

Use these sources when the poster mentions:

- A drug, medical device, supplement, food product, procedure, clinic, brand, price, discount, appointment, or before-after result
- Any phrase like "cure", "reverse", "guarantee", "no side effects", "best", "clinically proven", or "doctor recommended"
- A benefit claim that may imply treatment, prevention, diagnosis, or mitigation of disease
- A product-like recommendation where the user may spend money or delay care

If in doubt, frame the prompt as neutral education, remove sales language, and keep full source review outside the image.

## Accessibility and Web Publishing

- W3C WCAG 2.2: provide text alternatives for non-text content and use current accessibility guidance.
  - https://www.w3.org/TR/WCAG22/
- W3C WAI complex images: complex charts and infographics need short alt text plus longer descriptions when needed.
  - https://www.w3.org/WAI/tutorials/images/complex/
- HHS Web Style Guide: plain language, image accessibility, captions, alt text, and short lowercase hyphenated filenames.
  - https://www.hhs.gov/web/policies-and-standards/web-style-guide/index.html

Use these sources when preparing the generated image for upload:

- Add alt text that summarizes the health message, not only the visual style.
- Add a longer caption if the image contains charts, steps, or risk categories.
- Keep color contrast high enough for phone screens.
- Avoid conveying warnings by color alone.
- Use short lowercase filenames with hyphens.
- Do not hide essential medical instructions only inside the image.

## Practical Source Review Order

1. Check medical claim support from the user's article or supplied citations.
2. Check whether the poster accidentally becomes advertising.
3. Check whether the visual prompt could generate misleading anatomy, fake credentials, or unsupported statistics.
4. Check whether a phone user can read the title, callouts, and action.
5. Check whether alt text and caption preserve the same health message.
