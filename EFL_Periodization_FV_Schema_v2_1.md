# EFL Force-Velocity Periodization Schema v2.1

## 1. Overview

This schema defines the **8 Force-Velocity Zones** used by Elite Fitness Lab to categorize exercises, prescribe intensity, and sequence training phases. It is fully integrated with **Load Standards v2.2.0**, **Governance v4.1**, and **Exercise Library v2.5**, ensuring that every zone prescription is safe, legal, and effective for the assigned population.

**Key integrations:**
- **Load Standards v2.2.0:** F-V Bias Profiles (FORCE_BIASED, VELOCITY_BIASED, BALANCED), band distribution targets, population rules
- **Governance v4.1:** 7-Gate Decision Tree (Gate 2 season declaration, Gate 7 bias validation)
- **Exercise Library v2.5:** Zone tags, E-node classification, plyometric flags

This schema defines how zones map to F-V bias profiles and enables **Gate 7 compliance validation** for weekly program distribution.

---

## 2. The 8 Force-Velocity Zones (v2.0 Definition - Unchanged)

Each exercise in the library is tagged with one or more `fv_zones`. Program Architect selects exercises based on the target zone of the training block.

| Zone ID | Name | Primary Quality | Velocity (m/s) | %1RM / Intensity | Library Tags | E-Node | Is Plyo? | Examples |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Zone_1** | Max Strength | Neural drive, Recruitment | < 0.5 m/s | 85–100% | Squat, Hinge, Push, Pull | E0, E1 | FALSE | Squat - Barbell, Deadlift - Trap Bar |
| **Zone_2** | Strength-Speed | Power (Load-Biased) | 0.5–0.75 m/s | 70–85% | Oly Lifts, Loaded Jumps | E1, E2 | FALSE | Clean - Power, Squat Jump - Loaded, Snatch |
| **Zone_3** | Speed-Strength | Power (Velocity-Biased) | 0.75–1.0 m/s | 30–60% | Elastic Plyos (Mod), Ballistic | E1, E2 | TRUE | Box Jump, Pillar Skip, Med Ball Throw, Countermovement Jump |
| **Zone_4** | Elastic / Reactive | Stiffness, SSC, Shock | > 1.3 m/s | BW / <30% | High-CNS Plyos, Depth Jumps | E3 | TRUE | Depth Jump, Continuous Hurdle Hop, Shock Method |
| **Zone_5** | Strength-Endurance | Capacity, Control | Controlled | 60–75% | Foundational Lifts, Accessories | E0 | FALSE | Goblet Squat (Tempo), DB Press, Split Squat |
| **Zone_6** | Hypertrophy | Muscle Growth, Volume | Controlled | 60–80% | Isolation, Volume Compounds | E0 | FALSE | Lat Pulldown, DB Curl, Leg Extension, Glute Bridge |
| **Zone_7** | Speed (Linear) | Max Velocity | Max | BW | Gait / Locomotion | E1 | TRUE | Sprint - Free, Flying 10s, Max Velocity Runs |
| **Zone_8** | Agility / COD | Change of Direction | Max | BW | Gait / Locomotion | E0, E1 | TRUE | Pro Agility, 5-10-5, Curved Runs, Mirror Drills |

### Key Classification Rules
- **E-Nodes (E1–E3):** Appear in Zones 1–4 and 7–8 to denote neural demand.
- **Is Plyometric:** Only `TRUE` for Zones 3, 4, 7, and 8.
  - *Exception:* Olympic lifts (Zone 1/2) are E1/E2 but `is_plyometric = FALSE`. They do **not** count toward plyo contact ceilings.
- **Zone 4 (Elastic/Reactive):** Reserved strictly for **E3** high-shock drills. Governance blocks this zone for Youth and early Rehab.

---

## 2A. Zone to F-V Bias Mapping (NEW in v2.1)

**Every zone contributes to one or more F-V bias profiles.** Coaches use this table to understand which zones align with their athlete's bias goal.

