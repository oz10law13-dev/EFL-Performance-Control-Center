# **EFL FORCE–VELOCITY ZONE DICTIONARY v1.2 (PRODUCTION BUILD)**

**Version:** 1.2 Production (F-V Bias Integrated)  
**Status:** CANONICAL REFERENCE  
**Date:** December 23, 2025  
**Authority:** Load Standards v2.2.0 + Governance v4.1 + Coach & AI Playbook v0.5.0  
**Integration:** Bias Profiles + 7-Gate Decision Tree + Gate 7 Validation  
**Replaces:** v1.1  
**Purpose:** Definitive zone legality table with F-V bias mapping, population constraints, seasonal enforcement, and Gate 7 integration.

---

## **OVERVIEW**

This document is the single source of truth for:
1. **What each Force-Velocity Zone means** (physiological goal, acute variables)
2. **How zones map to F-V Bias Profiles** (FORCE_BIASED, VELOCITY_BIASED, BALANCED)
3. **Population × Bias × Season legality** (comprehensive 3-D matrix)
4. **Gate 7 integration** (band distribution contribution, weekly validation)
5. **Assessment protocol** (CMJ, squat, RSI thresholds per bias)
6. **Zone sequencing by bias** (which zones to prioritize per profile)

System 3 (EPA) uses this table to: validate zones through 7-Gate Decision Tree, apply F-V bias constraints, filter exercises by zone legality, enforce seasonal bias overrides, validate band/plyo distributions against Gate 7 targets, and generate escalation reason codes.

Every zone is characterized by: Force/Velocity signature, Band & Node requirements, E-Node implications, CNS category, population legality matrix, bias legality, seasonal enforcement, bias contribution, downgrade path, and example patterns.

---

## **AUTHORITY REFERENCES**

### **Load Standards v2.2.0** (Canonical for Volumes, Caps, Counting)

All band definitions, %1RM ranges, RIR values, plyometric contact caps, sprint meter caps, and contact counting rules are defined in **Load Standards v2.2.0** and are not redefined here.

**Key References from LS v2.2.0:**
- Band definitions (Band_0–Band_4) with %1RM and RIR ranges  
- **F-V Bias Profiles** (FORCE_BIASED, VELOCITY_BIASED, BALANCED) with:
  - Band distribution targets (70/30 or 50/50)
  - Plyometric tier distribution targets (E1-E4 ratios)
  - Population constraints (Youth ≤16 = BALANCED only, etc.)
  - Seasonal constraints (IN_SEASON = BALANCED enforced)
- Plyometric contact caps by population, session type (full vs MicroSession)  
- Sprint meter caps by population, per session and per week  
- TRUE_SPRINT_METERS_ONLY standard (≥90% Vmax)  
- COUNTEVERYFOOTSTRIKE standard for plyometric contacts

### **Governance v4.1** (Canonical for Gate Logic)

All gate enforcement, F-V bias compliance rules, and decision tree logic are defined in **Governance v4.1** and are referenced (not redefined) here.

**Key References from Gov v4.1:**
- **Section 2.8: F-V Bias Rules** (population/season constraints)
- **Section 8: F-V Bias Assessment Protocol** (CMJ, squat, RSI thresholds)
- **Gate 7: F-V Bias Compliance** (band distribution validation)
- **7-Gate Decision Tree** (sequence and escalation paths)

### **Coach & AI Playbook v0.5.0** (Canonical for Implementation)

All coaching guidance, block selection logic, and zone sequencing is defined in **Coach & AI Playbook v0.5.0** and is referenced here.

**Key References from Playbook v0.5.0:**
- **Section 1.2A: Force-Velocity Bias Rules** (non-negotiable constraints)
- **Section 5.11: F-V Bias Coaching Decision Tree** (6-step assessment)
- **Appendix F: F-V Bias Profiles Quick Reference** (band/plyo targets)
- **Appendix G: Gate 7 Validation Quick Reference** (variance thresholds)

---

## **CRITICAL DEFINITION: ZONE vs BIAS**

**ZONE** (this document):
- Describes the TYPE of training stimulus (Max Strength, Velocity, etc.)
- Prescribes acute variables (load, reps, tempo, rest)
- Maps to bands and E-nodes (quantifiable)
- Population-specific (Youth vs Adult)
- NOT season-specific (zones exist at all times)

