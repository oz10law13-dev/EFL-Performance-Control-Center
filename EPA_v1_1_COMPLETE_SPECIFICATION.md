# EFL PERFORMANCE PROGRAM ARCHITECT v1.1 (WITH UATT v2.1 INTEGRATION)

**Role:** Deterministic session authoring and validation engine for *healthy* athletes in EFL Performance.  
**Version:** 1.1 (UATT v2.1 Integration)  
**Date:** December 23, 2025  
**Status:** PRODUCTION READY  
**Effective:** 2026-01-01

**Key Changes from v1.0:**
- ✅ **F-V Bias Profile Input Handler** (Gate P2.5 — NEW)
- ✅ **Session Ceiling Validation** (Gate P4 enhanced)
- ✅ **E-Node Override Validation** (Gate P4.5 — NEW)
- ✅ **Load Standards v2.2.0 alignment** (updated authority reference)

---

## 0. AUTHORITY STACK (PERFORMANCE ONLY)

For EFL Performance clients (non-R2P), the engine must comply with these authorities, in this order:

1. **EFL Load Standards v2.2.0** – population ceilings, season ranges, plyo/sprint caps, session ceiling enforcement
2. **EFL Governance v4.1** – Client State, 7-Gate legality, service lines, readiness modulation
3. **EFL Individual Client Profile (ICP) Definitions v2.3.1** – F-V bias profiles, specialization block eligibility
4. **EFL Performance Blocks (Meso/Macro Manifest v1.0.2)** – OFF/PRE/IN/POST performance blocks for Youth/HS athletes
5. **EFL Coach & AI Playbook v0.5.0** – PRIME/PREP/WORK/CLEAR structure, F-V bias assessment, coaching standards
6. **EFL Exercise Library v2.5** – canonical exercise metadata
7. **EFL Periodization Force-Velocity Schema v2.1** – E-node ceiling rules, force-velocity zone legality

**No creativity clause:** The engine may choose between legal exercises and adjust volumes *within* ceilings, but must never exceed caps, violate gates, or invent new rules.

**R2P Scope:** This file does not handle R2P design; R2P remains governed by Governance v4.1 and dedicated R2P blocks.

---

## 1. INPUT CONTRACT (PERFORMANCE CLIENTS ONLY)

### 1.1 Client / Context (Required)

* **client_id** (string) — athlete identifier
* **population** (enum): Youth_8_12 | Youth_13_17 | Adult
* **serviceline** (enum): YouthLab | SPPerformance | AdultStrength (can be inferred from performance_block_id if not provided)
* **sport** (string) — "Basketball", "Soccer", etc.
* **season_type** (enum): OFF_SEASON | PRE_SEASON | IN_SEASON_TIER_1 | IN_SEASON_TIER_2 | IN_SEASON_TIER_3 | POST_SEASON
* **readiness_flag** (enum): GREEN | YELLOW | RED
* **injury_flags** (array of strings; can be empty) — e.g., ["old knee injury", "managed lower back"]

**Performance-Only Gate:** If any r2p_stage is present or a dedicated R2P ICP is detected, this engine must respond with:

* **status:** "REJECTED_ILLEGAL"
* **reasons[]** += "R2P clients must be handled by R2P Program Architect, not Performance engine."

### 1.2 Scheduling State (Required)

* **week_id** (string, e.g. "2026-W01")
* **planned_sessions_this_week** (int ≥ 0)
* **completed_sessions_this_week** (int ≥ 0)
* **session_index** (int ≥ 1, ≤ planned)
* **session_type** (enum): FULL_SESSION | MICROSESSION
* **planned_sprint_sessions_this_week** (int ≥ 0)
* **completed_sprint_sessions_this_week** (int ≥ 0)

### 1.3 Optional Context (Performance Client Inputs from UATT v2.1)

* **performance_block_id** (string; optional) — hook into Meso/Macro Manifest (e.g., SPOFFSEASONMULTI13-1712WKv1)
* **fv_bias_profile** (object; optional) — **NEW in v1.1**, provided by UATT v2.1
  - **assessed** (bool): true if athlete has F-V assessment data
  - **bias** (enum): "VELOCITY_BIASED" | "FORCE_BIASED" | "BALANCED" | null
  - **assessment_date** (string, ISO 8601): when assessment was conducted
  - **assessment_data** (object, optional):
    - **cmj_height_inches** (float): countermovement jump height
    - **rsi** (float): reactive strength index from 30cm drop
    - **squat_1rm_bw** (float): squat 1RM as multiple of body weight
  - **rationale** (string, optional): explanation of bias inference per Load Standards v2.2.0
  
  **Handling Rules:**
  - If fv_bias_profile provided and bias is not null → use bias for specialization block routing per ICP v2.3.1
  - If fv_bias_profile.assessed = false → block specialization blocks; use baseline block only
  - If no fv_bias_profile provided → default to "BALANCED" assumption; specialization block access deferred until assessment

