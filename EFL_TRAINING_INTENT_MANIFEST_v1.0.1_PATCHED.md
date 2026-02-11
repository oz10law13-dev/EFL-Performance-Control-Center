# EFL Training Intent Manifest v1.0.1

**Specification ID:** EFL_TRAINING_INTENT_MANIFEST  
**Version:** 1.0.1 (PATCHED)  
**Effective Date:** 2026-01-15  
**Status:** PRODUCTION-LOCKED  
**Authority:** Elite Fitness Lab — Director of Performance Systems

**Version History:**
- v1.0.1 (2026-01-15): Standardized override_id naming, clarified tier semantics, tightened hard constraint enforcement
- v1.0.0 (2026-01-15): Initial release

---

## Document Role

This manifest defines all **training-related intents** (actions) that can be requested in the EFL training operating system. Each intent specifies:
- Required role/tier authorization
- Input validation requirements
- Routing to enforcement layers
- Audit logging requirements

**Companion Documents:**
- EFL_UID_ROLE_REGISTRY_SCHEMA_v1.0.1.json (role definitions)
- EFL_OVERRIDE_RECORD_SCHEMA_v1.0.1.json (override protocol)
- EFL_CI_VALIDATOR_INVARIANTS_v1.0.1.md (enforcement rules)

---

## Role Tier Semantics

**Tier Assignment:**
- Tier 0: System (automated processes)
- Tier 1: Coach (individual athlete access)
- Tier 2: SeniorCoach (facility-wide access + approvals)
- Tier 3: MedicalProvider (clinical authority)
- Tier 4: QA (audit/review only)
- Tier 5: Admin (configuration management)

**Important:** Tiers represent organizational hierarchy and priority, **not capability supersets**. Actual permissions are determined by the `capabilities` array in each role definition. A higher tier does not automatically inherit lower-tier permissions (e.g., MedicalProvider cannot generate sessions).

---

## Intent Categories

### Category A: Training Artifact Generation
Intents that create new training artifacts (session sheets, meso plans, notices).

### Category B: Manual Program Submission
Intents for human-authored programs submitted for validation.

### Category C: Override & Approval
Intents that request or approve rule exceptions.

### Category D: Configuration Management
Intents that modify schemas, specs, or project registry.

### Category E: Audit & Review
Intents for querying history, violations, and compliance reports.

---

## Intent Definitions

### A1: REQUEST_SESSION_GENERATION

**Description:** Request AI-generated training session for a specific client and project.

**Allowed Roles:**
- `Coach` (for own athletes only)
- `SeniorCoach` (for any athlete in facility)
- `Admin` (for any athlete)
- `System` (automated scheduler)

**Required Input:**
- `clientid` (must exist in ClientState DB)
- `projectid` (must exist in Project Registry)
- `session_date` (ISO 8601 date)
- `requestor_uid` (authenticated user ID)

**Validation Flow:**
1. **GATE:** Verify requestor role permits this intent
2. **STRATA:** Validate input structure against ClientState schema
3. **SIGIL:** Check client eligibility via Router Decision Matrix
4. **THESIS:** If eligible, route to generator; if not, return NOTICE_DENIAL
5. **VERITAS:** Log request with timestamp, requestor, outcome

**Routing:**
- Input Gate → Router → Generator (if eligible)
- Generated artifact enters 4-phase CI validation pipeline

**Audit Fields:**
- `intent_id` (UUID)
- `timestamp`
- `requestor_uid`
- `clientid`
- `projectid`
- `outcome` (APPROVED | DENIED | FAILED_VALIDATION)
- `artifact_id` (if successful)

**Error Codes:**
- `INTENT_ROLE_DENIED`: Requestor lacks required role
- `INTENT_INPUT_INVALID`: Missing or malformed required fields
- `CLIENT_NOT_FOUND`: clientid does not exist
- `PROJECT_NOT_REGISTERED`: projectid not in registry

---

### A2: REQUEST_MESOCYCLE_GENERATION

**Description:** Request AI-generated training mesocycle (multi-week block).

**Allowed Roles:**
- `SeniorCoach` (for any athlete)
- `Admin` (for any athlete)

**Required Input:**
- `clientid`
- `projectid`
- `meso_start_date` (ISO 8601)
- `meso_duration_weeks` (integer, 3-8)
- `requestor_uid`

