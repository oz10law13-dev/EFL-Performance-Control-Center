# EFL CI Validator Invariants v1.0

**Specification ID:** EFL_CI_VALIDATOR_INVARIANTS  
**Version:** 1.0.0  
**Effective Date:** 2026-01-15  
**Status:** PRODUCTION-LOCKED  
**Authority:** Elite Fitness Lab — Director of Performance Systems

---

## Document Role

This document defines the **CI-enforceable validation invariants** for all EFL training artifacts. It specifies validation logic that cannot be expressed in JSON Schema alone (arithmetic checks, cross-artifact constraints, ordering requirements).

**What this document IS:**
- Phase 2-4 validation logic (beyond JSON Schema)
- Named invariants with error codes
- CI integration commands
- Cross-artifact constraint enforcement

**What this document IS NOT:**
- JSON Schema logic (Phase 1 is in EFL_OUTPUT_ARTIFACT_SCHEMA_v1.0.1.json)
- Generator implementation details
- Router decision logic

**Companion Documents:**
- EFL_OUTPUT_ARTIFACT_SCHEMA_v1.0.1.json (Phase 1 schema validation)
- EFL_OUTPUT_SPEC_GLOBAL_CONTRACT_v1.0.md (human law)
- EFL_GLOBAL_CLIENT_STATE_v1.0.2.json (state structure)

---

## 1. Validation Architecture

```
Artifact Generation
        ↓
┌─────────────────────────────────────┐
│ Phase 1: JSON Schema Validation    │ ← Ajv (EFL_OUTPUT_ARTIFACT_SCHEMA_v1.0.1.json)
│ - Structure, types, enums           │
│ - Conditional requirements          │
│ - Drift lock enforcement            │
└─────────────────┬───────────────────┘
                  ↓ (pass)
┌─────────────────────────────────────┐
│ Phase 2: Coherence Validation      │ ← This doc (INV-CI-002, INV-OUT-008)
│ - Header ↔ Legality alignment       │
│ - Cap math correctness              │
│ - Version consistency               │
└─────────────────┬───────────────────┘
                  ↓ (pass)
┌─────────────────────────────────────┐
│ Phase 3: Cap Compliance Validation │ ← This doc (INV-CI-001, INV-OUT-007)
│ - Exposure ≤ Applied caps           │
│ - Weekly cumulative caps            │
│ - Youth accent caps                 │
│ - Band/E-node ceilings              │
└─────────────────┬───────────────────┘
                  ↓ (pass)
┌─────────────────────────────────────┐
│ Phase 4: Content Accuracy          │ ← This doc (INV-CI-003, project specs)
│ - Exposure summary math             │
│ - Adjustment logging                │
│ - Content null when ineligible      │
│ - Project-specific constraints      │
└─────────────────┬───────────────────┘
                  ↓ (pass)
        Artifact Approved
```

**Execution Policy:**
- Phases run sequentially (1 → 2 → 3 → 4)
- Any phase failure → reject artifact, emit error code
- All phases must pass for artifact approval

---

## 2. CI-Enforced Invariants

### 2.1 Cross-Artifact Invariants

**INV-CI-001: Weekly Cap Enforcement**

**Rule:**
```
FOR clientid IN artifact.header.clientid:
  LET artifacts_this_week = all artifacts for clientid in rolling 7 days from generated_at
  LET total_weekly_contacts = SUM(artifacts_this_week[*].exposure_summary.total_contacts)

  ASSERT total_weekly_contacts <= artifact.cap_proof.weeklycontactscap_applied
```

**Purpose:** Prevent cumulative weekly cap violations across multiple sessions

**Phase:** 3 (Cap Compliance Validation)

**Error Code:** `WEEKLY_CAP_EXCEEDED`

**Error Message Template:**
```
Weekly cap exceeded for client {clientid}.
Weekly contacts: {total_weekly_contacts}
Weekly cap: {weeklycontactscap_applied}
Violation: +{total_weekly_contacts - weeklycontactscap_applied} contacts over cap
```

**Notes:**
- Rolling 7-day window calculated from `artifact.header.generated_at`
- Includes current artifact in sum
- Generator should check before emission (defensive)
- CI validates as final gate

---

### 2.2 Coherence Invariants

**INV-CI-002: Reason Codes Coherence**

