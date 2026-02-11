# EFL Output Artifact Schema v1.0 — MAP & MATRIX

**Schema ID:** EFL_OUTPUT_ARTIFACT_SCHEMA_v1.0.json  
**Version:** 1.0.0  
**Effective Date:** 2026-01-15  
**Status:** PRODUCTION-LOCKED  
**Authority:** Elite Fitness Lab — Director of Performance Systems

---

## 1. Document Role

This schema is the **machine-enforceable validation contract** for all EFL training artifacts. It implements `EFL_OUTPUT_SPEC_GLOBAL_CONTRACT_v1.0` as a JSON Schema 2020-12 document.

**What this schema IS:**
- Executable validation logic for CI/QA
- Structural enforcement of global output contract
- Drift prevention via `additionalProperties: false`
- Type safety and enum constraints

**What this schema IS NOT:**
- A human-readable specification (see: EFL_OUTPUT_SPEC_GLOBAL_CONTRACT_v1.0.md)
- Project-specific content rules (those extend this schema)
- Router logic or state structure

**Companion Documents:**
- EFL_OUTPUT_SPEC_GLOBAL_CONTRACT_v1.0.md (human law this implements)
- EFL_GLOBAL_CLIENT_STATE_v1.0.2.json (state structure)
- EFL_PROJECT_REGISTRY_v1.0.json (project bindings)

---

## 2. Schema Structure Map

```
EFL_OUTPUT_ARTIFACT_SCHEMA_v1.0.json
├── properties
│   ├── header (GlobalHeader) — REQUIRED, drift-locked
│   ├── legality_snapshot (LegalitySnapshot) — REQUIRED, denial-mode aware
│   ├── cap_proof (CapProof) — CONDITIONAL (when caps_exist=true)
│   ├── exposure_summary (ExposureSummary) — CONDITIONAL (per artifact class)
│   ├── content_payload (ContentPayload) — CONDITIONAL (null for NOTICE_DENIAL)
│   └── metadata (ArtifactMetadata) — REQUIRED, version traceability
├── allOf (conditional requirements by artifact_class)
│   ├── SESSION/MICROSESSION/MESOCYCLE → require cap_proof + exposure_summary + content
│   ├── NOTICE_DENIAL → content_payload must be null
│   └── COMPLIANCE_SUMMARY → require cap_proof + exposure_summary
└── $defs
    ├── GlobalHeader (11 required fields, enums enforced)
    ├── LegalitySnapshot (denial explanation required when eligible=false)
    ├── CapProof (caps_exist predicate, structured adjustments)
    ├── CapAdjustment (5 cap types, 5 action types)
    ├── ExposureSummary (total_contacts + total_sets accuracy)
    ├── ContentPayload (null or project-specific object)
    └── ArtifactMetadata (4 version fields)
```

---

## 3. Conditional Requirements Matrix

This table shows which sections are required based on `artifact_class`:

| artifact_class | header | legality_snapshot | cap_proof | exposure_summary | content_payload |
|----------------|--------|-------------------|-----------|------------------|-----------------|
| **SESSION** | ✅ Required | ✅ Required | ✅ Required | ✅ Required | ✅ Required (non-null) |
| **MICROSESSION** | ✅ Required | ✅ Required | ✅ Required | ✅ Required | ✅ Required (non-null) |
| **MESOCYCLE** | ✅ Required | ✅ Required | ✅ Required | ✅ Required | ✅ Required (non-null) |
| **NOTICE_DENIAL** | ✅ Required | ✅ Required (+ denial_explanation) | Optional | Optional | ✅ Must be null |
| **COMPLIANCE_SUMMARY** | ✅ Required | ✅ Required | ✅ Required | ✅ Required | Optional |

**Implementation:** Uses `allOf` with `if/then` conditionals to enforce per-class requirements.

---

## 4. Global Header Field Matrix

All 11 fields are **required** and **drift-locked** (no additional properties).

| Field | Type | Enum/Format | Source | Validation Rule |
|-------|------|-------------|--------|-----------------|
| `clientid` | string | minLength: 1 | ClientState | Non-empty |
| `artifact_id` | string | format: uuid | Generator | Valid UUID |
| `artifact_class` | string | enum: [SESSION, MICROSESSION, MESOCYCLE, NOTICE_DENIAL, COMPLIANCE_SUMMARY] | Generator | Must be one of 5 classes |
| `target` | string | enum: [BRIDGEATHLETIC, COACHSHEET, MICROSESSION, MESOCYCLE, NOTICE] | Registry | Must be valid target |
| `generated_at` | string | format: date-time | Generator | ISO8601 timestamp |
| `projectid` | string | enum: [14 projects + NONE] | ClientState.decisions | Must be registered project or NONE |
| `routerversion` | string | minLength: 1 | ClientState.decisions | Non-empty |
| `state_lastupdated` | string | format: date-time | ClientState | ISO8601 timestamp |
| `seasontype` | string | enum: [OFFSEASON, PRESEASON, INSEASON, POSTSEASON] | ClientState.inputs | Must be valid season |
| `eligible_for_training_today` | boolean | — | ClientState.decisions | true or false |
| `reasoncodes` | array[string] | uniqueItems: true | ClientState.decisions | No duplicates |

