# EFL GOVERNANCE LAYER — v4.1 OPERATIONAL

**Version:** 4.1 (Load Standards v2.2.0 Aligned)  
**Status:** OPERATIONAL — Ready for Production  
**Date:** 2025-12-22  
**Scope:** Unified Governance System (System 1) for EFL Ecosystem  
**Effective:** 2025-12-22  
**Supersedes:** v4.0 (2025-12-15)

---

# EXECUTIVE SUMMARY

This document is the **Operating System for Elite Fitness Lab**. It defines:

1. **The 4-level hierarchy** that governs all programming decisions
2. **The Client State Engine** that computes what each athlete can legally do
3. **The 7-Gate Decision Tree** that validates every exercise (NEW: Gate 7 = F-V Bias)
4. **MicroSessions enforcement** (Adult + Athlete codices fully integrated)
5. **Service Line routing** with legal bounds
6. **F-V Bias Integration** (NEW in v4.1 — Layer 3 Force-Velocity Targeting)
7. **Integration points** with System 2 (Force-Velocity Engine) and System 3 (Program Architect)

All downstream training generation (meso/macro cycles, acute variables, progression) flows through these gates.

---

# MAJOR CHANGES IN v4.1

## Critical Updates from v4.0 → v4.1

1. **Load Standards Reference Updated:** Now uses **EFL_LOAD_STANDARDS_v2_2_0.json** (effective 2025-12-22) with complete Layer 3 Force-Velocity targeting framework.

2. **Gate 7 Added:** New Force-Velocity Bias Compliance Check validates program distribution matches selected bias targets (FORCE_BIASED, VELOCITY_BIASED, or BALANCED).

3. **Client State Enhanced:** Added `fv_bias_context` field to compute F-V bias legality, restrictions, and compliance.

4. **Youth Protection Enforced:** Youth 16 and under = BALANCED ONLY (no override possible). Youth 17 Advanced = Conditional FORCE_BIASED only (max 60/40 split).

5. **In-Season Enforcement:** BALANCED bias required for IN_SEASON (except Tier 3 low fixture density with approval).

6. **Band:Tier Ratio Validation:** Gate 7 checks that distribution matches bias targets (70/30 force emphasis for FORCE_BIASED, 70/30 velocity emphasis for VELOCITY_BIASED).

7. **Weekly Distribution Validator:** Tracks actual program composition vs target distribution, flags deviations (YELLOW 10-20%, RED >20%).

8. **F-V Bias Diagnostics Integration:** CMJ profiling, F-V slope testing, practical assessments inform bias selection.

9. **Coaching Decision Tree Added:** Step-by-step guide for coaches to select appropriate bias for their athlete.

10. **Backward Compatibility Maintained:** If `fvBiasProfile` not set or = BALANCED, system behaves identically to v4.0.

---

# SECTION 1: FOUNDATION & PRECEDENCE RULES

## 1.1 Governance Stack Hierarchy

The EFL system operates on a **deterministic precedence stack**. When rules conflict, this hierarchy decides:

### Level 1: SAFETY GATES (Absolute Veto)
These are non-negotiable. No override possible without medical/legal exemption.

- **Population Legal Gates:** Youth (8-12), Youth (13-17), Youth (17 Advanced), Adult, R2P_Stage1-4
- **F-V Bias Gates:** Youth ≤16 = BALANCED enforced; Youth 17 = FORCE only; Adult = all bias types allowed
- **Load Ceiling Gates:** Population + Season + R2P combination determines max band
- **Node Legality Gates:** What nodes are legal for each population/stage
- **Injury-Specific Gates:** Contraindications per injury type (ACL, Shoulder, Knee, Ankle)

**Source:** Codex §4.1, EFL_LOAD_STANDARDS_v2_2_0.json, AETHER Schema v1.1

---

### Level 2: PROGRAMMING RULES (Must Follow)
These govern session structure, progression, and frequency. Can be modified only by Austin.

- **Block Assignment Rules:** Block Selector v2.2 outputs block; all exercises in that block must be legal
- **Seasonal Constraints:** Sport Demands Grid + Load Standards season rules
- **F-V Bias Targeting:** Gate 7 validates distribution matches bias targets
- **R2P Progression Gates:** Stage-to-stage transitions require performance thresholds
- **Service-Line Rules:** Adult Strength ≠ Youth Lab ≠ Rehab; each has its own set/rep/frequency laws
- **Weekly Frequency & Budget Laws:** Per-pattern cap, per-band cap, per-CNS cap

**Source:** Codex §3.0-5.0, Appendix J Global Laws, Load Standards v2.2.0

---

### Level 3: SERVICE CONTEXT (Shapes Application)
These define who the client is and how to apply rules to them.

- **ICP Classification:** Who are they? (Adult Strength, Youth Athlete, R2P, etc.)
- **Price Tier:** What service are they purchasing?
- **F-V Bias Profile:** FORCE_BIASED, VELOCITY_BIASED, BALANCED, or null (default)
- **Readiness Metrics:** What is their current state? (Stress, Sleep, Injury, Skill)
- **Season Context:** In-season, Off-season, Prep, Competition?

**Source:** Price Sheet v1.0, ICP definitions, Athlete Profile Schema, Load Standards v2.2.0

---

### Level 4: EXERCISE SELECTION (Details Implementation)
These are **the exercises we use**. They must be legal under Levels 1-3.

- **AETHER Metadata:** Node, Difficulty, Load Band, Population Gates, etc.
- **Load Band Assignment:** Band_0-4 per exercise (BA Exercise Library v2.5)
- **F-V Classification:** Which zones and bias profiles the exercise supports
- **Multi-Band Flexibility:** Min/Max ranges per exercise for load scaling
- **Movement Pattern:** Strength, Plyo, Mobility, etc.

**Source:** AETHER Schema v1.1, BA Exercise Library v2.5, Load Standards v2.2.0

---

## 1.2 Conflict Resolution Precedence

When rules from different layers conflict, **this is the precedence order:**

```
LEVEL 1 (Safety Gates) OVERRIDES everything
    ↓
LEVEL 2 (Programming Rules) OVERRIDES Levels 3-4
    ↓
LEVEL 3 (Service Context) OVERRIDES Level 4
    ↓
LEVEL 4 (Exercise Selection) applies within all constraints above
```

---

## 1.3 The Client State Object (Complete Schema)

Every programming decision begins here. This is the **single source of truth** about what a client can legally do.