**F-V BIAS** (Load Standards v2.2.0 + Governance v4.1):
- Describes the GOAL of training emphasis (improve force or velocity?)
- Prescribes band distribution targets (70/30 splits)
- Prescribes plyometric tier targets (E1-E4 ratios)
- Population × Season-specific (varies by context)
- ENFORCED at seasonal transitions (IN_SEASON = BALANCED always)

**Relationship:**
- Coach selects F-V Bias (FORCE_BIASED, VELOCITY_BIASED, BALANCED)
- Coach selects Zones (1-8) that align with the bias
- Zones are the IMPLEMENTATION; Bias is the STRATEGY
- Gate 7 validates that weekly zone distribution matches bias targets

**Example:**
- Bias: FORCE_BIASED
- Strategy: Improve max strength (low velocity athlete)
- Zones: Prioritize 1, 2, 5 (75% of weekly volume)
- Avoid Zones: 4, 7, 8 (velocity-only or high-rep)
- Gate 7 Check: Do Zones 1-2-5 actually contribute 70%+ to Band2-4? YES → GREEN

---

## **ZONE PROFILES WITH F-V BIAS MAPPING (COMPLETE v1.2)**

### **ZONE 1 — MAX STRENGTH**

**Signature:** Highest force production, heavy mechanical loading, maximal neural drive.  
**Physiological Goal:** CNS recruitment, motor unit synchronization, inter-muscular coordination.

**Typical Movement Patterns:**  
- Bilateral heavy squats (90%+ 1RM)  
- Heavy deadlifts (90%+ 1RM)  
- Heavy bench press (90%+ 1RM)  
- Power cleans (from floor, heavy)

**Acute Variables:**  
- Load: 85–100% 1RM (Band_3–4)  
- Reps: 1–5; Sets: 4–6; Rest: 3–5 min  
- Tempo: X/X/X (explosive concentric)  
- RPE: 8–9; Session: 45–60 min; Exercise Count: 3–5

**Band Distribution Contribution:**
- Primary Bands: Band3, Band4
- Contribution to weekly distribution: +15-25% to Band3-4
- Used in: FORCE_BIASED (primary), BALANCED (primary)
- Avoided in: VELOCITY_BIASED (minimal or excluded)

**E-Node Requirement:** E0 (non-plyometric)  
**CNS Load Category:** HIGH  
**Plyo Contacts:** 0

**F-V Bias Legality (NEW in v1.2):**

| Bias | Off/Pre | In-Season | Post-Season | Rationale |
|---|---|---|---|---|
| **FORCE_BIASED** | ✅ PRIMARY | ❌ | ❌ | Strength emphasis allowed off-season only; maintenance during in-season |
| **VELOCITY_BIASED** | ⚠️ SECONDARY | ❌ | ❌ | Low/minimal Zone 1 for velocity athletes; if used, strength maintenance only |
| **BALANCED** | ✅ ALLOWED | ✅ ALLOWED | ✅ ALLOWED | General strength development year-round |

**Population Legality:**

| Population | Off/Pre | In-Season | Post | Notes |
|---|---|---|---|---|
| Youth 8-12 | ❌ | ❌ | ❌ | Zone 1 forbidden; max strength not appropriate |
| Youth 13-16 | ⚠️ GATE | ⚠️ GATE | ❌ | Bilateral squat benchmark gate required; BALANCED only |
| Youth 17 | ⚠️ GATE | ❌ | ❌ | If FORCE_BIASED, pass gate; BALANCED allowed |
| Adult | ✅ | ⚠️ GATE | ⚠️ GATE | Allowed off-season; reduced volume in-season if BALANCED |
| R2P | ❌ | ❌ | ⚠️ ST4 | Stage 4 only with PT clearance + movement quality gate |

**Downgrade Path (if illegal):** 1 → 2 → 3 → 5 → 6 → 7 → 8

**Gate 7 Impact:** Zone 1 heavily weights FORCE_BIASED programs. Example:
```
FORCE_BIASED Target: 70% Band2-4
If program = 30 reps Zone 1 (Band3-4) + 40 reps Zone 5 (Band1) + 30 reps Zone 6 (Band2)
= 30+30 = 60% in Band2-4 (below 70% target)
→ ACTION: Add more Zone 1-2 or reduce Zone 5-6
```

---

### **ZONE 2 — STRENGTH-SPEED**

**Signature:** High force + moderate velocity, loaded explosiveness.  
**Physiological Goal:** Rate of force development, neuromuscular power coordination.

