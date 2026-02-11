# EFL Router Decision Matrix v1.0

**Specification ID:** EFL_ROUTER_DECISION_MATRIX  
**Version:** 1.0.0  
**Effective Date:** 2026-01-15  
**Status:** PRODUCTION-LOCKED  
**Authority:** Elite Fitness Lab — Director of Performance Systems

---

## Document Role

This document defines the **logic truth layer** for the EFL Global Router. It specifies the exact precedence, conditions, and effects of all routing decisions.

**What this document IS:**
- Authoritative legality truth table
- Ordered execution precedence
- Rule-by-rule decision logic
- Test coverage mapping

**What this document IS NOT:**
- Schema definition (see: EFL_GLOBAL_CLIENT_STATE_v1.0.2.json)
- Implementation guide (see: EFL_ROUTER_IMPLEMENTATION_GUIDE_v1.0.1_PATCHED.md)
- Code samples or algorithms

**Companion Documents:**
- EFL_GLOBAL_CLIENT_STATE_v1.0.2.json (structure truth)
- EFL_ROUTER_IMPLEMENTATION_GUIDE_v1.0.1_PATCHED.md (execution contract)
- EFL_ROUTER_TEST_FIXTURES_v1.0.json (validation cases)

---

## 1. Router Decision Precedence Ladder

Rules fire in strict order. **First match wins.**

| Priority | Layer | Description | Overrides All Lower Layers |
|----------|-------|-------------|----------------------------|
| 1 | **Version Gate** | Router version must be in allowlist | ✅ ALL |
| 2 | **Schema Validation** | Output must pass JSON Schema v1.0.2 | ✅ ALL |
| 3 | **Coherence Validation** | stateheader ↔ inputs ↔ decisions alignment | ✅ ALL |
| 4 | **Medical Lock** | ≥2 hardstops in 14 days OR provider directive | ✅ ALL |
| 5 | **Hardstop (Non-Lock)** | Acute symptoms present | ✅ ALL (except R2P routes) |
| 6 | **R2P Enrollment** | isinr2pservice=true | ✅ SP Performance, ICP, Adult projects |
| 7 | **Age/Population** | Youth vs Adult legality gates | ✅ Specializations |
| 8 | **Season** | OFFSEASON/PRESEASON/INSEASON/POSTSEASON | ✅ Developmental vs ICP |
| 9 | **Exit Gates** | Foundations/Reload completion flags | ✅ Specializations |
| 10 | **Macro Caps** | Annual block limits, CNS fatigue caps | ✅ Project selection |
| 11 | **Default Allow** | Lowest-priority legal project selected | ❌ NONE |

**Execution Rule:** Router evaluates Priority 1 → 11. If any Priority 1–5 rule fires, Router returns collapse state immediately.

---

## 2. Collapse Rules (Immediate Termination)

**Effect:** `activeproject=NONE`, `derived=null`, `eligible_for_training_today=false`, all projects denied.

| Rule ID | Condition | Fires When | Reason Code | Test Fixture |
|---------|-----------|------------|-------------|--------------|
| **C-01** | Missing Critical Input | Any field in "never default" list is missing or null | `DEFAULTDENY_MISSING_CRITICAL_INPUTS` | COLLAPSE_01 |
| **C-02** | Version Mismatch | `routerversion ∉ allowlist` | `DEFAULTDENY_VERSION_MISMATCH` | COLLAPSE_02 |
| **C-03** | Schema Validation Failure | Output fails Ajv validation against v1.0.2 | `ROUTEROUTPUTINCOMPLETE` | — |
| **C-04** | Coherence Failure | Any Phase-2 coherence rule fails | `DEFAULTDENY_STATEHEADER_MISMATCH` | COLLAPSE_04 |
| **C-05** | Medical Lock | `inputs.medicalstatus.hardstopstatus.medicallocktriggered=true` | `DEFAULTDENY_MEDICAL_LOCK` | COLLAPSE_03 |
| **C-06** | Hardstop (Non-R2P Youth) | `hardstoptriggered=true` AND `isinr2pservice=false` AND `age<18` | `YOUTH_HARDSTOP_NONR2P_DENY_AND_REFER` | — |
| **C-07** | Hardstop (No Route) | `hardstoptriggered=true` AND `isinr2pservice=false` AND no recovery route available | `DEFAULTDENY_HARDSTOP_NO_ROUTE` | — |

