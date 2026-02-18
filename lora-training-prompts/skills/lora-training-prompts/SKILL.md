---
name: lora-training-prompts
description: "Generate AI image/video prompts and training datasets for LoRA fine-tuning. Supports character, style, object, concept, and scene LoRA types across all major models (SD1.5, SDXL, Flux, SD3, Pony, Kolors, Wan Video, HunyuanVideo, CogVideoX). Covers prompt generation, captioning strategy, dataset preparation, and training parameter recommendations. Triggers: 'generate LoRA training prompts', 'create training dataset', 'LoRA captioning', 'training parameters', '產生 LoRA 訓練素材'."
---

# LoRA Training Prompts & Dataset Generator

Generate prompt sets, captioning strategies, and dataset configurations for LoRA fine-tuning across all major generative AI models.

## LoRA Type Selection

Determine the LoRA type before starting. Each type has different dataset requirements and captioning strategies.

| LoRA Type | What It Learns | Dataset Size | Key Captioning Rule |
|-----------|---------------|--------------|---------------------|
| **Character** | A specific person/character's identity | 15-50 images | Do NOT caption fixed identity features |
| **Style** | An artistic style, aesthetic, or look | 30-200 images | Caption content, NOT style attributes |
| **Object** | A specific product, item, or prop | 15-40 images | Do NOT caption the object's fixed features |
| **Concept** | An abstract concept (pose, composition, mood) | 20-100 images | Caption everything except the target concept |
| **Scene** | A specific environment or background type | 20-80 images | Caption foreground subjects, NOT scene features |

### Universal LoRA Captioning Principle