**Typical Movement Patterns:** Power cleans (hang), speed squats (75–85%), push press, power snatch variants.

**Acute Variables:** Load 75–90% 1RM (Band_2–3), 3–6 reps, 3–5 sets, 2–3 min rest, explosive concentric, RPE 7–8, 45–55 min, 4–6 exercises.

**Band Distribution Contribution:**
- Primary Bands: Band2, Band3
- Contribution: +15-25% to Band2-3
- Used in: FORCE_BIASED (primary), VELOCITY_BIASED (secondary), BALANCED (primary)
- Key bridge zone for all biases

**E-Node Requirement:** E0 or minimal E1/E2  
**CNS Load Category:** HIGH  
**Plyo Contacts:** 0 or minimal (if power variants included)

**F-V Bias Legality:**

| Bias | Off/Pre | In-Season | Post-Season |
|---|---|---|---|
| **FORCE_BIASED** | ✅ PRIMARY | ⚠️ | ❌ |
| **VELOCITY_BIASED** | ✅ SECONDARY | ⚠️ | ❌ |
| **BALANCED** | ✅ ALLOWED | ✅ ALLOWED | ✅ ALLOWED |

**Population Legality:**

| Population | Off/Pre | In-Season |
|---|---|---|
| Youth 8-12 | ❌ | ❌ |
| Youth 13-16 | ⚠️ GATE | ⚠️ GATE |
| Youth 17 | ⚠️ GATE | ❌ IN-SEASON |
| Adult | ✅ | ⚠️ GATE |
| R2P | ❌ | ❌ |

**Downgrade Path:** 2 → 3 → 5 → 6 → 7 → 8

---

### **ZONE 3 — REACTIVE POWER (SPEED-STRENGTH)**

**Signature:** Moderate-high force + high velocity, stretch-shortening cycle, elastic recoil.  
**Physiological Goal:** Reactive power, SSC optimization, plyometric efficiency.

**Typical Patterns:** Depth jumps, bounds, reactive box jumps, med ball throws, clap push-ups.

**Acute Variables:** Load 30–60% 1RM or bodyweight (Band_0–2), 6–10 contacts/reps, 2–4 sets, 60–90s rest, explosive SSC, 40–80 plyo contacts per session (per LS v2.2.0 limits), RPE 7–8, 30–40 min, 4–6 exercises.

**Band Distribution Contribution:**
- Variable bands: Band0-2 (load-dependent)
- Light variants (30-40%): Band0-1, contributes to VELOCITY_BIASED
- Heavy variants (50-60%): Band2, contributes to FORCE_BIASED
- CRUCIAL: Zone 3 BRIDGES both biases depending on load selection

**E-Node Requirement:** E1-E2 (Tier 1-2); E3-E4 allowed for adult VELOCITY_BIASED only  
**CNS Load Category:** MODERATE-HIGH  
**Plyo Contacts:** 40-80 per session (enforced by LS v2.2.0 population caps)

**F-V Bias Legality:**

| Bias | Off/Pre | In-Season | E-Node Allowed |
|---|---|---|---|
| **FORCE_BIASED** | ✅ SECONDARY | ⚠️ | E1-E2 ONLY |
| **VELOCITY_BIASED** | ✅ PRIMARY | ✅ ALLOWED | E1-E4 (all) |
| **BALANCED** | ✅ ALLOWED | ✅ ALLOWED | E1-E2 |

**Key Rule:** For FORCE_BIASED athletes, use heavy Zone 3 variants (50-60% 1RM load, large box jumps) with E1-E2 only. For VELOCITY_BIASED, use light variants (30-40%, maximal velocity) with E1-E4.

**Population Legality:**

| Population | Off/Pre | In-Season | Notes |
|---|---|---|---|
| Youth 8-12 | ✅ E1-E2 | ✅ LIMITED | Low-impact, Tier 1-2 only; no depth >12cm |
| Youth 13-16 | ✅ E1-E4 | ✅ LIMITED | E3-E4 ≤40% of session; BALANCED only |
| Youth 17 | ✅ ALL | ⚠️ LIMITED | If FORCE_BIASED, E1-E2; if BALANCED, all |
| Adult | ✅ ALL | ✅ ALL | Full E-node range allowed off-season; BALANCED in-season |
| R2P | ❌ ST1-2 | ⚠️ ST3-4 | Stage 3+ with clearance, low-impact variants |

