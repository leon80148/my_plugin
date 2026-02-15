# Prompt Templates Reference

Complete prompt sets organized by character type and use case.

## Real Person Style (寫實風格)

### Young Asian Woman (20s)

**Appearance Anchor:**
```
25 year old asian woman, oval face, single eyelid, brown eyes, shoulder length black straight hair, fair skin, natural makeup
```

**Full Prompt Set (30 prompts with rich variation):**

Front Closeups - Basic Expressions (5):
```
[anchor], front view, looking at viewer, gentle smile, white blouse, white background, soft studio lighting
[anchor], front view, looking at viewer, neutral expression, cream sweater, simple background, natural window light
[anchor], front view, serious expression, black turtleneck, gray background, dramatic studio lighting
[anchor], front view, slight smile, lips slightly parted, light blue shirt, white background, soft diffused lighting
[anchor], front view, soft expression, eyes looking to side, beige cardigan, simple background, warm soft lighting
```

Front Closeups - Dynamic Expressions (5):
```
[anchor], front view, laughing, eyes closed, big smile showing teeth, casual hoodie, blurred background, warm lighting
[anchor], front view, surprised expression, eyes wide open, raised eyebrows, mouth open, white t-shirt, simple background, bright lighting
[anchor], front view, winking, playful smile, tongue out slightly, graphic tee, colorful background, fun lighting
[anchor], front view, pouting, puffed cheeks, cute expression, pink sweater, pastel background, soft lighting
[anchor], front view, shy expression, blushing, looking down slightly, off-shoulder top, simple background, gentle lighting
```

3/4 Angle - With Gestures (8):
```
[anchor], three quarter view, peace sign, cheerful smile, casual t-shirt, park background bokeh, golden hour
[anchor], three quarter view, hand on cheek, thoughtful expression, cozy sweater, cafe interior blurred, warm indoor light
[anchor], three quarter view, tucking hair behind ear, gentle smile, white blouse, simple background, soft lighting
[anchor], three quarter view, finger to lips shh gesture, playful wink, black top, studio background, dramatic lighting
[anchor], three quarter view, stretching arms up, yawning, sleepy expression, oversized hoodie, bedroom background, morning light
[anchor], three quarter view, holding phone, looking at screen, focused expression, casual clothes, urban background, natural daylight
[anchor], three quarter view, covering mouth laughing, embarrassed smile, cute cardigan, outdoor background, afternoon light
[anchor], three quarter view, thumbs up, excited expression, sporty outfit, gym background blurred, bright lighting
```

Side Profile (4):
```
[anchor], side profile, neutral expression, wind blowing hair, white shirt, outdoor background, golden hour backlight
[anchor], side profile, drinking from cup, relaxed, cozy sweater, cafe interior, warm window light
[anchor], side profile, eyes closed, peaceful smile, hair accessories, simple background, soft rim lighting
[anchor], side profile, looking over shoulder, confident smirk, leather jacket, urban background, dramatic lighting
```

Interactions with Objects (5):
```
[anchor], holding coffee mug, both hands wrapped around cup, warm smile, oversized sweater, cozy interior, morning light
[anchor], reading book, focused expression, glasses, cardigan, library background, soft indoor lighting
[anchor], taking selfie, holding phone up, playful expression, casual outfit, mirror reflection, natural lighting
[anchor], holding flowers, smelling, eyes closed, happy expression, sundress, garden background, bright daylight
[anchor], wearing headphones, eyes closed, enjoying music, relaxed smile, hoodie, simple background, moody lighting
```

Upper Body - Dynamic Poses (5):
```
[anchor], upper body, arms crossed, confident expression, blazer, office background blurred, professional lighting
[anchor], upper body, leaning forward, curious expression, hands on table, casual top, cafe background, warm light
[anchor], upper body, dancing pose, arms raised, joyful expression, party outfit, colorful lights, night setting
[anchor], upper body, hugging pillow, cozy expression, pajamas, bedroom setting, soft lamp light
[anchor], upper body, applying lipstick, looking in mirror, focused, elegant top, vanity background, glamorous lighting
```

Full Body (3):
```
[anchor], full body, walking pose, looking back over shoulder, flowing dress, city street, golden hour
[anchor], full body, jumping, arms spread, excited expression, casual outfit, outdoor park, bright daylight
[anchor], full body, sitting cross-legged on floor, relaxed, holding mug, living room, cozy warm lighting
```

---

## Expression Variety Checklist

Ensure your set includes at least ONE of each category:

**Happy spectrum:**
- [ ] gentle smile
- [ ] big smile/laughing
- [ ] excited/joyful

**Playful spectrum:**
- [ ] winking
- [ ] tongue out
- [ ] peace sign/gesture

**Calm spectrum:**
- [ ] neutral
- [ ] peaceful/serene
- [ ] thoughtful

**Intense spectrum:**
- [ ] serious
- [ ] focused/determined
- [ ] confident

**Vulnerable spectrum:**
- [ ] shy/embarrassed
- [ ] surprised
- [ ] sleepy/tired

---

## Pose Variety Checklist

**Face/Head actions:**
- [ ] head tilt
- [ ] looking away/side glance
- [ ] eyes closed
- [ ] hair interaction (brushing, tucking)

**Hand gestures:**
- [ ] peace sign
- [ ] hand on face/cheek
- [ ] covering mouth
- [ ] pointing or other gesture

**Body poses:**
- [ ] arms crossed
- [ ] stretching
- [ ] leaning
- [ ] sitting variation