```json
{
  "client_id": "CLN_001",
  "icp_classification": "Adult_Strength",
  "service_line": "Adult_Strength",
  "service_tier": "Premium",
  
  "population_context": {
    "age_group": "Adult",
    "chronological_age": 35,
    "max_population_band": "Band_4",
    "max_population_node": "D",
    "population_gate": "ADULT"
  },
  
  "fv_bias_context": {
    "fv_bias_profile": "FORCE_BIASED",
    "bias_allowed": true,
    "bias_selection_rationale": "Squat 1.4x BW, RSI 2.1, low peak force 1680N",
    "diagnostic_data": {
      "cmj_height_cm": 68,
      "rsi": 2.1,
      "squat_bw_ratio": 1.4,
      "peak_force_n": 1680,
      "assessment_date": "2025-12-20",
      "assessment_type": "CMJ_PROFILING"
    },
    "bias_band_targets": {
      "Band0": "5-10%",
      "Band1": "10-20%",
      "Band2": "25-35%",
      "Band3": "25-35%",
      "Band4": "5-15%"
    },
    "bias_plyo_targets": {
      "E0": "unlimited",
      "E1": "20-30%",
      "E2": "15-25%",
      "E3_E4": "5-10%"
    },
    "bias_sprint_volume": "Lower end (minimal velocity emphasis)",
    "session_frequency": {
      "strength": "4-5x/week",
      "elastic": "2x/week",
      "sprint": "1x/week"
    },
    "bias_restrictions": {
      "youth_16_under": "BALANCED enforced, no override",
      "youth_17": "FORCE_BIASED moderate only, 60/40 max, Director approval required",
      "adult_elite": "All bias types allowed, 70/30 splits allowed",
      "in_season": "BALANCED enforced (except Tier 3 low fixture density)"
    },
    "bias_compliance_status": null
  },
  
  "r2p_context": {
    "is_r2p": false,
    "stage": null,
    "max_r2p_band": null,
    "max_r2p_node": null,
    "r2p_gate": null
  },
  
  "season_context": {
    "current_season": "Off_Season",
    "sport": "Basketball",
    "season_load_mod": "NORMAL",
    "season_max_band": "Band_4",
    "season_max_node": "D",
    "season_gate": "OFF_SEASON"
  },
  
  "injury_context": {
    "active_injuries": [],
    "affected_nodes": [],
    "affected_bands": [],
    "injury_gates": []
  },
  
  "readiness_context": {
    "sleep_score": 8,
    "stress_score": 4,
    "rpe_fatigue": 3,
    "readiness_flag": "GREEN"
  },
  
  "COMPUTED_LEGALITY": {
    "max_band_allowed": "Band_4",
    "max_node_allowed": "D",
    "max_e_node_allowed": "E2",
    "contacts_allowed": 240,
    "allowed_services": ["Adult_Strength", "SP_Performance"],
    "forbidden_services": ["Youth_Lab", "R2P"],
    "required_rules": ["ADULT_LOAD_CEILING", "GREEN_READINESS"],
    "gate_7_status": "PENDING_VALIDATION"
  }
}
```

### How COMPUTED_LEGALITY is Calculated

**Max Band Allowed** = Most restrictive of:
- Population max band
- R2P max band
- Season max band
- Injury max band
- Readiness adjustment

**Max Node Allowed** = Most restrictive of:
- Population max node
- R2P max node
- Injury contraindications

**max_e_node_allowed** (Elasticity ceiling) = Most restrictive of:
- Population max E-node
- R2P max E-node
- Season E restrictions
- Readiness (RED = E0_only)

**contacts_allowed** (Plyo contact ceiling) = Based on:
- Age tier (Youth 8-12: 50/80, Youth 13-17: 80/120, Adult: 100/140)
- Service line (Athlete vs Adult MicroSessions)
- Season fixture density
- Readiness flag (RED = 0, YELLOW = -20%)

**bias_compliance_status** (NEW) = Computed by Gate 7:
- Matches actual program distribution to bias targets
- Returns: GREEN (within ±10%), YELLOW (10-20% off), RED (>20% off or safety violation)

---

## 1.4 Binding Rules Between Systems

These rules **enforce integration** between the 4 layers and Systems 2-3.

### Rule 1: Load Standards ALWAYS WIN over Service Tier
If Load Standards define a population ceiling (e.g., "Youth max Band_1"), that ceiling applies regardless of service tier.

---

### Rule 2: R2P Stage Gates OVERRIDE Season Gates
R2P progression requirements override seasonal load reduction rules.

---

### Rule 3: Injury Contraindications ALWAYS VETO
If an exercise is contraindicated for a specific injury, it is forbidden. No exception.

---

### Rule 4: Block Selector Output is ADVISORY, Not Final
Block Selector suggests a block. The exercises within must pass legality checks. If they don't, substitute.

---

### Rule 5: MicroSessions MUST RESPECT Governance Ceilings
MicroSessions must comply with population ceilings and seasonal restrictions.

---

### Rule 6: No Loosening Rule (CRITICAL)
**Governance may ONLY ever tighten ceilings. It may NEVER expand them.**

---

### Rule 7: System-2 Integration (FV Zone + F-V Bias Validation)
When System 2 (Force-Velocity Engine) outputs a training zone:

**Implementation:**
```
IF System2_outputs(zone):
  VALIDATE(zone against client.max_band, client.max_node, client.max_e_node_allowed)
  VALIDATE(zone against season_legality[current_season])
  VALIDATE(zone against service_line_zone_legality[service_line])
  VALIDATE(zone against fv_bias_targets if bias profile set)
  IF any validation FAILS:
    QUARANTINE zone, RECOMMEND legal alternatives
```

---

### Rule 8: Gate 7 Integration (F-V Bias Compliance) — NEW
Before program approval, Gate 7 validates that weekly program distribution matches selected F-V bias targets:

**Implementation:**
```
IF fv_bias_profile NOT in [null, BALANCED]:
  CALCULATE actual_band_distribution from weekly_program
  CALCULATE actual_plyo_distribution from weekly_program
  COMPARE to fv_bias_profile.targets
  IF within ±10% AND all safety gates passed:
    bias_compliance_status = GREEN ✅
  ELSE IF 10-20% off AND safety gates passed:
    bias_compliance_status = YELLOW ⚠️
  ELSE IF >20% off OR safety violation:
    bias_compliance_status = RED ❌ QUARANTINE
ELSE:
  bias_compliance_status = PASS (no targets)
```

---

# SECTION 2: CLIENT STATE ENGINE

## 2.1 Overview

The Client State Engine takes **raw input** (age, injury, stress, season, F-V bias) and computes **legal bounds** (max band, max node, max_e_node_allowed, contacts_allowed, bias_targets).

It answers: **"Given this client, what can I legally do?"**