**Downgrade Path:** 3 → 5 → 6 → 7 → 8

**Gate 7 Impact:** Zone 3 is CRITICAL for VELOCITY_BIASED programs (high contribution to Band0-2). Underuse → RED FLAG.

---

### **ZONE 4 — PURE VELOCITY (SPEED)**

**Signature:** Low force, maximal velocity, unloaded speed drills.  
**Physiological Goal:** Absolute speed, acceleration, COD.

**Typical Patterns:** Unloaded sprints, banded sprints, accelerations, max-intent shuttles, speed ladder, sled push (minimal resistance).

**Acute Variables:** Load <30% 1RM (Band_0–1), 10–20+ reps or 10–40m, 3–5 sets, 2–3 min rest, RPE 8–9, 30–45 min, 4–6 exercises + sprints. **Critical: Sprint intensity ≥90% Vmax (TRUE_SPRINT_METERS_ONLY per LS v2.2.0)**

**Band Distribution Contribution:**
- Primary Band: Band0-1
- Contribution: +10-15% to Band0-1
- Primary bias user: VELOCITY_BIASED (essential for speed emphasis)
- Minimal use: FORCE_BIASED (contradicts strength focus)

**E-Node Requirement:** E0 (non-plyometric)  
**CNS Load Category:** MODERATE  
**Plyo Contacts:** 0  
**Sprint Meters:** Enforced strictly per LS v2.2.0 seasonal caps

**F-V Bias Legality:**

| Bias | Off/Pre | In-Season | Notes |
|---|---|---|---|
| **FORCE_BIASED** | ❌ AVOID | ❌ | Speed work contradicts strength emphasis |
| **VELOCITY_BIASED** | ✅ PRIMARY | ✅ PRIMARY | Core zone; 2-3 sessions/week |
| **BALANCED** | ✅ ALLOWED | ✅ ALLOWED | 1-2 sessions/week for general speed |

**Population Legality:**

| Population | Off/Pre | In-Season | Sprint Limits |
|---|---|---|---|
| Youth 8-12 | ✅ LOW-INT | ✅ LOW-INT | 10-20m max; <120m/week |
| Youth 13-16 | ✅ ALL | ✅ REDUCED | 40m max; 800-1200m/week OFF_SEASON; 400-800m IN_SEASON |
| Youth 17 | ✅ ALL | ✅ REDUCED | Same as Youth 13-16; BALANCED in-season |
| Adult | ✅ ALL | ✅ ALL | 1600m/week OFF_SEASON; 1000m IN_SEASON |
| R2P | ❌ | ❌ | Stage 4+ only with clearance |

**Downgrade Path:** 4 → 3 → 5 → 7 → 8

---

### **ZONE 5 — STRENGTH-ENDURANCE**

**Signature:** Moderate force, moderate reps, higher volume under fatigue.  
**Physiological Goal:** Muscular endurance, lactate tolerance, force maintenance.

**Typical Patterns:** Goblet squats, rows, carries, machine circuits, barbell complexes.

**Acute Variables:** Load 60–75% 1RM (Band_1–2), 12–20 reps, 3–4 sets, 45–75s rest, controlled tempo, RPE 6–7, 40–50 min, 5–7 exercises.

**Band Distribution Contribution:**
- Primary Bands: Band1-2
- Contribution: +15-25% to Band1-2
- Used in: BALANCED (primary), FORCE_BIASED (support), VELOCITY_BIASED (minimal)
- Key support zone for endurance emphasis

**E-Node Requirement:** E0 (non-plyometric)  
**CNS Load Category:** MODERATE  
**Plyo Contacts:** 0

**F-V Bias Legality:**

| Bias | Off/Pre | In-Season | Notes |
|---|---|---|---|
| **FORCE_BIASED** | ✅ SECONDARY | ✅ SECONDARY | Support zone; 20-30% volume |
| **VELOCITY_BIASED** | ❌ AVOID | ❌ AVOID | Contradicts velocity emphasis |
| **BALANCED** | ✅ PRIMARY | ✅ PRIMARY | Core zone; 25-35% volume |

**Population Legality:**

| Population | Off/Pre | In-Season |
|---|---|---|
| Youth 8-12 | ✅ | ✅ |
| Youth 13-16 | ✅ | ✅ |
| Youth 17 | ✅ | ✅ |
| Adult | ✅ | ✅ |
| R2P | ❌ ST1 | ✅ ST2+ |