**Validation Flow:**
Same as A1 but generates mesocycle-class artifact.

**Routing:**
Input Gate → Router → Meso Generator → CI validation

**Additional Constraints:**
- Cannot overlap with existing approved mesocycles for same client
- Must respect project-specific meso duration limits (e.g., R2P-ACL Stage 2 = 4-6 weeks)

**Error Codes:**
- All from A1, plus:
- `MESO_OVERLAP_CONFLICT`: Overlaps with existing meso
- `MESO_DURATION_INVALID`: Duration outside project limits

---

### B1: SUBMIT_MANUAL_PROGRAM

**Description:** Submit human-authored training program for validation and approval.

**Allowed Roles:**
- `Coach` (for own athletes only)
- `SeniorCoach` (for any athlete)
- `MedicalProvider` (for rehab programs only)

**Required Input:**
- `artifact_json` (full artifact conforming to EFL_OUTPUT_ARTIFACT_SCHEMA_v1.0.1)
- `submitter_uid`
- `submission_notes` (optional, string)

**Validation Flow:**
1. **GATE:** Verify submitter role
2. **STRATA:** Schema validation (Phase 1)
3. **THESIS:** Phases 2-4 validation (coherence, caps, content)
4. **VERITAS:** If pass all phases, approve and log; if fail, quarantine

**Routing:**
Direct to 4-phase CI pipeline, bypass generator

**Audit Fields:**
- `intent_id`
- `timestamp`
- `submitter_uid`
- `artifact_id`
- `validation_outcome` (PASS | FAIL)
- `failed_phase` (if failed)
- `error_code` (if failed)

**Error Codes:**
- All CI validation error codes (22 codes from CI Invariants v1.0.1)

---

### C1: REQUEST_OVERRIDE_STAGE

**Description:** Request override of stage progression rule (e.g., advance ACL client to Stage 3 despite missing gate criteria).

**Allowed Roles:**
- `MedicalProvider` (can request)
- `SeniorCoach` (can request)

**Required Input:**
- `clientid`
- `current_stage` (e.g., "R2P-ACL-S2")
- `requested_stage` (e.g., "R2P-ACL-S3")
- `rule_id` (which gate/hardstop is being overridden)
- `justification` (string, min 50 chars)
- `requestor_uid`
- `supporting_documents` (optional, array of file URLs)

**Validation Flow:**
1. **GATE:** Verify requestor role can request overrides
2. **SIGIL:** Check if rule_id is in overrideable catalog
3. **COUNCIL:** Route to approval flow (see C2: APPROVE_OVERRIDE)
4. **VERITAS:** Log request with justification

**Routing:**
Override Request Store → Pending Approval Queue

**Approval Requirements:**
- 1 `MedicalProvider` + 1 `SeniorCoach` (if requestor is one, need the other)
- Timeout: 24 hours or next training day, whichever is sooner
- If timeout, auto-deny

**Error Codes:**
- `OVERRIDE_RULE_NOT_OVERRIDEABLE`: Rule cannot be overridden
- `OVERRIDE_JUSTIFICATION_TOO_SHORT`: < 50 chars
- `OVERRIDE_REQUESTOR_LACKS_AUTHORITY`: Role insufficient

---

### C2: APPROVE_OVERRIDE

**Description:** Approve or deny an override request.

**Allowed Roles:**
- `MedicalProvider` (if request came from non-MedicalProvider)
- `SeniorCoach` (if request came from non-SeniorCoach)
- `Admin` (can approve any)

**Required Input:**
- `override_id` (UUID) **[v1.0.1: STANDARDIZED from override_request_id]**
- `approver_uid`
- `decision` (APPROVE | DENY)
- `approval_notes` (optional, string)

**Validation Flow:**
1. **GATE:** Verify approver role satisfies quorum requirements
2. **COUNCIL:** If quorum met and decision = APPROVE, apply override to ClientState
3. **VERITAS:** Log approval decision with full context

**Routing:**
If APPROVE: Update ClientState + emit override record
If DENY: Close request, log denial

**Audit Fields:**
- `override_id` (from record)
- `requestor_uid`
- `approver_uid`
- `decision`
- `timestamp`
- `justification` (from request)
- `approval_notes`