> **In caption = Model learns to differentiate (controllable)**
> **NOT in caption = Model learns to bind (becomes the LoRA's identity)**

This principle applies to ALL LoRA types. Whatever you want the LoRA to "become", leave it out of captions.

## Model & Platform Selection

| Model | Architecture | Prompt Style | Resolution | LoRA Framework |
|-------|-------------|-------------|------------|----------------|
| SD1.5 | UNet | Tag-based | 512×512 | kohya_ss, LoRA |
| SDXL | UNet (dual text encoder) | Tag-based / Hybrid | 1024×1024 | kohya_ss, LoRA/LyCORIS |
| Pony Diffusion | SDXL-based | Tag-based (booru) | 1024×1024 | kohya_ss |
| **Flux** | DiT (Transformer) | **Natural Language** | 512-1024 flex | kohya_ss, ai-toolkit |
| **SD3 / SD3.5** | MMDiT | **Natural Language** | 1024×1024 | kohya_ss, diffusers |
| Kolors | SDXL-based (bilingual) | Tag / NL (ZH+EN) | 1024×1024 | kohya_ss |
| **Wan Video 2.x** | Video DiT | **Natural Language** | 480p-720p | musev, custom |
| **HunyuanVideo** | Video DiT | **Natural Language** | 720p | custom trainers |
| **CogVideoX** | Video DiT | **Natural Language** | 480p-720p | custom trainers |

### Training Parameter Quick Reference

| Model | Learning Rate | Steps (character) | Steps (style) | Rank | Batch Size |
|-------|-------------|-------------------|---------------|------|------------|
| SD1.5 | 1e-4 | 1500-3000 | 3000-6000 | 4-16 | 1-2 |
| SDXL | 1e-4 to 5e-5 | 1500-4000 | 3000-8000 | 8-32 | 1-4 |
| Flux | 1e-4 to 4e-4 | 1000-3000 | 2000-5000 | 16-64 | 1-2 |
| SD3 | 5e-5 to 1e-4 | 1500-3000 | 2000-5000 | 16-32 | 1-2 |
| Pony | 1e-4 | 2000-4000 | 3000-6000 | 8-32 | 1-4 |
| Video models | 1e-5 to 5e-5 | 2000-5000 | 3000-8000 | 16-64 | 1 |

> These are starting points. Monitor loss curves and adjust. Lower LR + more steps = safer. Use cosine scheduler with warmup.

## Dataset Preparation Guidelines

### Image Quality Requirements

| Criterion | Requirement | Tool |
|-----------|-------------|------|
| Resolution | ≥ model's native (e.g., 1024 for SDXL) | Upscale with Real-ESRGAN if needed |
| Artifacts | No JPEG compression artifacts, no watermarks | Manual curation |
| Consistency | All images should represent the target concept clearly | Manual review |
| Variety | Diverse conditions (lighting, angle, background) | See variation elements below |
| Format | PNG preferred, JPEG ≥ 95% quality acceptable | Batch convert |

### Dataset Size Recommendations

| LoRA Type | Minimum | Recommended | Maximum (before diminishing returns) |
|-----------|---------|-------------|--------------------------------------|
| Character | 15 | 25-35 | 50 |
| Style | 30 | 50-100 | 200 |
| Object | 15 | 25-35 | 40 |
| Concept | 20 | 40-60 | 100 |
| Scene | 20 | 40-60 | 80 |
| Video (per clip) | 10 clips | 20-30 clips | 50 clips |

### Regularization / Class Images

For character and object LoRA, use regularization images to prevent language drift:
- **Class prompt**: Generic description (e.g., "a woman", "a handbag")
- **Count**: 1x to 5x the training images
- **Source**: Generate from the base model using the class prompt
- **Skip for style/concept LoRA**: Usually unnecessary

---

## Character LoRA Workflow (Primary Example)

### Step 1: Gather Character Specifications

Ask for these essential details if not provided:

| Attribute | Examples | Required |
|-----------|----------|----------|
| Gender/Age | 25-year-old woman | Yes |
| Ethnicity/Skin | Asian, fair skin | Yes |
| Face shape | Oval, round, angular | Recommended |
| Eye features | Single eyelid, double eyelid, eye color | Recommended |
| Hair | Black shoulder-length, brown ponytail | Yes |
| Style | Natural, sweet, mature, cool | Optional |
| Base model | SD1.5 / SDXL / Flux / SD3 | Yes (affects prompt style & resolution) |

## Step 2: Build Fixed Appearance Anchor

Create a core description that remains constant across all prompts:

```
[age] [ethnicity] [gender], [face_shape] face, [eye_features], 
[hair_description], [skin_tone], [style_keywords]
```

**Example:**
```
25 year old asian woman, oval face, single eyelid, brown eyes,
shoulder length black straight hair, fair skin, natural makeup
```

## Step 3: Generate Prompt Variations

### Required Distribution (25-30 images recommended)

| Category | Count | Purpose |
|----------|-------|---------|
| Front face closeup | 8-10 | Core facial features |
| 3/4 angle | 6-8 | Dimensional understanding |
| Side profile | 3-4 | Silhouette learning |
| Upper body | 4-5 | Body proportion |
| Full body | 2-3 | Overall figure |

### Variation Elements

**Angles (vary across set):**
- `front view`, `looking at viewer`, `facing camera`
- `three quarter view`, `slight angle`, `turned slightly`
- `side profile`, `looking away`, `looking to the side`
- `from below`, `from above`, `dutch angle`
- `head tilted`, `chin up`, `chin down`, `looking over shoulder`

**Expressions (CRITICAL - use wide variety to prevent overfitting):**

Basic:
- `neutral expression`, `gentle smile`, `slight smile`
- `serious expression`, `soft expression`

Dynamic/Emotional:
- `laughing`, `giggling`, `chuckling`, `big smile showing teeth`
- `surprised expression`, `eyes wide open`, `raised eyebrows`
- `winking`, `one eye closed`, `playful wink`
- `pouting`, `puffed cheeks`, `pursed lips`
- `smirking`, `sly smile`, `mischievous grin`
- `yawning`, `sleepy expression`, `tired look`
- `crying`, `teary eyes`, `emotional expression`
- `angry expression`, `frowning`, `annoyed look`
- `shy expression`, `embarrassed`, `blushing`
- `excited expression`, `happy`, `joyful`
- `confused expression`, `puzzled look`, `questioning look`
- `focused expression`, `concentrated`, `determined look`

Subtle variations:
- `lips slightly parted`, `mouth open slightly`
- `biting lip`, `tongue out`, `licking lips`
- `eyes closed`, `closed eyes smile`, `squinting`
- `looking up`, `looking down`, `side glance`, `eyes looking away`

**Head/Face Actions:**
- `tilting head`, `head tilt to side`
- `resting chin on hand`, `hand on cheek`
- `touching face`, `hand near face`
- `brushing hair`, `tucking hair behind ear`
- `covering mouth`, `hand over mouth laughing`

**Body Poses & Gestures:**
- `arms crossed`, `hands on hips`, `hand on hip`
- `arms raised`, `stretching`, `arms behind head`
- `peace sign`, `victory sign`, `waving hand`
- `thumbs up`, `pointing`, `finger to lips (shh gesture)`
- `hands clasped`, `praying hands`, `hands together`
- `leaning forward`, `leaning back`, `slouching`
- `sitting`, `sitting cross-legged`, `kneeling`
- `walking`, `running`, `jumping`
- `dancing`, `spinning`, `twirling`
- `lying down`, `reclining`, `on stomach`

**Interactions with Objects:**
- `holding phone`, `looking at phone`, `taking selfie`
- `holding cup`, `drinking coffee`, `holding mug`
- `holding book`, `reading`, `studying`
- `holding flowers`, `smelling flower`
- `holding umbrella`, `holding bag`
- `eating`, `holding food`, `biting into food`
- `wearing headphones`, `adjusting earbuds`
- `holding pen`, `writing`, `drawing`
- `applying makeup`, `holding lipstick`, `looking in mirror`

**Lighting (mix throughout):**
- `natural lighting`, `soft light`, `diffused lighting`
- `studio lighting`, `golden hour`, `sunset lighting`
- `indoor lighting`, `window light`, `backlight`
- `rim lighting`, `dramatic lighting`, `high contrast`
- `neon lighting`, `colorful lighting`, `warm lighting`, `cool lighting`
- `dappled light`, `light through leaves`, `shadows on face`
- `low key lighting`, `high key lighting`
- `candlelight`, `lamp light`, `screen glow`

**Backgrounds (IMPORTANT: mix to prevent background-character binding):**

Recommended ratio: 60-70% simple + 30-40% contextual

Simple (use for majority):
- `simple background`, `white background`, `gray background`
- `blurred background`, `bokeh`, `plain studio`
- `solid color background`, `gradient background`

Contextual (use for variety, prevents overfitting):
- `outdoor`, `park background`, `garden`, `forest`
- `urban background`, `city street`, `alley`
- `beach`, `ocean background`, `seaside`
- `cafe interior`, `restaurant`, `coffee shop`
- `bedroom`, `living room`, `kitchen`
- `office`, `library`, `classroom`
- `rooftop`, `balcony`, `window view`
- `night city`, `evening sky`, `sunset background`

**Clothing (CRITICAL: must vary every image to prevent clothing-character binding):**

Rule: No two images should have identical clothing. Aim for 8-10+ different outfits in a 30-image set.

Casual:
- `white t-shirt`, `black t-shirt`, `graphic tee`
- `hoodie`, `sweatshirt`, `oversized sweater`
- `tank top`, `crop top`, `off-shoulder top`
- `jeans`, `shorts`, `sweatpants`

Formal/Semi-formal:
- `white blouse`, `button-up shirt`, `dress shirt`
- `blazer`, `suit jacket`, `cardigan`
- `formal dress`, `cocktail dress`, `evening gown`

Seasonal/Weather:
- `summer dress`, `sundress`, `floral dress`
- `winter coat`, `puffer jacket`, `leather jacket`
- `scarf`, `beanie`, `hat`, `cap`
- `raincoat`, `holding umbrella`

Special:
- `school uniform`, `sailor uniform`
- `sportswear`, `gym clothes`, `yoga outfit`
- `swimsuit`, `bikini`
- `pajamas`, `sleepwear`, `bathrobe`
- `traditional clothing`, `hanbok`, `kimono`, `cheongsam`

Color variety reminder: Mix light/dark, warm/cool colors across outfits.

**Accessories (add variety):**
- `glasses`, `sunglasses`, `reading glasses`
- `earrings`, `necklace`, `bracelet`, `watch`
- `hair accessories`, `hairpin`, `hair ribbon`, `scrunchie`
- `backpack`, `handbag`, `shoulder bag`

## Step 4: Output Format

### Standard Prompt Template

```
[APPEARANCE_ANCHOR], [angle], [expression], [clothing], [background], [lighting], [quality_tags]
```

### Quality Tags (append to all)

**For SD1.5:**
```
masterpiece, best quality, highly detailed, sharp focus, 8k
```

**For SDXL:**
```
masterpiece, best quality, highly detailed, professional photography, sharp focus
```

### Negative Prompt (provide once)

```
bad anatomy, bad hands, missing fingers, extra fingers, deformed face, 
ugly, blurry, low quality, watermark, text, signature, duplicate, 
mutation, worst quality, low resolution
```

## Output Examples

**Front closeup - basic:**
```
25 year old asian woman, oval face, single eyelid, brown eyes, shoulder length black straight hair, fair skin, natural makeup, front view, looking at viewer, gentle smile, white blouse, simple white background, soft natural lighting, masterpiece, best quality, highly detailed, sharp focus
```

**Front closeup - dynamic expression:**
```
25 year old asian woman, oval face, single eyelid, brown eyes, shoulder length black straight hair, fair skin, natural makeup, front view, laughing, eyes closed, big smile showing teeth, casual hoodie, blurred cafe background, warm indoor lighting, masterpiece, best quality, highly detailed, sharp focus
```

**3/4 angle - with gesture:**
```
25 year old asian woman, oval face, single eyelid, brown eyes, shoulder length black straight hair, fair skin, natural makeup, three quarter view, winking, peace sign, playful expression, graphic tee, park background bokeh, golden hour lighting, masterpiece, best quality, highly detailed, sharp focus
```

**Side profile - interaction:**
```
25 year old asian woman, oval face, single eyelid, brown eyes, shoulder length black straight hair, fair skin, natural makeup, side profile, holding coffee cup, drinking, relaxed expression, oversized sweater, coffee shop interior, warm window light, masterpiece, best quality, highly detailed, sharp focus
```

**Upper body - dynamic pose:**
```
25 year old asian woman, oval face, single eyelid, brown eyes, shoulder length black straight hair, fair skin, natural makeup, upper body, stretching, arms raised, yawning, sleepy expression, pajamas, bedroom background, soft morning light, masterpiece, best quality, highly detailed, sharp focus
```

**Full body - action:**
```
25 year old asian woman, oval face, single eyelid, brown eyes, shoulder length black straight hair, fair skin, natural makeup, full body, walking pose, looking over shoulder, confident smile, leather jacket and jeans, urban street background, evening golden hour, masterpiece, best quality, highly detailed, sharp focus
```

**With accessories:**
```
25 year old asian woman, oval face, single eyelid, brown eyes, shoulder length black straight hair, fair skin, natural makeup, three quarter view, wearing glasses, reading book, focused expression, cozy cardigan, library background blurred, soft indoor lighting, masterpiece, best quality, highly detailed, sharp focus
```

**Emotional range:**
```
25 year old asian woman, oval face, single eyelid, brown eyes, shoulder length black straight hair, fair skin, natural makeup, front view, surprised expression, eyes wide, raised eyebrows, mouth open, casual top, simple background, bright even lighting, masterpiece, best quality, highly detailed, sharp focus
```

---

## Style LoRA Workflow

### Step 1: Define Target Style

| Attribute | Examples | Required |
|-----------|----------|----------|
| Style name / trigger word | `mystyle`, `watercolor_wash` | Yes |
| Visual characteristics | Muted colors, thick outlines, cel shading | Yes |
| Reference artists/works | "Like Studio Ghibli backgrounds" | Recommended |
| Base model | SDXL / Flux / SD3 | Yes |

### Step 2: Dataset Curation

- Collect 50-100 images that exemplify the target style
- **Subject diversity is critical**: Include various subjects (people, landscapes, objects, animals)
- If all images show the same subject, the model will learn the subject, not the style
- Include different compositions, lighting conditions, color palettes within the style

### Step 3: Captioning for Style

> Caption the CONTENT of each image, NOT the style. The style is what gets "baked in" as the LoRA identity.

```
# ✅ Correct (describes content only):
mystyle, a cat sitting on a windowsill, afternoon sunlight, indoor

# ❌ Wrong (describes style features):
mystyle, watercolor painting, muted colors, soft edges, a cat on windowsill
```

### Step 4: Recommended Distribution

| Content Category | Percentage | Purpose |
|-----------------|-----------|---------|
| Portraits / Characters | 25-30% | Ensure style works on people |
| Landscapes / Scenes | 25-30% | Outdoor/indoor environment coverage |
| Objects / Still life | 15-20% | Small-scale detail rendering |
| Animals | 10-15% | Organic form coverage |
| Abstract / Other | 5-10% | Edge case coverage |

---

## Object / Product LoRA Workflow

### Step 1: Define Target Object

| Attribute | Examples | Required |
|-----------|----------|----------|
| Object name / trigger word | `myproduct`, `xphone_pro` | Yes |
| Key features | Silver body, round logo, glass back | Yes |
| Scale / proportion | Handheld, furniture-sized | Recommended |
| Base model | SDXL / Flux | Yes |

### Step 2: Photography Guidelines

- Shoot on diverse backgrounds (white, colored, contextual)
- Vary angles: front, back, side, 45°, top-down, detail closeup
- Vary lighting: studio, natural, dramatic
- Include scale references (hand holding, on desk, in use)
- 25-35 images recommended

### Step 3: Captioning for Object

> Caption the CONTEXT (background, lighting, angle), NOT the object's appearance.

```
# ✅ Correct:
myproduct, on wooden desk, soft natural lighting, three quarter view

# ❌ Wrong:
myproduct, silver metallic body, round logo, glass back panel, on desk
```

---

## Concept / Abstract LoRA Workflow

### Examples of Concept LoRA

- **Pose LoRA**: Specific body pose (e.g., "JoJo pose", "ballet position")
- **Composition LoRA**: Specific framing (e.g., "rule of thirds", "Dutch angle")
- **Effect LoRA**: Visual effect (e.g., "motion blur", "double exposure")
- **Mood LoRA**: Atmosphere (e.g., "cozy", "cyberpunk", "nostalgic")

### Captioning Strategy

Caption everything EXCEPT the target concept:

```
# For a "double exposure" concept LoRA:
# ✅ Correct (describes the subjects, not the effect):
dblexp, portrait of a woman, city skyline, warm tones

# ❌ Wrong:
dblexp, double exposure effect, overlay of woman and city, transparent blending
```

---

## Video LoRA Workflow

### Supported Video Models

| Model | Frame Count | Resolution | Prompt Style |
|-------|------------|-----------|-------------|
| Wan Video 2.1 | 16-81 frames | 480p-720p | Natural language, scene description |
| HunyuanVideo | 16-49 frames | 720p | Natural language |
| CogVideoX | 16-49 frames | 480p-720p | Natural language, action-focused |

### Video Dataset Requirements

- 2-5 second clips, consistent frame rate (24/30 fps)
- Export as frame sequences (PNG) for training
- Caption describes the action/motion, not visual style (for style LoRA)
- 20-50 clips recommended

### Video Captioning Example

```
# For a character video LoRA:
ohwx woman, walking through a park, smiling, wind blowing hair, sunny day, handheld camera

# For a motion/action concept LoRA:
myconcept, a cat stretching on a couch, natural lighting, living room background
```

---

## Advanced: IPAdapter/Reference Workflow

If user mentions using IPAdapter or reference-based generation:

1. Generate first image with seed lock
2. Use that image as IPAdapter reference
3. Subsequent prompts focus more on pose/angle changes
4. Can reduce appearance anchor detail since reference handles it

## Consistency Tips to Include

- Use same trigger word format: `ohwx woman` or custom unique token
- Recommend fixed seed batches per angle category
- Suggest ControlNet OpenPose for precise pose control
- Advise checking generated images for: hand errors, ear deformation, hair consistency

## Caption/Tagging Strategy for Training

### Core Principle

> **In caption = Model learns to differentiate (controllable)**
> **NOT in caption = Model learns to bind (character identity)**

### What TO Include in Captions

```
[trigger_word], [expression], [eye_direction], [pose/gesture], [clothing], [background], [lighting]
```

### What NOT to Include in Captions

- Facial features (face shape, eye shape, skin tone)
- Fixed hair color/style (unless you want hair to be controllable)
- Age, ethnicity, basic appearance settings
- Any feature that defines the character identity

### Caption Detail Level Guide

| Element | Detail Level | Good Example | Bad Example |
|---------|--------------|--------------|-------------|
| Expression | Specific | `laughing with eyes closed` | `happy` |
| Eye direction | Specific | `looking at viewer`, `looking away to left` | `looking` |
| Pose/Gesture | Specific | `peace sign near face`, `hand resting on cheek` | `posing` |
| Clothing | Medium | `white blouse`, `casual gray hoodie` | `wearing clothes` |
| Background | Brief | `simple background`, `outdoor blurred` | (too detailed) |
| Lighting | Brief | `natural lighting`, `golden hour` | (too detailed) |

### Caption Examples

**Image: Front view, laughing with closed eyes, peace sign, white t-shirt, park, golden hour**

✅ Correct:
```
ohwx woman, front view, laughing, eyes closed, peace sign, white t-shirt, park background, golden hour lighting
```

❌ Wrong (includes fixed features):
```
ohwx woman, asian, oval face, black hair, brown eyes, front view, laughing, white t-shirt
```

❌ Wrong (too brief):
```
ohwx woman, smiling
```

❌ Wrong (too detailed):
```
ohwx woman, standing in a beautiful park on a sunny afternoon with golden sunlight streaming through the trees, wearing a crisp white cotton t-shirt...
```

### Hair Handling

**Single hairstyle in dataset:** Do NOT caption hair, let LoRA bind it to identity.

**Multiple hairstyles in dataset:** Caption hair to make it controllable:
```
ohwx woman, ponytail, ...
ohwx woman, hair down, ...
ohwx woman, braided hair, ...
```

### Recommended Captioning Workflow

1. **Auto-tag first** using WD14 Tagger or Florence-2
2. **Batch remove fixed feature tags:**
   - Remove: `asian`, `black hair`, `brown eyes`, `oval face`, `fair skin`, `1girl`, `solo`, etc.
3. **Add trigger word** to the beginning of every caption
4. **Standardize vocabulary:**
   - Pick ONE term and use consistently: `laughing` (not mixing `laugh`/`laughing`/`laughter`)
   - Pick ONE format: `three quarter view` (not mixing with `3/4 view`)
5. **Verify completeness:** Every caption should have: expression + eye direction + clothing + background + lighting
6. **Check for leaks:** Search for any appearance-related tags that slipped through

### AI-Assisted Captioning

For using AI models (Claude, GPT-4V, etc.) to caption images, see `references/captioning-system-prompt.md` for ready-to-use system prompts.

**Select captioning style based on your training model:**

| Training Model | Captioning Style |
|----------------|------------------|
| SD1.5 | Tag-based |
| SDXL (traditional) | Tag-based |
| SDXL (modern) | Hybrid or Natural Language |
| Pony Diffusion | Tag-based |
| **Flux** | **Natural Language** |
| **SD3 / SD3.5** | **Natural Language** |
| **Wan Video 2.x** | **Natural Language (Video)** |
| **Qwen-VL** | **Natural Language** |
| **HunyuanVideo** | **Natural Language (Video)** |
| **CogVideoX** | **Natural Language (Video)** |

**Available prompts in reference file:**
- Natural Language - Standard (Flux/Qwen/SD3)
- Natural Language - Video Focused (Wan/Hunyuan/CogVideo)
- Natural Language - Detailed / Concise variants
- Tag-Based - Standard / Strict / Batch variants
- Hybrid Style (SDXL transition)
- 繁體中文版本

### Vocabulary Standardization Reference

| Category | Standardized Terms |
|----------|-------------------|
| Angles | `front view`, `three quarter view`, `side profile`, `from above`, `from below` |
| Expressions | `gentle smile`, `laughing`, `serious expression`, `surprised expression`, `neutral expression` |
| Eye direction | `looking at viewer`, `looking away`, `looking down`, `looking up`, `eyes closed` |
| Lighting | `natural lighting`, `studio lighting`, `golden hour`, `dramatic lighting`, `soft lighting` |

### Common Captioning Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Including ethnicity/age | Model won't generalize | Remove all identity descriptors |
| Inconsistent terms | Confuses model | Standardize vocabulary |
| Too brief | Model can't differentiate poses | Add specific details |
| Too verbose | Noise in training | Keep concise, relevant only |
| Forgetting expression | Expression becomes random | Always include expression |
| Same clothing description | Model binds clothing | Describe each outfit differently |

---

## VRAM 需求參考表

| GPU | VRAM | SD 1.5 | SDXL | Flux | SD3 | 建議 |
|-----|------|--------|------|------|-----|------|
| RTX 3060 | 12 GB | LoRA rank 32, batch 1-2 | LoRA rank 16, batch 1 | 不建議 | 不建議 | 入門訓練 SD1.5 |
| RTX 3090 | 24 GB | LoRA rank 128, batch 4-6 | LoRA rank 64, batch 2-3 | LoRA rank 16, batch 1 | LoRA rank 16, batch 1 | 主力訓練卡 |
| RTX 4090 | 24 GB | LoRA rank 128, batch 8 | LoRA rank 128, batch 4 | LoRA rank 32, batch 2 | LoRA rank 32, batch 2 | 高效訓練 |
| A100 | 40/80 GB | Full fine-tune possible | LoRA rank 256, batch 8+ | LoRA rank 128, batch 4+ | LoRA rank 128, batch 4+ | 專業/商用 |

### VRAM 節省技巧

| 技巧 | 節省量 | 副作用 |
|------|--------|--------|
| gradient checkpointing | ~30% | 訓練速度降 20-30% |
| mixed precision (fp16/bf16) | ~40% | 幾乎無 |
| 8-bit Adam optimizer | ~30% | 微小精度損失 |
| 降低 batch size | 線性 | 需增加 gradient accumulation |
| 降低解析度 | 大幅 | 影響輸出品質 |
| xformers / flash attention | ~10-20% | 無 |

---

## Multi-Concept LoRA 訓練

### 概念

單一 LoRA 中訓練多個概念（如角色 A + 角色 B + 風格），每個概念用不同的觸發詞區分。

### 資料準備

| 概念 | 觸發詞 | 圖片數 | 注意事項 |
|------|--------|--------|---------|
| 角色 A | `character_a` | 20-40 | 確保無角色 B 出現 |
| 角色 B | `character_b` | 20-40 | 確保無角色 A 出現 |
| 共同風格 | 不需要額外觸發詞 | 所有圖片自然包含 | 風格一致即可 |

### 訓練設定

- 在 caption 中為每個概念加上各自的觸發詞
- 使用 `--dataset_config` 為不同概念設定不同 `num_repeats`
- 概念數量不均時，用 `num_repeats` 平衡（少的概念重複多次）
- 建議 rank 提高至 64-128（多概念需要更多容量）

### 常見問題

| 問題 | 原因 | 解法 |
|------|------|------|
| 概念混合（A 長得像 B） | 訓練圖片有重疊特徵 | 確保每個概念的圖片集互不包含 |
| 某概念不穩定 | 訓練資料量不均 | 調整 num_repeats 平衡 |
| 風格不一致 | 概念間風格差異大 | 統一圖片的後處理風格 |

---

## LoRA 變體比較

| 方法 | 參數量 | 品質 | VRAM | 適用場景 |
|------|--------|------|------|---------|
| **LoRA** | 中 | 好 | 中 | 通用，最成熟穩定 |
| **LyCORIS/LoHa** | 少 | 好 | 低 | VRAM 受限時 |
| **LyCORIS/LoKr** | 最少 | 一般 | 最低 | 極端低 VRAM |
| **DoRA** | 中 | 較好 | 中偏高 | 追求更好品質 |
| **OFT** | 中 | 好 | 中 | 保持原模型能力 |
| **BOFT** | 中偏少 | 好 | 中 | OFT 的改進版 |

### 選擇建議

- 新手/通用 → **LoRA**（社群支援最多、教學最多）
- VRAM 不足 → **LoHa**（12GB 也能訓 SDXL）
- 追求品質 → **DoRA**（但需更多 VRAM 和訓練時間）
- 保持原模型泛化能力 → **OFT/BOFT**

---

## 訓練失敗排錯表

| 症狀 | 可能原因 | 排除方法 |
|------|---------|---------|
| Loss 不下降 | Learning rate 太低 / 資料品質差 | 提高 LR 至 1e-4；檢查 caption 品質 |
| Loss 震盪劇烈 | LR 太高 / batch size 太小 | 降低 LR；增加 gradient accumulation |
| 過擬合（輸出像訓練圖片的複製品） | 訓練太久 / 資料太少 / rank 太高 | 減少 epochs；增加正則化圖片；降低 rank |
| 欠擬合（觸發詞沒效果） | 訓練不足 / caption 中觸發詞不一致 | 增加 epochs；確認每張圖的 caption 都有觸發詞 |
| CUDA OOM | VRAM 不足 | 降低 batch size / rank；啟用 gradient checkpointing |
| 生成圖片有色偏 | 訓練資料色彩分佈偏差 | 確保訓練圖片涵蓋多種光照/背景色 |

---

## WD14 Tagger 自動標註工作流程

### 概述

使用 WD14 Tagger 自動為訓練圖片生成 booru-style tags，再手動修正為自然語言 caption。

### 流程

1. **批次標註**：用 WD14 Tagger 對所有訓練圖片生成 tags
2. **過濾調整**：移除不相關的 tags（如錯誤的頭髮顏色、錯誤的背景描述）
3. **觸發詞插入**：在每個 tag 檔案開頭加入觸發詞
4. **轉換格式**（可選）：將 booru tags 轉為自然語言 caption

### 設定建議

| 參數 | 建議值 | 說明 |
|------|--------|------|
| 模型 | `wd-swinv2-tagger-v3` | 目前最準確的版本 |
| 信心閾值 | 0.35 (一般) / 0.5 (嚴格) | 低閾值多 tags 但有雜訊 |
| 排除 tags | `rating:*`, `score:*` | 排除品質/評分相關 |
| 加入字元 tags | 視需求 | 角色 LoRA 保留；風格 LoRA 移除 |

### 自動標註到 Caption 的轉換

| Tagger 輸出 | 轉換後 Caption |
|-------------|---------------|
| `1girl, brown hair, blue eyes, school uniform, smiling, outdoors` | `a girl with brown hair and blue eyes wearing a school uniform, smiling while standing outdoors` |
| `landscape, sunset, mountains, lake, trees, clouds` | `a scenic landscape at sunset with mountains in the background, a calm lake in the foreground, surrounded by trees under cloudy skies` |
