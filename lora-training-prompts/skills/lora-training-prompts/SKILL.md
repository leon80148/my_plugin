---
name: lora-training-prompts
description: Generate consistent AI image prompts for LoRA training datasets. Use when users need to create a set of prompts that will produce visually consistent character images across different poses, angles, expressions, and lighting conditions for training custom LoRA models. Triggers include requests like "generate LoRA training prompts", "create prompts for training a character LoRA", "help me make training images for a person LoRA", or "產生 LoRA 訓練素材的提示詞".
---

# LoRA Training Prompts Generator

Generate prompt sets for creating consistent character images suitable for LoRA training.

## Core Workflow

1. Gather character specifications from user
2. Build the fixed appearance anchor
3. Generate varied prompts across required categories
4. Output in requested format (plain text or structured)

## Step 1: Gather Character Specifications

Ask for these essential details if not provided:

| Attribute | Examples | Required |
|-----------|----------|----------|
| Gender/Age | 25-year-old woman | Yes |
| Ethnicity/Skin | Asian, fair skin | Yes |
| Face shape | Oval, round, angular | Recommended |
| Eye features | Single eyelid, double eyelid, eye color | Recommended |
| Hair | Black shoulder-length, brown ponytail | Yes |
| Style | Natural, sweet, mature, cool | Optional |
| Base model | SD1.5 / SDXL | Yes (affects resolution) |

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