---

## 5. Legality Snapshot Field Matrix

| Field | Type | Required | Conditional Requirement |
|-------|------|----------|------------------------|
| `activeproject` | string (enum) | ✅ Always | Must match projectid enum |
| `eligible` | boolean | ✅ Always | Must match header.eligible_for_training_today |
| `reasoncodes` | array[string] | ✅ Always | Must match header.reasoncodes |
| `legal_projects` | array[string] | ❌ Optional | Context only |
| `rationale_snippet` | array[object] | ❌ Optional | Top rules fired (audit trail) |
| `denial_explanation` | string | ✅ When eligible=false | Human-readable denial reason |

**Coherence Rule (enforced in CI, not schema):**
```
legality_snapshot.eligible === header.eligible_for_training_today
legality_snapshot.activeproject === header.projectid
legality_snapshot.reasoncodes === header.reasoncodes
```

---

## 6. Cap Proof Field Matrix

**Predicate:** `caps_exist = (derived != null AND populationoverrides != null AND readinessmultipliers != null)`

When `caps_exist=true`, all these fields are required:

| Field | Type | Validation Rule |
|-------|------|-----------------|
| `caps_exist` | boolean | Must be `true` (const) |
| `population_enforced` | string (enum) | One of: Youth812, Youth1316, Youth17Advanced, Adult_GENERAL, Adult_ATHLETE |
| `readinessflag` | string (enum) | One of: GREEN, YELLOW, RED |
| `weeklymultiplier` | number | Range: 0.0–1.0 |
| `sessionmultiplier` | number | Range: 0.0–1.0 |
| `weeklycontactscap_base` | integer | >= 0 |
| `weeklycontactscap_applied` | integer | >= 0, must equal base × weeklymultiplier |
| `sessioncontactscap_base` | integer | >= 0 |
| `sessioncontactscap_applied` | integer | >= 0, must equal base × sessionmultiplier |
| `enode_accent_cap_pct` | number or null | 0.40 for Youth812/1316, null otherwise |
| `maxbandallowed_population` | string (enum) | Band1, Band2, Band3, or Band4 |
| `maxenodeallowed_population` | string (enum) | E1, E2, E3, or E4 |
| `adjustments` | array[CapAdjustment] | Structured adjustment records |

**Youth Accent Cap Conditional (INV-OUT-007):**
```
IF population_enforced ∈ {Youth812, Youth1316}
  THEN enode_accent_cap_pct = 0.40 (const)
  ELSE enode_accent_cap_pct = null
```

---

## 7. Cap Adjustment Structure Matrix

When content is truncated/denied/limited, adjustments must be recorded:

| Field | Type | Enum | Required |
|-------|------|------|----------|
| `cap_type` | string | SESSION_CONTACT_CAP, WEEKLY_CONTACT_CAP, ENODE_ACCENT_CAP, BAND_CEILING, PROVIDER_CLEARANCE_GATE | ✅ |
| `action` | string | TRUNCATED, DENIED, AUTO_LIMITED, DOWNGRADED, BLOCKED | ✅ |
| `original_value` | integer/number/string | — | Optional |
| `applied_cap` | integer/number/string | — | Optional |
| `adjusted_value` | integer/number/string | — | Optional |
| `reason` | string | minLength: 1 | ✅ |

**Example:**
```json
{
  "cap_type": "SESSION_CONTACT_CAP",
  "action": "TRUNCATED",
  "original_value": 32,
  "applied_cap": 24,
  "adjusted_value": 24,
  "reason": "Readiness YELLOW, session cap applied (30 × 0.8 = 24)"
}
```

---

## 8. Exposure Summary Field Matrix

| Field | Type | Required | Validation Rule |
|-------|------|----------|-----------------|
| `total_contacts` | integer | ✅ | >= 0, must equal sum of contacts in content_payload (INV-OUT-006) |
| `total_sets` | integer | ✅ | >= 0, project must define computation in output spec |
| `exposure_breakdown` | object | Optional | Keys are categories, values are integers >= 0 |
| `key_exposures` | object | Optional | Project-specific highlights (max E-node, COD angle, etc.) |