**Rule:**
```
ASSERT artifact.header.reasoncodes === artifact.legality_snapshot.reasoncodes
  BY VALUE AND ORDER

Router outputs reasoncodes in precedence order (Priority 1 → 11)
Artifact must preserve exact ordering
```

**Purpose:** Ensure legality snapshot exactly mirrors Router decision

**Phase:** 2 (Coherence Validation)

**Error Code:** `COHERENCE_MISMATCH_REASONCODES`

**Error Message Template:**
```
Reason codes mismatch between header and legality_snapshot.
Header: {header.reasoncodes}
Legality: {legality_snapshot.reasoncodes}
```

**Additional Coherence Checks (INV-CI-002 family):**

| Check | Rule | Error Code |
|-------|------|------------|
| Eligibility match | `header.eligible_for_training_today === legality_snapshot.eligible` | `COHERENCE_MISMATCH_ELIGIBILITY` |
| Project match | `header.projectid === legality_snapshot.activeproject` | `COHERENCE_MISMATCH_PROJECTID` |
| Season match | `header.seasontype === ClientState.inputs.trainingcontext_global.seasontype` | `COHERENCE_MISMATCH_SEASONTYPE` |
| Router version match | `header.routerversion === ClientState.decisions.routerversion` | `COHERENCE_MISMATCH_ROUTERVERSION` |

---

**INV-OUT-008: Cap Proof Prohibition When Ineligible**

**Rule:**
```
IF artifact.header.eligible_for_training_today = false
  THEN artifact.cap_proof MUST NOT exist (must be undefined/null)
  AND artifact.header.artifact_class MUST = "NOTICE_DENIAL"
  AND artifact.content_payload MUST = null
```

**Purpose:** Prevent generators from fabricating cap proof when training is denied

**Phase:** 2 (Coherence Validation)

**Error Code:** `CAP_PROOF_WHEN_INELIGIBLE`

**Error Message Template:**
```
Cap proof must not exist when training is denied.
Eligible: false
Artifact class: {artifact_class}
Cap proof present: true (VIOLATION)
```

**Notes:**
- This closes GAP-01 from gap analysis
- Implicit via artifact_class conditioning, but now explicit invariant

---

### 2.3 Cap Math Invariants

**INV-CI-002-CAP-MATH: Applied Caps Correctness**

**Rules:**
```
ASSERT cap_proof.weeklycontactscap_applied 
  = ROUND(cap_proof.weeklycontactscap_base × cap_proof.weeklymultiplier)

ASSERT cap_proof.sessioncontactscap_applied 
  = ROUND(cap_proof.sessioncontactscap_base × cap_proof.sessionmultiplier)
```

**Purpose:** Verify cap math is correct (base × multiplier = applied)

**Phase:** 2 (Coherence Validation)

**Error Code:** `CAP_APPLIED_MISMATCH`

**Error Message Template:**
```
Applied cap does not match base × multiplier.
Type: {weekly|session}
Base: {base}
Multiplier: {multiplier}
Expected: {base × multiplier}
Actual: {applied}
```

---

### 2.4 Cap Compliance Invariants

**INV-OUT-007: Session Cap Compliance**

**Rule:**
```
ASSERT artifact.exposure_summary.total_contacts 
  <= artifact.cap_proof.sessioncontactscap_applied
```

**Purpose:** Ensure session does not exceed applied cap

**Phase:** 3 (Cap Compliance Validation)

**Error Code:** `CAP_EXCEEDED`

**Error Message Template:**
```
Session contacts exceed applied cap.
Total contacts: {total_contacts}
Session cap: {sessioncontactscap_applied}
Violation: +{total_contacts - cap} contacts over cap
```

**Notes:**
- This closes GAP-02 from gap analysis
- Generator should enforce; CI validates

---

**INV-OUT-009: Youth Accent Cap Compliance**

**Rule:**
```
IF cap_proof.population_enforced IN ["Youth812", "Youth1316"]
  THEN:
    LET accent_contacts = SUM(content_payload movements where E-node ∈ {E3, E4})
    LET accent_pct = accent_contacts / exposure_summary.total_contacts

    ASSERT accent_pct <= 0.40
    ASSERT cap_proof.enode_accent_cap_pct = 0.40
```

**Purpose:** Enforce Youth E3+ accent cap (40%)