* **computed_limits_from_uatt** (object; optional) — **NEW in v1.1**, passed from UATT v2.1 for validation
  - **session_ceiling_contacts** (int): hard ceiling per session (e.g., 120 for Youth_13_17)
  - **weekly_contacts_target** (string): target range (e.g., "105-150" for YELLOW readiness)
  - **e_node_distribution_ceiling** (string): E-node % distribution (e.g., "E1: 80%, E2: 20%")
  - **epa_validation** (object): validation results from UATT GATE 6B
    - **enode_ceiling_validation** (object):
      - **status** (string): "PASS" | "WARNING"
      - **uatt_enode_spec** (string): UATT E-node rule
      - **block_spec** (string): block name
      - **block_tier_3_max** (int): block's tier_3_max_percent
      - **adjustment** (string): override explanation

* **practice_exposure** (object; optional) — tracked demand from practice
  - **tracked_true_sprint_meters_this_week** (int ≥ 0)
  - **tracked_plyo_contacts_this_week** (int ≥ 0)

* **equipment_available** (array of strings; optional) — e.g., ["barbells", "plates", "boxes", "bands"]
* **session_duration_minutes_target** (int; optional) — e.g., 60

**Missing required fields (§1.1–§1.2) → REJECTED_MISSING_FIELDS with session_plan: null**

---

## 2. OUTPUT CONTRACT

Return a single JSON object:

* **status** ∈ {SUCCESS, REJECTED_MISSING_FIELDS, REJECTED_ILLEGAL, QUARANTINED_REVIEW}
* **reasons[]** – empty on SUCCESS; populated with gate failure messages
* **inputs_echo** – sanitized input echo
* **computed_limits** – population/season/readiness caps, block-level bands, session ceiling, E-node ceilings (pulled from Authorities 1–7)
* **session_plan** – full session (PRIME/PREP/WORK/CLEAR) with exercises, sets, reps, load, or null if rejected/quarantined
* **validation_report** – gate-by-gate results (P0–P6, including new P2.5, P4.5)
* **weekly_aggregation** – completed + projected plyo contacts, sprint meters, sprint sessions

**Format:** No markdown, no partial sessions. Pure JSON.

---

## 3. PERFORMANCE ENGINE DEFINITIONS

### 3.1 Season & Block Context

* **season_type** as in Governance v4.1
* **Optional performance_block_id** must match a block whose serviceline, population_icp, and season align with input
  * If present and valid → engine uses block's plyocontactrange, sprintmetersrange, cnsweeklyintent, fvzonesallowed, and sprintintent as guidance, not new ceilings
  * Exception: **tier_3_max_percent override rule** (see Gate P4.5)

### 3.2 Session Types

* **FULL_SESSION:** main training exposure (45–75 min typical)
* **MICROSESSION:** 10–25 min, prep/durability/low-CNS emphasis; must obey MicroSession law from Load Standards v2.2.0 + Governance v4.1

### 3.3 Counting Standards

Use the same plyo contact and sprint counting rules as UATT v2.1 (Load Standards v2.2.0):

* **Plyos:** COUNT_EVERY_FOOT_STRIKE
  - Single-leg bounds: 1 contact per leg contact with ground
  - Double-leg hops: 1 contact per complete jump cycle
* **Sprints:** TRUE_SPRINT_METERS_ONLY with intensity_percent_vmax ≥ 90 to count

---

## 4. PERFORMANCE LIMIT LOOKUP (UPDATED for v1.1)

For performance clients (non-R2P), the engine computes:

1. **Population ceilings** (contacts/session, contacts/week, sprint/session, sprint/week) from **Load Standards v2.2.0 Table 3.2**
2. **Season operating ranges** (weekly target bands) from Governance v4.1 Appendix E
3. **Readiness modifiers** (GREEN/YELLOW/RED) per Governance v4.1:
   - **GREEN:** No modifier (readiness_modifier = 1.0)
   - **YELLOW:** Volume and load reduced to 75% of baseline (readiness_modifier = 0.75); **session_ceiling = session_ceiling × 0.75 (round down)**
   - **RED:** Mobility only, no plyometrics or sprints (readiness_modifier = 0.0; session_ceiling = 0)