**Accuracy Invariant (INV-OUT-006):**
```
exposure_summary.total_contacts === sum(all contacts in content_payload)
```

**total_sets Definition Requirement:**
Each project output spec must explicitly define how `total_sets` is computed (e.g., "work sets only, excludes warm-up").

---

## 9. Content Payload Conditional Logic

| Condition | content_payload Type | Validation |
|-----------|---------------------|------------|
| `artifact_class=NOTICE_DENIAL` | `null` | Must be null (no training content) |
| `eligible_for_training_today=false` | `null` | Must be null (INV-OUT-005) |
| `artifact_class ∈ {SESSION, MICROSESSION, MESOCYCLE}` | `object` | Must be non-null, structure per project spec |
| `artifact_class=COMPLIANCE_SUMMARY` | `object` or `null` | Optional |

---

## 10. Artifact Metadata Matrix

Ensures version traceability for reproducibility and audits:

| Field | Type | Pattern/Constraint | Purpose |
|-------|------|-------------------|---------|
| `generator_version` | string | minLength: 1 | Generator code version |
| `wrapper_version` | string | minLength: 1 | Project wrapper version used |
| `outputspec_version` | string | minLength: 1 | Project output spec version used |
| `global_contract_version` | string | pattern: `^1\.0(\.\d+)?$` | Must be v1.0.x |
| `validation_timestamp` | string | format: date-time (optional) | When artifact was validated |

---

## 11. Drift Lock Enforcement

These objects have `additionalProperties: false` to prevent schema drift:

| Object | Drift Lock | Effect |
|--------|------------|--------|
| Root artifact | ✅ | Cannot add top-level fields |
| GlobalHeader | ✅ | Cannot add header fields |
| LegalitySnapshot | ✅ | Cannot add legality fields |
| CapProof | ✅ | Cannot add cap proof fields |
| CapAdjustment | ✅ | Cannot add adjustment fields |
| ExposureSummary | ✅ | Cannot add summary fields (except exposure_breakdown/key_exposures) |
| ArtifactMetadata | ✅ | Cannot add metadata fields |

**Exception:** `exposure_breakdown` and `key_exposures` allow additional properties (project-specific extensions).

---

## 12. Validation Phase Matrix

**Phase 1: Schema Validation (Ajv strict mode)**
- Run artifact through this JSON Schema
- Check all required fields present
- Check types, formats, enums
- Check conditional requirements (allOf)

**Phase 2: Coherence Validation (CI script)**
- Verify `header.eligible_for_training_today === legality_snapshot.eligible`
- Verify `header.projectid === legality_snapshot.activeproject`
- Verify `header.reasoncodes === legality_snapshot.reasoncodes`
- Verify `weeklycontactscap_applied === weeklycontactscap_base × weeklymultiplier`
- Verify `sessioncontactscap_applied === sessioncontactscap_base × sessionmultiplier`

**Phase 3: Cap Compliance Validation (CI script)**
- Verify `exposure_summary.total_contacts <= cap_proof.sessioncontactscap_applied`
- Verify E-node accent cap enforced (if Youth812/1316)
- Verify band ceiling enforced
- Verify no E-node > maxenodeallowed_population

**Phase 4: Content Accuracy Validation (CI script)**
- Verify `exposure_summary.total_contacts` matches sum of contacts in `content_payload`
- Verify no content when `eligible=false`
- Verify project-specific constraints (from project output spec)

---

## 13. Error Code Matrix

When validation fails, emit structured error with code:

| Error Code | Phase | Meaning |
|------------|-------|---------|
| `SCHEMA_VALIDATION_FAILED` | 1 | Artifact structure invalid (missing field, wrong type, etc.) |
| `HEADER_INCOMPLETE` | 1 | Required header field missing |
| `COHERENCE_MISMATCH` | 2 | header ↔ legality_snapshot mismatch |
| `CAP_APPLIED_MISMATCH` | 2 | Applied cap ≠ base × multiplier |
| `CAP_EXCEEDED` | 3 | Exposure exceeds applied cap |
| `ACCENT_CAP_VIOLATED` | 3 | Youth E-node accent > 40% |
| `BAND_CEILING_VIOLATED` | 3 | Movement band > population ceiling |
| `EXPOSURE_MISMATCH` | 4 | total_contacts ≠ sum(content contacts) |
| `CONTENT_WHEN_INELIGIBLE` | 4 | content_payload non-null when eligible=false |
| `DENIAL_MISSING_EXPLANATION` | 1 | eligible=false but no denial_explanation |

---

## 14. CI Integration Spec

