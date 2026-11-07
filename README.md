# Aesthetic Case Report PPT Generator (`aesthetic-case-report-ppt-gem`)

> **Claude Code / Codex / Agent Skill**: Transform medical aesthetics clinical case records, injection mappings, before/after photography, and optional academic literature into publication-grade, conference-ready 16:9 Case Report PPTX presentations.

---

## 🌟 Overview

`aesthetic-case-report-ppt-gem` is a specialized medical aesthetics skill engineered for aesthetic physicians, dermatologists, plastic surgeons, and medical science liaisons (MSLs). It synthesizes clinical real-world patient records, anatomical mappings, and academic papers into visually compelling, academically rigorous case presentations (e.g. for AMWC, IMCAS, Galderma AART symposia, and clinical rounds).

It is built upon two proven gold-standard aesthetic paradigms:
1. **Mode A: Academic-Clinical Synthesis (双核精读+案例实证型)** — Inspired by *The Blending Technique for Tear Trough Correction*. Combines literature critical appraisal, layer-by-layer anatomical mechanisms (ORL, TTL, Arcus Marginalis, DMCFP), clinical classifications (Innie vs Outie), rheological selection ($G'$, cohesivity), and case validation.
2. **Mode B: Longitudinal Patient Journey (纵向面部全层抗衰型)** — Inspired by *Aesthetic Lives (Dr Jovi Liu Edition)*. Focuses on holistic assessment (FAS - Facial Assessment Scale), baseline imaging, 1st treatment mapping & dosage tables, immediate post-op multi-angle comparisons, 6-month follow-up, 2nd treatment evolution, and multi-year journey corridors (2024 → 2025 → 2026).

---

## 🔄 5-Phase Interactive Pipeline

```
[ Phase 1: Intake & Asset Discovery (Papers, notes, photo directory, speaker info) ]
                                   ↓
[ Phase 2: Template Selection (Default Template A / B vs. Custom design.md) ]
                                   ↓
[ Phase 3: Clinical Parameter Extraction & Slide Outline Review ]
                                   ↓
[ Phase 4: Deck Automation & python-pptx Rendering ]
                                   ↓
[ Phase 5: Delivery, Preview & Iteration ]
```

### 1. Intake Discovery
The skill actively asks for your input assets:
- **Reference Paper**: Optional (PDF, PubMed ID, or literature notes).
- **Case Records**: Patient profile, complaints, target areas, layers, tools (sharp needle / cannula gauge), dosage (left/right ml), materials.
- **Photos Directory**: Path to patient images (pre-treatment, marking, immediate post-op, 3m/6m follow-ups; frontal, 45° oblique, 90° profile, dynamic smile).
- **Speaker & Venue**: Doctor name, institution, presentation occasion.

### 2. Template Flexibility
- **Default Mode A (Academic-Clinical)**: 16–24 slides. Literature dilemma → Anatomy & Spaces → Classification Tree → Rheology & Technique → Representative Case Before/After → Dynamic Smile Validation → Local Practice.
- **Default Mode B (Patient Journey)**: 18–28 slides. Aging Philosophy (Bone to Dermis) → FAS Baseline Card → Treatment Mapping & Dose Grid → Immediate 2-Up / 3-Up Matrix → Mid-term Stability → 2nd Stage Planning → Multi-year Journey Timeline → Doctor's Takeaways.
- **Custom `design.md`**: Supply your own color tokens (Galderma Navy `#0F2C59`, Allergan tones, minimal dark mode), custom section layouts, and slide budgets.

### 3. Automated PPTX Engine
Powered by `python-pptx`, the generator provides:
- Clean 16:9 widescreen layout (13.33 x 7.50 inches).
- Elegant cards with soft borders and medical palette styling.
- Standardized Before/After paired alignment with temporal capsule tags.
- Dynamic smile verification grids (preventing sausage-like deformities and Tyndall effect).
- Mandatory clinical compliance & non-disclosure disclaimers on every slide.

---

## 📂 Repository Structure

```
aesthetic-case-report-ppt-gem/
├── SKILL.md                               # Skill instruction & prompt rules for agents
├── README.md                              # Repository overview & usage guide
├── .gitignore
├── templates/
│   ├── default_template_A_academic.md     # 16-24 slide outline: Literature + Case Validation
│   ├── default_template_B_journey.md      # 18-28 slide outline: Longitudinal Patient Journey
│   ├── design_sample.md                   # Custom design.md specification guide & sample
│   └── case_record_prompt_guide.md        # Case notes & photo naming input guide
├── scripts/
│   ├── generate_case_deck.py              # Main automated 16:9 PPTX generation engine
│   └── pptx_builder_utils.py              # Layout, geometry, color palette & styling utils
└── references/
    ├── anatomy_and_injection_vocabulary.md # Medical aesthetics terminology & rheology lexicon
    └── aesthetic_case_best_practices.md   # Presentation narrative & photography gold standards
```

---

## 🚀 Installation & Usage

### 1. Install Skill for Claude Code / Codex / Agents
Clone into your local agent skills directory:

```bash
# For Codex / Antigravity / Agent Skills:
git clone https://github.com/qitong/aesthetic-case-report-ppt-gem.git ~/.agents/skills/aesthetic-case-report-ppt-gem

# For Claude Code:
git clone https://github.com/qitong/aesthetic-case-report-ppt-gem.git ~/.claude/skills/aesthetic-case-report-ppt-gem
```

### 2. Requirements
```bash
pip install python-pptx pillow
```

### 3. Generate a Demo Deck
```bash
python3 scripts/generate_case_deck.py --demo --output "output/Demo_Aesthetic_Case_Deck.pptx"
```

### 4. Direct Prompt Triggers
Ask your AI assistant:
- *"我有一份眶周泪沟治疗的病程和照片，帮我生成一份高德美学术研讨会用的 Case Report PPT。"*
- *"参考这篇韧带解剖论文和患者的随访记录，用 default 模板 A 制作一套精读与病例汇报幻灯片。"*
- *"我这里有患者两年的抗衰照片和打法记录，做一个 Patient Journey 风格的 PPT。" *

---

## ⚖️ Compliance & Ethical Notice
- All presentations generated with this skill incorporate required medical disclaimer notices.
- Ensure all patient photographs have obtained explicit informed consent for academic presentation.
- Different products and medical devices must adhere to local regulatory approvals (e.g. NMPA / FDA / CE) and official package inserts.

---

## 📄 License
MIT License. Created by [@qitong](https://github.com/qitong).