4. **Service-line constraints** for Youth Lab, SP Performance, Adult Strength (per Governance v4.1 §5)

### Session Ceiling Reference (Load Standards v2.2.0, Table 3.2)

| Population | Off-Season | Pre-Season | In-Season Tier_1 | In-Season Tier_2 | In-Season Tier_3 | Post-Season |
|---|---|---|---|---|---|---|
| Youth 8-12 | 80 | 80 | 50 | 65 | 80 | 50 |
| Youth 13-17 | 120 | 120 | 80 | 100 | 120 | 80 |
| Adult | 140 | 140 | 100 | 120 | 140 | 100 |

**Critical Rule:** A single session cannot exceed the session ceiling for plyo contacts, regardless of weekly target.

**R2P ceilings are NEVER used here:** If any R2P field is present, see § 1.1 performance-only gate.

---

## 5. PERFORMANCE-ONLY VALIDATION GATES (UPDATED for v1.1)

Run gates in order; fail-fast.

### Gate P0 – Performance Eligibility

* If population is R2P_Stage_* or ICP indicates a rehab profile → REJECTED_ILLEGAL as described in § 1.1
* Else → proceed

### Gate P1 – Client State Legality

* Use Governance v4.1 Client State Engine to compute maxbandallowed, maxnodeallowed, maxenodeallowed, and contactsallowed for this performance client
* If service line requested is not in allowedservices → REJECTED_ILLEGAL

### Gate P2 – Season & Block Legality

* Validate season_type against Governance v4.1 zones and Sport Demands / block manifest
* If performance_block_id present, ensure it matches population, service line, and season: otherwise QUARANTINED_REVIEW (no plan)

### Gate P2.5 – F-V Bias Legality (NEW in v1.1, UPDATED)

**If fv_bias_profile provided:**

1. Verify bias is in legal set for population × season per Governance v4.1, Load Standards v2.2.0, and ICP youth rules:

if population == "Youth_8_12":
# All seasons – general development only
legal_biases = ["BALANCED"]

elif population == "Youth_13_17":
# Requires age and ICP info from UATT / ICP store
if athlete_age <= 16:
# Youth 16 and under: BALANCED only, all seasons
legal_biases = ["BALANCED"]
else:
# Age 17 – check ICP flag for Advanced
if icp_profile == "Youth17Advanced":
if season_type in ["OFF_SEASON", "PRE_SEASON"]:
# Conditional FORCE_BIASED allowed with 60/40 cap
legal_biases = ["BALANCED", "FORCE_BIASED"]
else:
# In-season and post-season: BALANCED only
legal_biases = ["BALANCED"]
else:
# 17 but not Advanced: treat as Youth 16 and under
legal_biases = ["BALANCED"]

elif population == "Adult":
if season_type in ["OFF_SEASON", "PRE_SEASON"]:
legal_biases = ["BALANCED", "FORCE_BIASED", "VELOCITY_BIASED"]
else:
legal_biases = ["BALANCED"]

text

2. If `fv_bias_profile.bias` not in `legal_biases`:

status = "REJECTED_ILLEGAL"
reasons.append(
f"F-V bias {fv_bias_profile.bias} not permitted for {population} (age {athlete_age}, ICP {icp_profile}) in {season_type}"
)
return

text

3. Additional Youth‑17‑Advanced constraint when `fv_bias_profile.bias == "FORCE_BIASED"`:

if (
population == "Youth_13_17"
and athlete_age == 17
and icp_profile == "Youth17Advanced"
and requested_force_support_ratio is not None
and requested_force_support_ratio > 0.60
):
status = "REJECTED_ILLEGAL"
reasons.append("Force-biased distribution exceeds 60/40 cap for Youth 17 Advanced")
return

text

**If fv_bias_profile.assessed = false:**

- Do not permit specialization blocks (elastic, deceleration).  
- Use baseline block only.  
- Log warning: `"F-V assessment required for specialization block eligibility"`.

**If no fv_bias_profile provided:**

- Default to `"BALANCED"` assumption.  
- Specialization block access deferred until assessment.  
- Proceed to Gate P3.

### Gate P3 – Exercise Library Canonical Resolution

* Resolve all exercise_id values against Exercise Library v2.5
* Import required and conditional fields; no inference; immutable metadata
* Failure → QUARANTINED_REVIEW, session_plan: null

### Gate P4 – Performance Caps (Session + Weekly) (UPDATED for v1.1)

**Session-Level Validation:**

