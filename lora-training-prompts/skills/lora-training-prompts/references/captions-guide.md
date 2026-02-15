# Training Captions Guide

Complete guide for writing effective captions/tags for LoRA training.

## Core Captioning Philosophy

> **In caption = Model learns to differentiate (controllable)**
> **NOT in caption = Model learns to bind (character identity)**

The goal is to teach the model:
- "This person's face" = always the same (NOT in caption)
- "This expression/pose/clothing" = varies (IN caption)

## What Goes IN vs OUT of Captions

### INCLUDE in Every Caption

| Element | Why | Example |
|---------|-----|---------|
| Trigger word | Activates LoRA | `ohwx woman` |
| Expression | Control emotions | `laughing`, `serious expression` |
| Eye direction | Control gaze | `looking at viewer`, `eyes closed` |
| Pose/Gesture | Control body language | `peace sign`, `arms crossed` |
| Clothing | Prevent clothing binding | `white blouse`, `casual hoodie` |
| Background type | Prevent background binding | `simple background`, `outdoor` |
| Lighting | Control mood | `natural lighting`, `dramatic lighting` |

### EXCLUDE from All Captions

| Element | Why Exclude |
|---------|-------------|
| Ethnicity | Part of identity |
| Age | Part of identity |
| Face shape | Part of identity |
| Eye color/shape | Part of identity |
| Skin tone | Part of identity |
| Fixed hair color | Part of identity (unless multi-hair dataset) |
| Fixed hair style | Part of identity (unless multi-hair dataset) |
| Body type | Part of identity |

## Caption Format

```
[trigger_word], [expression], [eye_direction], [pose/gesture], [clothing], [background], [lighting]
```

## Trigger Word Selection

**Good trigger words are:**
- Unique, unlikely to exist in model vocabulary
- Short and easy to type
- Memorable

**Recommended formats:**
```
ohwx woman
ohwx man
sks person
xyz_[name]
[uniquename]_lora
```

**Avoid:**
- Common words alone: `woman`, `girl`, `person`
- Real celebrity names: `emma`, `taylor`
- Words that might conflict: `beautiful`, `young`

## Caption Detail Levels

### Expression - BE SPECIFIC

❌ Too vague:
```
happy
```

✅ Specific:
```
gentle smile
laughing with eyes closed
big smile showing teeth
surprised expression with raised eyebrows
```

### Eye Direction - BE SPECIFIC

❌ Too vague:
```
looking
```

✅ Specific:
```
looking at viewer
looking away to the left
looking down shyly
side glance to the right
eyes closed peacefully
```

### Pose/Gesture - BE SPECIFIC

❌ Too vague:
```
posing
hand gesture
```

✅ Specific:
```
peace sign near face
hand resting on cheek
arms crossed over chest
tilting head to the right
tucking hair behind ear
```

### Clothing - MEDIUM DETAIL

❌ Too vague:
```
casual clothes
```

❌ Too detailed:
```
vintage 1990s stone-washed high-waisted denim jeans with brass button fly
```

✅ Just right:
```
white t-shirt
casual gray hoodie
black leather jacket
blue floral sundress
```

### Background - KEEP BRIEF

❌ Too detailed:
```
standing in a cozy coffee shop with exposed brick walls and warm Edison bulb lighting and vintage wooden furniture
```

✅ Brief and functional:
```
cafe interior blurred
simple white background
outdoor park bokeh
urban street background
```

### Lighting - KEEP BRIEF

✅ Good examples:
```
natural lighting
soft studio lighting
golden hour
dramatic side lighting
warm indoor lighting
```

## Complete Caption Examples

### Example Set for One Character

**Image 1: Front, smiling, peace sign, white tee, studio**
```
ohwx woman, front view, looking at viewer, gentle smile, peace sign, white t-shirt, simple white background, soft studio lighting
```

**Image 2: 3/4 angle, laughing, hand on cheek, hoodie, cafe**
```
ohwx woman, three quarter view, laughing, eyes closed, hand on cheek, gray hoodie, cafe interior blurred, warm natural lighting
```

**Image 3: Side profile, serious, arms crossed, blazer, outdoor**
```
ohwx woman, side profile, serious expression, looking away, arms crossed, black blazer, urban background blurred, golden hour lighting
```

**Image 4: Front, surprised, both hands up, sweater, bedroom**
```
ohwx woman, front view, surprised expression, eyes wide, raised eyebrows, hands raised, cream sweater, bedroom background, soft morning light
```

**Image 5: 3/4 view, winking, holding coffee, cardigan, window**
```
ohwx woman, three quarter view, winking, playful smile, holding coffee cup, beige cardigan, window background, natural window light
```