**Error Codes:**
- `OVERRIDE_NOT_FOUND`: override_id does not exist
- `OVERRIDE_ALREADY_DECIDED`: Decision already made
- `OVERRIDE_APPROVER_INSUFFICIENT`: Approver doesn't satisfy quorum

---

### C3: REQUEST_OVERRIDE_CAP

**Description:** Request temporary cap increase (session or weekly).

**Allowed Roles:**
- `SeniorCoach`
- `Admin`

**Required Input:**
- `clientid`
- `cap_type` (SESSION | WEEKLY)
- `current_cap` (integer)
- `requested_cap` (integer)
- `duration` (number of sessions or days)
- `justification` (string, min 100 chars)
- `requestor_uid`

**Validation Flow:**
1. **GATE:** Verify requestor role
2. **SIGIL:** Check if requested_cap exceeds population absolute ceiling (if yes, deny immediately)
3. **COUNCIL:** Route to approval (requires 1 SeniorCoach + 1 Admin if requestor is SeniorCoach)
4. **VERITAS:** Log request

**Routing:**
Override Request Store → Pending Approval Queue

**Hard Constraints (non-overrideable, enforced at SIGIL):**
- Youth812: Weekly cap cannot exceed 180 (ever)
- Youth1316: Weekly cap cannot exceed 200 (ever)
- Session cap cannot exceed 1.5x base cap for population

**Error Codes:**
- `CAP_OVERRIDE_EXCEEDS_HARD_LIMIT`: Requested cap violates absolute population ceiling
- `CAP_OVERRIDE_JUSTIFICATION_TOO_SHORT`: < 100 chars

---

### D1: DEPLOY_GENERATOR_VERSION

**Description:** Deploy new generator version to production.

**Allowed Roles:**
- `Admin` only

**Required Input:**
- `projectid`
- `generator_version` (semver, e.g., "1.2.0")
- `generator_artifact_url` (where binary/code lives)
- `changelog_summary` (string)
- `deployer_uid`

**Validation Flow:**
1. **GATE:** Verify admin role
2. **STRATA:** Verify generator passes test fixtures (must have passing test report)
3. **SIGIL:** Check that generator_version > current production version
4. **VERITAS:** Log deployment with rollback instructions

**Routing:**
Project Registry update → CI config update → Production deployment

**Audit Fields:**
- `intent_id`
- `timestamp`
- `deployer_uid`
- `projectid`
- `old_version`
- `new_version`
- `test_report_url`

**Error Codes:**
- `GENERATOR_TESTS_FAILED`
- `GENERATOR_VERSION_REGRESSION`: New version <= current

---

### D2: UPDATE_PROJECT_SPEC

**Description:** Update project wrapper or output spec.

**Allowed Roles:**
- `Admin` only

**Required Input:**
- `projectid`
- `spec_type` (WRAPPER | OUTPUT_SPEC | STAGE_SPEC)
- `spec_version` (semver)
- `spec_content` (full markdown or JSON)
- `changelog` (string)
- `updater_uid`

**Validation Flow:**
1. **GATE:** Verify admin role
2. **STRATA:** Validate spec content structure (must parse, must include version header)
3. **SIGIL:** Verify no existing artifacts depend on older version in incompatible way
4. **VERITAS:** Log update with hash of old and new versions

**Routing:**
Project Registry update → Schema drift check → Production deployment

**Error Codes:**
- `SPEC_MALFORMED`
- `SPEC_VERSION_CONFLICT`
- `SPEC_BREAKING_CHANGE_UNSAFE`: Would invalidate existing artifacts

---

### D3: UPDATE_ARTIFACT_SCHEMA

**Description:** Update the global artifact schema (structural changes).

**Allowed Roles:**
- `Admin` only (with QA sign-off)

**Required Input:**
- `schema_version` (semver)
- `schema_json` (full JSON Schema)
- `migration_guide` (how to upgrade existing artifacts)
- `test_coverage_report` (must show 100% validator coverage)
- `updater_uid`

**Validation Flow:**
1. **GATE:** Verify admin role + QA approval flag
2. **STRATA:** Validate schema is valid JSON Schema Draft 2020-12
3. **SIGIL:** Run schema against all test fixtures and existing artifacts
4. **THESIS:** If any artifacts fail new schema without migration, DENY
5. **VERITAS:** Log schema change with full diff