---

## 2.2 Input Data Sources

| Source | Example Fields | Source Doc |
|--------|---|---|
| **ICP & Intake** | age, population, sport, service_tier, fv_bias_profile | Price Sheet v1.0, ICP definitions |
| **Load Standards** | population_band_ceiling, season_adjustment, bias_profiles | EFL_LOAD_STANDARDS_v2_2_0.json |
| **Diagnostics** | cmj_height, rsi, squat_bw_ratio, peak_force | Athlete Profile Schema v1.1 |
| **Readiness Metrics** | sleep_score (1-10), stress_score (1-10), rpe_fatigue (1-10) | Athlete Profile Schema v1.1 |
| **Medical/Rehab** | active_injuries, r2p_stage, medical_flags | AETHER Schema, Codex §2.3 |

---

## 2.3 Step 1: Determine Population Base Ceiling

```
IF age <= 12:
  population_band_ceiling = Band_1
  population_node_ceiling = B
  population_name = "Youth_8_12"
  fv_bias_allowed = false (BALANCED enforced)
  
ELSE IF age <= 16:
  population_band_ceiling = Band_2
  population_node_ceiling = C
  population_name = "Youth_13_16"
  fv_bias_allowed = false (BALANCED enforced)
  
ELSE IF age == 17:
  population_band_ceiling = Band_2
  population_node_ceiling = C
  population_name = "Youth_17_Advanced"
  fv_bias_allowed = CONDITIONAL (FORCE_BIASED moderate only, max 60/40)
  
ELSE IF age >= 18:
  population_band_ceiling = Band_4
  population_node_ceiling = D
  population_name = "Adult"
  fv_bias_allowed = true (all bias types)
```

---

## 2.4 Step 2: Apply R2P Stage Restrictions

If the client is in Return-to-Play, R2P rules override population ceilings.

```
IF r2p_stage == 1 (Reactivation):
  r2p_band_ceiling = Band_0
  r2p_node_ceiling = A
  fv_bias_allowed = false (BALANCED only)
  
ELSE IF r2p_stage == 2 (Progressive Loading):
  r2p_band_ceiling = Band_1
  r2p_node_ceiling = B
  fv_bias_allowed = false (BALANCED only)
  
ELSE IF r2p_stage == 3 (Sport Integration):
  r2p_band_ceiling = Band_2
  r2p_node_ceiling = C
  fv_bias_allowed = false (BALANCED only)
  
ELSE IF r2p_stage == 4 (Full Return):
  r2p_band_ceiling = Band_3
  r2p_node_ceiling = D
  fv_bias_allowed = conditional (depends on progress)
```

---

## 2.5 Step 3: Apply Injury-Specific Contraindications

Injuries create **hard vetoes**. No exercises allowed that violate the injury gate.

---

## 2.6 Step 4: Apply Season Load Adjustments

Seasonal context modifies load ceilings (but does NOT override Safety Gates).

```
IF season == "Off_Season":
  season_mod = 0% (no reduction)
  fv_bias_allowed = true (if population allows)
  
ELSE IF season == "Prep_Season":
  season_mod = -20%
  season_max_band = population_ceiling - 0.5
  fv_bias_allowed = true (if population allows)
  
ELSE IF season == "In_Season":
  season_mod = -40% to -60%
  season_max_band = population_ceiling - 1.0
  fv_bias_allowed = false (BALANCED enforced, except Tier 3)
  
ELSE IF season == "Post_Season":
  season_mod = -50%
  fv_bias_allowed = false (BALANCED enforced)
```

---

## 2.7 Step 5: Apply Readiness Real-Time Adjustments

Readiness metrics modify load **on a session-by-session basis** (temporary).

```
readiness_score = (sleep_score + (10 - stress_score) + (10 - rpe_fatigue)) / 3

IF readiness_score >= 8.0:
  readiness_status = "GREEN"
  load_mod = +0% (use full ceiling)
  
ELSE IF readiness_score >= 6.0:
  readiness_status = "YELLOW"
  load_mod = -1 band
  max_band = Max(Band_0, max_band - 1)
  max_e_node_allowed = E0_only (restrict elasticity)
  contacts_allowed = contacts_allowed * 0.8
  
ELSE IF readiness_score < 6.0:
  readiness_status = "RED"
  load_mod = -2 bands
  max_band = Max(Band_0, max_band - 2)
  max_e_node_allowed = E0_only (strictly no elasticity)
  contacts_allowed = contacts_allowed * 0.5
```

---

## 2.8 Step 6A: Compute F-V Bias Legality — NEW

Determine if client can use F-V bias targeting, and if so, which bias profile.

```
IF age <= 16:
  fv_bias_allowed = false
  fv_bias_profile_forced = BALANCED
  override_possible = false
  
ELSE IF age == 17 AND training_age >= 2 AND documentation_complete:
  fv_bias_allowed = CONDITIONAL
  allowed_profiles = [FORCE_BIASED (moderate), BALANCED]
  forbidden_profiles = [VELOCITY_BIASED]
  ratio_max = 60/40 (never 70/30 like adults)
  requires_director_approval = true
  
ELSE IF age >= 18 AND training_age >= 2:
  fv_bias_allowed = true
  allowed_profiles = [FORCE_BIASED, VELOCITY_BIASED, BALANCED]
  ratio_max = 70/30 (or 30/70 for velocity)
  requires_testing_or_rationale = true
  
ELSE:
  fv_bias_allowed = false
  fv_bias_profile_forced = BALANCED

IF season IN [In_Season, Post_Season] AND tier != Tier_3:
  OVERRIDE: fv_bias_allowed = false
  fv_bias_profile_forced = BALANCED
  reason = "Seasonal enforcement"
```

---

## 2.9 Step 7: Compute Final Legal Bounds

