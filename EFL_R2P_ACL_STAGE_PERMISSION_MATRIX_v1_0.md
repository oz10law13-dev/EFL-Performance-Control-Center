---
**Meta**

- **Document ID:** `EFL_R2P_ACL_STAGE_PERMISSION_MATRIX_v1_0`
- **Version:** 1.0
- **Effective Date:** 2026-01-11
- **Owner:** Elite Fitness Lab
- **Status:** OPERATIONAL
- **Project Scope:** R2P-ACL (ACL Reconstruction & High-Grade ACL Sprain Return-to-Performance)
- **Populations:** Youth 13-17, Adult 18+
- **Supersedes:** None (initial release)
- **Dependencies:**
  - `EFL_SP_PROJECT_WRAPPER_R2P_ACL_v1_1` (stage definitions + conflict resolution)
  - `_EFL_R2P_ACL_PROJECT_INPUT_GATE_v1_0` (clearance requirements + readiness defaults)
  - `EFL_SP_OUTPUT_SPEC_R2P_ACL_v1_0` (display requirements)
  - `EFL_R2P_ACL_GATES_v1_0_2` (gate thresholds + hardstop definitions)
  - `EFL_R2P_ACL_SYSTEM1_LEGALITY_ENGINE_v1_0_5` (computed stage + envelopes)

---

# EFL R2P-ACL Stage Permission Matrix v1.0

## Purpose

This **Stage Permission Matrix** is a **single-page truth table** that answers, per stage:
- What exposures are allowed (running / jumping / decel / COD / reactive)
- What provider clearances must be TRUE
- What the hard ceilings are (band / node / E-node, contact caps)
- What changes when readiness is YELLOW or RED
- What is always illegal (stage-locked)

