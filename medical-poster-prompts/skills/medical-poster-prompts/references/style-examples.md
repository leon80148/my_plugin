# Style Examples

Use these examples as reusable formats. Replace the medical content, sources, and callouts with the user's article-derived facts.

## Fast Style Intake

Use this one-line style intake when a user gives content but no visual direction:

> 你有偏好的風格嗎？可直接回：臨床格線、友善插畫、急症警示、機轉爆炸圖、迷思破解、照護路線圖、微型世界。若沒有，我會自動選最適合的。

Do not ask follow-up questions unless a missing fact would create a medical safety problem.

## Auto-Routing Table

| User content | Recommended style | Alternate styles |
|---|---|---|
| Screening, vaccination, chronic disease reminders | Clinical grid | Minimal myth-vs-fact, care pathway map |
| Family prevention, school health, home care | Friendly illustrated | Care pathway map, isometric micro-world |
| Red flags, emergency symptoms, triage | Emergency high-contrast | Clinical grid |
| Anatomy, lab values, disease mechanisms | Mechanism exploded view | Clinical grid, isometric micro-world |
| Misinformation, supplement myths, "true or false" topics | Minimal myth-vs-fact | Clinical grid |
| Step-by-step care, patient journey, referral flow | Care pathway map | Clinical grid |
| Community environment, clinic workflow, household safety | Isometric micro-world | Friendly illustrated |

## YouMind-Inspired Patterns To Adapt

These are pattern inspirations from the YouMind/OpenLab prompt library, not text to copy:

- **Structured product callout poster:** Use for mechanism or anatomy explainers. Convert product parts into schematic medical components, and keep labels conservative.
- **Hand-drawn map infographic:** Use for care pathways, screening journeys, or daily habit routes. Replace decorative destinations with numbered health actions.
- **Dense explanatory slide / ponchi-e:** Use only for professional audiences. Reduce density for public-facing posters.
- **Clean product infographic:** Use for clinical grid layouts. Keep annotation lines, feature blocks, and polished spacing; remove sales tone.
- **Isometric micro-world cross-section:** Use for household, school, clinic, or community health environments. Keep the scene explorable but not crowded.
- **Reference-sheet grid:** Use for exercise, rehab, inhaler technique, or step sequences only when each panel is medically reviewed.
- **UI overlay / app mockup:** Use for LINE, app, appointment, or patient portal workflows, not for general disease education.

## 1. Clinical Grid

Best for hospital-style screening, vaccination, chronic disease management, preventive care, and professional public health posts.

```json
{
  "type": "medical education poster",
  "language": "Traditional Chinese",
  "format": {
    "platform": "Instagram / LINE / clinic website",
    "aspect_ratio": "4:5 vertical",
    "size": "1080x1350"
  },
  "subject": "居家量血壓的正確步驟",
  "audience": "高血壓患者、照顧者、一般成人",
  "inspiration_pattern": "clean product infographic with restrained annotation lines, adapted for non-promotional clinical education",
  "style": "clean clinical grid, calm hospital education design, white background, teal and navy accents, precise line icons, generous spacing, no decorative clutter",
  "layout": {
    "hierarchy": "top title, center four-step grid, bottom reminder strip",
    "sections": [
      {
        "position": "top",
        "content": "large title and short subtitle"
      },
      {
        "position": "center",
        "content": "2x2 grid with numbered clinical icons: chair, arm cuff, clock, notebook"
      },
      {
        "position": "bottom",
        "content": "when-to-seek-care reminder and source/date footer"
      }
    ],
    "footer": "small but legible footer: 資料來源：請填入來源｜更新日期：請填入日期"
  },
  "exact_text": {
    "title": "居家量血壓 4 步驟",
    "subtitle": "同一時間、同一手臂，記錄趨勢更重要",
    "callouts": [
      "先休息 5 分鐘",
      "手臂與心臟同高",
      "袖帶貼合上臂",
      "記下日期與數值"
    ],
    "disclaimer": "數值異常或不舒服，請諮詢醫療專業"
  },
  "visuals": {
    "main_illustration": "flat vector illustration of an adult sitting calmly at a table measuring blood pressure, schematic and non-identifiable",
    "supporting_icons": [
      "simple chair icon",
      "blood pressure cuff icon",
      "clock icon",
      "record sheet icon"
    ],
    "color_palette": "white, teal #0F766E, navy #1E3A5F, light gray #E5E7EB",
    "typography": "large readable Traditional Chinese sans-serif, no tiny text, strong contrast"
  },
  "safety_constraints": [
    "education only, not diagnosis",
    "do not show a specific treatment plan or medication dose",
    "do not invent exact blood pressure thresholds unless supplied by the source",
    "show patient as non-identifiable"
  ],
  "negative_prompt": [
    "sales language",
    "guaranteed control claims",
    "fake hospital logo",
    "illegible chart",
    "fear-based imagery"
  ]
}
```

## 2. Friendly Illustrated

Best for prevention behaviors, family health, child/parent education, school and community health.