```python
def compute_client_legality(client):
  
  # Step 1: Population baseline
  pop_band = POPULATION_CEILINGS[client.age_group]["band"]
  pop_node = POPULATION_CEILINGS[client.age_group]["node"]
  pop_fv_allowed = POPULATION_CEILINGS[client.age_group]["fv_bias_allowed"]
  
  # Step 2: R2P override if applicable
  if client.r2p_stage:
    pop_band = Min(pop_band, R2P_CEILINGS[client.r2p_stage]["band"])
    pop_node = Min(pop_node, R2P_CEILINGS[client.r2p_stage]["node"])
    pop_fv_allowed = false  # R2P = BALANCED only
  
  # Step 3: Injury veto
  for injury in client.active_injuries:
    injury_gate = INJURY_GATES[injury]
    pop_band = Min(pop_band, injury_gate["max_band"])
    pop_node = Min(pop_node, injury_gate["max_node"])
  
  # Step 4: Season adjustment
  season_band = SEASON_MODS[client.season]["max_band"]
  season_node = SEASON_MODS[client.season]["max_node"]
  season_fv_allowed = SEASON_MODS[client.season]["fv_bias_allowed"]
  
  # R2P overrides season
  if client.r2p_stage >= 3:
    season_band = pop_band
    season_node = pop_node
    season_fv_allowed = false
  
  max_band = Min(pop_band, season_band)
  max_node = Min(pop_node, season_node)
  fv_allowed = pop_fv_allowed AND season_fv_allowed
  
  # Step 5: Readiness adjustment (temporary)
  readiness_score = compute_readiness_score(client)
  if readiness_score < 6.0:
    max_band = Max(Band_0, max_band - 2)
    max_e_node_allowed = "E0_only"
    contacts_allowed = contacts_allowed * 0.5
  elif readiness_score < 8.0:
    max_band = Max(Band_0, max_band - 1)
    max_e_node_allowed = "E0_only"
    contacts_allowed = contacts_allowed * 0.8
  else:
    max_e_node_allowed = compute_max_e_node_allowed(client)
  
  # Step 6A: F-V Bias Legality
  if not fv_allowed:
    fv_bias_profile = BALANCED
    bias_band_targets = BIAS_PROFILES["BALANCED"]["band_targets"]
    bias_plyo_targets = BIAS_PROFILES["BALANCED"]["plyo_targets"]
  elif client.fv_bias_profile:
    fv_bias_profile = client.fv_bias_profile
    bias_band_targets = BIAS_PROFILES[fv_bias_profile]["band_targets"]
    bias_plyo_targets = BIAS_PROFILES[fv_bias_profile]["plyo_targets"]
  else:
    fv_bias_profile = BALANCED  # default
    bias_band_targets = BIAS_PROFILES["BALANCED"]["band_targets"]
    bias_plyo_targets = BIAS_PROFILES["BALANCED"]["plyo_targets"]
  
  # Step 7: Compute final bounds
  return {
    "max_band_allowed": max_band,
    "max_node_allowed": max_node,
    "max_e_node_allowed": max_e_node_allowed,
    "contacts_allowed": contacts_allowed,
    "fv_bias_profile": fv_bias_profile,
    "bias_band_targets": bias_band_targets,
    "bias_plyo_targets": bias_plyo_targets,
    "allowed_services": services_where(service.min_band <= max_band),
    "forbidden_services": services_where(service.min_band > max_band),
    "required_rules": [population_gate, r2p_gate, season_gate, injury_gate, readiness_flag]
  }
```

---

# SECTION 3: THE 7-GATE DECISION TREE (Exercise Legality)

Every exercise assignment goes through **7 sequential gates**:

## Gates 1-6 (Unchanged from v4.0)

### Gate 1: Load Band Check
```
IF exercise.load_band > client.max_band_allowed:
  ❌ REJECT
  reason = "Exceeds client load ceiling"
  substitute = "Use lower-band variant"
```

### Gate 2: Node Check
```
IF exercise.node > client.max_node_allowed:
  ❌ REJECT
  reason = "Exceeds client node ceiling"
  substitute = "Use lower-node variant"
```

### Gate 3: Injury Gate Check
```
IF exercise.aether_pattern IN client.injury_gates:
  ❌ REJECT (VETO)
  reason = "Contraindicated for [INJURY]"
  substitute = "No substitute; exercise is forbidden"
```

### Gate 4: Service Line Legality
```
IF exercise.legal_service_lines NOT contains client.service_line:
  ❌ REJECT
  reason = "Exercise not part of your service line"
  substitute = "Use service-line-approved variant"
```

### Gate 5: Weekly Frequency / Budget Laws
```
IF (exercises_this_week_same_pattern >= FREQUENCY_CAP[client.max_band]):
  ❌ QUARANTINE
  reason = "Already at frequency cap"

IF (total_plyo_contacts_this_week + proposed_exercise_contacts > client.contacts_allowed):
  ❌ QUARANTINE
  reason = "Would exceed weekly plyo budget"

IF (high_cns_sessions_this_week >= CNS_CAP[season][fixture_tier]):
  ❌ QUARANTINE
  reason = "Would exceed weekly CNS cap"
```

### Gate 6: Progression / Testing Rules
```
IF (proposed_exercise.band > last_week_band + 1):
  IF (recent_test_result == PASSED):
    ✅ ALLOW with note "Progression tested"
  ELSE:
    ❌ REJECT
    reason = "Band jump requires test"

IF (form_breakdown detected) OR (pain > 2/10):
  ❌ REGRESS
  action = "Drop 1 band; reassess in 3 days"
```

---

## Gate 7: Force-Velocity Bias Compliance Check — NEW

**Name:** Force-Velocity Bias Compliance Validation  
**Purpose:** Ensure weekly program distribution matches selected F-V bias targets  
**When:** After Gates 1-6 pass, before program approval  
**Applies To:** Programs where `fv_bias_profile` is set (not null or BALANCED)

### Validation Logic

