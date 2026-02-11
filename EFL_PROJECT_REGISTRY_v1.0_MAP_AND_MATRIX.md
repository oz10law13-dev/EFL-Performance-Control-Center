# EFL_PROJECT_REGISTRY_v1.0 — MAP & MATRIX

**Effective Date:** 2026-01-15  
**Status:** PRODUCTION-LOCKED  
**Purpose:** Canonical registry binding `projectid → wrapper + output spec + runtime requirements`. This is the glue layer between Router decisions and generator/runtime execution.

---

## 1) What this document is (and is not)

### IS
- A **closed registry** of all projects the Router can ever select
- A deterministic mapping from **projectid** to:
  - wrapper authority (file + version)
  - output spec authority (file + version + targets)
  - System-1 dependency (if any)
  - runtime required inputs / exit gates / macro counters

### IS NOT
- Router precedence logic (that remains in `EFL_ROUTER_DECISION_MATRIX_v1.0.md`)
- Client state schema (that remains in `EFL_GLOBAL_CLIENT_STATE_v1.0.2.json`)
- Session content (lives in meso/micro content libraries)

---

## 2) Files produced

- **Registry data:** `EFL_PROJECT_REGISTRY_v1.0.json`
- **Registry schema:** `EFL_PROJECT_REGISTRY_SCHEMA_v1.0.json`
- **This reference:** `EFL_PROJECT_REGISTRY_v1.0_MAP_AND_MATRIX.md`

---

## 3) Core Registry Table (project → wrapper/output)

| projectid | projecttype | wrapper file | output spec file | System-1 dependency |
|---|---|---|---|---|
| ADULT_ERL | ADULT | EFL_ADULT_ERL_WRAPPER_v1_0.md | EFL_OUTPUTSPEC_ADULT_ERL_v1.0.json | none |
| ADULT_MOBILITY | ADULT | EFL_ADULT_MOBILITY_WRAPPER_v1_0.md | EFL_OUTPUTSPEC_ADULT_MOBILITY_v1.0.json | none |
| ADULT_STRENGTH | ADULT | EFL_ADULT_STRENGTH_WRAPPER_v1_0.md | EFL_OUTPUTSPEC_ADULT_STRENGTH_v1.0.json | none |
| COURT_SPORT_FOUNDATIONS | SP_FOUNDATIONS | EFL_SP_PROJECT_WRAPPER_COURT_SPORT_FOUNDATIONS_v1_0.md | EFL_SP_OUTPUT_SPEC_COURT_SPORT_FOUNDATIONS_v1_0.md | none |
| DECEL_SPECIALIZATION | SP_SPECIALIZATION | EFL_SP_PROJECT_WRAPPER_DECEL_SPECIALIZATION_v1_0.md | EFL_OUTPUTSPEC_DECEL_SPECIALIZATION_v1.0.json | none |
| ELASTIC_RELOAD | SP_RELOAD | EFL-ELASTIC-RELOAD-BLOCK-WRAPPER-v1.0.md | EFL_OUTPUTSPEC_ELASTIC_RELOAD_v1.0.json | none |
| ELASTIC_SPECIALIZATION | SP_SPECIALIZATION | EFL_SP_PROJECT_WRAPPER_ELASTIC_SPECIALIZATION_v1_0.md | EFL_OUTPUTSPEC_ELASTIC_SPECIALIZATION_v1.0.json | none |
| FORCE_SPECIALIZATION | SP_SPECIALIZATION | EFL_SP_PROJECT_WRAPPER_FORCE_SPECIALIZATION_v1_0.md | EFL_OUTPUTSPEC_FORCE_SPECIALIZATION_v1.0.json | none |
| ICP_BASKETBALL_INSEASON | ICP | EFL_ICP_BASKETBALL_INSEASON_WRAPPER_v1_0.md | EFL_OUTPUTSPEC_ICP_BASKETBALL_IN_v1.0.json | none |
| ICP_BASKETBALL_POSTSEASON | ICP | EFL_ICP_BASKETBALL_POSTSEASON_WRAPPER_v1_0.md | EFL_OUTPUTSPEC_ICP_BASKETBALL_POST_v1.0.json | none |
| ICP_VOLLEYBALL_INSEASON | ICP | EFL_ICP_VOLLEYBALL_INSEASON_WRAPPER_v1_0.md | EFL_OUTPUTSPEC_ICP_VOLLEYBALL_IN_v1.0.json | none |
| ICP_VOLLEYBALL_POSTSEASON | ICP | EFL_ICP_VOLLEYBALL_POSTSEASON_WRAPPER_v1_0.md | EFL_OUTPUTSPEC_ICP_VOLLEYBALL_POST_v1.0.json | none |
| OFF_SEASON_BASELINE_COURT_VERTICAL | BASELINE | EFL_SP_PROJECT_WRAPPER_OFFSEASON_BASELINE_COURT_VERTICAL_v1_0.md | EFL_OUTPUTSPEC_BASELINE_COURT_VERTICAL_v1.0.json | none |
| R2P_ACL | R2P | EFL_SP_PROJECT_WRAPPER_R2P_ACL_v1_1.md | EFL_SP_OUTPUT_SPEC_R2P_ACL_v1_0.md | EFL_R2P_ACL_SYSTEM1_LEGALITY_ENGINE_v1_0_6.json |