**Never Default Fields (C-01 Trigger List):**
- `inputs.athleteprofile.age`
- `inputs.athleteprofile.sport`
- `inputs.athleteprofile.athletetrack`
- `inputs.medicalstatus.isinr2pservice`
- `inputs.medicalstatus.injurytype`
- `inputs.trainingcontext_global.seasontype`

**Coherence Rules (C-04 Trigger List):**
1. `stateheader.lastupdated === lastupdated`
2. `stateheader.activeproject === decisions.activeproject`
3. `stateheader.routerversion === decisions.routerversion`
4. `stateheader.seasontype === inputs.trainingcontext_global.seasontype`
5. `stateheader.readinessflag === (inputs.trainingcontext_global.readinessflag ?? 'YELLOW')`

---

## 3. Mandatory Routing Rules (Priority 6)

**R2P enrollment overrides all SP Performance and ICP projects.**

| Rule ID | Condition | Enforced Outcome | Effect on Legal Set | Test Fixture |
|---------|-----------|------------------|---------------------|--------------|
| **R-01** | `isinr2pservice=true` | `activeproject=R2P_ACL` | `legal_projects=[R2P_ACL]` only | LEGAL_02 |
| **R-02** | `isinr2pservice=true` AND `injurytype ∈ {ACLRECONSTRUCTION, ACLHIGHGRADESPRAIN}` | Require: `weekspostop`, `grafttype`, `providerclearance` | Schema-enforced (v1.0.2 PATCH 1) | LEGAL_02 |
| **R-03** | `isinr2pservice=true` AND `hardstoptriggered=true` | `r2p_systemone_output.r2pstagestatus=HARDSTOP` | System-1 output drives stage | COLLAPSE_03 |

**R-01 Effect Matrix:**

| Project Type | When R2P Enrolled | Reason Code |
|--------------|-------------------|-------------|
| SP Performance (Foundations, Reload, Specializations) | ❌ BLOCKED | `R2P_ENROLLMENT_LOCKS_SP` |
| ICP (INSEASON/POSTSEASON) | ❌ BLOCKED | `R2P_ENROLLMENT_LOCKS_SP` |
| Adult (Strength, Mobility, ERL) | ❌ BLOCKED | `R2P_ENROLLMENT_LOCKS_SP` |
| R2P_ACL | ✅ LEGAL | — |

---

## 4. Population Enforcement Matrix (Priority 7)

**Source:** `derived.populationoverrides.population_enforced` (computed from `age` + `athletetrack`)

### 4.1 Population Classification Rules

| Rule ID | Age Range | athletetrack | population_enforced | Test Fixture |
|---------|-----------|--------------|---------------------|--------------|
| **POP-01** | 8–12 | ATHLETE or GENERAL | `Youth812` | — |
| **POP-02** | 13–16 | ATHLETE or GENERAL | `Youth1316` | LEGAL_01 |
| **POP-03** | 17 | ATHLETE or GENERAL | `Youth17Advanced` | — |
| **POP-04** | ≥18 | GENERAL | `Adult_GENERAL` | — |
| **POP-05** | ≥18 | ATHLETE | `Adult_ATHLETE` | — |

### 4.2 Population Constraint Matrix

| Population | Max Band | Max E-Node | E-Node Accent Cap | FV Bias Lock | Weekly Contacts Cap | Session Contacts Cap |
|------------|----------|------------|-------------------|--------------|---------------------|----------------------|
| **Youth812** | Band2 | E2 | **0.40** | BALANCED_ONLY | 60 | 20 |
| **Youth1316** | Band2 | E2 | **0.40** | BALANCED_ONLY | 80 | 30 |
| **Youth17Advanced** | Band3 | E3 | **null** | BALANCED_OR_FORCE | 100 | 40 |
| **Adult_GENERAL** | Band4 | E4 | **null** | ALL | 120 | 50 |
| **Adult_ATHLETE** | Band4 | E4 | **null** | ALL | 140 | 60 |

**INV-001 (Youth E-Node Accent Cap):**
```
IF population_enforced ∈ {Youth812, Youth1316}
  THEN enode_accent_cap_pct = 0.40
  ELSE enode_accent_cap_pct = null
```

**Test Coverage:** LEGAL_01 validates INV-001 (Youth1316 → enode_accent_cap_pct=0.40)

### 4.3 Population Legality Matrix