**Phase:** 3 (Cap Compliance Validation)

**Error Code:** `ACCENT_CAP_VIOLATED`

**Error Message Template:**
```
Youth E-node accent cap violated.
Population: {population_enforced}
Accent contacts: {accent_contacts}
Total contacts: {total_contacts}
Accent percentage: {accent_pct} (> 40%)
```

---

**INV-OUT-010: Band Ceiling Compliance**

**Rule:**
```
FOR EACH movement IN content_payload:
  IF movement.band EXISTS:
    ASSERT movement.band <= cap_proof.maxbandallowed_population
```

**Purpose:** Ensure no movements exceed population band ceiling

**Phase:** 3 (Cap Compliance Validation)

**Error Code:** `BAND_CEILING_VIOLATED`

**Error Message Template:**
```
Movement exceeds population band ceiling.
Movement: {movement_name}
Band: {movement.band}
Ceiling: {maxbandallowed_population}
Population: {population_enforced}
```

---

**INV-OUT-011: E-Node Ceiling Compliance**

**Rule:**
```
FOR EACH movement IN content_payload:
  IF movement.enode EXISTS:
    ASSERT movement.enode <= cap_proof.maxenodeallowed_population
```

**Purpose:** Ensure no movements exceed population E-node ceiling

**Phase:** 3 (Cap Compliance Validation)

**Error Code:** `ENODE_CEILING_VIOLATED`

**Error Message Template:**
```
Movement exceeds population E-node ceiling.
Movement: {movement_name}
E-node: {movement.enode}
Ceiling: {maxenodeallowed_population}
Population: {population_enforced}
```

---

### 2.5 Content Accuracy Invariants

**INV-CI-003: Adjustment Logging Required**

**Rule:**
```
IF content was modified to respect caps (truncate/deny/limit):
  THEN cap_proof.adjustments.length >= 1
  AND adjustments[*] contain entry matching the modification
```

**Purpose:** Prevent silent cap enforcement without audit trail

**Phase:** 4 (Content Accuracy Validation)

**Error Code:** `CAP_ADJUSTMENT_NOT_LOGGED`

**Error Message Template:**
```
Content appears truncated but no adjustment logged.
Expected contacts: {expected} (from project spec)
Actual contacts: {total_contacts}
Adjustments logged: {adjustments.length}
```

**Notes:**
- This closes GAP-M2 from gap analysis
- Heuristic: if total_contacts < typical_project_contacts → adjustment expected

---

**INV-OUT-006: Exposure Summary Accuracy** (from Global Contract)

**Rule:**
```
LET computed_contacts = SUM(all contact-generating movements in content_payload)

ASSERT exposure_summary.total_contacts = computed_contacts
```

**Purpose:** Ensure exposure summary matches actual content

**Phase:** 4 (Content Accuracy Validation)

**Error Code:** `EXPOSURE_MISMATCH`

**Error Message Template:**
```
Exposure summary does not match content payload.
Summary total_contacts: {exposure_summary.total_contacts}
Computed from content: {computed_contacts}
Difference: {|summary - computed|}
```

**Notes:**
- Requires parsing content_payload (project-specific structure)
- Generator must compute accurately

---

**INV-OUT-005: No Content When Ineligible** (from Global Contract)

**Rule:**
```
IF artifact.header.eligible_for_training_today = false:
  THEN artifact.content_payload MUST = null
  AND artifact.header.artifact_class MUST = "NOTICE_DENIAL"
```

**Purpose:** Prevent training content when Router denied permission

**Phase:** 4 (Content Accuracy Validation)

**Error Code:** `CONTENT_WHEN_INELIGIBLE`

**Error Message Template:**
```
Content payload must be null when training is denied.
Eligible: false
Artifact class: {artifact_class}
Content payload: {content_payload !== null ? "PRESENT (VIOLATION)" : "null"}
```

---

## 3. Error Code Reference

### 3.1 Complete Error Code Matrix