> Note: Several wrapper/output-spec filenames are placeholders where the authority file is not yet created in the repo. The registry still locks the *expected* authority name so you can build those artifacts without ambiguity.

---

## 4) Router Binding Matrix (copied authority)

| projectid | allowed_populations | allowed_seasons | requires_r2p_enrollment |
|---|---|---|---|
| ADULT_ERL | Adult_GENERAL, Adult_ATHLETE | OFFSEASON, PRESEASON, INSEASON, POSTSEASON | false |
| ADULT_MOBILITY | Adult_GENERAL, Adult_ATHLETE | OFFSEASON, PRESEASON, INSEASON, POSTSEASON | false |
| ADULT_STRENGTH | Adult_GENERAL, Adult_ATHLETE | OFFSEASON, PRESEASON, INSEASON, POSTSEASON | false |
| COURT_SPORT_FOUNDATIONS | Youth812, Youth1316, Youth17Advanced | OFFSEASON, PRESEASON | false |
| DECEL_SPECIALIZATION | Youth17Advanced, Adult_ATHLETE | OFFSEASON, PRESEASON | false |
| ELASTIC_RELOAD | Youth812, Youth1316, Youth17Advanced | OFFSEASON, PRESEASON | false |
| ELASTIC_SPECIALIZATION | Youth17Advanced, Adult_ATHLETE | OFFSEASON, PRESEASON | false |
| FORCE_SPECIALIZATION | Youth17Advanced, Adult_ATHLETE | OFFSEASON, PRESEASON | false |
| ICP_BASKETBALL_INSEASON | Youth1316, Youth17Advanced | INSEASON | false |
| ICP_BASKETBALL_POSTSEASON | Youth1316, Youth17Advanced | POSTSEASON | false |
| ICP_VOLLEYBALL_INSEASON | Youth1316, Youth17Advanced | INSEASON | false |
| ICP_VOLLEYBALL_POSTSEASON | Youth1316, Youth17Advanced | POSTSEASON | false |
| OFF_SEASON_BASELINE_COURT_VERTICAL | Youth1316, Youth17Advanced | OFFSEASON, PRESEASON | false |
| R2P_ACL | Youth812, Youth1316, Youth17Advanced, Adult_GENERAL, Adult_ATHLETE | OFFSEASON, PRESEASON, INSEASON, POSTSEASON | true |


**Interpretation rules (runtime):**
- If Router selects a project that violates these bindings, that is a **Router bug** (CI should catch it).
- Runtime may still enforce these as a **sanity check** (defensive deny).

---

## 5) Runtime Requirements Matrix (inputs / exit / macro)