| Project | Youth812 | Youth1316 | Youth17Advanced | Adult_GENERAL | Adult_ATHLETE |
|---------|----------|-----------|-----------------|---------------|---------------|
| **R2P_ACL** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **COURT_SPORT_FOUNDATIONS** | ✅ | ✅ | ✅ | ❌ | ❌ |
| **ELASTIC_RELOAD** | ✅ | ✅ | ✅ | ❌ | ❌ |
| **ELASTIC_SPECIALIZATION** | ❌ | ❌ | ✅ | ❌ | ✅ |
| **DECEL_SPECIALIZATION** | ❌ | ❌ | ✅ | ❌ | ✅ |
| **FORCE_SPECIALIZATION** | ❌ | ❌ | ✅ | ❌ | ✅ |
| **ICP_BASKETBALL_INSEASON** | ❌ | ✅ | ✅ | ❌ | ❌ |
| **ICP_VOLLEYBALL_INSEASON** | ❌ | ✅ | ✅ | ❌ | ❌ |
| **ICP_BASKETBALL_POSTSEASON** | ❌ | ✅ | ✅ | ❌ | ❌ |
| **ICP_VOLLEYBALL_POSTSEASON** | ❌ | ✅ | ✅ | ❌ | ❌ |
| **OFF_SEASON_BASELINE_COURT_VERTICAL** | ❌ | ✅ | ✅ | ❌ | ❌ |
| **ADULT_STRENGTH** | ❌ | ❌ | ❌ | ✅ | ✅ |
| **ADULT_MOBILITY** | ❌ | ❌ | ❌ | ✅ | ✅ |
| **ADULT_ERL** | ❌ | ❌ | ❌ | ✅ | ✅ |

**Denial Reason Code:** `AGE_POPULATION_DENY`

---

## 5. Season Routing Matrix (Priority 8)

**Source:** `inputs.trainingcontext_global.seasontype`

### 5.1 Season Legality Matrix

| Project | OFFSEASON | PRESEASON | INSEASON | POSTSEASON |
|---------|-----------|-----------|----------|------------|
| **R2P_ACL** | ✅ | ✅ | ✅ | ✅ |
| **COURT_SPORT_FOUNDATIONS** | ✅ | ✅ | ❌ | ❌ |
| **ELASTIC_RELOAD** | ✅ | ✅ | ❌ | ❌ |
| **ELASTIC_SPECIALIZATION** | ✅ | ✅ | ❌ | ❌ |
| **DECEL_SPECIALIZATION** | ✅ | ✅ | ❌ | ❌ |
| **FORCE_SPECIALIZATION** | ✅ | ✅ | ❌ | ❌ |
| **ICP_BASKETBALL_INSEASON** | ❌ | ❌ | ✅ | ❌ |
| **ICP_VOLLEYBALL_INSEASON** | ❌ | ❌ | ✅ | ❌ |
| **ICP_BASKETBALL_POSTSEASON** | ❌ | ❌ | ❌ | ✅ |
| **ICP_VOLLEYBALL_POSTSEASON** | ❌ | ❌ | ❌ | ✅ |
| **OFF_SEASON_BASELINE_COURT_VERTICAL** | ✅ | ✅ | ❌ | ❌ |
| **ADULT_STRENGTH** | ✅ | ✅ | ✅ | ✅ |
| **ADULT_MOBILITY** | ✅ | ✅ | ✅ | ✅ |
| **ADULT_ERL** | ✅ | ✅ | ✅ | ✅ |

**Denial Reason Code:** `SEASON_DENY`

**Season Rule Summary:**
- **Developmental projects** (Foundations, Reload, Specializations, Baseline): OFFSEASON/PRESEASON only
- **ICP projects**: INSEASON or POSTSEASON only (sport-specific)
- **R2P + Adult projects**: All seasons

**ICP Bridge Exception:**
- IF `derived.icp_bridge_allowed=true` → ICP wrapper may allow brief Reload/Foundations insertion during INSEASON

---

## 6. Exit Gate Matrix (Priority 9)

**Source:** `inputs.performancegates.exitflagssp`

### 6.1 Specialization Entry Requirements