```
IF client.fv_bias_profile IN [FORCE_BIASED, VELOCITY_BIASED]:
  
  STEP 1: Calculate Actual Band Distribution
    actual_band_pct = {}
    FOR each exercise in weekly_program:
      band = exercise.load_band
      sets = exercise.sets
      actual_band_pct[band] += sets
    actual_band_pct = (actual_band_pct / total_sets) * 100
  
  STEP 2: Calculate Actual Plyo Distribution
    actual_plyo_pct = {}
    FOR each exercise in weekly_program:
      IF exercise.has_plyometric_component:
        e_node = exercise.e_node
        contacts = exercise.contacts
        actual_plyo_pct[e_node] += contacts
    actual_plyo_pct = (actual_plyo_pct / total_contacts) * 100
  
  STEP 3: Compare to Bias Targets
    target_band_dist = BIAS_PROFILES[client.fv_bias_profile]["band_targets"]
    target_plyo_dist = BIAS_PROFILES[client.fv_bias_profile]["plyo_targets"]
    
    band_variance = |actual_band_pct - target_band_dist|
    plyo_variance = |actual_plyo_pct - target_plyo_dist|
  
  STEP 4: Check Critical Ratios
    IF client.fv_bias_profile == FORCE_BIASED:
      critical_ratio = (Band2 + Band3 + Band4) / (Band0 + Band1)
      target_ratio = 2.0 (70/30)
      tolerance = ±0.15 (min 1.7 acceptable)
      
    ELSE IF client.fv_bias_profile == VELOCITY_BIASED:
      critical_ratio = (Band0 + Band1 + Band2) / (Band3 + Band4)
      target_ratio = 2.0 (70/30)
      tolerance = ±0.15 (min 1.7 acceptable)
  
  STEP 5: Validate Safety Gates Still Passed
    ENSURE client.max_band ceiling not violated
    ENSURE client.max_node ceiling not violated
    ENSURE client.contacts_allowed not exceeded
    ENSURE all v2.1.4 safety gates still PASS
  
  STEP 6: Output Result
    IF band_variance ≤ 10% AND plyo_variance ≤ 10% AND critical_ratio >= 1.7 AND all safety gates PASS:
      ✅ PASS_GREEN
      bias_compliance_status = GREEN
      action = "Approve program for athlete assignment"
      
    ELSE IF band_variance ≤ 20% AND plyo_variance ≤ 20% AND all safety gates PASS:
      ⚠️ CAUTION_YELLOW
      bias_compliance_status = YELLOW
      action = "Flag for coach review - program functional but off-target"
      recommendation = "Adjust next week to correct drift; consider if bias appropriate"
      
    ELSE IF band_variance > 20% OR plyo_variance > 20% OR any safety gate FAILS:
      ❌ FAIL_RED
      bias_compliance_status = RED
      action = "QUARANTINE program - do not assign"
      recommendation = "Regenerate with stricter bias constraints OR switch to BALANCED"

ELSE IF client.fv_bias_profile == BALANCED OR null:
  ✅ BYPASS_GREEN
  bias_compliance_status = PASS (no distribution targets)
  reason = "BALANCED profile has no specific targets"
```

### Special Cases

```
IF client.population == Youth_16_or_under:
  ENFORCE client.fv_bias_profile = BALANCED
  REJECT any FORCE_BIASED or VELOCITY_BIASED attempt
  reason = "Youth protection - developmental priority"

IF client.population == Youth_17 AND fv_bias_profile = FORCE_BIASED:
  ENFORCE 60/40 split (NOT 70/30)
  REJECT 70/30 split
  reason = "Youth 17 conditional - reduced intensity"

IF season IN [In_Season, Post_Season] AND fixture_tier != Tier_3:
  ENFORCE client.fv_bias_profile = BALANCED
  REJECT any FORCE_BIASED or VELOCITY_BIASED attempt
  reason = "In-season maintenance priority"
```

---

# SECTION 4: MICROSESSIONS ENFORCEMENT (Complete)

## 4.1 Adult MicroSessions Validation

**All of these must be true for legality:**

- ✅ Duration: 10–25 min
- ✅ RPE: 3–4 only (no higher)
- ❌ **E-nodes FORBIDDEN** (No plyometric work allowed)
- ✅ Node ceilings: PREP (Node C max), DURABILITY (Node D-lite max), RECOVERY (Node C-D-lite)
- ✅ Implements: Bodyweight, bands (Band 0–1), light DB/KB (Band 1 equiv), foam rollers
- ❌ Implements FORBIDDEN: Barbells, medballs (except light carries), sleds, heavy implements
- ✅ Respect client ceilings: `max_band`, `max_node`, `max_e_node_allowed`

---

## 4.2 Athlete MicroSessions Validation

**All of these must be true for legality:**

- ✅ Duration: 10–25 min
- ✅ Plyo contacts: ≤ 50 (Youth 8-12), ≤ 80 (Youth 13-17), ≤ 100 (Adult MicroSession)
- ✅ Plyo types: Youth legal types only
- ✅ Node law: Legal nodes per category (WARM-UP, ELASTICITY, SPORT-SPECIFIC)
- ✅ E-node access: Only Zone E1 in specific categories, with approval
- ✅ Game-day legal: Only WARM-UP and RECOVERY categories on game days
- ✅ Respect client ceilings: `max_band`, `max_node`, `max_e_node_allowed`, `contacts_allowed`

---

## 4.3 MicroSessions + Client State Integration

When a client state changes, re-validate all assigned MicroSessions:

```
ON (readiness_flag changes to RED):
  FOR each assigned_microsession:
    IF microsession.category IN [ELASTICITY, COND_LITE]:
      ❌ UNASSIGN

ON (max_e_node_allowed changes to E0_only):
  FOR each assigned_microsession:
    IF any exercise uses E1+ OR exercise.node > client.max_node:
      ❌ QUARANTINE and RESELECT legal variant
```

---

# SECTION 5: SERVICE LINE LEGAL BOUNDS MATRIX

| Service Line | Typical Client | Min Band | Max Band | Max Node | Allowed Seasons | MicroSessions | F-V Bias Allowed | Forbidden |
|---|---|---|---|---|---|---|---|---|
| **Youth Lab** | Youth 8-12 | Band_0 | Band_0-1 | A/B | All | Athlete (Youth) | ❌ NO (BALANCED) | D node, E-nodes, In-Season plyos |
| **Youth Performance** | Youth 13-17 | Band_0 | Band_1-2 | B/C | All except In-Season | Athlete (Youth) | ❌ NO (BALANCED) | D node, High-CNS in-season |
| **Adult Strength** | Adult 18+ | Band_1 | Band_2-4 | A/B/C/D | Off/Prep/Post | Adult MS only | ✅ YES (all types) | — |
| **SP Performance** | Athlete | Band_1 | Band_2-4 | C/D | Prep/Comp | Athlete (Sport-tier) | ⚠️ CONDITIONAL (off-season only) | In-Season plyos |
| **ERL** | ERL adults | Band_0 | Band_1-2 | A/B | All (conservative) | Adult MS (PREP/RECOVERY) | ❌ NO (BALANCED) | High-load, E-nodes, Cond-lite |
| **R2P / Rehab** | R2P Stage 1-4 | Band_0 | Band_0-3 (by stage) | A/B/C | All (Stage rules supersede) | R2P-specific MS | ❌ NO (BALANCED) | Population ceiling, Injury gates |
| **Mobility / Recovery** | Any | Band_0 | Band_0-1 | A/B | All | Adult/Athlete (Recovery-only) | ❌ NO (BALANCED) | High-load, plyos |

---

# SECTION 6: INTEGRATION WITH SYSTEM 2 (FORCE-VELOCITY ENGINE)

## 6.1 How System 2 Feeds Into Governance

**Flow:**