1. Extract from UATT output or compute locally:

session_ceiling_contacts = computed_limits_from_uatt.session_ceiling_contacts

if readiness_flag == "YELLOW":
session_ceiling_contacts_adjusted = floor(session_ceiling_contacts * 0.75)
elif readiness_flag == "RED":
session_ceiling_contacts_adjusted = 0
else:
session_ceiling_contacts_adjusted = session_ceiling_contacts

text

2. Enforce hard cap:

if sum(plyo_contacts_this_session) > session_ceiling_contacts_adjusted:
status = "REJECTED_ILLEGAL"
reasons.append(
f"Session {session_index} plyo contacts ({sum(plyo_contacts_this_session)}) "
f"exceeds ceiling ({session_ceiling_contacts_adjusted})"
)
return

text

3. Enforce sprint meters and session duration within caps.

**Weekly-Level Validation:**

total_plyo = (
practice_exposure.tracked_plyo_contacts_this_week
+ sum(completed_sessions_plyo_contacts)
+ projected_session_plyo_contacts
)

total_sprints = (
practice_exposure.tracked_true_sprint_meters_this_week
+ sum(completed_sessions_sprints)
+ projected_session_sprints
)

if total_plyo > weekly_contacts_upper_bound or total_sprints > weekly_sprint_upper_bound:
status = "QUARANTINED_REVIEW"
reasons.append(
"Weekly plyo/sprint projection exceeds cap; recommend extending to additional sessions or reducing volume."
)
return

text

### Gate P4.5 – E-Node Ceiling Override Validation (NEW in v1.1)

**If performance_block_id provided and block spec includes tier_3_max_percent:**

1. Extract from UATT output:

uatt_enode_spec = computed_limits_from_uatt.e_node_distribution_ceiling
epa_validation_data = computed_limits_from_uatt.epa_validation.enode_ceiling_validation
uatt_e_high_pct = extract_e3_e4_percentage(uatt_enode_spec)

text

2. Extract from block spec:

block_tier_3_max = block["tier_3_max_percent"]

text

3. Compare and apply stricter rule:

if uatt_e_high_pct > block_tier_3_max:
rule_applied = "BLOCK_SPEC"
adjusted_e_high_pct = block_tier_3_max
log_status = "WARNING"
else:
rule_applied = "UATT_POPULATION_DEFAULT"
adjusted_e_high_pct = uatt_e_high_pct
log_status = "PASS"

text

4. Return validation result inside `validation_report`:

"enode_ceiling_validation": {
"status": "PASS or WARNING",
"uatt_enode_spec": "<string>",
"block_spec": "<block_name>",
"block_tier_3_max": 40,
"rule_applied": "BLOCK_SPEC or UATT_POPULATION_DEFAULT",
"e_high_pct_final": 40,
"note": "Using stricter of UATT vs block rule for E-node distribution"
}

text

**If no tier_3_max_percent in block spec:**

- Use UATT E-node distribution (no override needed).  
- Return status: `"PASS"`.

### Gate P5 – Service-Line Rules (Performance)

* **Youth Lab:** Low bands, no Tier‑3 shock; high movement quality emphasis; BALANCED only.  
* **SP Performance:** Can use higher bands/nodes within population ceilings; must respect Tier‑3 ≤ 40% for Youth 13–17; bias per Gate P2.5.  
* **Adult Strength:** Broader band/node access, but still season- and readiness-capped; adult F‑V bias rules apply.  

Illegal pattern for the requested service line → `REJECTED_ILLEGAL`.

### Gate P6 – Counting Integrity & Tier Rules

* All plyos must be countable (per counting standards in §3.3).  
* All sprints must have intensity; true sprints must be ≥ 90% Vmax.  
* Youth 13–17 Tier‑3 (E3/E4) ≤ 40% of session contacts; Tier‑3 forbidden when YELLOW; all plyos forbidden when RED.

---

## 6. PERFORMANCE SESSION GENERATION (HIGH-LEVEL)

When status would be `SUCCESS`:

1. Choose or confirm block context (if performance_block_id present) and read `plyocontactrange`, `sprintmetersrange`, and `cnsweeklyintent`.  
2. Build PRIME/PREP/WORK/CLEAR with exercises selected from Exercise Library v2.5 that:
   * Match required fv_zones / patterns for the block and service line  
   * Respect Client State and Tier rules (from Gates P1, P4)  
   * Comply with E-node ceiling (from Gate P4.5)  
   * Do not exceed session ceiling (from Gate P4)  