| Project | Required Exit Gate | Gate Source | Denial Code | Notes |
|---------|-------------------|-------------|-------------|-------|
| **ELASTIC_SPECIALIZATION** | `elasticreloadexitpassed=true` | performancegates.exitflagssp | `EXIT_GATE_NOT_MET` | Reload must be completed first |
| **DECEL_SPECIALIZATION** | `foundationsexitpassed=true` | performancegates.exitflagssp | `EXIT_GATE_NOT_MET` | Foundations must be completed first |
| **FORCE_SPECIALIZATION** | `foundationsexitpassed=true` | performancegates.exitflagssp | `EXIT_GATE_NOT_MET` | Foundations must be completed first |

**Projects with NO exit gate requirement:**
- R2P_ACL
- COURT_SPORT_FOUNDATIONS
- ELASTIC_RELOAD
- ICP projects (all)
- OFF_SEASON_BASELINE_COURT_VERTICAL
- Adult projects (all)

**Exit Gate Logic:**
```
IF project requires exit gate AND gate flag is missing/false
  THEN project denied with EXIT_GATE_NOT_MET
```

---

## 7. Macro Cap Matrix (Priority 10)

**Source:** `derived.macrocounters`

### 7.1 Annual Block Limits (Population-Specific)

| Counter | Youth812 | Youth1316 | Youth17Advanced | Adult_GENERAL | Adult_ATHLETE |
|---------|----------|-----------|-----------------|---------------|---------------|
| `elasticspecialization_blocks_used` | 0 (blocked) | 0 (blocked) | ≤2 per year | N/A | ≤3 per year |
| `forcebias_specialization_blocks_used` | 0 (blocked) | 0 (blocked) | ≤1 per year | N/A | ≤2 per year |
| `decel_specialization_blocks_used` | 0 (blocked) | 0 (blocked) | ≤2 per year | N/A | ≤3 per year |
| `consecutive_highcns_blocks` | ≤2 | ≤3 | ≤4 | N/A | ≤5 |
| `weekssincelastunload` | ≤4 | ≤6 | ≤8 | ≤8 | ≤8 |

**Denial Reason Code:** `MACRO_CAP_EXCEEDED`

**High-CNS Block Definition:**
- ELASTIC_SPECIALIZATION
- DECEL_SPECIALIZATION
- FORCE_SPECIALIZATION
- ICP_BASKETBALL_INSEASON (Tier 1)
- ICP_VOLLEYBALL_INSEASON (Tier 1)

**Macro Cap Logic:**
```
IF (counter for requested project >= population cap)
  THEN project denied with MACRO_CAP_EXCEEDED
```

---

## 8. Derived Construction Rules

**Timing:** Derived is constructed **after** collapse checks pass, **before** routing logic.

### 8.1 Population Overrides Construction

| Field | Formula | Notes |
|-------|---------|-------|
| `population_enforced` | `computePopulation(age, athletetrack)` | See POP-01 through POP-05 |
| `maxbandallowed_population` | Population → Band cap table | See Population Constraint Matrix |
| `maxenodeallowed_population` | Population → E-node cap table | See Population Constraint Matrix |
| `enode_accent_cap_pct` | `IF Youth812/1316 → 0.40, ELSE → null` | INV-001 enforced |
| `fvbiaslock` | Population → FV bias table | See Population Constraint Matrix |
| `weeklycontactscap_population` | Population → base cap | Before readiness multipliers |
| `sessioncontactscap_population` | Population → base cap | Before readiness multipliers |

### 8.2 Readiness Multipliers Construction

| Field | Formula | Notes |
|-------|---------|-------|
| `weeklymultiplier` | `readinessflag → {GREEN:1.0, YELLOW:0.75, RED:0.0}` | Applied to weekly caps |
| `sessionmultiplier` | `readinessflag → {GREEN:1.0, YELLOW:0.8, RED:0.0}` | Applied to session caps |

**Readiness Default Rule:**
```
IF inputs.trainingcontext_global.readinessflag === null
  THEN derived.readinessflag = 'YELLOW'
  AND stateheader.readinessflag = 'YELLOW'
  AND rationale_stack.push({rule: 'DEFAULT_READINESS_YELLOW'})
```

### 8.3 Applied Caps (Post-Multiplier)

| Field | Formula |
|-------|---------|
| `weeklycontactscap_applied` | `weeklycontactscap_population × weeklymultiplier` |
| `sessioncontactscap_applied` | `sessioncontactscap_population × sessionmultiplier` |

### 8.4 Macro Counters (Optional)

**Constructed when:** Project history exists  
**Source:** `derived.projecthistory` (trailing 365 days)

---

## 9. Output Assembly Rules

**Timing:** After routing logic completes