```
Force-Velocity Engine (System 2)
    ↓ Outputs: Zone [1-8] + Acute Variables (sets/reps/rest/tempo)
    ↓
Governance Layer (System 1)
    ↓ Validates: Band, Node, max_e_node_allowed, contacts, F-V bias targets
    ↓ Runs 7-Gate Decision Tree (including Gate 7)
    ↓
Exercise Library (AETHER)
    ↓ Substitutes if violation
    ↓
Program Architect (System 3)
    ↓
FINAL SESSION (Legal, Safe, Effective)
```

---

## 6.2 System 2 → System 1 Validation Rules

When System 2 selects a **training zone**, System 1 must validate:

```
IF System2_outputs(zone):
  
  VALIDATE(zone against client.max_band)
  VALIDATE(zone against client.max_node)
  VALIDATE(zone against client.max_e_node_allowed)
  
  VALIDATE(zone against SEASON_ZONE_LEGALITY[current_season])
  VALIDATE(zone against SERVICE_LINE_ZONE_LEGALITY[service_line])
  VALIDATE(zone against FIXTURE_TIER_ZONE_LEGALITY[fixture_tier])
  
  IF client.fv_bias_profile IN [FORCE_BIASED, VELOCITY_BIASED]:
    VALIDATE(zone supports bias profile)
    Example: FORCE_BIASED favors Zone1, Zone2, Zone6
    Example: VELOCITY_BIASED favors Zone3, Zone4
  
  IF any validation FAILS:
    ❌ QUARANTINE zone
    RECOMMEND: Legal zones that pass all validations
  
  ELSE:
    ✅ APPROVE zone for exercise selection
```

---

# SECTION 7: OPERATIONS & ENFORCEMENT CHECKPOINTS

## 7.1 Intake & ICP — Governance Checkpoints

At intake or major status change:

- Create or update **Client State Object**
- Compute `max_band_allowed`, `max_node_allowed`, `max_e_node_allowed`, `contacts_allowed`
- **NEW:** Compute `fv_bias_allowed`, `fv_bias_profile`, `bias_band_targets`, `bias_plyo_targets`
- Validate Service Line legality
- **Block Purchase** if service line is not in `allowed_services`

---

## 7.2 Plan Build — Governance Checkpoints

When building a plan:

- **Block Selector Integration:** Validate all proposed exercises against Client State
- **Weekly Frequency Check:** Sum up high-band exposures, plyometric contacts, CNS load for the week
- **MicroSessions Planning:** Ensure Adult vs Athlete codex, respect category ceilings
- **NEW:** Prepare program for Gate 7 validation (calculate expected band and plyo distribution)

---

## 7.3 Session Publish — Governance Checkpoints

Before a session becomes assignable:

- **Session Manifest Validation:** Band, Node, Duration all within bounds
- **MicroSessions Manifest Validation:** RPE, contacts, nodes, implements all legal
- **NEW:** **Gate 7 Validation:** If `fv_bias_profile` set, run full bias compliance check
- **Legality Stamp:** Status = `LEGAL_READY`, `ILLEGAL_QUARANTINED`, or `REQUIRES_REVIEW`
- **Lock Rule:** Once stamped `LEGAL_READY`, structural edits (bands, nodes, bias) invalidate the stamp

---

## 7.4 Day-of Check-In — Governance Checkpoints

Before session execution:

- **Readiness Capture:** Sleep, stress, fatigue
- **Recompute Client State:** Apply readiness modifiers (tightening only)
- **Re-Validate Today's Session:** Check if it still respects updated ceilings
- **Conditional Restrictions:**
  - **RED:** Restrict to Zone 8 (Skill/Mobility) only, no E-nodes, no plyos
  - **YELLOW:** Restrict to Zones 3, 4, 8 (no high-CNS work)

---

## 7.5 Post-Session Review & Audit — Governance Checkpoints

After each session:

- **Compliance Logging:** What was actually done vs planned
- **Overshoot Flag:** If execution exceeded planned band/node, flag as `ILLEGAL_OVERSHOOT`
- **NEW:** **F-V Bias Tracking:** Log actual band/plyo distribution; flag if session drift >10% from targets
- **MicroSessions Impact:** Track category use, correlate with soreness/fatigue
- **Regression Triggers:** Pain > 2/10, form breakdown, or repeated RED states → Auto-regress 1 band

---

## 7.6 Override Protocol (COUNCIL Logic)

Overrides are rare, explicit, and strictly bounded.

- **Hard NO Overrides (Level 1 Safety Gates):** Population, injury, R2P, Youth F-V bias
- **Conditional Overrides (COUNCIL-Only):** Temporary band expansion with documented rationale
- **No silent approvals:** Every override logged as `UNDER_OVERRIDE` with trace

---

# SECTION 8: F-V BIAS COACHING DECISION TREE

**When should you select a specific F-V bias for your athlete?**

### Step 1: Is your athlete Youth 16 or under?
- **YES** → USE BALANCED (enforced by system, no override)
- **NO** → Continue to Step 2

### Step 2: Is your athlete Youth 17 Advanced (2+ years training age)?
- **YES** → Continue to Step 2A (conditional FORCE_BIASED only)
- **NO** → Continue to Step 3

### Step 2A: Can you document training age ≥2 years AND tissue health screening passed?
- **YES** → FORCE_BIASED is conditional option (60/40 max, Director approval)
- **NO** → USE BALANCED

### Step 3: Is current season OFF_SEASON or PRE_SEASON?
- **YES** → Continue to Step 4
- **NO** → USE BALANCED (in-season maintenance)

### Step 4: Do you have F-V diagnostic data (CMJ, squat 1RM, force plate)?
- **YES** → Continue to Step 5 (use testing data)
- **NO** → USE BALANCED (safe default without data)

### Step 5: What does your diagnostic data indicate?

| Finding | Indicator | Recommendation |
|---------|-----------|-----------------|
| **Force-Deficit** | Squat <1.5x BW, RSI >1.8, low peak force | **FORCE_BIASED** — improve max strength |
| **Velocity-Deficit** | Squat >2.0x BW, RSI <1.5, slow RFD | **VELOCITY_BIASED** — improve explosiveness |
| **Balanced** | Squat 1.5-2.0x BW, RSI 1.5-1.8, proportional | **BALANCED** — general development |
| **Unclear** | Conflicting indicators | **BALANCED** — default when uncertain |

### Step 6: Document Your Rationale

**Before assigning FORCE_BIASED or VELOCITY_BIASED, document:**

1. **Athlete Profile:** Age, training age, sport/position
2. **Diagnostic Data:** CMJ height, RSI, squat 1RM, peak force
3. **Bias Selection:** Why this bias? (deficit observed, sport-specific need, etc.)
4. **Testing Date:** When was athlete assessed?
5. **Approval Status:** Coach approval logged? Director approval if required?