**Routing:**
Schema Registry → CI config → Validator updates → Production

**Audit Fields:**
- `intent_id`
- `timestamp`
- `updater_uid`
- `old_schema_version`
- `new_schema_version`
- `schema_diff_url`
- `test_report_url`

**Error Codes:**
- `SCHEMA_INVALID_JSON_SCHEMA`
- `SCHEMA_BREAKS_EXISTING_ARTIFACTS`
- `SCHEMA_TEST_COVERAGE_INSUFFICIENT`

---

### E1: QUERY_ARTIFACT_HISTORY

**Description:** Query artifact history for a client (audit/review).

**Allowed Roles:**
- `Coach` (for own athletes only)
- `SeniorCoach` (for any athlete)
- `MedicalProvider` (for any athlete)
- `Admin` (for any athlete)
- `QA` (for any athlete)

**Required Input:**
- `clientid`
- `date_range_start` (ISO 8601)
- `date_range_end` (ISO 8601)
- `requestor_uid`

**Validation Flow:**
1. **GATE:** Verify requestor role permits access to this client
2. **STRATA:** Validate date range (max 90 days)
3. **VERITAS:** Log query for audit trail

**Routing:**
Artifact History DB → Query → Return JSON

**Response:**
Array of artifact summaries:
```json
[
  {
    "artifact_id": "uuid",
    "generated_at": "timestamp",
    "projectid": "R2P-ACL",
    "artifact_class": "SESSION",
    "total_contacts": 45,
    "sessioncap_applied": 60,
    "weeklycap_applied": 120,
    "validation_status": "PASS"
  }
]
```

**Error Codes:**
- `QUERY_DATE_RANGE_TOO_LARGE`
- `QUERY_CLIENT_ACCESS_DENIED`

---

### E2: QUERY_VIOLATIONS

**Description:** Query quarantined artifacts and validation errors.

**Allowed Roles:**
- `QA`
- `Admin`

**Required Input:**
- `date_range_start`
- `date_range_end`
- `error_code_filter` (optional, array of error codes)
- `projectid_filter` (optional)
- `requestor_uid`

**Validation Flow:**
1. **GATE:** Verify QA or Admin role
2. **STRATA:** Validate filters
3. **VERITAS:** Log query

**Routing:**
Quarantine Store → Query → Return JSON

**Response:**
Array of violation records:
```json
[
  {
    "artifact_id": "uuid",
    "validation_status": "FAIL",
    "failed_phase": 3,
    "error_code": "WEEKLY_CAP_EXCEEDED",
    "error_message": "...",
    "details": { ... },
    "quarantine_timestamp": "...",
    "reviewed": false
  }
]
```

**Error Codes:**
- `QUERY_ROLE_INSUFFICIENT`

---

### E3: GENERATE_COMPLIANCE_REPORT

**Description:** Generate formal compliance report for regulatory review.

**Allowed Roles:**
- `Admin` only

**Required Input:**
- `report_type` (MONTHLY | QUARTERLY | ANNUAL | CUSTOM)
- `date_range_start`
- `date_range_end`
- `include_overrides` (boolean)
- `include_violations` (boolean)
- `requestor_uid`

**Validation Flow:**
1. **GATE:** Verify admin role
2. **STRATA:** Validate report parameters
3. **VERITAS:** Generate report from audit logs, artifact history, override records

**Routing:**
Audit DB + Artifact History + Override Store → Report Generator → PDF/JSON output

**Report Contents:**
- Total artifacts generated
- Validation pass/fail rates by phase
- Error code distribution
- Override requests and approvals
- Youth protection compliance metrics (accent cap violations, band/E-node ceiling violations)
- ClientState changes and readiness distributions
- Generator version history
- Schema/spec version history

**Output Format:**
- PDF (for human review)
- JSON (for machine consumption)

**Error Codes:**
- `REPORT_DATE_RANGE_INVALID`

---

## Intent Routing Summary

