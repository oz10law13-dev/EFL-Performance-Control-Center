# EFL Output Artifact Schema — Changelog

## v1.0.1 (2026-01-15) — GAP-C1 Fix

**Status:** PRODUCTION-LOCKED  
**Type:** Patch (clarification, non-breaking)

### Changes

#### 1. Enhanced cap_proof Presence Enforcement (GAP-C1 Fix)
- **Problem:** Schema didn't explicitly enforce cap_proof requirement for training artifacts
- **Fix:** Added explicit conditional requiring cap_proof to be non-null for SESSION/MICROSESSION/MESOCYCLE
- **Location:** Root-level allOf conditional
- **Impact:** Generators cannot emit training artifacts without cap proof

#### 2. Added reasoncodes Ordering Clarification
- **Updated:** GlobalHeader.reasoncodes description now states "precedence-ordered"
- **Updated:** LegalitySnapshot.reasoncodes description now states "must match header.reasoncodes exactly"
- **Impact:** Clarifies expectation for Phase 2 coherence validation

#### 3. Enhanced CapProof Required Fields
- **Updated:** Made all core cap_proof fields explicitly required (previously implied)
- **Added:** weeklymultiplier, sessionmultiplier, and all base/applied caps to required list
- **Impact:** Prevents partial cap_proof objects

#### 4. Strengthened Youth Accent Cap Conditional
- **Updated:** Added explicit `required: ["enode_accent_cap_pct"]` when Youth812/1316
- **Impact:** Ensures Youth accent cap cannot be omitted

#### 5. Documentation Clarifications
- **Updated:** adjustments description notes it's required when content modified
- **Updated:** total_contacts description emphasizes must match actual content
- **Updated:** Multiple field descriptions enhanced for clarity

### Compatibility

- ✅ **Backward compatible:** All v1.0.0-valid artifacts remain valid under v1.0.1
- ✅ **Non-breaking:** No field removals or type changes
- ⚠️ **Stricter enforcement:** Some previously-valid (but incorrect) artifacts may now fail

### Migration Guide

**No migration required** if generators were already:
- Including cap_proof for all training artifacts
- Populating all cap_proof fields
- Ordering reasoncodes by precedence

If generators were omitting cap_proof:
- Update to include full cap_proof object for SESSION/MICROSESSION/MESOCYCLE
- Ensure all required fields populated

### Testing

All existing test fixtures should continue to pass. Add new fixtures for:
- SESSION without cap_proof (should fail)
- Youth artifact with enode_accent_cap_pct omitted (should fail)
- Reasoncodes ordering mismatch (Phase 2 validation should catch)

---

## v1.0.0 (2026-01-15) — Initial Release

- Initial production-locked schema
- Implements EFL_OUTPUT_SPEC_GLOBAL_CONTRACT_v1.0
- 5 artifact classes with conditional requirements
- 11 required global header fields
- Cap proof with structured adjustments
- Exposure summary with accuracy requirements