| Zone | Primary Focus | FORCE_BIASED | VELOCITY_BIASED | BALANCED | Band Contribution |
|---|---|---|---|---|---|
| Z1 | Max Strength | ✅ PRIMARY (70%) | ❌ AVOID | ✅ PRIMARY (20-25%) | Band3-4: +20-25% |
| Z2 | Strength-Speed | ✅ PRIMARY (70%) | ✅ SECONDARY (30%) | ✅ PRIMARY (20-25%) | Band2-3: +15-20% |
| Z3 | Speed-Strength | ⚠️ CONDITIONAL* | ✅ PRIMARY (70%) | ✅ PRIMARY (20-25%) | Band0-2: +15-25% |
| Z4 | Elastic/Reactive | ❌ AVOID | ✅ PRIMARY (70%) | ✅ SECONDARY (15-25%) | Band0-2: +15-20% |
| Z5 | Strength-Endurance | ✅ SECONDARY (30%) | ❌ AVOID | ✅ PRIMARY (25-30%) | Band1-2: +15-25% |
| Z6 | Hypertrophy | ✅ SECONDARY (30%) | ❌ AVOID | ✅ PRIMARY (25-30%) | Band1-2: +15-25% |
| Z7 | Speed (Linear) | ❌ AVOID | ✅ PRIMARY (70%) | ✅ ALLOWED (15-20%) | Band0-1: +10-15% |
| Z8 | Agility/COD | ✅ RECOVERY | ✅ RECOVERY | ✅ RECOVERY (10-15%) | Band0-1: +5-10% |

**Z3 CONDITIONAL:**
- If load >50% 1RM (heavy variants): FORCE_BIASED secondary (Z3 heavy = strength emphasis)
- If load <50% 1RM (light variants): VELOCITY_BIASED primary (Z3 light = speed emphasis)

**Gate 7 Logic:** 
- For FORCE_BIASED, target 70% weekly volume in (Z1+Z2+Z5+Z6) = Band2-4 heavy zones.
- For VELOCITY_BIASED, target 70% in (Z3+Z4+Z7+Z8) = Band0-2 velocity zones.
- For BALANCED, target 50/50 across all bands.

---

## 2B. Band Distribution by Zone (NEW in v2.1, for Gate 7 Calculation)

**Each zone's primary band range determines its contribution to weekly band distribution.**
Load Standards v2.2.0 defines Band_0 through Band_4 by %1RM (Band_0 = <30%, Band_4 = 90-100%).

| Zone | %1RM Range | Primary Band(s) | Secondary Band(s) | Weekly Contribution |
|---|---|---|---|---|
| Z1 (Max Strength) | 85-100% | Band4 (90-100%) | Band3 (80-90%) | 20-25% to Band3-4 |
| Z2 (Strength-Speed) | 70-85% | Band2 (60-75%), Band3 (80-90%) | | 15-20% to Band2-3 |
| Z3 (Speed-Strength) | 30-60% | Band0-2 (varies by load) | | 15-25% to Band0-2 |
| Z4 (Elastic/Reactive) | <30% BW | Band0-1 (<30%) | | 15-20% to Band0-1 |
| Z5 (Strength-Endurance) | 60-75% | Band1-2 (55-75%) | | 15-25% to Band1-2 |
| Z6 (Hypertrophy) | 60-80% | Band1-2 (55-80%) | | 15-25% to Band1-2 |
| Z7 (Speed - Linear) | BW (unloaded) | Band0-1 (<30%) | | 10-15% to Band0-1 |
| Z8 (Agility/COD) | BW (unloaded) | Band0-1 (<30%) | | 5-10% to Band0-1 |

**Gate 7 Example (FORCE_BIASED, target 70% Band2-4):**
```
Weekly Program:
  Z1: 4 sets × 5 = 20 reps → Band3-4 (contributes +20% of total)
  Z2: 3 sets × 5 = 15 reps → Band2-3 (contributes +15% of total)
  Z5: 3 sets × 15 = 45 reps → Band1-2 (contributes +45% of total)
  
Band Distribution Calculation:
  Band0-1: 0%
  Band1-2: 45%
  Band2-3: 15%
  Band3-4: 20%
  
Total Band2-4: 15% + 20% = 35% (FAR below 70% target)
→ YELLOW FLAG: Program has too much Z5 (endurance), not enough Z1-Z2 (strength)
→ ACTION: Increase Z1-Z2 volume or reduce Z5 for next week
```

---

## 3. Phase-Based Zone Availability & Governance

Program Architect enforces these overlays to ensure legal programming.

### A. Youth Lab (Ages 8–12)
- **Primary Zones:** Zone 5, Zone 6 (Movement Quality & Capacity).
- **Secondary Zones:** Zone 8 (Game Speed / Agility).
- **Conditional:** Zone 3 (E1 only) – *Must use low-amplitude drills (e.g., Pillar Skips, Pogo).*
- **Blocked:** Zone 1, Zone 2, Zone 4, Zone 7 (Max V).
- **Plyo Ceiling:** Max 50 contacts/session (Zones 3 & 8 combined).
- **F-V Bias:** BALANCED only (enforced, no override).