| projectid | required_inputs.critical | exit_gates.required_flags | macro_caps.counters |
|---|---|---|---|
| ADULT_ERL | inputs.trainingcontext_global.seasontype<br>inputs.athleteprofile.athletetrack | — | — |
| ADULT_MOBILITY | inputs.trainingcontext_global.seasontype<br>inputs.athleteprofile.athletetrack | — | — |
| ADULT_STRENGTH | inputs.trainingcontext_global.seasontype<br>inputs.athleteprofile.athletetrack | — | — |
| COURT_SPORT_FOUNDATIONS | inputs.trainingcontext_global.seasontype | — | — |
| DECEL_SPECIALIZATION | inputs.performancegates.exitflagssp.foundationsexitpassed<br>derived.macrocounters.decel_specialization_blocks_used | inputs.performancegates.exitflagssp.foundationsexitpassed | derived.macrocounters.decel_specialization_blocks_used |
| ELASTIC_RELOAD | inputs.trainingcontext_global.seasontype | — | — |
| ELASTIC_SPECIALIZATION | inputs.performancegates.exitflagssp.elasticreloadexitpassed<br>derived.macrocounters.elasticspecialization_blocks_used | inputs.performancegates.exitflagssp.elasticreloadexitpassed | derived.macrocounters.elasticspecialization_blocks_used |
| FORCE_SPECIALIZATION | inputs.performancegates.exitflagssp.foundationsexitpassed<br>derived.macrocounters.forcebias_specialization_blocks_used | inputs.performancegates.exitflagssp.foundationsexitpassed | derived.macrocounters.forcebias_specialization_blocks_used |
| ICP_BASKETBALL_INSEASON | inputs.trainingcontext_global.seasontype<br>inputs.athleteprofile.sport | — | derived.macrocounters.consecutive_highcns_blocks |
| ICP_BASKETBALL_POSTSEASON | inputs.trainingcontext_global.seasontype<br>inputs.athleteprofile.sport | — | derived.macrocounters.consecutive_highcns_blocks |
| ICP_VOLLEYBALL_INSEASON | inputs.trainingcontext_global.seasontype<br>inputs.athleteprofile.sport | — | derived.macrocounters.consecutive_highcns_blocks |
| ICP_VOLLEYBALL_POSTSEASON | inputs.trainingcontext_global.seasontype<br>inputs.athleteprofile.sport | — | derived.macrocounters.consecutive_highcns_blocks |
| OFF_SEASON_BASELINE_COURT_VERTICAL | inputs.trainingcontext_global.seasontype | — | — |
| R2P_ACL | inputs.medicalstatus.isinr2pservice<br>inputs.medicalstatus.injurytype<br>inputs.medicalstatus.hardstopstatus<br>inputs.trainingcontext_global.seasontype | — | — |


---

## 6) Registry-Level Invariants (enforced by schema + CI)

1. **ProjectID closure**
   - The registry contains **exactly** the project set defined by `ClientState.decisions.activeproject` enum (minus `NONE`).

2. **One-to-one binding**
   - Each project appears **exactly once**.
   - Implemented by making `projects` an **object keyed by projectid** with `additionalProperties:false` (stronger than an array + uniqueItems).

3. **Deterministic output targets**
   - Generator may only emit the `outputspec.targets` declared here.

4. **System-1 dependency clarity**
   - If `system1 != null`, runtime must not execute without System-1 producing the required derived slice(s).

5. **Wrapper isolation**
   - Wrappers are **read-only consumers** of `{inputs, derived, decisions}` for their project. No back-writes.

---

## 7) Runtime Interfaces

### 7.1 Router → Registry (minimal dependency)
Router may use the registry only for:
- **Project existence check** (registered / not-registered)
- Optional **CI sanity**: ensure router’s legal project set equals registry project set

### 7.2 Runtime → Registry (authoritative)
Given `decisions.activeproject`:
1. Lookup `projects[activeproject]`
2. Load wrapper authority
3. Load output spec authority
4. Assert presence of `required_inputs.critical`
5. Assert exit gates and macro counters if the project requires them
6. If any missing → deny generation (fail-closed)

### 7.3 Generator → Registry (deterministic emit)
Generator uses:
- `outputspec.targets` to decide which artifacts it’s allowed to produce
- `outputspec.file` to determine the payload structure for each target

---

## 8) Change protocol (how to evolve v1.0 safely)

- **Any new project** requires:
  1) adding it to ClientState enum  
  2) adding it to Router Decision Matrix  
  3) adding it here (registry)  
  4) adding fixtures proving selection/denial paths

- **Any wrapper/output spec rename** requires:
  - registry update + version bump (v1.0 → v1.1)
  - CI check that old name is not referenced anywhere

---

## 9) Known TODOs (authority file creation)

The registry names several authority artifacts that should be created next (wrappers and output specs for specialization/ICP/baseline/adult projects). Until those exist, runtime should treat these entries as **registered but not executable** unless the referenced file is present.