**Object interactions:**
- [ ] holding drink
- [ ] phone interaction
- [ ] wearing accessories (glasses, headphones)

---

## Anti-Overfitting Tips

1. **Never repeat same expression twice** - Even "smile" should vary: gentle smile, big smile, smirk, shy smile

2. **Vary eye direction** - looking at viewer, looking away, looking down, side glance, eyes closed

3. **Mix static and dynamic** - Include action shots (laughing, stretching, walking) not just posed shots

4. **Environmental variety** - Mix studio (60-70%) with contextual backgrounds (30-40%)

5. **Lighting diversity** - Dramatic, soft, golden hour, backlit, etc. (at least 4-5 types)

6. **Clothing changes** - EVERY image should have different clothing, no repeats

7. **Include imperfect moments** - Yawning, messy hair, candid expressions feel more natural

8. **Gesture variety** - Include hand gestures, object interactions, not just static poses

---

## Background Strategy

| Type | Percentage | Purpose |
|------|------------|---------|
| Simple/Studio | 60-70% | Clean training signal |
| Indoor scenes | 15-20% | Indoor generalization |
| Outdoor scenes | 10-20% | Outdoor generalization |

**Why mix backgrounds:**
- 100% simple background → Model only works well on simple backgrounds
- 100% scene backgrounds → Model may learn unwanted background elements
- Mixed → Best generalization

---

## Clothing Strategy

**Rule:** No two images should have identical clothing

**Minimum variety for 30 images:**
- At least 8-10 completely different outfits
- Mix colors: light, dark, warm, cool
- Mix styles: casual, formal, sporty, cozy
- Mix coverage: t-shirt, long sleeve, off-shoulder, etc.

**Why this matters:**
If you use the same white t-shirt in 10 images, the model will associate "white t-shirt" with the character's identity, making it hard to change clothes during generation.

---

## Male Character Template

**Appearance Anchor:**
```
28 year old asian man, angular jawline, short black hair, natural eyebrows, light stubble, fair skin
```

**Expression variations for men:**
- `confident smile`, `smirking`, `stoic expression`
- `laughing heartily`, `grinning`, `chuckling`
- `focused expression`, `intense gaze`, `determined look`
- `relaxed smile`, `friendly expression`, `warm smile`

**Pose variations:**
- `hands in pockets`, `adjusting tie`, `running hand through hair`
- `leaning against wall`, `arms crossed`, `casual stance`
- `holding coffee`, `checking watch`, `on phone`

---

## Stylized/Anime-Adjacent Style

For semi-realistic or stylized character LoRA:

**Appearance Anchor:**
```
1girl, young woman, delicate face, large expressive eyes, black long hair, fair skin, soft features
```

**Add anime-specific expressions:**
- `>_<`, `^_^`, `o_o` (for very stylized)
- `sparkly eyes`, `star pupils`, `heart eyes`
- `sweatdrop`, `blush lines`, `nose blush`

Adjust quality tags:
```
masterpiece, best quality, detailed face, detailed eyes, beautiful lighting
```

---

## Negative Prompt Templates

**Standard (SD1.5):**
```
bad anatomy, bad hands, missing fingers, extra fingers, deformed face, ugly, blurry, low quality, watermark, text, signature, duplicate, mutation, worst quality, low resolution, jpeg artifacts, cropped, out of frame
```

**Enhanced (SDXL):**
```
bad anatomy, bad hands, missing fingers, extra fingers, deformed face, asymmetrical face, ugly, blurry, low quality, watermark, text, signature, duplicate, mutation, worst quality, low resolution, jpeg artifacts, cropped, out of frame, bad proportions, malformed limbs, extra limbs, fused fingers, too many fingers, long neck, cross-eyed
```

**For realistic portraits add:**
```
anime, cartoon, illustration, painting, drawing, art, render, cgi, 3d, doll
```

---

## Quick Generation Checklist

Before finalizing your prompt set, verify:

**Expression Variety:**
- [ ] At least 5 different expression types
- [ ] Includes dynamic expressions (laughing, surprised, etc.)
- [ ] Includes subtle expressions (gentle smile, neutral, etc.)

**Eye Direction Variety:**
- [ ] Looking at viewer (multiple)
- [ ] Looking away / side glance
- [ ] Eyes closed (at least 1-2)
- [ ] Looking up/down variations

**Pose & Gesture Variety:**
- [ ] At least 3 different hand gestures
- [ ] Mix of static and dynamic poses
- [ ] At least 1-2 object interactions

**Background Distribution:**
- [ ] 60-70% simple/studio backgrounds
- [ ] 15-20% indoor scene backgrounds  
- [ ] 10-20% outdoor scene backgrounds

**Clothing Variety:**
- [ ] Minimum 8-10 different outfits for 30 images
- [ ] NO repeated outfits
- [ ] Mix of casual, formal, and special styles
- [ ] Color variety (light, dark, warm, cool)

**Lighting Variety:**
- [ ] At least 4-5 different lighting types
- [ ] Includes: natural, studio, golden hour, dramatic

**Accessory Variation:**
- [ ] At least 2-3 accessory changes (glasses, jewelry, etc.)

## Captioning Checklist

For EVERY caption, verify:
- [ ] Starts with trigger word
- [ ] Has specific expression
- [ ] Has eye direction
- [ ] Has clothing description (unique per image)
- [ ] Has background type
- [ ] Has lighting type
- [ ] NO identity features (ethnicity, face shape, fixed hair)
