# EFL Output Spec Global Contract v1.0

**Specification ID:** EFL_OUTPUT_SPEC_GLOBAL_CONTRACT  
**Version:** 1.0.0  
**Effective Date:** 2026-01-15  
**Status:** PRODUCTION-LOCKED  
**Authority:** Elite Fitness Lab — Director of Performance Systems

---

## Document Role

This document defines the **global output law** for all generated training artifacts across all EFL service lines (R2P, SP Performance, ICP, Adult). It specifies the mandatory chassis (header, legality snapshot, cap proof, exposure summary) that every artifact must carry, regardless of project or target.

**What this document IS:**
- Global required structure for all emitted artifacts
- Cross-project safety enforcement rules
- Audit trail and traceability requirements
- Cap enforcement and proof obligations

**What this document IS NOT:**
- Router precedence logic (see: EFL_ROUTER_DECISION_MATRIX_v1.0.md)
- Project-specific programming rules (see: project wrappers + project output specs)
- Exercise library or content definitions
- Target-specific serialization formats (those extend this contract)

**Companion Documents:**
- EFL_GLOBAL_CLIENT_STATE_v1.0.2.json (structure truth)
- EFL_ROUTER_DECISION_MATRIX_v1.0.md (logic truth)
- EFL_PROJECT_REGISTRY_v1.0.json (project bindings)
- Project-specific output specs (extensions of this contract)

---

## 1. System Position

This contract sits at **Layer 6** in the EFL deterministic system stack:

```
Input Gates → Client State → Router → Project Registry → [THIS DOC] → Project Output Specs → Emitters
```

**Inputs consumed (read-only):**
- `ClientState.inputs` (ground truth)
- `ClientState.derived` (router/system-1 computed)
- `ClientState.decisions` (activeproject + reasoncodes + rationale)
- Project Registry (projectid → output targets)

**Outputs governed:**
- BridgeAthletic payloads
- Coach sheet payloads
- MicroSession payloads
- Meso/block payloads
- Denial/notice payloads

---

## 2. Artifact Class Matrix

Every artifact must belong to one of these classes and satisfy the corresponding requirements:

| Artifact Class | Must Include Header | Must Include Legality Snapshot | Must Include Cap Proof | Must Include Exposure Summary | Must Include Content Payload |
|----------------|---------------------|-------------------------------|------------------------|-------------------------------|------------------------------|
| **SESSION** | ✅ | ✅ | ✅ (if caps exist) | ✅ | ✅ |
| **MICROSESSION** | ✅ | ✅ | ✅ (if caps exist) | ✅ | ✅ |
| **MESOCYCLE** | ✅ | ✅ | ✅ (if caps exist) | ✅ | ✅ |
| **NOTICE_DENIAL** | ✅ | ✅ (denial form) | ✅ (if caps were denial basis) | Optional | ❌ |
| **COMPLIANCE_SUMMARY** | ✅ | ✅ | ✅ | ✅ | Optional |

**Enforcement:**
- If an artifact is missing any required section → **invalid artifact** (fail generation).
- QA/CI must validate artifacts against this matrix.

---

## 3. Target Serialization Matrix

Defines expectations for each output target:

| Target | Typical Output Form | Must Carry Global Header | Must Carry Legality Snapshot | Notes |
|--------|---------------------|-------------------------|------------------------------|-------|
| **BRIDGEATHLETIC** | JSON workout payload | ✅ | ✅ | Proof blocks embedded in metadata fields or sidecar object |
| **COACHSHEET** | Print layout (PDF/HTML) | ✅ | ✅ | Proof blocks appear as top "Compliance Strip" |
| **MICROSESSION** | Short session JSON | ✅ | ✅ | Same legality strip, abbreviated content |
| **MESOCYCLE** | Multi-week payload | ✅ | ✅ | Includes weekly cap proof + macro counters |
| **NOTICE** | Text/report payload | ✅ | ✅ | Used when eligible=false or audit export |

**Generator Contract:**
- Generator must know which **target** it's emitting for (from Project Registry).
- Target determines serialization format, but **not** whether global sections are required.
- All targets must implement the same global header + legality snapshot.

---

## 4. Global Header Contract

**Purpose:** Minimum audit echo for traceability and reproducibility.

**Required Fields:**

