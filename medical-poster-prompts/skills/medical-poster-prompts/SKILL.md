---
name: medical-poster-prompts
description: |
  Use when turning medical articles, patient education copy, public health messages, or science communication content into safe image-generation prompts for posters, infographics, social cards, carousel covers, or health education visuals.

  觸發時機：
  (1) 使用者提供醫學文章、衛教內容、科普素材，希望轉成「生圖 AI 可用的海報提示詞」
  (2) 需要產生醫學衛教海報、科普海報、健康資訊圖表、社群衛教圖卡、疾病機轉解釋圖
  (3) 需要同時顧及醫學準確性、法規風險、版權、可讀性、alt text、發布前檢查

  觸發詞：醫學衛教海報、科普海報、衛教圖卡、醫療海報提示詞、生圖 prompt、健康資訊圖表、
  疾病科普圖、衛教圖片生成、醫學資訊圖、醫療內容生圖、AI 海報提示詞、health education poster prompt
---

# Medical Poster Prompts

## Overview

Create source-aware, medically cautious prompts for image-generation AI. The output must help the user generate a poster image while preserving medical accuracy, clear risk boundaries, readable layout, and publication hygiene.

Use Traditional Chinese by default unless the user asks otherwise. If platform, audience, or dimensions are missing, assume a Taiwan-facing public health post, 4:5 vertical social poster, 1080 x 1350.

## Minimal Interaction Rule

Ask at most **one** lightweight style question before producing the poster prompt. Do not run a long intake interview.

If the user provides content but no style preference, ask this only when a pause is acceptable:

> 你有偏好的風格嗎？可直接回：臨床格線、友善插畫、急症警示、機轉爆炸圖、迷思破解、照護路線圖、微型世界。若沒有，我會自動選最適合的。

If the user says "直接做", seems rushed, or already supplied enough context, do not wait. Auto-select one recommended style and include 1 to 2 alternatives in the output.

## Workflow

1. Read the user's article or notes and extract:
   - One main message
   - Target audience
   - 3 to 5 key points
   - Required warnings, limitations, or "when to seek care"
   - Source names, dates, and evidence caveats if provided
2. Capture or infer style preference:
   - Use the user's requested style if it does not weaken medical safety or readability.
   - If no style is provided, choose a recommended style from `Style Selection`.
   - If two styles could work, present the recommended style plus alternatives without asking more questions.
3. Classify the content risk:
   - **Low:** general prevention, screening reminders, symptom awareness
   - **Medium:** disease management, medication concepts, test interpretation
   - **High:** drug/device/treatment claims, food/supplement benefits, clinic/service promotion, before-after claims, urgent symptoms, specific dosing
4. If risk is medium or high, add a short caution note before the prompt. Do not generate promotional medical claims, cure guarantees, diagnosis instructions, individualized dosing, or unsupported efficacy claims.
5. Convert the content into a prompt with:
   - Structured fields, inspired by image prompt libraries: `type`, `subject`, `style`, `layout`, `exact_text`, `visuals`, `safety_constraints`, `negative_prompt`
   - Explicit callout labels and text blocks
   - Clear format, aspect ratio, and mobile readability requirements
   - A footer/source area without inventing logos, citations, QR codes, institutional seals, or author names
6. Include post-generation checks:
   - Verify all text, numbers, anatomy, labels, and charts
   - Remove misleading medical imagery
   - Add alt text and caption outside the image

## Output Format

Return these sections:

````markdown
**內容轉譯**
- 主訊息：
- 受眾：
- 風險等級：
- 必留資訊：

**風格選擇**
- 推薦風格：
- 理由：
- 可替代風格：

**給生圖 AI 的提示詞**
```json
{
  "type": "medical education poster",
  "language": "Traditional Chinese",
  "format": {
    "platform": "Instagram / LINE / web",
    "aspect_ratio": "4:5 vertical",
    "size": "1080x1350"
  },
  "subject": "...",
  "audience": "...",
  "style_source": "selected from medical-poster-prompts style routing; adapted from structured infographic patterns, not copied from any source prompt",
  "style": "...",
  "layout": {
    "hierarchy": "...",
    "sections": [],
    "footer": "..."
  },
  "exact_text": {
    "title": "...",
    "subtitle": "...",
    "callouts": [],
    "disclaimer": "..."
  },
  "visuals": {
    "main_illustration": "...",
    "supporting_icons": [],
    "color_palette": "...",
    "typography": "large, legible, no tiny body text"
  },
  "safety_constraints": [
    "educational tone, not diagnosis or treatment instruction",
    "show representative or schematic visuals, not shocking pathology",
    "do not invent statistics, citations, logos, QR codes, drug names, or endorsements"
  ],
  "negative_prompt": [
    "miracle cure claims",
    "before-after transformation",
    "fake medical license badges",
    "illegible small text",
    "incorrect anatomy",
    "sensational fear imagery"
  ]
}
```