**Implementation:**
```json
{
  "fv_bias_profile": "FORCE_BIASED",
  "bias_selection_rationale": "Squat 1.4x BW, RSI 2.1, peak force 1680N - high reactivity but low absolute strength",
  "diagnostic_data": {
    "cmj_height_cm": 68,
    "rsi": 2.1,
    "squat_bw_ratio": 1.4,
    "peak_force_n": 1680,
    "assessment_date": "2025-12-20",
    "assessment_type": "CMJ_PROFILING"
  },
  "approvals": {
    "coach_approved": true,
    "director_approval_required": false,
    "block_duration_weeks": 6,
    "block_season": "Off_Season"
  }
}
```

---

# SECTION 9: IMPLEMENTATION CHECKLIST

- [ ] Implement Client State Object computation with `fv_bias_context`
- [ ] Build 7-Gate validation engine (Gates 1-6 + new Gate 7)
- [ ] Add Gate 7 F-V bias compliance logic
- [ ] Add band:tier ratio calculator
- [ ] Add weekly distribution validator
- [ ] Implement MicroSessions full validation (7-point checklist)
- [ ] Build Service Line routing logic with bias permissions
- [ ] Wire System 2 (FV Engine) validation into Governance Layer
- [ ] Implement coaching decision tree for bias selection
- [ ] Add post-session F-V bias tracking and drift reporting
- [ ] Test on 5 real client scenarios (various ages, biases, seasons)
- [ ] Validate against EFL_LOAD_STANDARDS_v2_2_0.json
- [ ] Deploy System 3 (Program Architect) with full Governance v4.1 integration

---

# END GOVERNANCE v4.1 OPERATIONAL

**This document is the Operating System. All downstream programming flows through these gates.**

**All values, ceilings, F-V bias profiles, and counting standards are derived from EFL_LOAD_STANDARDS_v2_2_0.json (effective 2025-12-22).**

---

# APPENDIX A: E-NODE TO PLYO TIER MAPPING (AUTHORITATIVE)

This mapping connects the E-node classification system (used in exercise library) to the Plyo Tier system (used in Load Standards v2.2.0):

| E-Node | Plyo Tier | Description | Examples | Youth 8-12 | Youth 13-17 | Adult |
|---|---|---|---|---|---|---|
| E0 | NON_PLYOMETRIC | No elastic component | Squat, Lunge, Core, Mobility | ✅ Allowed | ✅ Allowed | ✅ Allowed |
| E1 | TIER_1 | Low-intensity plyos | Ankle Hops, Jump Rope, Low Box Jump | ✅ Allowed | ✅ Allowed | ✅ Allowed |
| E2 | TIER_2 | Moderate plyos | Broad Jump, Lateral Bound, Box Jump 12-24in | ✅ Allowed | ✅ Allowed | ✅ Allowed |
| E3 | TIER_3_LOWER | High shock | Depth Jump 12-18in, Single-Leg Bound | ❌ Forbidden* | ✅ Allowed (≤40%) | ✅ Allowed |
| E4 | TIER_3_UPPER | Max shock | Depth Jump >18in, Reactive Single-Leg | ❌ Forbidden* | ✅ Allowed (≤40%) | ✅ Allowed |

*Youth 8-12: Tier 3 (E3/E4) requires Director override with developmental readiness documentation

---

# APPENDIX B: POPULATION CEILINGS QUICK REFERENCE

**Source:** EFL_LOAD_STANDARDS_v2_2_0.json

| Population | Full Session Contacts | MicroSession Contacts | Weekly Contacts | F-V Bias Allowed | Notes |
|---|---|---|---|---|---|
| **Youth 8-12** | 80 | 50 | 160 | ❌ NO (BALANCED) | All Tier 3 forbidden |
| **Youth 13-17** | 120 | 80 | 240 | ❌ NO (BALANCED) | Tier 3 ≤40% of session |
| **Youth 17 Advanced** | 120 | 80 | 240 | ⚠️ FORCE only (60/40) | Director approval, testing required |
| **Adult** | 140 | 100 | 280 | ✅ YES (all types) | Testing or documented rationale |

---

# APPENDIX C: F-V BIAS PROFILES QUICK REFERENCE

**Source:** EFL_LOAD_STANDARDS_v2_2_0.json

## FORCE_BIASED (Shift athlete rightward on F-V curve)

**Target Athlete Profile:**
- Squat <1.5x BW
- RSI >1.8 (high reactivity, low force)
- Peak force 2.0x BW
- Sport examples: Guards, skill position athletes lacking finishing power

**Band Distribution Targets:**
- Band0 (Primer): 5-10%
- Band1 (Endurance): 10-20%
- Band2 (Power): 25-35%
- Band3 (Strength): 25-35%
- Band4 (Max): 5-15%
- **Critical Ratio:** Band2-4 : Band0-1 = 2.0 (70:30)

**Plyo Distribution Targets:**
- E0 (Non-Plyo): Unlimited strength emphasis
- E1 (Tier 1): 20-30%
- E2 (Tier 2): 15-25%
- E3/E4 (Tier 3): 5-10%
- **Critical Ratio:** Strength (E0) : Elastic (E1-E4) = 70:30

**Session Frequency:**
- Strength: 4-5x/week
- Elastic: 2x/week
- Sprint: 1x/week

**Expected 48-Week Outcomes:**
- Squat 1RM: +5-10%
- Peak force: +8-15%
- CMJ height: +3-5cm (from improved force)

---

## VELOCITY_BIASED (Shift athlete leftward on F-V curve)

**Target Athlete Profile:**
- Squat >2.0x BW
- RSI <1.5 (low reactivity, high force)
- Peak force 2.5x BW
- Sport examples: Posts, linemen lacking vertical explosion

**Band Distribution Targets:**
- Band0 (Primer): 15-25%
- Band1 (Velocity): 30-40%
- Band2 (Power): 25-35%
- Band3 (Strength): 5-15%
- Band4 (Max): 0-5%
- **Critical Ratio:** Band0-2 : Band3-4 = 2.0 (70:30)

**Plyo Distribution Targets:**
- E0 (Non-Plyo): Minimal support only
- E1 (Tier 1): 20-30%
- E2 (Tier 2): 30-40%
- E3/E4 (Tier 3): 20-30%
- **Critical Ratio:** Elastic (E1-E4) : Strength (E0) = 70:30

**Session Frequency:**
- Strength: 2-3x/week (maintenance)
- Elastic: 3-4x/week
- Sprint: 2-3x/week

**Expected 48-Week Outcomes:**
- RSI: +10-20%
- CMJ height: +5-8cm (from improved RFD)
- 10-yard sprint: -0.05 to -0.10s