| Header Field | Source of Truth | Type | Why It Exists |
|--------------|-----------------|------|---------------|
| `clientid` | ClientState | string | Athlete traceability |
| `artifact_id` | Generator | string (UUID) | Unique output identity |
| `artifact_class` | Generator | enum (SESSION/MICROSESSION/MESOCYCLE/NOTICE_DENIAL/COMPLIANCE_SUMMARY) | Validation + routing |
| `target` | Registry/output request | enum (BRIDGEATHLETIC/COACHSHEET/MICROSESSION/MESOCYCLE/NOTICE) | Rendering expectations |
| `generated_at` | Generator | ISO8601 timestamp | Audit timestamp |
| `projectid` | ClientState.decisions.activeproject | string | What Router selected |
| `routerversion` | ClientState.decisions.routerversion | string | Reproducibility |
| `state_lastupdated` | ClientState.lastupdated | ISO8601 timestamp | Snapshot integrity |
| `seasontype` | ClientState.inputs.trainingcontext_global.seasontype | enum (OFFSEASON/PRESEASON/INSEASON/POSTSEASON) | Coherence check |
| `eligible_for_training_today` | ClientState.decisions.eligible_for_training_today | boolean | Hard gate |
| `reasoncodes` | ClientState.decisions.router_reasoncodes | array[string] | Explainability |

**Enforcement:**
- If any required header field is missing → **invalid artifact**.
- Header must be the first section in serialized output.

---

## 5. Legality Snapshot Section

**Purpose:** Show **why** training was allowed (or denied) in human-readable form.

**Required Fields:**

| Field | Source | Type | Description |
|-------|--------|------|-------------|
| `activeproject` | ClientState.decisions.activeproject | string | Selected project (or "NONE") |
| `eligible_for_training_today` | ClientState.decisions.eligible_for_training_today | boolean | Global permission flag |
| `reasoncodes` | ClientState.decisions.router_reasoncodes | array[string] | Reason codes fired |
| `legal_projects` | ClientState.decisions.legal_projects | array[string] | All legal options (optional, for context) |
| `rationale_snippet` | ClientState.decisions.rationale_stack (top 3 rules) | array[object] | Top rules fired (optional, for audit) |

**When eligible=false:**
- Legality snapshot becomes **denial notice**.
- Must include `reasoncodes` and human-readable explanation.
- Content payload must be empty (artifact_class=NOTICE_DENIAL).

**Example (rendered):**
```
LEGALITY SNAPSHOT
-----------------
Active Project: COURT_SPORT_FOUNDATIONS
Eligible: true
Reason Codes: [DEFAULT_READINESS_YELLOW]
Legal Alternatives: ELASTIC_RELOAD, OFF_SEASON_BASELINE_COURT_VERTICAL
```

---

## 6. Cap Proof Section

**Purpose:** Show what population/readiness constraints were applied, and that the artifact respects them.

**Required Fields (when caps exist):**

| Field | Source | Type | Description |
|-------|--------|------|-------------|
| `population_enforced` | ClientState.derived.populationoverrides.population_enforced | enum | Computed population class |
| `readinessflag` | ClientState.stateheader.readinessflag | enum (GREEN/YELLOW/RED) | Readiness state |
| `weeklymultiplier` | ClientState.derived.readinessmultipliers.weeklymultiplier | number (0.0–1.0) | Weekly cap adjustment |
| `sessionmultiplier` | ClientState.derived.readinessmultipliers.sessionmultiplier | number (0.0–1.0) | Session cap adjustment |
| `weeklycontactscap_applied` | derived.populationoverrides.weeklycontactscap_population × weeklymultiplier | integer | Weekly plyo contact ceiling |
| `sessioncontactscap_applied` | derived.populationoverrides.sessioncontactscap_population × sessionmultiplier | integer | Session plyo contact ceiling |
| `enode_accent_cap_pct` | ClientState.derived.populationoverrides.enode_accent_cap_pct | number (0.0–1.0) or null | Youth E3+ accent cap (Youth812/1316 only) |

**Enforcement Rules:**

| Situation | Generator Action | Artifact Class | Required Proof |
|-----------|------------------|----------------|----------------|
| `eligible=false` | Do not render training content | `NOTICE_DENIAL` | Legality snapshot + reasoncodes |
| `derived=null` but `eligible=true` | Invalid state (schema violation) | `NOTICE_DENIAL` | Emit invariant failure code |
| Session would exceed `sessioncontactscap_applied` | Truncate OR deny (policy-set), never silent | `SESSION` or `NOTICE_DENIAL` | Cap proof + "adjustment note" |
| Weekly exposure would exceed `weeklycontactscap_applied` | Downgrade volume OR deny | `SESSION` or `NOTICE_DENIAL` | Cap proof + "weekly cap applied" |
| Youth population with accent cap | Auto-limit E3+ accent exposure | `SESSION` | Cap proof + accent cap note |