**Validation Command:**
```bash
ajv validate   --spec=draft2020   --strict=true   --all-errors   -s EFL_OUTPUT_ARTIFACT_SCHEMA_v1.0.json   -d artifact.json
```

**CI Pipeline Steps:**
1. Run Ajv schema validation (Phase 1)
2. If pass → run coherence validator (Phase 2)
3. If pass → run cap compliance validator (Phase 3)
4. If pass → run content accuracy validator (Phase 4)
5. If all pass → artifact is valid
6. If any fail → reject artifact with error code + details

**CI Fail Policy:**
- Any Phase 1 failure → hard fail (block merge/deploy)
- Any Phase 2-4 failure → hard fail (structural issue)
- Log all failures to audit trail

---

## 15. Schema Versioning Rules

**Version bump policy:**
- **Patch (v1.0.0 → v1.0.1):** Clarification only (e.g., description field update)
- **Minor (v1.0 → v1.1):** New optional field added (backward-compatible)
- **Major (v1.0 → v2.0):** Required field removed or type changed (breaking change)

**Compatibility Contract:**
- Artifacts valid under v1.0.0 must remain valid under v1.0.x
- Artifacts may become invalid under v1.1.0 if they rely on removed optionality
- Artifacts will likely be invalid under v2.0.0

**Current Version:** v1.0.0 (implements EFL_OUTPUT_SPEC_GLOBAL_CONTRACT_v1.0.md exactly)

---

## 16. Extension Protocol (How Projects Extend)

**Allowed Extensions (project schemas may):**
- Add fields to `exposure_summary.exposure_breakdown` (categories)
- Add fields to `exposure_summary.key_exposures` (project-specific highlights)
- Define `content_payload` structure (project-specific)
- Add target-specific rendering rules (serialization formats)

**Prohibited Overrides (project schemas must NOT):**
- Remove any required global field
- Change types or enums of global fields
- Set `additionalProperties: true` on drift-locked objects
- Violate conditional requirements (e.g., allow content when eligible=false)

**Enforcement:**
- Project schemas validated against this schema in CI
- Any violation → project schema rejected

---

## Appendix A: Quick Reference Tables

### A.1 Required vs Optional by Artifact Class

| Section | SESSION | MICROSESSION | MESOCYCLE | NOTICE_DENIAL | COMPLIANCE_SUMMARY |
|---------|---------|--------------|-----------|---------------|-------------------|
| header | Required | Required | Required | Required | Required |
| legality_snapshot | Required | Required | Required | Required | Required |
| cap_proof | Required | Required | Required | Optional | Required |
| exposure_summary | Required | Required | Required | Optional | Required |
| content_payload | Required (non-null) | Required (non-null) | Required (non-null) | Must be null | Optional |
| metadata | Required | Required | Required | Required | Required |

### A.2 Enum Constraint Summary

| Field | Enum Values |
|-------|-------------|
| artifact_class | SESSION, MICROSESSION, MESOCYCLE, NOTICE_DENIAL, COMPLIANCE_SUMMARY |
| target | BRIDGEATHLETIC, COACHSHEET, MICROSESSION, MESOCYCLE, NOTICE |
| projectid | 14 projects + NONE |
| seasontype | OFFSEASON, PRESEASON, INSEASON, POSTSEASON |
| population_enforced | Youth812, Youth1316, Youth17Advanced, Adult_GENERAL, Adult_ATHLETE |
| readinessflag | GREEN, YELLOW, RED |
| maxbandallowed_population | Band1, Band2, Band3, Band4 |
| maxenodeallowed_population | E1, E2, E3, E4 |
| cap_adjustment.cap_type | SESSION_CONTACT_CAP, WEEKLY_CONTACT_CAP, ENODE_ACCENT_CAP, BAND_CEILING, PROVIDER_CLEARANCE_GATE |
| cap_adjustment.action | TRUNCATED, DENIED, AUTO_LIMITED, DOWNGRADED, BLOCKED |

### A.3 Format Validation Summary

| Field | Format | Validation |
|-------|--------|------------|
| artifact_id | uuid | RFC 4122 UUID |
| generated_at | date-time | ISO8601 timestamp |
| state_lastupdated | date-time | ISO8601 timestamp |
| validation_timestamp | date-time | ISO8601 timestamp |

---

**Version:** 1.0.0  
**Status:** PRODUCTION-LOCKED  
**Companion Contract:** EFL_OUTPUT_SPEC_GLOBAL_CONTRACT_v1.0.md  
**Date:** 2026-01-15  

**This schema is the machine-enforceable validation contract for all EFL training artifacts. All generators must produce artifacts that validate against this schema.**