| Error Code | Phase | Invariant | Severity | Action |
|------------|-------|-----------|----------|--------|
| `SCHEMA_VALIDATION_FAILED` | 1 | JSON Schema | Critical | Reject artifact |
| `HEADER_INCOMPLETE` | 1 | JSON Schema | Critical | Reject artifact |
| `COHERENCE_MISMATCH_ELIGIBILITY` | 2 | INV-CI-002 | Critical | Reject artifact |
| `COHERENCE_MISMATCH_PROJECTID` | 2 | INV-CI-002 | Critical | Reject artifact |
| `COHERENCE_MISMATCH_SEASONTYPE` | 2 | INV-CI-002 | Critical | Reject artifact |
| `COHERENCE_MISMATCH_ROUTERVERSION` | 2 | INV-CI-002 | Critical | Reject artifact |
| `COHERENCE_MISMATCH_REASONCODES` | 2 | INV-CI-002 | Critical | Reject artifact |
| `CAP_PROOF_WHEN_INELIGIBLE` | 2 | INV-OUT-008 | Critical | Reject artifact |
| `CAP_APPLIED_MISMATCH` | 2 | INV-CI-002-CAP-MATH | Critical | Reject artifact |
| `CAP_EXCEEDED` | 3 | INV-OUT-007 | Critical | Reject artifact |
| `WEEKLY_CAP_EXCEEDED` | 3 | INV-CI-001 | Critical | Reject artifact |
| `ACCENT_CAP_VIOLATED` | 3 | INV-OUT-009 | Critical | Reject artifact |
| `BAND_CEILING_VIOLATED` | 3 | INV-OUT-010 | Critical | Reject artifact |
| `ENODE_CEILING_VIOLATED` | 3 | INV-OUT-011 | Critical | Reject artifact |
| `EXPOSURE_MISMATCH` | 4 | INV-OUT-006 | Critical | Reject artifact |
| `CONTENT_WHEN_INELIGIBLE` | 4 | INV-OUT-005 | Critical | Reject artifact |
| `CAP_ADJUSTMENT_NOT_LOGGED` | 4 | INV-CI-003 | Warning | Log + flag for review |
| `DENIAL_MISSING_EXPLANATION` | 1 | JSON Schema | Critical | Reject artifact |

### 3.2 Error Severity Levels

| Severity | Meaning | CI Action |
|----------|---------|-----------|
| **Critical** | Artifact violates safety constraint or audit requirement | Hard fail (block merge/deploy) |
| **Warning** | Artifact may be incomplete but not unsafe | Log + flag for review (allow with notice) |

---

## 4. CI Integration Specification

### 4.1 Validation Pipeline

**Step 1: Phase 1 (JSON Schema)**
```bash
ajv validate   --spec=draft2020   --strict=true   --all-errors   -s EFL_OUTPUT_ARTIFACT_SCHEMA_v1.0.1.json   -d artifact.json

# Exit code 0 → pass, proceed to Phase 2
# Exit code non-zero → fail, emit SCHEMA_VALIDATION_FAILED
```

**Step 2: Phase 2 (Coherence)**
```bash
python3 validate_phase2_coherence.py artifact.json

# Checks:
# - INV-CI-002 (reason codes, eligibility, project, season, router version)
# - INV-OUT-008 (cap proof prohibition when ineligible)
# - INV-CI-002-CAP-MATH (cap applied = base × multiplier)

# Exit code 0 → pass, proceed to Phase 3
# Exit code non-zero → fail, emit error code from stderr
```

**Step 3: Phase 3 (Cap Compliance)**
```bash
python3 validate_phase3_caps.py artifact.json   --state-db state.db   --clientid {artifact.header.clientid}

# Checks:
# - INV-OUT-007 (session cap compliance)
# - INV-CI-001 (weekly cap enforcement, cross-artifact)
# - INV-OUT-009 (youth accent cap)
# - INV-OUT-010 (band ceiling)
# - INV-OUT-011 (E-node ceiling)

# Exit code 0 → pass, proceed to Phase 4
# Exit code non-zero → fail, emit error code from stderr
```

**Step 4: Phase 4 (Content Accuracy)**
```bash
python3 validate_phase4_content.py artifact.json   --project-spec {artifact.metadata.outputspec_version}

# Checks:
# - INV-OUT-006 (exposure summary accuracy)
# - INV-OUT-005 (no content when ineligible)
# - INV-CI-003 (adjustment logging)
# - Project-specific constraints (from project output spec)

# Exit code 0 → pass, artifact approved
# Exit code non-zero → fail, emit error code from stderr
```

### 4.2 CI Fail Policy