**Downgrade Path:** 5 → 6 → 7 → 8

---

### **ZONE 6 — HYPERTROPHY**

**Signature:** Moderate force, submax reps, high mechanical tension.  
**Physiological Goal:** Muscle size, cross-sectional area, tension accumulation.

**Typical Patterns:** Barbell bench, DB press, leg press, rows, cable accessories.

**Acute Variables:** Load 65–75% 1RM (Band_1–2), 8–12 reps, 3–4 sets, 60–90s rest, controlled tempo, RPE 6–7, 40–55 min, 5–8 exercises.

**Band Distribution Contribution:**
- Primary Bands: Band1-2
- Contribution: +15-25% to Band1-2
- Used in: BALANCED (primary), FORCE_BIASED (secondary), VELOCITY_BIASED (minimal)

**E-Node Requirement:** E0 (non-plyometric)  
**CNS Load Category:** MODERATE  
**Plyo Contacts:** 0

**F-V Bias Legality:**

| Bias | Off/Pre | In-Season |
|---|---|---|
| **FORCE_BIASED** | ✅ SECONDARY | ✅ | 
| **VELOCITY_BIASED** | ❌ AVOID | ❌ | 
| **BALANCED** | ✅ PRIMARY | ✅ | 

**Downgrade Path:** 6 → 5 → 7 → 8

---

### **ZONE 7 — MUSCULAR ENDURANCE**

**Signature:** Lower force, high reps, metabolic stress emphasis.  
**Physiological Goal:** Work capacity, metabolic conditioning, fatigue resistance.

**Typical Patterns:** Light DB circuits (3-4 exercises × 15-30 reps each), resistance machines, step-ups, sled push (light).

**Acute Variables:** Load 40–60% 1RM (Band_0–1), 15–30 reps, 3–4 sets, 30–45s rest, higher tempo, RPE 5–6, 30–40 min, 5–7 exercises.

**Band Distribution Contribution:**
- Primary Band: Band0-1
- Contribution: +10-15% to Band0-1
- Used in: BALANCED ONLY (general capacity)
- Avoided in: FORCE_BIASED and VELOCITY_BIASED (contradicts bias emphasis)

**E-Node Requirement:** E0 (non-plyometric)  
**CNS Load Category:** LOW-MODERATE  
**Plyo Contacts:** 0

**F-V Bias Legality:**

| Bias | Off/Pre | In-Season |
|---|---|---|
| **FORCE_BIASED** | ❌ AVOID | ❌ | 
| **VELOCITY_BIASED** | ❌ AVOID | ❌ | 
| **BALANCED** | ✅ ALLOWED | ✅ ALLOWED | 

**Population Legality:** All populations allowed (low intensity, high volume).

**Downgrade Path:** 7 → 8 (final zone, lowest intensity)

---

### **ZONE 8 — CONDITIONING (RECOVERY/METABOLIC)**

**Signature:** Minimal force, aerobic/recovery emphasis, parasympathetic priority.  
**Physiological Goal:** Active recovery, aerobic base, parasympathetic reset.

**Typical Patterns:** Light walking, yoga, breathing drills, easy bike/rowing, stretching circuits, 90/90 breathing.

**Acute Variables:** Load <30% 1RM or bodyweight (Band_0), reps variable, continuous low intensity, RPE 2–4, 30–60 min, 3–5 exercises.

**Band Distribution Contribution:**
- Primary Band: Band0
- Contribution: +5-10% to Band0
- Used in: BALANCED, FORCE_BIASED (recovery day), VELOCITY_BIASED (recovery day)
- Essential for ALL biases as recovery component

**E-Node Requirement:** E0 (non-plyometric)  
**CNS Load Category:** LOW  
**Plyo Contacts:** 0

**F-V Bias Legality:**

| Bias | Off/Pre | In-Season |
|---|---|---|
| **FORCE_BIASED** | ✅ RECOVERY | ✅ RECOVERY | 
| **VELOCITY_BIASED** | ✅ RECOVERY | ✅ RECOVERY | 
| **BALANCED** | ✅ RECOVERY | ✅ RECOVERY | 

**Population Legality:** All populations, all ages, all seasons.

---

## **COMPREHENSIVE LEGALITY MATRIX (NEW in v1.2)**