### 9.1 Atomic Write Requirements (INV-004)

Router must write **stateheader + decisions atomically**. No partial writes allowed.

| Field | Source | Must Match |
|-------|--------|------------|
| `stateheader.activeproject` | Router decision | `decisions.activeproject` |
| `stateheader.routerversion` | Router | `decisions.routerversion` |
| `stateheader.seasontype` | Inputs | `inputs.trainingcontext_global.seasontype` |
| `stateheader.readinessflag` | Router (defaulted if needed) | `inputs.trainingcontext_global.readinessflag ?? 'YELLOW'` |
| `stateheader.eligible_for_training_today` | Router decision | `decisions.eligible_for_training_today` |
| `stateheader.lastupdated` | Router | Root `lastupdated` |
| `stateheader.clientid` | Inputs | Root `clientid` |

**Phase 2 Validation:** All "Must Match" rules enforced or collapse with `DEFAULTDENY_STATEHEADER_MISMATCH`

### 9.2 Decisions Construction

| Field | Construction Rule | Schema Enforcement |
|-------|------------------|-------------------|
| `activeproject` | Selected from legal_projects OR 'NONE' | Enum + 'NONE' |
| `legal_projects` | Array of projects passing all gates | `uniqueItems: true` (v1.0.2) |
| `illegal_projects_with_reasons` | All denied projects with reason codes | `reasoncode` must be from ReasonCode enum |
| `eligible_for_training_today` | `FALSE` if collapse, `TRUE` if legal_projects.length > 0 | boolean |
| `router_reasoncodes` | Array of all reason codes fired | `uniqueItems: true` (v1.0.2) |
| `rationale_stack` | Ordered list of rules evaluated | All 4 fields required per item |
| `routerversion` | Router version identifier | Must be in allowlist |

---

## 10. Conservative Defaults Matrix

**Rule:** Only context fields may be defaulted. Critical inputs trigger collapse (C-01).

| Field | Default Value | Condition | Log Code | Critical Input |
|-------|---------------|-----------|----------|----------------|
| `readinessflag` | `YELLOW` | If null | `DEFAULT_READINESS_YELLOW` | ❌ NO |
| `daysuntilnextgame` | `2` | If null AND `seasontype=INSEASON` | `DEFAULT_ASSUME_GAME_PROXIMITY` | ❌ NO |
| `practicegamesperweek` | `4` | If null AND `seasontype=INSEASON` | `DEFAULT_ASSUME_PRACTICE_VOLUME` | ❌ NO |

**Never Defaulted (trigger C-01):**
- `seasontype`
- `age`
- `sport`
- `athletetrack`
- `isinr2pservice`
- `injurytype`

**Default Logging Rule (INV-005):**
```
IF any field was defaulted
  THEN rationale_stack must include corresponding log code
```

---

## 11. Test Coverage Mapping

**Purpose:** Every rule must be validated by at least one test fixture.

| Rule ID | Description | Test Fixture ID | Pass Criteria |
|---------|-------------|-----------------|---------------|
| **C-01** | Missing critical input | COLLAPSE_01 | activeproject=NONE, reasoncode=DEFAULTDENY_MISSING_CRITICAL_INPUTS |
| **C-02** | Version mismatch | COLLAPSE_02 | activeproject=NONE, reasoncode=DEFAULTDENY_VERSION_MISMATCH |
| **C-04** | Coherence failure | COLLAPSE_04 | activeproject=NONE, reasoncode=DEFAULTDENY_STATEHEADER_MISMATCH |
| **C-05** | Medical lock | COLLAPSE_03 | activeproject=NONE, reasoncode=DEFAULTDENY_MEDICAL_LOCK |
| **R-01** | R2P enrollment locks SP | LEGAL_02 | activeproject=R2P_ACL, legal_projects=[R2P_ACL] |
| **POP-02** | Youth1316 routing | LEGAL_01 | population_enforced=Youth1316, enode_accent_cap_pct=0.40 |
| **INV-001** | Youth e-node accent cap | LEGAL_01 | enode_accent_cap_pct=0.40 for Youth1316 |

**Coverage Status:** 6 fixtures cover 7 core rules (collapse + routing + invariants)

**Gaps (future fixtures):**
- C-06 (Youth hardstop denial)
- C-07 (Hardstop no route)
- R-03 (R2P hardstop state)
- POP-01, POP-03, POP-04, POP-05 (other populations)
- Exit gate denials
- Macro cap denials
- Season denials