```json
{
  "type": "friendly public health poster",
  "language": "Traditional Chinese",
  "format": {
    "platform": "school newsletter / LINE share card / web",
    "aspect_ratio": "4:5 vertical",
    "size": "1080x1350"
  },
  "subject": "流感季節的日常預防",
  "audience": "家庭、家長、學生、一般社區民眾",
  "inspiration_pattern": "hand-drawn map warmth simplified into a friendly action poster, without decorative clutter",
  "style": "warm editorial illustration, soft daylight, rounded human figures, clear icon labels, optimistic but not childish, cream-white background with coral, green, and blue accents",
  "layout": {
    "hierarchy": "large friendly title, central family scene, three action cards, bottom care reminder",
    "sections": [
      {
        "position": "top",
        "content": "title and one-line value message"
      },
      {
        "position": "middle",
        "content": "simple family-at-home scene with visual separation from text"
      },
      {
        "position": "lower middle",
        "content": "three icon cards for vaccine, hand hygiene, staying home when sick"
      },
      {
        "position": "bottom",
        "content": "seek-care reminder and source/date footer"
      }
    ],
    "footer": "資料來源：請填入來源｜更新日期：請填入日期"
  },
  "exact_text": {
    "title": "流感季，先做好 3 件事",
    "subtitle": "降低感染與重症風險，從日常開始",
    "callouts": [
      "接種疫苗",
      "勤洗手",
      "有症狀先休息"
    ],
    "disclaimer": "高燒、喘、胸痛或意識改變，請盡快就醫"
  },
  "visuals": {
    "main_illustration": "friendly illustrated household scene with diverse adults and children, no visible brand products, no alarming medical setting",
    "supporting_icons": [
      "vaccine card icon without brand",
      "handwashing icon",
      "rest-at-home icon"
    ],
    "color_palette": "warm white, coral #F97373, green #16A34A, blue #2563EB, charcoal text",
    "typography": "large rounded Traditional Chinese sans-serif, clear hierarchy, no all-caps Latin text"
  },
  "safety_constraints": [
    "do not claim vaccination prevents all infection",
    "avoid implying blame toward infected people",
    "do not include drug names or dosage",
    "keep the tone practical and non-stigmatizing"
  ],
  "negative_prompt": [
    "crowded tiny text",
    "panic tone",
    "product placement",
    "fake official seal",
    "medical misinformation"
  ]
}
```

## 3. Emergency High-Contrast

Best for urgent warning signs, safety triage, crisis cards, and time-sensitive public health messages.

```json
{
  "type": "urgent medical warning poster",
  "language": "Traditional Chinese",
  "format": {
    "platform": "mobile social post / clinic waiting room screen",
    "aspect_ratio": "4:5 vertical",
    "size": "1080x1350"
  },
  "subject": "疑似中風警訊",
  "audience": "一般民眾、照顧者、長者家庭",
  "inspiration_pattern": "poster/flyer structure stripped down to urgent action, not decorative campaign art",
  "style": "high-contrast emergency information design, red and black accents on white, bold typography, large pictograms, clear action focus, serious but not sensational",
  "layout": {
    "hierarchy": "top emergency title, central FAST-style four-panel warning signs, bottom immediate action bar",
    "sections": [
      {
        "position": "top",
        "content": "large title with warning icon"
      },
      {
        "position": "center",
        "content": "four equal panels with simple face, arm, speech, time icons"
      },
      {
        "position": "bottom",
        "content": "large call-to-action bar"
      }
    ],
    "footer": "資料來源：請填入來源｜更新日期：請填入日期"
  },
  "exact_text": {
    "title": "疑似中風，別等",
    "subtitle": "看見警訊，立即求助",
    "callouts": [
      "臉歪",
      "手無力",
      "說話不清",
      "記下時間"
    ],
    "cta": "立即撥打 119",
    "disclaimer": "本圖為警訊提醒，不能取代醫療判斷"
  },
  "visuals": {
    "main_illustration": "four large schematic pictograms, no graphic injury, no distressed close-up face, no hospital brand",
    "supporting_icons": [
      "face asymmetry schematic",
      "arm weakness schematic",
      "speech bubble icon",
      "clock icon"
    ],
    "color_palette": "white, emergency red #DC2626, black #111827, amber #F59E0B",
    "typography": "very large Traditional Chinese sans-serif, thick weight, high contrast, readable from a phone thumbnail"
  },
  "safety_constraints": [
    "do not add extra symptoms not supplied by the source",
    "do not suggest driving oneself to the hospital",
    "do not show blood, surgery, or shock imagery",
    "make the emergency action unmistakable"
  ],
  "negative_prompt": [
    "small body text",
    "ambiguous call to action",
    "gory medical imagery",
    "fake ambulance logo",
    "decorative background that reduces readability"
  ]
}
```

## 4. Mechanism Exploded View

Best for anatomy, physiology, disease mechanisms, lab values, and "why this happens" science communication.