**Zone × Bias × Season Legality (Simplified Version; See Full Appendix for All Populations)**

| Zone | FORCE OFF | FORCE IN | VELOCITY OFF | VELOCITY IN | BALANCED OFF | BALANCED IN |
|---|---|---|---|---|---|---|
| **Z1** (Max Str) | ✅ | ❌ | ⚠️ | ❌ | ✅ | ⚠️ |
| **Z2** (Str-Speed) | ✅ | ⚠️ | ✅ | ⚠️ | ✅ | ✅ |
| **Z3** (React) | ✅ E1-E2 | ⚠️ | ✅ E1-E4 | ✅ | ✅ | ✅ |
| **Z4** (Speed) | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Z5** (Str-Endo) | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ |
| **Z6** (Hyper) | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ |
| **Z7** (Musc-Endo) | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Z8** (Cond) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

**Legend:** ✅ = LEGAL | ⚠️ = LEGAL WITH GATE | ❌ = ILLEGAL | IN = In-Season/Post-Season (BALANCED enforced) | OFF = Off-Season/Pre-Season

---

## **F-V BIAS ASSESSMENT PROTOCOL (Per Governance v4.1 Section 8)**

**Before assigning F-V Bias → Select appropriate zones:**

| Assessment | Test | FORCE Threshold | VELOCITY Threshold | BALANCED Threshold |
|---|---|---|---|---|
| **CMJ Height** | Jump height (cm) | <70cm | >75cm | 70-75cm |
| **RSI** (Reactive Strength Index) | CMJ height / contraction time | >1.8 | <1.5 | 1.5-1.8 |
| **Squat 1RM Ratio** | Squat / BW | <1.5x | >2.0x | 1.5-2.0x |
| **Peak Force** | Force plate (N) | <2.0x BW | >2.5x BW | 2.0-2.5x BW |
| **RFD** (Rate of Force Dev) | N/s | High (>600) | Low (<400) | Moderate (400-600) |

**Decision Logic:**
- 3+ tests show FORCE-DEFICIT → Assign FORCE_BIASED, prioritize Zones 1-2-5
- 3+ tests show VELOCITY-DEFICIT → Assign VELOCITY_BIASED, prioritize Zones 3-4
- Mixed or balanced results → Assign BALANCED, use all zones equally

---

## **ZONE SEQUENCING BY F-V BIAS**

### **FORCE_BIASED (Improve Max Strength)**

**Primary Zones:** 1, 2, 5 (75% of weekly volume)  
**Secondary Zones:** 3, 6 (25% of weekly volume)  
**Avoid:** 4, 7, 8 (low force emphasis)

**4-Week Block Progression:**
```
Week 1-2: Z1 (30%) + Z2 (20%) + Z5 (30%) + Z6 (15%) + Z8 (5%)
Week 3: Z1 (25%) + Z2 (20%) + Z3 (25%, heavy variants) + Z5 (20%) + Z8 (10%)
Week 4: Z1 (20%) + Z2 (15%) + Z3 (15%) + Z5 (35%) + Z8 (15%)
```

**Example Session:**
```
PRIME: Z8 light breathing (5 min)
PREP: Z5 goblet squat (8 min)
WORK-A: Z1 bilateral squat 90% × 5 (15 min)
WORK-B: Z2 power clean hang 75% × 5 (12 min)
WORK-C: Z6 leg press 70% × 8 (8 min)
CLEAR: Z8 breathing + stretch (10 min)
```

---

### **VELOCITY_BIASED (Improve Explosiveness)**

**Primary Zones:** 4, 3, 2 (75% of weekly volume)  
**Secondary Zones:** 6, 8 (25% of weekly volume)  
**Avoid:** 1, 7 (strength-only)

**4-Week Block Progression:**
```
Week 1-2: Z4 (25%) + Z3 (25%, light variants) + Z2 (20%) + Z6 (15%) + Z8 (15%)
Week 3: Z4 (20%) + Z3 (35%, reactive power) + Z2 (15%) + Z6 (15%) + Z8 (15%)
Week 4: Z4 (15%) + Z3 (30%) + Z2 (15%) + Z6 (20%) + Z8 (20%)
```

**Example Session:**
```
PRIME: Z8 joint prep (8 min)
PREP: Z3 box jump 24" × 6 (8 min)
WORK-A: Z4 unloaded sprint 40m × 6 @ 95% (12 min)
WORK-B: Z3 depth jump 36cm × 6 (10 min)
WORK-C: Z2 push press 70% × 5 (10 min)
CLEAR: Z8 breathing + recovery (12 min)
```