### B. SP Foundation (HS / Adult Novice)
- **Primary Zones:** Zone 5, Zone 6 (GPP), Zone 3 (Intro Plyo E1).
- **Secondary Zones:** Zone 8 (Agility), Zone 1 (Technique Only).
- **Blocked:** Zone 4 (No Shock Method), Zone 2 (Unless technique cleared).
- **Plyo Ceiling:** Max 80 contacts/session (E1 only).
- **F-V Bias:** BALANCED only (enforced per Governance v4.1).

### C. SP Development (HS Intermediate)
- **Primary Zones:** Zone 1 (Strength), Zone 2 (Power), Zone 3 (Elastic E2).
- **Secondary Zones:** Zone 7 (Speed), Zone 8 (Agility).
- **Blocked:** Zone 4 (E3) – *Unless specific gate passed.*
- **Plyo Ceiling:** 80–100 contacts/session (E1–E2).
- **F-V Bias:** FORCE_BIASED (off-season/pre-season only; BALANCED enforced in-season per Gate 2).

### D. SP Power (Elite / Collegiate / Advanced)
- **Primary Zones:** Zone 1, Zone 2 (Peak Power), Zone 4 (E3 Shock).
- **Secondary:** Zone 7 (Max Velocity).
- **Plyo Ceiling:** Max 120 contacts/session (E1–E3).
- **F-V Bias:** FORCE_BIASED, VELOCITY_BIASED, or BALANCED (seasonal control via Gate 2).

### E. R2P / Rehab Stages
- **Stage 1 (Reactivation):** Zone 5/6 (Tempo/Iso), Zone 8 (Walk/Jog). **No Plyo (Zone 3/4 blocked).**
- **Stage 2 (Load):** Zone 5 (Progression). Zone 3 (E1 only, low amp).
- **Stage 3 (Sport Prep):** Zone 2 (Power Intro), Zone 3 (E2 Plyo Return).
- **Stage 4 (Return to Sport):** Full Spectrum (Zones 1–8).
- **F-V Bias:** BALANCED only (enforced, medical priority overrides performance).

---

## 3F. F-V Bias Rules by Population & Season (NEW in v2.1, per Governance v4.1 Section 2.8)

**CRITICAL:** These rules are mandatory and override zone selection. If bias is illegal for the population/season, the entire program is DENIED (Gate 2 failure).

### Youth 16 and Under
- **F-V Bias Allowed:** BALANCED only (enforced, no override)
- **Season:** All seasons (OFF, PRE, IN, POST) = BALANCED enforced
- **Zone Impact:** Only BALANCED-primary zones allowed (Z5, Z6, Z8, Z3 light, Z2 bridge)
- **Zone Restriction:** Z1, Z4, Z7 forbidden

### Youth 17 Advanced (2+ years training age, documented)
- **F-V Bias Allowed:**
  - OFF_SEASON / PRE_SEASON: FORCE_BIASED (60/40 max, Director approval) OR BALANCED
  - IN_SEASON / POST_SEASON: BALANCED enforced (bias override)
- **Zone Impact:**
  - If FORCE_BIASED + OFF_SEASON: Z1-Z2-Z5 primary (70%), Z3-Z6 secondary (30%)
  - If BALANCED (any season): Z1-Z8 general rotation (12% each)
- **Gate 2 Logic:** Season declaration forces bias reset if needed

### Adult (18+, 2+ years training age)
- **F-V Bias Allowed:**
  - OFF_SEASON / PRE_SEASON: FORCE_BIASED, VELOCITY_BIASED, or BALANCED
  - IN_SEASON / POST_SEASON: BALANCED enforced (bias override)
- **Zone Impact:**
  - FORCE_BIASED: Z1-Z2-Z5 primary (70%), Z3-Z6 secondary (30%), avoid Z4-Z7
  - VELOCITY_BIASED: Z3-Z4-Z7 primary (70%), Z2-Z6 secondary (30%), avoid Z1-Z5
  - BALANCED: Z1-Z8 equal (12% each weekly)

### R2P (Return to Performance, All Stages)
- **F-V Bias:** BALANCED only (enforced, medical priority)
- **Zone Impact:**
  - Stage 1-2: Z5-Z6 only (NO plyos)
  - Stage 3: Z5-Z6 + Z3 (E1 light)
  - Stage 4: Z1-Z8 allowed (with clearance gates)