**Example (rendered):**
```
CAP PROOF
---------
Population: Youth1316
Readiness: YELLOW (weekly: 0.75×, session: 0.8×)
Weekly Contact Cap: 80 base → 60 applied
Session Contact Cap: 30 base → 24 applied
E-Node Accent Cap: 40% (Youth E3+ limit)
```

---

## 7. Exposure Summary Section

**Purpose:** Quantify what the artifact actually delivers (contacts, sets, volume, key exposures).

**Required Fields:**

| Field | Definition | Source |
|-------|------------|--------|
| `total_contacts` | Sum of plyo contacts across all movements | Generator (computed from content) |
| `total_sets` | Count of work sets (project-dependent definition) | Generator |
| `exposure_breakdown` | Object/table showing contacts by category (elastic/reactive/etc.) | Generator + project wrapper |
| `key_exposures` | Project-specific highlights (e.g., max jump height, max COD angle) | Project output spec |

**Project-specific extensions allowed:**
- Projects may add fields (e.g., R2P: `max_e_node`, `bilateral_vs_unilateral`).
- Projects may NOT remove `total_contacts` or `total_sets`.

**Example (rendered):**
```
EXPOSURE SUMMARY
----------------
Total Contacts: 18 (within 24 cap)
Total Sets: 12
Breakdown:
  - Elastic Reload (E1-E2): 12 contacts
  - Reactive (E2): 6 contacts
Key Exposures:
  - Max E-Node: E2
  - Max Jump Height: 18 inches
```

---

## 8. Content Payload Section

**Purpose:** The actual training prescription (exercises, sets, reps, load, tempo, etc.).

**Structure:**
- Governed by **project wrapper** + **project output spec**.
- Must conform to Load Standards, Sport Demands Grid, and Governance constraints.
- This contract does NOT specify content structure (project-specific).

**Global Content Invariants:**
1. **No content when ineligible** — If `eligible_for_training_today=false`, content section must be empty.
2. **Cap enforcement** — Generator must not emit content that would violate caps shown in Cap Proof section.
3. **Audit trail** — Content must reference wrapper + output spec versions used to generate it.

---

## 9. Global Output Invariants

**INV-OUT-001: Header completeness**
```
All required header fields must be present and non-null.
If any missing → generator must fail (not emit partial artifact).
```

**INV-OUT-002: Legality snapshot inclusion**
```
IF artifact_class ∈ {SESSION, MICROSESSION, MESOCYCLE, NOTICE_DENIAL, COMPLIANCE_SUMMARY}
  THEN legality_snapshot section must exist
```

**INV-OUT-003: Cap proof when caps exist**
```
IF ClientState.derived != null
  THEN cap_proof section must exist and show applied caps
```

**INV-OUT-004: No silent truncation**
```
IF generator adjusts content to respect caps (truncate, downgrade)
  THEN cap_proof must include explicit note of adjustment
```

**INV-OUT-005: No content when ineligible**
```
IF ClientState.decisions.eligible_for_training_today = false
  THEN content_payload section must be empty
  AND artifact_class must be NOTICE_DENIAL
```

**INV-OUT-006: Exposure summary accuracy**
```
exposure_summary.total_contacts must equal sum of all contacts in content_payload
IF mismatch → artifact is invalid
```

---

## 10. Cap Enforcement Decision Matrix

Generator must follow this logic when caps could be exceeded:

| Cap Type | Policy | Generator Action | Proof Requirement |
|----------|--------|------------------|-------------------|
| **Session contact cap** | Hard ceiling | Truncate content OR deny session | Cap proof + "truncated to cap" note |
| **Weekly contact cap** | Soft ceiling | Warn + downgrade volume OR deny | Cap proof + "weekly cap applied" note |
| **E-node accent cap (Youth)** | Hard ceiling (40%) | Auto-limit E3+ accent contacts | Cap proof + "accent cap applied" |
| **Band ceiling (population)** | Hard ceiling | Block any movement > maxbandallowed_population | Cap proof + "band ceiling enforced" |
| **Provider clearance gates** | Hard gate | Block entire exposure type (e.g., running, COD) if not cleared | Legality snapshot + gate reason |