```json
{
  "type": "medical science mechanism explainer poster",
  "language": "Traditional Chinese",
  "format": {
    "platform": "science education post / lecture slide cover / web article image",
    "aspect_ratio": "4:5 vertical",
    "size": "1080x1350"
  },
  "subject": "胰島素阻抗的概念示意",
  "audience": "一般成人、糖尿病前期族群、健康科普讀者",
  "inspiration_pattern": "exploded product callout poster adapted into a schematic medical mechanism diagram",
  "style": "clean 3D medical schematic mixed with flat infographic labels, soft white background, blue and orange contrast, exploded-view callout structure, polished but not photorealistic pathology",
  "layout": {
    "hierarchy": "top concept title, center cell-and-glucose schematic, side callout labels, bottom lifestyle context note",
    "sections": [
      {
        "position": "top",
        "content": "title and short explanation"
      },
      {
        "position": "center",
        "content": "large simplified exploded-view cell membrane with insulin signal, receptor, and glucose particles separated into clearly labeled layers"
      },
      {
        "position": "left and right",
        "content": "three callout labels with arrows"
      },
      {
        "position": "bottom",
        "content": "context note and source/date footer"
      }
    ],
    "footer": "資料來源：請填入來源｜更新日期：請填入日期"
  },
  "exact_text": {
    "title": "什麼是胰島素阻抗？",
    "subtitle": "身體對胰島素反應變差，血糖較不易進入細胞",
    "callouts": [
      "胰島素訊號",
      "葡萄糖",
      "細胞反應下降"
    ],
    "disclaimer": "健康風險需依個人狀況由醫療專業評估"
  },
  "visuals": {
    "main_illustration": "schematic exploded-view 3D cell membrane, insulin as abstract signal icon, glucose as small labeled dots, arrows showing reduced entry, no real patient image",
    "supporting_icons": [
      "abstract hormone signal",
      "glucose particle",
      "cell membrane",
      "downward response arrow"
    ],
    "color_palette": "white, medical blue #2563EB, glucose orange #F97316, slate gray #334155",
    "typography": "modern Traditional Chinese sans-serif, label arrows clean and sparse"
  },
  "safety_constraints": [
    "mark as schematic concept, not diagnostic image",
    "do not include specific lab thresholds unless supplied",
    "do not imply one behavior alone reverses disease",
    "avoid body-shaming or blame language"
  ],
  "negative_prompt": [
    "incorrect organ anatomy",
    "photorealistic diseased tissue",
    "oversimplified cure claims",
    "tiny labels",
    "unlabeled random molecules"
  ]
}
```

## 5. Minimal Myth-vs-Fact

Best for misinformation correction, quick science education, and shareable social cards.

```json
{
  "type": "myth versus fact medical education poster",
  "language": "Traditional Chinese",
  "format": {
    "platform": "Instagram / Threads / LINE share image",
    "aspect_ratio": "4:5 vertical",
    "size": "1080x1350"
  },
  "subject": "感冒與抗生素迷思",
  "audience": "一般民眾、家長、門診衛教讀者",
  "inspiration_pattern": "minimal social card and typographic comparison layout, optimized for quick sharing",
  "style": "minimal editorial poster, two-column myth-versus-fact layout, crisp typography, strong whitespace, muted teal with yellow highlight, clean medical credibility without hospital branding",
  "layout": {
    "hierarchy": "top title, two large comparison columns, bottom decision reminder",
    "sections": [
      {
        "position": "top",
        "content": "title and one-sentence framing"
      },
      {
        "position": "left column",
        "content": "myth card with X icon"
      },
      {
        "position": "right column",
        "content": "fact card with check icon"
      },
      {
        "position": "bottom",
        "content": "consultation reminder and source/date footer"
      }
    ],
    "footer": "資料來源：請填入來源｜更新日期：請填入日期"
  },
  "exact_text": {
    "title": "抗生素不是感冒萬用藥",
    "subtitle": "先分清楚：病毒與細菌不同",
    "myth": "迷思：感冒吃抗生素會快好",
    "fact": "事實：多數感冒由病毒造成，抗生素無效",
    "callouts": [
      "是否需要用藥，請由醫師評估",
      "不要自行停藥或分享藥物"
    ],
    "disclaimer": "症狀嚴重或持續惡化，請就醫"
  },
  "visuals": {
    "main_illustration": "simple split-screen card, left side muted warning symbol, right side clean check symbol, no pill brand, no drug packaging",
    "supporting_icons": [
      "X icon",
      "check icon",
      "doctor consultation icon",
      "medicine safety icon"
    ],
    "color_palette": "warm white, teal #0F766E, yellow #FACC15, charcoal #111827",
    "typography": "bold title, medium body text, mobile-readable Traditional Chinese"
  },
  "safety_constraints": [
    "do not tell users to refuse prescribed antibiotics",
    "do not include specific medication names",
    "avoid implying all respiratory infections are viral",
    "include professional evaluation reminder"
  ],
  "negative_prompt": [
    "pill bottle brand names",
    "blanket medical advice",
    "mocking tone",
    "crowded infographic",
    "fake certification marks"
  ]
}
```