| Phase | Failure Action | Merge Policy | Deploy Policy |
|-------|----------------|--------------|---------------|
| 1 | Block immediately | ❌ Block merge | ❌ Block deploy |
| 2 | Block immediately | ❌ Block merge | ❌ Block deploy |
| 3 | Block immediately | ❌ Block merge | ❌ Block deploy |
| 4 (Critical) | Block immediately | ❌ Block merge | ❌ Block deploy |
| 4 (Warning) | Log + flag | ✅ Allow merge with notice | ⚠️ Allow deploy with audit flag |

### 4.3 Validation Output Format

**Success:**
```json
{
  "artifact_id": "550e8400-e29b-41d4-a716-446655440000",
  "validation_status": "PASS",
  "phases_passed": [1, 2, 3, 4],
  "timestamp": "2026-01-15T23:45:00-06:00",
  "validator_version": "1.0.0"
}
```

**Failure:**
```json
{
  "artifact_id": "550e8400-e29b-41d4-a716-446655440000",
  "validation_status": "FAIL",
  "failed_phase": 3,
  "error_code": "CAP_EXCEEDED",
  "error_message": "Session contacts exceed applied cap. Total contacts: 32, Session cap: 24, Violation: +8 contacts over cap",
  "details": {
    "total_contacts": 32,
    "sessioncontactscap_applied": 24,
    "violation": 8
  },
  "timestamp": "2026-01-15T23:45:00-06:00",
  "validator_version": "1.0.0"
}
```

---

## 5. State Database Requirements (for INV-CI-001)

### 5.1 Weekly Cap Enforcement Data Model

To enforce `INV-CI-001` (weekly cap), CI must access artifact history.

**Minimum Schema:**
```sql
CREATE TABLE artifact_history (
  artifact_id UUID PRIMARY KEY,
  clientid VARCHAR(255) NOT NULL,
  generated_at TIMESTAMP NOT NULL,
  total_contacts INTEGER NOT NULL,
  weeklycontactscap_applied INTEGER NOT NULL,
  artifact_class VARCHAR(50) NOT NULL,
  INDEX idx_clientid_generated (clientid, generated_at)
);
```

**Query for Weekly Cap Check:**
```sql
SELECT SUM(total_contacts) as weekly_total
FROM artifact_history
WHERE clientid = ?
  AND generated_at >= (? - INTERVAL '7 days')
  AND artifact_class IN ('SESSION', 'MICROSESSION', 'MESOCYCLE');
```

**Alternative:** Stateless validation (generator tracks, validator trusts)
- Generator maintains rolling 7-day count
- Embeds count in artifact metadata
- Validator checks math, not history

---

## 6. Invariant Coverage Map

### 6.1 Gap Coverage Matrix

| Gap ID | Description | Closed By | Invariant |
|--------|-------------|-----------|-----------|
| GAP-C1 | cap_proof presence enforcement | Schema v1.0.1 | allOf conditional |
| GAP-C2 | Weekly cap enforcement | This doc | INV-CI-001 |
| GAP-C3 | Reason codes ordering | This doc | INV-CI-002 |
| GAP-M2 | Adjustments logging | This doc | INV-CI-003 |
| GAP-02 | Exposure vs cap check | This doc | INV-OUT-007 |
| GAP-01 | cap_proof when ineligible | This doc | INV-OUT-008 |

### 6.2 Invariant → Error Code → Phase Map

| Invariant | Error Code | Phase | Severity |
|-----------|------------|-------|----------|
| INV-CI-001 | WEEKLY_CAP_EXCEEDED | 3 | Critical |
| INV-CI-002 | COHERENCE_MISMATCH_* | 2 | Critical |
| INV-CI-003 | CAP_ADJUSTMENT_NOT_LOGGED | 4 | Warning |
| INV-OUT-005 | CONTENT_WHEN_INELIGIBLE | 4 | Critical |
| INV-OUT-006 | EXPOSURE_MISMATCH | 4 | Critical |
| INV-OUT-007 | CAP_EXCEEDED | 3 | Critical |
| INV-OUT-008 | CAP_PROOF_WHEN_INELIGIBLE | 2 | Critical |
| INV-OUT-009 | ACCENT_CAP_VIOLATED | 3 | Critical |
| INV-OUT-010 | BAND_CEILING_VIOLATED | 3 | Critical |
| INV-OUT-011 | ENODE_CEILING_VIOLATED | 3 | Critical |