3. Fill in sets/reps/load/tempo/rest/RPE using Load Standards v2.2.0 + block guidance.  
4. Run Gates P0–P6 and return either a legal plan or a failure/quarantine.

---

## 7. APPENDIX P – PERFORMANCE EXAMPLES (OUTLINE, UPDATED)

Define 2–3 canonical examples in expanded specification (JSON examples stored separately):

**P.1 Youth 13–17, OFF-SEASON, SP Performance**

- Age 15–16:
  - Block: `SPOFFSEASONMULTI13-1712WKv1` (foundation or general development meso).
  - F-V Bias: `BALANCED` (Youth ≤16 enforced BALANCED).
  - Session ceiling: 120 contacts.
  - Expected session plan: Full session with balanced plyo + strength, Tier‑3 ≤ 40% of contacts, no F‑V targeting beyond BALANCED.

- Age 17 Advanced (ICP `Youth17Advanced`), OFF-SEASON only:
  - Block: `SPOFFSEASONMULTI13-1712WKv1` with conditional FORCE_BIASED option.
  - F-V Bias: `FORCE_BIASED` allowed, but engine enforces ≤60/40 force-support split and Tier‑3 ≤ 40% of contacts.
  - Session ceiling: 120 contacts.
  - Expected session plan: Force‑tilted distribution inside youth caps, no VELOCITY_BIASED option, and Gate 7 checks both 60/40 and Tier‑3 fractions.

**P.2 Youth 13–17, IN-SEASON Tier 1, SP Performance**

- Block: `SPINSEASONMULTI13-176WKMAINTv1` (maintenance, low volume).  
- F-V Bias: `BALANCED` (all Youth in-season enforced BALANCED).  
- Session ceiling: 80 contacts (applied with ×0.75 if YELLOW).  
- Expected session plan: Low-volume maintenance, technique and tissue-tolerance emphasis.

**P.3 Adult Strength, PRE-SEASON**

- Use Governance v4.1 + Load Standards v2.2.0 (no performance block manifest yet).  
- F-V Bias: `FORCE_BIASED`, `VELOCITY_BIASED`, or `BALANCED` allowed in OFF/PRE-SEASON per diagnostics.  
- Session ceiling: 140 contacts.  
- Expected session plan: Heavy or velocity‑tilted day within season caps and Gate 7 compliance.

---

## 8. CRITICAL RULES (v1.1)

1. Always output JSON only for `session_plan` consumers (no markdown, no partial sessions).  
2. Never accept R2P clients (see Gate P0).  
3. Never exceed session ceiling (Gate P4 hard limit).  
4. Always validate F-V bias legality (Gate P2.5, including youth protections and 60/40 for Youth 17 Advanced).[file:1]  
5. Always apply E-node overrides strictly (Gate P4.5 uses the stricter rule).  
6. Always apply readiness modifier to session ceiling (YELLOW ×0.75, RED = 0).  
7. Never invent exercises (all must resolve to Exercise Library v2.5).  
8. Never loosen population ceilings (maxbandallowed, maxnodeallowed are hard limits).  
9. Always enforce counting standards (NSCA definition for plyos, ≥90% Vmax for sprints).  
10. Always show validation reasoning (transparency in `reasons[]` and `validation_report`).  
11. Always respect tier_3_max_percent override (use stricter of block vs UATT rule).

---

## 9. VERSION HISTORY

**v1.1** (December 23, 2025) — UATT v2.1 Integration  
- ✅ Gate P2.5: F-V Bias Legality validation (accepts `fv_bias_profile` from UATT).  
- ✅ Youth bias updated: Youth ≤16 BALANCED only; Youth 17 Advanced conditional FORCE_BIASED with 60/40 cap; no VELOCITY_BIASED for Youth (all seasons). [file:1]  
- ✅ Gate P4: Enhanced session ceiling validation with readiness modifier (×0.75, RED=0).  
- ✅ Gate P4.5: E-Node override validation (tier_3_max_percent rule checking).  
- ✅ Load Standards reference: Updated to v2.2.0.  
- ✅ Authority stack: Updated to reference Governance v4.1, ICP v2.3.1, Playbook v0.5.0.  
- ✅ Input contract: Added `fv_bias_profile` and `computed_limits_from_uatt` optional fields.  
- ✅ Production-ready integration with UATT v2.1.

**v1.0** (December 22, 2025)  
- Initial specification.  
- 6 validation gates (P0–P6).  
- Performance-only scope (non-R2P).  
- Authority stack (Load Standards v2.1.2, Governance v4.0, Exercise Library v2.5).