| Intent | Entry Point | Enforcement Layers | Terminal Action |
|--------|-------------|-------------------|-----------------|
| REQUEST_SESSION_GENERATION | Training Gateway API | GATE → STRATA → SIGIL → Router → Generator → THESIS (CI 4-phase) → VERITAS | Artifact approved or quarantined |
| REQUEST_MESOCYCLE_GENERATION | Training Gateway API | Same as above | Meso artifact approved or quarantined |
| SUBMIT_MANUAL_PROGRAM | Training Gateway API | GATE → STRATA → THESIS (CI 4-phase) → VERITAS | Artifact approved or quarantined |
| REQUEST_OVERRIDE_STAGE | Training Gateway API | GATE → SIGIL → COUNCIL (pending approval) → VERITAS | Override request logged |
| APPROVE_OVERRIDE | Training Gateway API | GATE → COUNCIL (quorum check) → ClientState update → VERITAS | Override approved/denied, ClientState updated |
| REQUEST_OVERRIDE_CAP | Training Gateway API | GATE → SIGIL (hard limit check) → COUNCIL (pending approval) → VERITAS | Override request logged |
| DEPLOY_GENERATOR_VERSION | Admin Portal | GATE → STRATA (test validation) → SIGIL → Project Registry update → VERITAS | Generator deployed |
| UPDATE_PROJECT_SPEC | Admin Portal | GATE → STRATA → SIGIL → Project Registry update → VERITAS | Spec updated |
| UPDATE_ARTIFACT_SCHEMA | Admin Portal | GATE → STRATA → SIGIL → THESIS (migration check) → Schema Registry → VERITAS | Schema updated |
| QUERY_ARTIFACT_HISTORY | Training Gateway API | GATE → Artifact History DB → VERITAS | JSON response |
| QUERY_VIOLATIONS | QA Portal | GATE → Quarantine Store → VERITAS | JSON response |
| GENERATE_COMPLIANCE_REPORT | Admin Portal | GATE → Audit DB aggregation → VERITAS | PDF/JSON report |

---

## Intent Authorization Matrix

| Intent | Coach | SeniorCoach | MedicalProvider | Admin | QA | System |
|--------|-------|-------------|-----------------|-------|----|----|
| REQUEST_SESSION_GENERATION | ✅ (own athletes) | ✅ | ❌ | ✅ | ❌ | ✅ |
| REQUEST_MESOCYCLE_GENERATION | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ |
| SUBMIT_MANUAL_PROGRAM | ✅ (own athletes) | ✅ | ✅ (rehab only) | ✅ | ❌ | ❌ |
| REQUEST_OVERRIDE_STAGE | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ |
| APPROVE_OVERRIDE | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ |
| REQUEST_OVERRIDE_CAP | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ |
| DEPLOY_GENERATOR_VERSION | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| UPDATE_PROJECT_SPEC | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| UPDATE_ARTIFACT_SCHEMA | ❌ | ❌ | ❌ | ✅ (+ QA approval) | ❌ | ❌ |
| QUERY_ARTIFACT_HISTORY | ✅ (own) | ✅ | ✅ | ✅ | ✅ | ❌ |
| QUERY_VIOLATIONS | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| GENERATE_COMPLIANCE_REPORT | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |

---

## Appendix A: SIGIL Overrideable Catalog (Reference)

**Purpose:** Defines which rules can be overridden and hard limits that cannot be bypassed.

### Overrideable Rules
- Stage progression gates (with MedicalProvider + SeniorCoach approval)
- Readiness holds (with MedicalProvider approval)
- Compliance holds (with SeniorCoach approval)
- Temporary cap increases within population absolute ceilings

### Non-Overrideable Rules (Hard Limits)
- Youth812: Weekly cap > 180
- Youth1316: Weekly cap > 200
- Session cap > 1.5x population base cap
- Youth accent cap > 40% E3+
- Band/E-node ceilings for populations

**Implementation Note:** SIGIL layer must check requested overrides against this catalog before routing to COUNCIL.

---

**Version:** 1.0.1 (PATCHED)  
**Status:** PRODUCTION-LOCKED  
**Effective Date:** 2026-01-15  

**Patches in v1.0.1:**
- Standardized `override_id` naming (removed `override_request_id`)
- Clarified tier semantics (tiers do not imply capability supersets)
- Added SIGIL Overrideable Catalog reference
- Tightened hard constraint language for cap overrides