- **Override:** Medical priority overrides performance optimization; no exception

---

## 4. Programming Logic for Architect

When building a session, the engine selects exercises based on the **Block Goal**:

### 1. Goal = Hypertrophy / Capacity
- **Target:** Zones 5, 6.
- **Selection:** `e_node_classification = E0`.
- **Volume:** Higher reps (8–12), moderate load.

### 2. Goal = Max Strength
- **Target:** Zone 1.
- **Selection:** `e_node_classification = E0` (Heavy Lifts) or E1 (Neural Lifts).
- **Governance:** Must verify client is NOT Youth.

### 3. Goal = Power (Velocity-Biased)
- **Target:** Zone 3.
- **Selection:** `e_node_classification ∈ {E1, E2}` AND `is_plyometric = TRUE`.
- **Check:** Sum of plyo contacts must remain below session ceiling.

### 4. Goal = Power (Load-Biased)
- **Target:** Zone 2.
- **Selection:** `e_node_classification ∈ {E1, E2}` AND `is_plyometric = FALSE` (Oly lifts, Loaded Jumps).
- **Check:** No contact cost, but high CNS cost.

### 5. Goal = Speed / Agility
- **Target:** Zones 7, 8.
- **Selection:** `movement_pattern = Gait` or `Locomotion`.
- **Check:** Sprint volume ceiling (meters) per Appendix J.

---

## 4A. Zone Sequencing by F-V Bias (NEW in v2.1)

**When a coach assigns an athlete a specific F-V bias, which zones should be prioritized each week?** This section provides 4-week progressions.

### FORCE_BIASED (Improve Max Strength)

**4-Week Block Progression:**

| Week | Z1 (Strength) | Z2 (Power) | Z3 (React) | Z5 (Endo) | Z6 (Hyper) | Z7 (Speed) | Z8 (Agility) |
|---|---|---|---|---|---|---|---|
| 1-2 | 35% | 20% | 5% | 25% | 10% | 0% | 5% |
| 3 | 30% | 20% | 15% | 20% | 10% | 0% | 5% |
| 4 (Deload) | 20% | 15% | 10% | 35% | 15% | 0% | 5% |

**Zone Selection Rules:**
- Prioritize Z1 (heavy squats, deadlifts 85-100% 1RM)
- Z2 support (power cleans 75-85%, load-biased power)
- Z3 heavy variants only (loaded jumps 50-60%, not plyos)
- Z5 maintenance (goblet squats, tempo work)
- Avoid Z4 (shock) and Z7 (pure speed)
- Z8 recovery only (agility drills)

**Example Week 1 Session:**
```
WORK-A: Z1 Bilateral Squat 90% × 5 (35%)
WORK-B: Z2 Power Clean 75% × 5 (20%)
WORK-C: Z5 Goblet Squat 70% × 10 (25%)
WORK-D: Z6 Leg Press 70% × 8 (10%)
CLEAR: Z8 Breathing/Agility (5%)
```

### VELOCITY_BIASED (Improve Explosiveness)

**4-Week Block Progression:**

| Week | Z1 | Z2 | Z3 (React) | Z4 (Shock) | Z5 | Z6 | Z7 (Speed) | Z8 (COD) |
|---|---|---|---|---|---|---|---|---|
| 1-2 | 0% | 10% | 20% | 20% | 0% | 10% | 20% | 20% |
| 3 | 0% | 10% | 25% | 30% | 0% | 5% | 20% | 10% |
| 4 (Deload) | 5% | 10% | 15% | 15% | 10% | 10% | 20% | 15% |