---

## 7. Validator Implementation Checklist

**Phase 1 (Ajv):**
- ✅ Install ajv-cli (`npm install -g ajv-cli`)
- ✅ Run schema validation
- ✅ Parse errors to structured JSON

**Phase 2 (Coherence):**
- [ ] Implement `validate_phase2_coherence.py`
- [ ] Check header ↔ legality_snapshot alignment
- [ ] Check cap math (base × multiplier = applied)
- [ ] Check cap_proof prohibition when ineligible
- [ ] Emit structured error JSON

**Phase 3 (Cap Compliance):**
- [ ] Implement `validate_phase3_caps.py`
- [ ] Query artifact history for weekly cap check
- [ ] Check session cap compliance
- [ ] Check youth accent cap
- [ ] Check band/E-node ceilings
- [ ] Emit structured error JSON

**Phase 4 (Content Accuracy):**
- [ ] Implement `validate_phase4_content.py`
- [ ] Parse content_payload (project-specific)
- [ ] Compute total contacts from content
- [ ] Check exposure summary accuracy
- [ ] Check adjustment logging
- [ ] Check no content when ineligible
- [ ] Emit structured error JSON

**CI Integration:**
- [ ] Add validation pipeline to `.github/workflows/` or equivalent
- [ ] Configure fail policy (block merge on critical, flag on warning)
- [ ] Set up artifact history database (or stateless alternative)
- [ ] Configure notifications for validation failures

---

## 8. Known Limitations

### 8.1 Deferred Hardening (Acceptable)

**reasoncodes Enum Binding (GAP-04)**
- **Status:** Deferred to v1.1+
- **Rationale:** Router enforces upstream; artifact is snapshot
- **Risk:** Low (artifact not used as input elsewhere)
- **Future fix:** Bind `reasoncodes` items to Router ReasonCode enum

**total_sets Validation (GAP-03)**
- **Status:** Delegated to project output specs
- **Rationale:** Computation is project-specific
- **Risk:** Medium (different projects could define differently)
- **Mitigation:** Require "total_sets Definition" section in all project output specs

### 8.2 Out of Scope

**Cross-Client Validation**
- Weekly cap is per-client, not facility-wide
- Facility-level caps (if needed) are separate constraint

**Historical Artifact Mutation**
- Validators assume artifacts are immutable once approved
- No validation of artifact updates/edits

---

## Appendix A: Quick Reference

### A.1 Validation Command Summary

```bash
# Phase 1: JSON Schema
ajv validate --spec=draft2020 --strict=true -s schema.json -d artifact.json

# Phase 2: Coherence
python3 validate_phase2_coherence.py artifact.json

# Phase 3: Cap Compliance
python3 validate_phase3_caps.py artifact.json --state-db state.db --clientid CLIENT_ID

# Phase 4: Content Accuracy
python3 validate_phase4_content.py artifact.json --project-spec SPEC_VERSION
```

### A.2 Error Code Quick Reference

| Code | Meaning | Phase | Action |
|------|---------|-------|--------|
| SCHEMA_VALIDATION_FAILED | Structure invalid | 1 | Reject |
| COHERENCE_MISMATCH_* | Header mismatch | 2 | Reject |
| CAP_PROOF_WHEN_INELIGIBLE | Cap proof present when denied | 2 | Reject |
| CAP_EXCEEDED | Session over cap | 3 | Reject |
| WEEKLY_CAP_EXCEEDED | Weekly total over cap | 3 | Reject |
| ACCENT_CAP_VIOLATED | Youth accent > 40% | 3 | Reject |
| EXPOSURE_MISMATCH | Summary ≠ content | 4 | Reject |
| CONTENT_WHEN_INELIGIBLE | Content when denied | 4 | Reject |
| CAP_ADJUSTMENT_NOT_LOGGED | Silent truncation | 4 | Warn |

---

**Version:** 1.0.0  
**Status:** PRODUCTION-LOCKED  
**Companion Schema:** EFL_OUTPUT_ARTIFACT_SCHEMA_v1.0.1.json  
**Date:** 2026-01-15  

**This document closes all identified validation gaps and provides executable CI validation logic for all EFL training artifacts.**