---

## 12. Rule Change Protocol

**Any change to this matrix requires:**
1. Version increment (e.g., v1.0 → v1.1)
2. Changelog entry with rule ID affected
3. New test fixture demonstrating change
4. Schema compatibility check (may require schema v1.0.3)
5. Router implementation update
6. Red-team audit sign-off

**Version Control:**
- Minor version (1.0 → 1.1): New rule added, existing rules unchanged
- Patch version (1.0.0 → 1.0.1): Clarification only, no logic change
- Major version (1.0 → 2.0): Breaking change to precedence or rule effects

---

## 13. Precedence Override Examples

**Example 1: Medical Lock Overrides R2P Enrollment**
```
inputs.medicalstatus.medicallocktriggered = true
inputs.medicalstatus.isinr2pservice = true

Priority 4 (Medical Lock) fires → activeproject=NONE
Priority 6 (R2P Enrollment) never evaluated
```

**Example 2: R2P Enrollment Overrides Population**
```
inputs.medicalstatus.isinr2pservice = true
derived.populationoverrides.population_enforced = Youth812

Priority 6 (R2P) fires → activeproject=R2P_ACL
Priority 7 (Population) never denies R2P_ACL (R2P is population-agnostic)
```

**Example 3: Season Overrides Exit Gates**
```
inputs.trainingcontext_global.seasontype = INSEASON
inputs.performancegates.exitflagssp.elasticreloadexitpassed = true

Priority 8 (Season) fires → ELASTIC_SPECIALIZATION denied (SEASON_DENY)
Priority 9 (Exit Gates) never evaluated
```

---

## Appendix A: Quick Reference Tables

### A.1 Reason Code Priority Map

| Reason Code | Priority Layer | Overridable |
|-------------|----------------|-------------|
| `DEFAULTDENY_VERSION_MISMATCH` | 1 | ❌ NO |
| `ROUTEROUTPUTINCOMPLETE` | 2 | ❌ NO |
| `DEFAULTDENY_STATEHEADER_MISMATCH` | 3 | ❌ NO |
| `DEFAULTDENY_MEDICAL_LOCK` | 4 | ❌ NO |
| `YOUTH_HARDSTOP_NONR2P_DENY_AND_REFER` | 5 | ❌ NO |
| `DEFAULTDENY_HARDSTOP_NO_ROUTE` | 5 | ❌ NO |
| `R2P_ENROLLMENT_LOCKS_SP` | 6 | ❌ NO |
| `AGE_POPULATION_DENY` | 7 | ✅ By R2P |
| `SEASON_DENY` | 8 | ✅ By R2P, Population |
| `EXIT_GATE_NOT_MET` | 9 | ✅ By R2P, Population, Season |
| `MACRO_CAP_EXCEEDED` | 10 | ✅ By R2P, Population, Season, Exit Gates |

### A.2 Project Classification

| Project Type | Projects | Allowed Populations | Allowed Seasons |
|--------------|----------|---------------------|-----------------|
| **R2P** | R2P_ACL | All | All |
| **SP Developmental** | COURT_SPORT_FOUNDATIONS, ELASTIC_RELOAD | Youth812+, Youth1316+, Youth17Advanced | OFF, PRE |
| **SP Specialization** | ELASTIC_SPECIALIZATION, DECEL_SPECIALIZATION, FORCE_SPECIALIZATION | Youth17Advanced, Adult_ATHLETE | OFF, PRE |
| **ICP** | ICP_BASKETBALL_INSEASON, ICP_VOLLEYBALL_INSEASON, ICP_BASKETBALL_POSTSEASON, ICP_VOLLEYBALL_POSTSEASON | Youth1316+, Youth17Advanced | IN or POST (project-specific) |
| **SP Baseline** | OFF_SEASON_BASELINE_COURT_VERTICAL | Youth1316+, Youth17Advanced | OFF, PRE |
| **Adult** | ADULT_STRENGTH, ADULT_MOBILITY, ADULT_ERL | Adult_GENERAL, Adult_ATHLETE | All |

---

**Version:** 1.0.0  
**Status:** PRODUCTION-LOCKED  
**Companion Schema:** EFL_GLOBAL_CLIENT_STATE_v1.0.2.json  
**Date:** 2026-01-15  

**This document is the authoritative logic truth for all Router decisions. Code must implement this matrix exactly.**