**Example Decision Tree:**
```
IF sessioncontacts_requested > sessioncontactscap_applied:
  IF policy = "truncate":
    content = truncate_to_cap(content, sessioncontactscap_applied)
    cap_proof.notes.append("Truncated to session cap")
  ELSE IF policy = "deny":
    artifact_class = NOTICE_DENIAL
    reasoncodes.append("SESSION_CAP_EXCEEDED")
```

---

## 11. Project Output Spec Extension Protocol

**Allowed extensions (project-specific output specs MAY):**
- Add fields to exposure_summary (e.g., max COD angle, bilateral/unilateral split)
- Add sections after content_payload (e.g., coaching notes, progression advice)
- Define content_payload structure (Prime/Prep/Work/Clear, session order, etc.)
- Add target-specific rendering rules (e.g., BridgeAthletic JSON structure)

**Prohibited overrides (project output specs MUST NOT):**
- Remove any required global header field
- Remove legality_snapshot or cap_proof sections
- Change cap enforcement rules (those are global)
- Emit artifacts when eligible=false with content

**Enforcement:**
- Project output specs are validated against this contract during CI.
- Any violation → project output spec is rejected.

---

## 12. Generator Interface Contract

**Input:** Generator receives:
```javascript
{
  clientState: ClientState,          // Full validated state
  projectid: string,                 // From decisions.activeproject
  target: string,                    // BRIDGEATHLETIC | COACHSHEET | etc.
  projectWrapper: object,            // Loaded from Project Registry
  projectOutputSpec: object          // Loaded from Project Registry
}
```

**Output:** Generator produces:
```javascript
{
  artifact: {
    header: { /* global header fields */ },
    legality_snapshot: { /* legality fields */ },
    cap_proof: { /* cap fields */ },
    exposure_summary: { /* exposure fields */ },
    content_payload: { /* project-specific content */ }
  },
  metadata: {
    generator_version: string,
    wrapper_version: string,
    outputspec_version: string
  }
}
```

**Error Handling:**
- If generator cannot produce valid artifact → return structured error with reasoncode.
- Never emit partial artifact.
- Log all cap adjustments and denials.

---

## 13. Artifact Validation Matrix

**Phase 1: Schema Validation**
- Validate artifact structure against global contract schema.
- Check all required fields present.
- Check field types match expectations.

**Phase 2: Coherence Validation**
- Verify `header.eligible_for_training_today === legality_snapshot.eligible_for_training_today`.
- Verify `header.projectid === ClientState.decisions.activeproject`.
- Verify `header.reasoncodes === ClientState.decisions.router_reasoncodes`.

**Phase 3: Cap Compliance Validation**
- Verify `exposure_summary.total_contacts <= cap_proof.sessioncontactscap_applied`.
- Verify E-node accent cap enforced (if Youth812/1316).
- Verify band ceiling enforced.

**Phase 4: Content Accuracy Validation**
- Verify `exposure_summary` matches `content_payload` (contact counts, set counts).
- Verify no content when eligible=false.

---

## 14. Target-Specific Rendering Extensions

### 14.1 BRIDGEATHLETIC

**Format:** JSON workout payload  
**Global Header Location:** Embedded in `metadata` or root-level fields  
**Legality Snapshot Location:** `metadata.legality_snapshot` or sidecar object  
**Cap Proof Location:** `metadata.cap_proof` or sidecar object  
**Content Structure:** BridgeAthletic workout schema (blocks, exercises, sets, reps)

**Extension Rules:**
- BridgeAthletic output spec defines exercise → BridgeAthletic ID mapping.
- Proof blocks may be embedded in metadata or attached as sidecar JSON.

### 14.2 COACHSHEET

**Format:** Print layout (PDF/HTML)  
**Global Header Location:** Top header strip  
**Legality Snapshot Location:** "Compliance Strip" at top of page  
**Cap Proof Location:** "Population & Readiness" box (sidebar or top)  
**Content Structure:** Formatted sections (Prime/Prep/Work/Clear for SP, stage-specific for R2P)

**Extension Rules:**
- CoachSheet output spec defines layout, fonts, logo placement.
- Proof blocks must be visually prominent (not buried in fine print).

### 14.3 MICROSESSION

**Format:** Short session JSON  
**Global Header Location:** Root-level fields  
**Legality Snapshot Location:** `legality_snapshot` object  
**Cap Proof Location:** `cap_proof` object  
**Content Structure:** Abbreviated content (key movements only, no warm-up details)