---

## BALANCED (General athletic development)

**Target Athlete Profile:**
- Squat 1.5-2.0x BW
- RSI 1.5-1.8
- Proportional acceleration and max velocity
- No clear force or velocity deficit

**Band Distribution Targets:**
- Band0 (Primer): 10-15%
- Band1 (Endurance): 20-30%
- Band2 (Power): 30-40%
- Band3 (Strength): 15-25%
- Band4 (Max): 5-10%
- **Ratio:** 50:50 across force-velocity spectrum

**Plyo Distribution Targets:**
- E0-E4: Equal emphasis
- No specific ratio targets

**Session Frequency:**
- Strength: 3-4x/week
- Elastic: 2-3x/week
- Sprint: 2x/week

**Expected 48-Week Outcomes:**
- Gradual improvements across all metrics
- Squat 1RM: +3-7%
- CMJ height: +2-4cm
- Balanced force-velocity development

---

# APPENDIX D: GATE 7 VALIDATION LOGIC

## Detailed Validation Algorithm

```python
def validate_gate_7_fv_bias(program, client):
    """
    Validate that weekly program distribution matches F-V bias targets
    Returns: (status, variance_details, recommendations)
    """
    
    # Skip if no bias profile or BALANCED
    if client.fv_bias_profile in [None, "BALANCED"]:
        return ("PASS", {}, "No distribution targets")
    
    bias_profile = BIAS_PROFILES[client.fv_bias_profile]
    
    # STEP 1: Calculate actual band distribution
    actual_band_dist = {}
    total_sets = 0
    for session in program.sessions:
        for exercise in session.exercises:
            band = exercise.load_band
            sets = exercise.sets
            actual_band_dist[band] = actual_band_dist.get(band, 0) + sets
            total_sets += sets
    
    actual_band_pct = {
        band: (count / total_sets * 100) 
        for band, count in actual_band_dist.items()
    }
    
    # STEP 2: Calculate actual plyo distribution
    actual_plyo_dist = {}
    total_contacts = 0
    for session in program.sessions:
        for exercise in session.exercises:
            if exercise.has_plyometric_component:
                e_node = exercise.e_node
                contacts = exercise.contacts
                actual_plyo_dist[e_node] = actual_plyo_dist.get(e_node, 0) + contacts
                total_contacts += contacts
    
    actual_plyo_pct = {
        e_node: (count / total_contacts * 100) 
        for e_node, count in actual_plyo_dist.items()
    }
    
    # STEP 3: Compare to targets
    target_band_targets = bias_profile["band_targets"]
    target_plyo_targets = bias_profile["plyo_targets"]
    
    band_variance = compare_distributions(actual_band_pct, target_band_targets)
    plyo_variance = compare_distributions(actual_plyo_pct, target_plyo_targets)
    
    # STEP 4: Check critical ratio
    if client.fv_bias_profile == "FORCE_BIASED":
        force_work = sum([actual_band_pct.get(b, 0) for b in ["Band2", "Band3", "Band4"]])
        support_work = sum([actual_band_pct.get(b, 0) for b in ["Band0", "Band1"]])
        critical_ratio = force_work / support_work if support_work > 0 else 0
        target_ratio = 2.0
        
    elif client.fv_bias_profile == "VELOCITY_BIASED":
        velocity_work = sum([actual_band_pct.get(b, 0) for b in ["Band0", "Band1", "Band2"]])
        strength_work = sum([actual_band_pct.get(b, 0) for b in ["Band3", "Band4"]])
        critical_ratio = velocity_work / strength_work if strength_work > 0 else 0
        target_ratio = 2.0
    
    ratio_acceptable = abs(critical_ratio - target_ratio) / target_ratio <= 0.15
    
    # STEP 5: Validate safety gates
    safety_gates_pass = all([
        max(actual_band_dist.keys()) <= client.max_band_allowed,
        total_contacts <= client.contacts_allowed,
        all_exercises_pass_gates_1_6(program, client)
    ])
    
    # STEP 6: Determine output
    max_variance = max(band_variance, plyo_variance)
    
    if max_variance <= 10 and ratio_acceptable and safety_gates_pass:
        return ("GREEN", {
            "band_variance": band_variance,
            "plyo_variance": plyo_variance,
            "ratio": critical_ratio,
            "actual_band_dist": actual_band_pct,
            "actual_plyo_dist": actual_plyo_pct
        }, "Approve program")
        
    elif max_variance <= 20 and safety_gates_pass:
        return ("YELLOW", {
            "band_variance": band_variance,
            "plyo_variance": plyo_variance,
            "ratio": critical_ratio,
            "actual_band_dist": actual_band_pct,
            "actual_plyo_dist": actual_plyo_pct
        }, "Flag for review - adjust next week")
        
    else:
        return ("RED", {
            "band_variance": band_variance,
            "plyo_variance": plyo_variance,
            "ratio": critical_ratio,
            "safety_gates_pass": safety_gates_pass,
            "actual_band_dist": actual_band_pct,
            "actual_plyo_dist": actual_plyo_pct
        }, "QUARANTINE - regenerate program")
```

---

# APPENDIX E: SEASON OPERATING RANGES

These are **recommended target ranges** beneath absolute ceilings.

**Youth 8-12:**
| Season | Contacts (Target) | Sprints (Target) |
|--------|---|---|
| OFF | 120-160 | 120-240m |
| PRE | 100-140 | 120-200m |
| IN_TIER_1 | 0-80 | 0-120m |
| IN_TIER_2 | 40-120 | 60-160m |
| IN_TIER_3 | 80-160 | 120-240m |
| POST | 0-80 | 0-120m |

**Youth 13-17:**
| Season | Contacts (Target) | Sprints (Target) |
|--------|---|---|
| OFF | 140-200 | 800-1200m |
| PRE | 120-180 | 600-1000m |
| IN_TIER_1 | 60-100 | 400-800m |
| IN_TIER_2 | 120-180 | 600-1000m |
| IN_TIER_3 | 160-240 | 1000-1600m |
| POST | 60-120 | 300-600m |

**Adult:**
| Season | Contacts (Target) | Sprints (Target) |
|--------|---|---|
| OFF | 160-240 | 1000-1600m |
| PRE | 140-220 | 800-1400m |
| IN_TIER_1 | 120-160 | 600-1000m |
| IN_TIER_2 | 140-200 | 800-1400m |
| IN_TIER_3 | 160-240 | 1000-1600m |
| POST | 80-140 | 300-800m |

---

**END APPENDICES — GOVERNANCE v4.1 COMPLETE**