**發布前檢查**
- 圖中文字是否完全正確：
- 數據/來源是否可追溯：
- 是否有誇大療效或廣告語：
- 是否需要專業審稿：

**Alt text / 貼文文字**
- Alt text：
- 貼文摘要：
````

If the user asks only for the prompt, still include a short "發布前檢查" unless they explicitly ask for prompt-only output.

## Prompt Rules

- Use **one main message**. Put secondary details in callouts, not the title.
- Keep on-image text short: title under 18 Chinese characters, 3 to 5 callouts, each under 16 Chinese characters when possible.
- Avoid dense citations inside the image. Put "資料來源：..." in a small footer only when supplied; provide full citations in the caption.
- Use exact numbers only when present in the source. Otherwise say "避免填入未提供數字".
- Prefer absolute risk or natural frequencies when the article provides them.
- Include "何時就醫" for symptom, medication, infection, chronic disease, pregnancy, child, older adult, or emergency topics.
- For medication, supplement, food, device, procedure, clinic, or brand content, remove sales language and add a conservative compliance warning.
- For AI-generated visuals, specify "示意圖" when showing anatomy, symptoms, disease mechanisms, procedures, or patient scenes.
- Do not ask the image model to imitate a living artist, copy an institution's brand, or use protected logos unless the user supplied rights.

## Style Selection

Pick one style based on the content and audience:

- **Clinical grid:** hospital, screening, vaccination, chronic disease, adult audience. Borrow the structure of clean product infographics: clear feature blocks, thin annotation lines, restrained color.
- **Friendly illustrated:** prevention, family health, children, everyday behavior. Borrow the warmth of hand-drawn map prompts, but keep health instructions short and not decorative.
- **Emergency high-contrast:** urgent symptoms, triage, safety warnings. Use the fewest words, strong action bar, and no ornamental illustration.
- **Mechanism exploded view:** anatomy, physiology, pathophysiology, lab concepts. Borrow exploded-product callout structure, but use schematic medical visuals and conservative labels.
- **Minimal myth-vs-fact:** misinformation correction, science communication, social sharing. Use two-column comparison and sparse typography.
- **Care pathway map:** stepwise care, screening pathway, patient journey, home-care decision flow. Borrow map/route prompt structure with numbered stations and a legend.
- **Isometric micro-world:** environment-based prevention, clinic workflow, household safety, school/community health. Borrow isometric cross-section prompt structure, but reduce detail enough for mobile readability.

Read `references/style-examples.md` when the user asks for examples, styles, reusable formats, or when auto-selecting among multiple plausible styles.

When borrowing inspiration from YouMind/OpenLab prompt libraries, adapt only the **pattern**: structured JSON, replaceable arguments, explicit layout sections, labels, grid, map, callouts, or cross-section. Do not copy community prompt text verbatim into user output.

## Safety Anchors

Use these principles without overloading the final answer:

- CDC Clear Communication Index: one main message, actionability, visuals that support understanding.
- NIH Clear & Simple: familiar words, logical sequence, limited concepts, uncluttered visuals.
- FDA/FTC advertising principles: health claims must be truthful, non-misleading, scientifically supported, and balanced with risks where relevant.
- W3C/WAI and HHS accessibility: text alternatives, sufficient contrast, captions/alt text, short accessible filenames for published assets.
- Taiwan MOHW/TFDA caution: medical institutions and food/supplement content can trigger medical or food advertising rules; avoid unapproved medical efficacy claims.

For official source links and when to consult them, read `references/safety-sources.md` when the task involves medical advertising, food/supplement claims, accessibility, or source-quality questions.

## Self-Learning Loop

This skill is subjective and benefits from iterative learning. When repeated outputs have weak visual hierarchy, unsafe claims, poor mobile readability, or mismatched style selection, record the case and promote stable rules back into the skill.

- Use `references/self-learning-loop.md` to log failures, hypotheses, experiments, and promotion rules.
- Use `references/autoresearch-eval-seeds.md` for regression prompts and binary checks before changing the skill.
- Promote only rules that pass at least two distinct poster topics and do not weaken medical safety.