**Zone Selection Rules:**
- Prioritize Z4 (depth jumps, shock work, E3)
- Z3 light variants (box jumps 24", reactive power)
- Z7 speed (maximal velocity sprints 40m+, 95-100% Vmax)
- Z2 minimal bridge (maintains strength substrate)
- Avoid Z1 (max strength contradicts velocity focus)
- Z5 minimal (only if time permits)
- Z8 agility for change-of-direction

**Example Week 2 Session:**
```
PREP: Z3 Box Jump 24" × 6 warm-up (8 min)
WORK-A: Z4 Depth Jump 36" × 6 (20%)
WORK-B: Z7 40m Sprint @ 95% Vmax × 5 (20%)
WORK-C: Z3 Reactive Box Jump 24" × 8 (20%)
WORK-D: Z2 Push Press 70% × 5 (10%)
CLEAR: Z8 Agility Cool-down (5%)
```

### BALANCED (General Athletic Development)

**Weekly Rotation (All 8 Zones Equal):**

```
Monday: Z1 Max Strength (12%)
  - Squat 85% × 5, Deadlift 85% × 3, Assistance

Tuesday: Z7 Speed (12%)
  - 40m Sprint × 6 @ 95% Vmax, COD drills, acceleration

Wednesday: Z3 Reactive Power (12%)
  - Box Jumps 24" × 6, Med Ball Throws, Bounding

Thursday: Z5 Strength-Endurance (12%)
  - Goblet Squats 12 reps, Rows 12 reps, Carries

Friday: Z6 Hypertrophy (12%)
  - Leg Press 8-10 reps, DB Work, Isolation

Weekend: Z4 Elastic (12%) + Z8 Recovery (16%)
  - Light mobility, breathing, parasympathetic reset
  
= 12% × 8 = 96% + 4% buffer = 100% weekly distribution
```

---

## 5. Integration with Exercise Library v2.5

- **Aether Pattern:** Maps exercise to family (e.g., `Plyometric-Landing` → Zone 3/4, `Squat-Bilateral` → Zone 1/5/6).
- **E-Node:** Determines neural demand (E0 vs E1–E3).
- **Is Plyometric:** Determines if contacts are counted.
- **FV Zones:** Explicit tag listing valid zones for each exercise.

*This schema is the strict logic layer for determining "What can I program today?" relative to the Force-Velocity curve.*

---

## 6. Gate 7 F-V Bias Compliance Validation (NEW in v2.1)

**Gate 7 validates that the weekly program's zone distribution matches the assigned F-V bias targets.**
This schema provides the zone-to-band mapping needed for Gate 7 calculation.

### Gate 7 Validation Process

**Step 1: Calculate zone volume per week**
- Count total reps/contacts per zone
- Total = sum of all zone reps/contacts

**Step 2: Map zones to band contribution**
- Use table from Section 2B
- Example: If Z1 = 20 reps and total = 100 reps, then Z1 contributes 20%

**Step 3: Sum band distribution**
- Band0-1: Sum contributions from Z4 + Z7 + Z8
- Band1-2: Sum contributions from Z5 + Z6 + (Z3 light variants)
- Band2-3: Sum contributions from Z2 + (Z3 heavy variants)
- Band3-4: Sum contributions from Z1

**Step 4: Compare to F-V bias target**
- FORCE_BIASED target: 70% in Band2-4 (strength bands)
- VELOCITY_BIASED target: 70% in Band0-2 (velocity bands)
- BALANCED target: 50/50 across all bands

**Step 5: Apply variance thresholds**
- Variance ≤ 10%: GREEN (approve program)
- Variance 10-20%: YELLOW (flag for coach review, functional but off-target)
- Variance > 20%: RED (quarantine program, escalate to coach)

### Example Gate 7 Calculation (FORCE_BIASED)

```
Weekly Program:
  Z1: 20 reps (Band3-4)
  Z2: 15 reps (Band2-3)
  Z3: 0 reps
  Z4: 0 reps
  Z5: 45 reps (Band1-2)
  Z6: 0 reps
  Z7: 0 reps
  Z8: 20 reps (Band0-1)
  Total: 100 reps

Band Calculation:
  Band0-1: 20 (Z8 only) = 20%
  Band1-2: 45 (Z5 only) = 45%
  Band2-3: 15 (Z2) = 15%
  Band3-4: 20 (Z1) = 20%
  
Total Band2-4: 15% + 20% = 35%
Target (FORCE): 70%
Variance: 70% - 35% = 35% BELOW TARGET

Gate 7 Result: RED ❌
Reason: Too much Z5 (endurance), not enough Z1-Z2 (strength)
Action: Coach must rebuild program with more Z1-Z2 volume
```

---

## Version History

| Version | Date | Changes |
|---|---|---|
| v2.0 | 2025-12-22 | Initial release; 8-zone framework, population-based legality |
| v2.1 | 2025-12-24 | **NEW:** F-V Bias mapping (Section 2A), band distribution (Section 2B), F-V Bias rules (Section 3F), zone sequencing by bias (Section 4A), Gate 7 integration (Section 6); updated authority references (Load Standards v2.2.0, Governance v4.1, Exercise Library v2.5) |

---

**Authority:** Load Standards v2.2.0, Governance v4.1, Exercise Library v2.5

**Effective:** January 1, 2026

**Next Review:** March 31, 2026 (post-deployment feedback cycle)