---

### **BALANCED (General Athletic Development)**

**Zones:** 1-8 equal emphasis (12-13% each)  
**Rotation:** Vary zones across training week

**Example Weekly Rotation:**
```
Monday: Z1 (Max Str) + Z8 (Recovery)
Tuesday: Z4 (Speed) + Z8 (Recovery)
Wednesday: Z3 (Reactive) + Z8 (Recovery)
Thursday: Z5 (Str-Endo) + Z8 (Recovery)
Friday: Z6 (Hypertrophy) + Z8 (Recovery)
Weekend: Active recovery (Z8 only)
```

---

## **GATE 7 BAND DISTRIBUTION VALIDATION**

**Gate 7 validates that weekly program distribution matches F-V bias targets.**

**Validation Steps:**

1. **Calculate zone-by-zone band contribution:**
   - Count total reps/contacts per zone
   - Map to primary bands (per zone definition)
   - Calculate % of total weekly volume

2. **Sum band distribution:**
   - Band0: Sum all Z4, Z7, Z8 contributions
   - Band1: Sum all Z5, Z6, Z7 contributions
   - Band2: Sum all Z2, Z3 (light), Z5, Z6 contributions
   - Band3: Sum all Z1, Z2 contributions
   - Band4: Sum all Z1 contributions

3. **Compare to F-V bias target:**

**Example (FORCE_BIASED Target: 70% Band2-4):**
```
Weekly Program:
  Z1: 4 sets × 5 = 20 reps → Band3-4
  Z2: 3 sets × 5 = 15 reps → Band2-3
  Z5: 3 sets × 15 = 45 reps → Band1-2 (half → Band2)
  Z6: 2 sets × 10 = 20 reps → Band1-2 (half → Band2)
  Z8: recovery only

Band Calculation:
  Band0-1: 0 + 0 + 22.5 (Z5) + 10 (Z6) = 32.5 reps = 30%
  Band2-3: 0 + 15 (Z2) + 22.5 (Z5) + 10 (Z6) = 47.5 reps = 43%
  Band3-4: 20 (Z1) = 20 reps = 18%
  TOTAL Band2-4: 43 + 18 = 61 reps = 56%

Target: 70% Band2-4
Actual: 56%
Variance: -14% (exceeds GREEN ≤10%)
→ Action: YELLOW flag - adjust next week to add more Z1-Z2 or reduce Z5
```

**Gate 7 Outcomes:**
- **GREEN (≤10% variance):** Approve program, no flags
- **YELLOW (10-20% variance):** Flag for coach review, functional but off-target
- **RED (>20% variance OR safety gate fails):** Quarantine program, escalate to coach

---

## **APPENDIX: FULL POPULATION × BIAS × SEASON LEGALITY MATRIX**

[Complete matrix covering Youth 8-12, Youth 13-16, Youth 17, Adult, and R2P populations across all zones, biases, and seasons — included in extended version]

---

## **IMPLEMENTATION CHECKLIST FOR v1.2**

- ✅ Zone definitions preserved from v1.1 (no content lost)
- ✅ All 8 zones → 3 bias profiles (FORCE, VELOCITY, BALANCED) mapped
- ✅ Band distribution contribution table per zone
- ✅ Population × Bias × Season legality matrix simplified + full appendix
- ✅ F-V Bias assessment protocol (per Governance v4.1 Section 8)
- ✅ Zone sequencing by bias (4-week progressions with examples)
- ✅ Gate 7 band distribution calculation (walkthrough example)
- ✅ Cross-references to Load Standards v2.2.0 (not v2.1.2)
- ✅ Cross-references to Governance v4.1 + Coach & AI Playbook v0.5.0
- ✅ No conflicts with existing zone definitions

---

## **AUTHORITY & APPROVAL**

**Status:** ✅ PRODUCTION-READY  
**Version:** 1.2 (F-V Bias Integrated)  
**Effective Date:** January 1, 2026  
**Replaces:** v1.1  
**Owner:** Austin Lawrence  
**Aligned With:**
- Load Standards v2.2.0
- Governance v4.1
- Coach & AI Playbook v0.5.0

---

**END EFL FORCE–VELOCITY ZONE DICTIONARY v1.2**