**Why This Document Exists:**  
Even though System-1 Legality Engine computes stage permissions dynamically, this matrix prevents:
- **Staff drift** — Coaches misremembering what's allowed at each stage
- **Interpretation coaching** — "I think S3 allows reactive work" (it doesn't)
- **Missing S2.5 exception rule** — E2 is scoped, not global in S2.5
- **Accidental COD/reactive creep** — Introducing exposures before provider clearance or stage gates pass

**This is the human-facing contract.**  
It translates Wrapper + System-1 + Gates into scannable tables for rapid auditing and onboarding.

---

## Authority Position

**Critical Rule:**  
This Permission Matrix is **derived from** upstream documents. It **cannot override** them.

**If mismatch exists between this matrix and upstream documents:**  
**Wrapper v1.1 + System-1 v1.0.5 + Gates v1.0.2 win.** This matrix must be updated to align.

**Upstream Authority (in order):**
1. `EFL_SP_PROJECT_WRAPPER_R2P_ACL_v1_1` (stage definitions, conflict resolution, hardstop rules)
2. `EFL_R2P_ACL_GATES_v1_0_2` (gate thresholds, hardstop triggers, clearance requirements)
3. `EFL_R2P_ACL_SYSTEM1_LEGALITY_ENGINE_v1_0_5` (computed stage, envelopes, caps)
4. `_EFL_R2P_ACL_PROJECT_INPUT_GATE_v1_0` (readiness defaults, clearance validation)
5. `EFL_SP_OUTPUT_SPEC_R2P_ACL_v1_0` (display requirements)

---

## Stage Legend (Quick Reference)

| **Stage** | **Name** | **Purpose** | **Typical Weeks Post-Op** |
|---|---|---|---|
| **S1** | Reactivation | Symptom stabilization, tissue tolerance rebuild, Band_0 work only | 0-12 weeks |
| **S2** | Progressive Loading | Strength + control rebuild, E1 plyos, unilateral work, LSI progression | 12-20 weeks |
| **S2.5** | Consolidation | Probe stage between S2 and S3, scoped E2 exception, linear running re-entry | 20-24 weeks |
| **S3** | Sport Integration | Running volume + E2 plyos, planned decel, sport-like movements (no COD yet) | 24-32 weeks |
| **S4** | Full Return | COD cleared, E3 plyos, reactive intent, high-velocity work, sport integration | 32-39 weeks |
| **S5** | RTS Complete | Full sport clearance obtained, RTS gates passed, monitoring + maintenance | 39+ weeks (Youth: 52-week advisory) |

---

## 1. Primary Exposure Permission Table

| **Stage** | **Running** | **Jumping (E-node)** | **Decel** | **COD** | **Reactive SSC** | **Notes** |
|---|---|---|---|---|---|
| **S1** | **NONE** | **E0** (stick only) | **NONE** | **NONE** | **NO** | Symptom stabilization only; no dynamic loading |
| **S2** | **NONE** | **E1** (low plyos) | **NONE** | **NONE** | **NO** | Strength + control rebuild; bilateral/unilateral plyos allowed |
| **S2.5** | **Walk/Jog ONLY** (if provider cleared) | **E1 max** + **E2 exception** (scoped) | **Linear ONLY** | **Planned ONLY** (if COD cleared) | **NO** | **Exception rule:** E2 only Week 3, Day 3, bilateral vertical, ≤15% contacts |
| **S3** | **Continuous run** (linear, submax to tempo) | **E2** | **Planned decel** (stick, braced) | **NONE** (planned drills allowed, no cutting) | **LIMITED** (low density) | Running re-entry stage; no reactive COD until S4 |
| **S4** | **Intensity progressions** (tempo, intervals) | **E3** (as allowed by caps) | **Higher intent** (reactive decel allowed) | **Planned + Reactive COD** (non-chaotic) | **LIMITED** (controlled density) | COD clearance required; reactive work introduced |
| **S5** | **Sport integration** (full intensity) | **E3/E4** (as allowed by caps + provider) | **Sport-like** | **Reactive COD** (chaotic, sport-specific) | **YES** (as allowed) | Full sport clearance required; RTS gates passed |

**Hard Rule:**  
This table **cannot override ACL Gates or System-1 computed permissions**. It is a reference only. If System-1 says `running_legal = NONE` at S3 (due to missing provider clearance), that overrides this table's "continuous run" entry.

---

## 2. Clearance Requirements Table (Provider Gates)

| **Stage** | **Resistance Cleared** | **Running Cleared** | **COD Cleared** | **Full Sport Cleared** |
|---|---|---|---|---|
| **S1** | ✅ **Required** | ❌ Not required | ❌ Not required | ❌ Not required |
| **S2** | ✅ **Required** | ❌ Not required | ❌ Not required | ❌ Not required |
| **S2.5** | ✅ **Required** | ✅ **Required** (for run exposure) | ⚠️ **Only if COD exposure added** | ❌ Not required |
| **S3** | ✅ Required | ✅ **Required** | ❌ Not required (planned decel allowed without COD clearance) | ❌ Not required |
| **S4** | ✅ Required | ✅ Required | ✅ **Required** | ❌ Not required |
| **S5** | ✅ Required | ✅ Required | ✅ Required | ✅ **Required** |

**Enforcement Source:**  
Exact enforcement comes from `GATE_PROVIDER_RESISTANCE_TRUE`, `GATE_PROVIDER_RUNNING_TRUE`, `GATE_PROVIDER_COD_TRUE`, `GATE_PROVIDER_FULL_SPORT_TRUE` in ACL Gates v1.0.2.

**Default Behavior:**  
Per Input Gate v1.0, all provider clearances default to **FALSE** unless explicitly provided as TRUE. This prevents assuming permissions that were never granted.

---

## 3. Load Ceiling Table (Band / Node / E-node)

| **Stage** | **Max Band Allowed** | **Max Node Allowed** | **Max E-Node Allowed** | **E-Node Policy Notes** |
|---|---|---|---|---|
| **S1** | **Band_0** | **Node_A** | **E0** | No plyos beyond stick landing |
| **S2** | **Band_1** | **Node_B** | **E1** | Low plyos (pogos, box step-ups, low box jumps) |
| **S2.5** | **Band_2** | **Node_C** | **E1 max** | **E2 exception:** Week 3, Day 3, bilateral vertical, ≤15% contacts only |
| **S3** | **Band_2** | **Node_C** | **E2** | Full E2 allowed (continuous bilateral/unilateral plyos) |
| **S4** | **Band_3** | **Node_D** | **E3** | Reactive plyos, depth drops, higher intent work |
| **S5** | **Band_3** | **Node_D** | **E3/E4** | E4 allowed only with explicit provider clearance + sport demands |

**Source:**  
Load ceilings are defined in `EFL_LOAD_STANDARDS_v2_2_0.json` and enforced by System-1 v1.0.5 per stage envelopes.

**Critical Note on S2.5:**  
`max_enode_allowed = E1` globally. E2 is allowed **only** under scoped exception (Week 3, Day 3 Expression Day, bilateral vertical continuous, ≤15% of session contacts). See Wrapper v1.1 Section 2.4 for full exception rules.

---

## 4. Contact Cap Table (Session + Weekly)

| **Stage** | **Contact Cap Source** | **Contact Cap Display Rule** | **Typical Session Cap (GREEN)** | **Typical Weekly Cap (GREEN)** |
|---|---|---|---|---|
| **S1** | System-1 Engine | Must print "0" (no plyos) | 0 | 0 |
| **S2** | System-1 Engine | Must print total | 30-40 | 80-100 |
| **S2.5** | System-1 Engine + exception rule | Must print total + % exception | 40-50 | 100-120 |
| **S3** | System-1 Engine | Must print per-drill + total | 40-50 | 100-120 |
| **S4** | System-1 Engine | Must print per-drill + total | 50-60 | 120-150 |
| **S5** | System-1 Engine | Must print per-drill + total | 60-80 | 150-180 |

**Note:**  
Caps are **computed by System-1** based on stage, population (youth vs adult), readiness, and historical volume tolerance. The "Typical" values above are **examples only** for GREEN readiness. Actual caps vary per athlete.

**Display Requirement:**  
Per Output Spec v1.0, all outputs must print session cap + weekly cap + current usage in Exposure Accounting footer.

---

## 5. Readiness Modifiers Table (GREEN / YELLOW / RED)

| **Readiness** | **What Changes Immediately** | **Cap Adjustments** | **Exposure Restrictions** |
|---|---|---|---|
| **GREEN** | Use stage caps and exposures as-is | No adjustment (1.0x multiplier) | None — all stage-legal exposures allowed |
| **YELLOW** | Reduce contact caps + tighten exposures | **0.75x weekly cap**, **0.8x session cap** | Some exposures restricted per engine (e.g., remove tempo runs, reduce E2 density) |
| **RED** | Collapse exposures + minimal work | **Caps → 0** or minimal (engine-derived) | Running = NONE, Jumping = minimal or NONE, COD = NONE (unless explicit override in Wrapper policy) |

**Source:**  
Readiness classification is defined in Input Gate v1.0 (defaults to YELLOW if not provided). Readiness modifiers are enforced by System-1 v1.0.5 and displayed per Output Spec v1.0.

**RED Persistence Rule:**  
Per Wrapper v1.1 Section 5.4, **2 consecutive RED sessions = forced rollback or medical route** (prevents indefinite stalling in RED).

---

## 6. Always Illegal Table (Drift-Killer Rules)

| **Stage** | **Always Illegal (No Override Pathway)** |
|---|---|
| **S1** | Running, COD, reactive work, any E1+ plyos, Band_1+ loading |
| **S2** | Running (unless walk/jog explicitly allowed in late S2 per provider), COD, reactive work, E2+ plyos |
| **S2.5** | Lateral reactive plyos, E2 outside scoped exception (Week 3, Day 3, bilateral vertical, ≤15% contacts), COD without provider clearance |
| **S3** | Reactive COD (planned COD allowed but no cutting), E3+ plyos (unless explicitly allowed by engine for advanced athletes) |
| **S4** | Chaotic reactive SSC density without provider clearance, E4 plyos (unless explicit sport demands + clearance) |
| **S5** | N/A (stage permits all exposures per provider clearance + RTS gates) |
| **ALL STAGES** | **Hardstop present = all exposures collapse to NONE** (no override), F-V bias manipulation (BALANCED only in R2P-ACL), specialization blocks (elastic/decel/force specialization illegal during R2P), E4 shock plyos without explicit clearance |

**Rationale:**  
These rules prevent "interpretation coaching" where a coach might think "S3 feels ready for reactive COD" when gates explicitly forbid it.

**Containment Rule:**  
If any of these illegal behaviors appear in a session/meso output → output is **INVALID** per Output Spec v1.0 and must be rejected.

---

## 7. Hardstop Override Rule (Absolute)

**Single-Line Law:**  
**HARDSTOP OVERRIDES STAGE.**

If **any** hardstop symptom is TRUE (effusion increase, giving way, sharp pain, limp, pain spike), the system **must**:
1. Set all exposures to **NONE** (running = NONE, COD = NONE, jumping = NONE)
2. Collapse envelopes to **minimum** (Band_0, Node_A, E0)
3. Route to **symptom control** or **medical review** (no normal training session)
4. **Preserve historical stage** per Wrapper v1.1 Section 4.2 (return path when hardstop clears)

**This rule beats:**
- Stage computed (even if S4)
- Readiness GREEN
- Coach-entered stage
- Provider clearances (they remain true but exposures collapse until hardstop clears)

**Hardstop Escalation Rule:**  
Per Wrapper v1.1 Section 4.3, **≥2 hardstops within 14 days = mandatory medical lock** (all training permissions blocked until provider clearance).

---

## 8. S2.5 Exception Transparency (Critical)

**S2.5 is NOT "S3 lite."**  
It is a **consolidation probe** with E1 global ceiling + narrow E2 exception.

**E2 Exception Rules (Non-Negotiable):**
- **When allowed:** Week 3 of 4-week S2.5 meso, Day 3 (Expression Day) only
- **Pattern allowed:** Bilateral vertical continuous **only** (no lateral, no single-leg, no control-day, no capacity-day)
- **Contact limit:** ≤15% of total session plyo contacts
- **Readiness gate:** GREEN only (YELLOW/RED collapses E2 exception to E1)

**Output Display Requirement:**  
Per Output Spec v1.0 Section 8.1, any S2.5 output with E2 drill must:
1. Label drill as `E2-EXCEPTION (S2.5 constrained)`
2. Show % of contacts allocated to E2 exception in footer
3. If >15% or outside scoped conditions → output is **INVALID**

---

## 9. Youth RTS Advisory (Legal/Ethical)

**For Youth (13-17) athletes reaching S5 at <52 weeks post-op:**
- **Advisory status:** Non-blocking (gates permit clearance if provider clears + S4 exit gates pass)
- **Legal/ethical requirement:** Advisory **must be surfaced** in all outputs as elevated re-injury risk flag
- **Display format:** Per Output Spec v1.0 Section 8.2, prominent warning banner with age, weeks post-op, risk disclosure, family discussion recommendation

**Containment Rule:**  
Any output that grants S5 clearance to youth <52 weeks without surfacing advisory violates ethical/legal risk disclosure requirements and must be rejected with reason code `YOUTH_RTS_ADVISORY_NOT_SURFACED`.

---

## 10. Audit Workflow (How to Use This Matrix)

### 10.1 Rapid Meso Audit (60 Seconds)

**Step 1:** Identify effective stage (from Legality Snapshot)  
**Step 2:** Check Exposure Permission Table — are all exposures stage-legal?  
**Step 3:** Check Clearance Requirements Table — are required provider clearances TRUE?  
**Step 4:** Check Load Ceiling Table — are all drills within band/node/E-node caps?  
**Step 5:** Check Always Illegal Table — does meso include any forbidden exposures?  
**Step 6:** If S2.5 — verify E2 exception rules (Week 3, Day 3, bilateral vertical, ≤15%)  
**Step 7:** If Youth + S5 — verify RTS advisory surfaced

**If all checks pass → meso is structurally legal (still requires System-1 validation for dynamic caps/gates).**

---

### 10.2 Onboarding New Coach

**Use this matrix as:**
1. **First-day reference** — "Here's what each stage allows"
2. **Decision-making tool** — "Can I include tempo runs in S2?" (check table → NO)
3. **Drift prevention** — "I think S3 allows reactive COD" (check table → NO, planned only)

**Critical Reminder for New Staff:**  
This matrix is **derived from** Wrapper + System-1 + Gates. If you find a mismatch, **upstream documents win** and this matrix must be updated.

---

### 10.3 Catching "S2.5 Creep"

**Most common violation:** Treating S2.5 as "full E2 stage" when global ceiling is E1.

**How to catch it:**
1. Scan meso for any E2 drills in S2.5
2. Check if labeled `E2-EXCEPTION (S2.5 constrained)`
3. Verify conditions: Week 3, Day 3, bilateral vertical, ≤15% contacts
4. If any condition fails → violation, output INVALID

---

## 11. Court-to-R2P Parity

| **Feature** | **Court Permission Matrix** | **R2P-ACL Permission Matrix v1.0** |
|---|---|---|
| One-page scannable format | ✅ | ✅ |
| Exposure permissions by stage | ✅ | ✅ (running/jumping/decel/COD/reactive) |
| Clearance requirements | ✅ | ✅ (provider gates) |
| Load ceilings by stage | ✅ | ✅ (band/node/E-node) |
| Readiness modifiers | ✅ | ✅ (GREEN/YELLOW/RED) |
| Always illegal table | ✅ | ✅ (drift-killer) |
| Hardstop override rule | ✅ | ✅ (symptoms beat stage) |
| Audit workflow | ✅ | ✅ (60-second meso check) |

**Architectural Mirror:**  
This R2P-ACL Permission Matrix mirrors Court Permission Matrix in purpose (human-facing truth table) and structure (scannable tables + drift-killer rules).

---

## 12. Litmus Test (Permission Matrix Validation)

| **Test Scenario** | **Expected Permission Matrix Answer** |
|---|---|
| Can I include tempo runs in S2? | **NO** — S2 running = NONE (check Exposure Permission Table) |
| Can I include reactive COD in S3? | **NO** — S3 COD = planned only, no reactive (check Exposure Permission Table) |
| Can I use E2 plyos in S2.5 Week 1? | **NO** — S2.5 E2 exception only allowed Week 3, Day 3 (check S2.5 Exception Transparency) |
| Does S4 require COD clearance? | **YES** — S4 COD cleared = required (check Clearance Requirements Table) |
| What happens to caps when readiness = YELLOW? | **0.75x weekly, 0.8x session** (check Readiness Modifiers Table) |
| Can I proceed with session if hardstop triggered? | **NO** — Hardstop overrides stage, all exposures collapse to NONE (check Hardstop Override Rule) |
| Can I include elastic specialization meso in S3? | **NO** — Specialization blocks illegal during R2P (check Always Illegal Table) |
| Does youth athlete at S5 (40 weeks post-op) need advisory? | **YES** — <52 weeks requires RTS advisory banner (check Youth RTS Advisory) |

**If Permission Matrix passes all tests → reference is accurate.**

---

## 13. Version Coherence & Changelog

### 13.1 Version Coherence Rule

This Permission Matrix is derived from:
- Wrapper: `EFL_SP_PROJECT_WRAPPER_R2P_ACL_v1_1`
- Input Gate: `_EFL_R2P_ACL_PROJECT_INPUT_GATE_v1_0`
- Output Spec: `EFL_SP_OUTPUT_SPEC_R2P_ACL_v1_0`
- System-1 Engine: `EFL_R2P_ACL_SYSTEM1_LEGALITY_ENGINE_v1_0_5`
- ACL Gates: `EFL_R2P_ACL_GATES_v1_0_2`

**If upstream documents are updated → this Permission Matrix must be updated to align.**

---

### 13.2 When This Permission Matrix Can Be Modified

This Permission Matrix may only be updated by:
- **EFL Director of Performance Systems**
- **Explicit versioning** with changelog and effective date

Users and coaches **cannot modify** this Permission Matrix during normal operations. If you find an error or mismatch → report to Performance Systems team.

---

### 13.3 Changelog

| **Version** | **Date** | **Changes** | **Author** |
|---|---|---|---|
| 1.0 | 2026-01-11 | Initial release for R2P-ACL Project. Defines stage legend, primary exposure permission table (running/jumping/decel/COD/reactive), clearance requirements table (provider gates), load ceiling table (band/node/E-node), contact cap table, readiness modifiers table (GREEN/YELLOW/RED), always illegal table (drift-killer), hardstop override rule, S2.5 exception transparency, youth RTS advisory, and audit workflow. | EFL |

---

## Conclusion

This **Stage Permission Matrix** is a **one-page truth table** that prevents staff drift, interpretation coaching, and accidental exposure creep.

**Its job is simple:**
- Answer "What's allowed at each stage?" in scannable table format
- Translate Wrapper + System-1 + Gates rules into human-facing reference
- Enable 60-second meso audits and rapid onboarding

**Remember:**  
**This matrix is derived from upstream documents.** If mismatch exists, **Wrapper v1.1 + System-1 v1.0.5 + Gates v1.0.2 win** and this matrix must be updated.

**Use this matrix as your first reference, but always validate against System-1 for dynamic caps and gate evaluation.**

---

**END OF PERMISSION MATRIX**