## Vocabulary Standardization

**CRITICAL:** Pick ONE term for each concept and use it consistently across ALL captions.

### Angles
| Use This | NOT These |
|----------|-----------|
| `front view` | `facing front`, `frontal`, `facing camera` |
| `three quarter view` | `3/4 view`, `angled view`, `turned slightly` |
| `side profile` | `profile view`, `side view`, `from side` |
| `from above` | `high angle`, `looking down at` |
| `from below` | `low angle`, `looking up at` |

### Expressions
| Use This | NOT These |
|----------|-----------|
| `gentle smile` | `soft smile`, `slight smile`, `small smile` |
| `laughing` | `laugh`, `laughter`, `laughs` |
| `serious expression` | `serious face`, `stern look`, `no smile` |
| `surprised expression` | `shocked`, `surprised look`, `shock` |

### Eye Direction
| Use This | NOT These |
|----------|-----------|
| `looking at viewer` | `looking at camera`, `eye contact`, `staring` |
| `looking away` | `looking to side`, `averted gaze` |
| `eyes closed` | `closed eyes`, `shut eyes` |

### Lighting
| Use This | NOT These |
|----------|-----------|
| `natural lighting` | `natural light`, `daylight` |
| `studio lighting` | `studio light`, `professional lighting` |
| `golden hour` | `golden hour lighting`, `sunset light` |

## Hair Handling Strategies

### Strategy 1: Single Hairstyle (Recommended for beginners)

If all training images have the same hairstyle:
- Do NOT include hair in captions
- LoRA will automatically bind hairstyle to the character

### Strategy 2: Multiple Hairstyles (Advanced)

If training images have different hairstyles and you want control:

```
ohwx woman, long hair down, ...
ohwx woman, ponytail, ...
ohwx woman, hair in bun, ...
ohwx woman, braided hair, ...
```

### Strategy 3: Hair Color Variations

If you want to control hair color:
```
ohwx woman, black hair, ...
ohwx woman, brown hair, ...
ohwx woman, blonde hair, ...
```

## Captioning Workflow

### Step 1: Auto-Tag All Images

Use one of these tools:
- **WD14 Tagger** - Good for anime/illustration style
- **Florence-2** - Good for natural language descriptions
- **BLIP/BLIP2** - Alternative natural language option

### Step 2: Batch Clean Tags

Remove these categories from ALL captions:
```
Remove: 1girl, solo, asian, black hair, brown eyes, oval face, 
fair skin, young, beautiful, pretty, cute, woman, female,
realistic, photo, photography
```

### Step 3: Add Trigger Word

Prepend trigger word to every caption:
```
Before: front view, smiling, white shirt, simple background
After:  ohwx woman, front view, smiling, white shirt, simple background
```

### Step 4: Standardize Vocabulary

Search and replace to unify terms:
```
"3/4 view" → "three quarter view"
"looking at camera" → "looking at viewer"
"slight smile" → "gentle smile"
```

### Step 5: Verify Completeness Checklist

For each caption, verify:
- [ ] Has trigger word
- [ ] Has expression
- [ ] Has eye direction (or eyes closed)
- [ ] Has clothing description
- [ ] Has background type
- [ ] Has lighting type
- [ ] NO fixed appearance features

### Step 6: Final Leak Check

Search all captions for leaked identity terms:
```
Search for: asian, black hair, brown eyes, fair skin, oval face, 
young woman, beautiful, pretty, 1girl, solo
```

If found, remove them.

## Common Mistakes and Fixes

| Mistake | Problem | Fix |
|---------|---------|-----|
| `ohwx woman, asian, black hair, smiling` | Identity in caption | Remove `asian, black hair` |
| `ohwx woman, happy` | Too vague | → `ohwx woman, gentle smile, looking at viewer` |
| Mixed terms: `laughing` and `laugh` | Inconsistent | Pick one, use everywhere |
| `ohwx woman, wearing a nice outfit` | Non-descriptive | → `ohwx woman, white blouse` |
| No lighting mentioned | Incomplete | Add `natural lighting` or appropriate term |
| Same clothing in multiple captions | Will bind clothing | Vary clothing descriptions |

## Regularization/Class Images

If using regularization images:

**Regularization image caption (NO trigger word):**
```
woman, front view, casual clothing, simple background, natural lighting
```

This teaches the model to separate your specific character from the generic "woman" concept.

**Ratio recommendation:**
- 1:1 ratio (same number of regularization as training images)
- Or use "no regularization" if training steps are low (<1500)