**Extension Rules:**
- MicroSession is a condensed SESSION artifact.
- May omit warm-up/cool-down details but must include all proof blocks.

### 14.4 MESOCYCLE

**Format:** Multi-week payload (JSON or structured doc)  
**Global Header Location:** Root-level metadata  
**Legality Snapshot Location:** Per-week legality snapshots  
**Cap Proof Location:** Weekly cap proofs + rolling macro counter proof  
**Content Structure:** Array of sessions + weekly summaries + progression notes

**Extension Rules:**
- Mesocycle output spec defines week-to-week structure.
- Must show macro cap usage (e.g., consecutive high-CNS blocks, specialization blocks used).

---

## 15. Denial Notice Format

**When:** Generated when `eligible_for_training_today=false`.

**Required Sections:**
- Header (all standard fields)
- Legality snapshot (denial form):
  - `activeproject: "NONE"`
  - `eligible: false`
  - `reasoncodes: [...]`
  - Human-readable explanation of denial
- Cap proof (if caps were basis for denial)
- Empty content payload

**Example:**
```
TRAINING NOTICE
===============
Client: ATHLETE-12345
Date: 2026-01-15T14:00:00-06:00

ELIGIBILITY STATUS
------------------
Eligible for Training: NO
Reason: Medical Lock Triggered (≥2 hardstops within 14 days)
Reason Codes: DEFAULTDENY_MEDICAL_LOCK

NEXT STEPS
----------
Contact provider for clearance before resuming training.
```

---

## 16. Change Protocol

**Any change to this global contract requires:**
1. Version increment (v1.0 → v1.1 for additions, v2.0 for breaking changes).
2. Update all project output specs to conform.
3. Regenerate all test fixtures.
4. CI validation that all emitters comply.
5. Red-team audit sign-off.

**Version Control:**
- **Minor version (1.0 → 1.1):** New optional field or section added.
- **Patch version (1.0.0 → 1.0.1):** Clarification only, no logic change.
- **Major version (1.0 → 2.0):** Required field removed or cap rule changed.

---

## Appendix A: Quick Reference Tables

### A.1 Required Sections by Artifact Class

| Artifact Class | Header | Legality Snapshot | Cap Proof | Exposure Summary | Content Payload |
|----------------|--------|-------------------|-----------|------------------|-----------------|
| SESSION | Required | Required | Required (if caps exist) | Required | Required |
| MICROSESSION | Required | Required | Required (if caps exist) | Required | Required |
| MESOCYCLE | Required | Required | Required (if caps exist) | Required | Required |
| NOTICE_DENIAL | Required | Required (denial form) | Optional | Optional | Empty |
| COMPLIANCE_SUMMARY | Required | Required | Required | Required | Optional |

### A.2 Global Header Field Summary

| Field | Type | Source | Required |
|-------|------|--------|----------|
| clientid | string | ClientState | ✅ |
| artifact_id | string (UUID) | Generator | ✅ |
| artifact_class | enum | Generator | ✅ |
| target | enum | Registry | ✅ |
| generated_at | ISO8601 | Generator | ✅ |
| projectid | string | ClientState.decisions | ✅ |
| routerversion | string | ClientState.decisions | ✅ |
| state_lastupdated | ISO8601 | ClientState | ✅ |
| seasontype | enum | ClientState.inputs | ✅ |
| eligible_for_training_today | boolean | ClientState.decisions | ✅ |
| reasoncodes | array[string] | ClientState.decisions | ✅ |

### A.3 Cap Enforcement Policy Summary

| Cap Type | Policy | Action on Violation |
|----------|--------|---------------------|
| Session contact cap | Hard ceiling | Truncate or deny |
| Weekly contact cap | Soft ceiling | Warn + downgrade or deny |
| E-node accent cap (Youth) | Hard ceiling (40%) | Auto-limit accent exposure |
| Band ceiling | Hard ceiling | Block movements > cap |
| Provider clearance | Hard gate | Block entire exposure type |

---

**Version:** 1.0.0  
**Status:** PRODUCTION-LOCKED  
**Companion Schema:** EFL_GLOBAL_CLIENT_STATE_v1.0.2.json  
**Date:** 2026-01-15  

**This document is the authoritative global output law. All project output specs must extend (not violate) this contract. All generators must implement these requirements exactly.**
