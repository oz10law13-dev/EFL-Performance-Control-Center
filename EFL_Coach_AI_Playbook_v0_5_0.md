# **EFL Coach & AI Playbook — Operating Guide**

**Status:** PRODUCTION-READY  
**Version:** 0.5.0  
**Date:** December 22, 2025 (Load Standards v2.2.0 & Governance v4.1 Aligned)  
**Authority:** Load Standards v2.2.0 + Governance v4.1 + Live Service Stack v1.1 + POSITRON v2.1  
**Owner:** Austin Lawrence, LMT, NASM-CPT, NASM-PES, NASM-CES, Stretching & Flexibility Coach, B.S. Kinesiology

---

## **AUTHORITY CLAUSE (READ FIRST)**

**This Playbook is an execution guide only.**

All decisions, programs, and sessions must comply with:
1. **EFL Load Standards v2.2.0** (authoritative source for all ceilings, counting methods, F-V bias profiles, and limits)
2. **EFL Governance System v4.1** (deterministic gate logic, 7-Gate Decision Tree, Client State Engine, and F-V Bias Compliance)
3. **EFL Codex v2.1.1** (mission, service architecture, pricing)

**If guidance in this Playbook conflicts with Load Standards v2.2.0 or Governance v4.1, LOAD STANDARDS & GOVERNANCE WIN.**

Coaches and AI must not improvise, override, or "use judgment" to bypass these documents. When in doubt, escalate to Owner.

---

## **Section 1: Operating Contract (All Coaches & AI)**

## **1.1 Sources of Truth (Only These Documents Are Legal)**

All decisions, answers, and programs must originate from and remain bound to:

* **Elite Fitness Lab Systems Codex v2.1.1** – Mission, service architecture, pricing, coaching standards, operations
* **EFL Live Service Stack v1.1** – The exact five services EFL currently offers (Youth Lab, SP Performance, R2P, ERL, Mobility Lab)
* **EFL Load Standards v2.2.0** – Population ceilings, season operating ranges, contact/sprint counting standards, R2P progression, **Force-Velocity Bias Profiles (NEW)**
* **EFL Governance System v4.1** – Client State Engine, 7-Gate Decision Tree (including **Gate 7 F-V Bias Compliance**), MicroSessions enforcement
* **EFL MesoMacro Manifest v1.0.1** – Locked macro blocks and progression gates for each service line
* **Appendix J – Global Programming Laws v1.0** – Plyometric exposure, elasticity, sprint, node, and session structure laws
* **AETHER Exercise Manifest v1.2** – Exercise legality, population gates, node eligibility, pattern, and difficulty tags
* **EFL Block Selector Spec v2.2** – Deterministic routing from athlete profile + season + flags → block tag
* **Project POSITRON v2.1** – Enforcement, escalation, audit, and change-control protocol

**If a service, rule, block, exercise, or F-V bias constraint is not defined in these manifests, it is not an EFL standard and must be treated as DENIED until the Owner updates the relevant standard.**

---

## **1.2 Allowed Actions (What Coaches & AI May Do)**

Within this contract, a coach or AI may:

* **Explain EFL's mission and non-negotiables** using only Codex language and Ideal Client Profile tables
* **Place new clients** into Youth Lab, SP Performance, R2P, Mobility Lab, or ERL via the Codex onboarding flow (Inquiry → Discovery → Consult → Placement)
* **Assess F-V bias profile** using CMJ testing, squat 1RM benchmarking, or F-V slope testing per Governance v4.1 Section 8
* **Describe and schedule only live services** (Youth Lab, SP Performance, R2P, ERL, Mobility Lab) with durations and pricing from the Aug 2025 price sheet; no other offers may be promoted
* **Select legal macro blocks** via Block Selector rules (e.g., YLGENFND8WKGENERAL, SPOFFDEV16WKHSBASKETBALL, ADULTSTRGENFND8WKGENERAL, R2P progressive builds)
* **Build sessions** that follow the PRIME → PREP → WORK → CLEAR 4-block chassis and respect population overlays, plyometric ceilings, sprint caps, node distribution, and F-V bias targets per Governance v4.1
* **Choose exercises** that are legal for the athlete's population, node, season, injury status, AND F-V bias profile per AETHER manifest and Governance v4.1
* **Educate on Codex and Governance concepts** (e.g., why youth do not get depth jumps, why FORCE_BIASED athletes need 70% of volume in strength bands, why failure on neural lifts is forbidden)

---

## **1.3 Forbidden Actions (What Coaches & AI Must Never Do)**

No coach or AI may:

* **Invent or promote any service** not listed in Live Service Stack v1.1 (e.g., adult HIIT bootcamps, generic group classes, custom memberships)
* **Change pricing, discounts, or policies**; all changes require Owner approval and a Codex/price-sheet version update
* **Design custom macros** outside the approved MesoMacro templates or alter block structures beyond what manifests allow
* **Assign an F-V bias** that violates population/season rules (e.g., VELOCITY_BIASED to Youth 17, any bias except BALANCED during in-season)
* **Recommend exercises, nodes, or loads** that violate AETHER, Load Standards, Governance v4.1, or Appendix J (e.g., youth depth jumps 18–45 cm, R2P Stage 1 plyos, exceeding plyometric ceilings)
* **Ignore pain, red flags, or stress data**; any implied pain 2–10/10, unresolved medical issues, or Codex red flags must trigger regression or escalation, not progression
* **Override population gates, sprint caps, node rules, or F-V bias rules** "because the athlete is advanced" without a logged Owner-level override via POSITRON/COUNCIL

---

## **1.4 Default-Deny & Escalation Rules**

When data is missing, ambiguous, or conflicting:

* **Default response is DENY or REGRESS**, not "best guess" or improvisation
* If the situation requires medical, ethical, or policy judgment beyond the manifests, **escalate to a human coach/medical provider**; AI must not auto-approve

---

## **1.5 Mandatory Season Declaration (System-Wide Requirement)**

**CRITICAL:** Before any program selection, session build, or load decision occurs, the following **must be explicitly declared and recorded**:

### Season Type (Required Input):
- `OFF_SEASON` – Highest volume development window; F-V bias allowed (all types)
- `PRE_SEASON` – Sport-specific preparation phase; F-V bias allowed (all types)
- `IN_SEASON_TIER_1` – High fixture density (3+ games/week); **BALANCED ONLY**
- `IN_SEASON_TIER_2` – Moderate fixture density (2 games/week); **BALANCED ONLY**
- `IN_SEASON_TIER_3` – Low fixture density (0-1 games/week); **BALANCED ONLY** (except Adult Tier 3 with approval)
- `POST_SEASON` – Recovery and restoration phase; **BALANCED ONLY**

**This declaration is NOT inferred** by date, sport, or assumption. It must be explicitly selected.

### Enforcement Rules:

✅ **If season_type is missing:** DEFAULT DENY - do not assign any program  
✅ **If season_type conflicts with fixture density:** ESCALATE to coach  
✅ **If season is IN_SEASON or POST_SEASON:** Enforce BALANCED bias (override any athlete-specific bias profile)  
✅ **All plyometric and sprint volumes:** Pulled from seasonal operating range in Load Standards v2.2.0, NOT absolute ceilings

---

## **1.2A Force-Velocity Bias Rules (Non-Negotiable, NEW in v4.1)**

These rules are **mandatory** and cannot be overridden by athlete preference, coach judgment, or competitive urgency. Violating any of these triggers automatic escalation.

### **Youth 16 and Under**
- **F-V Bias Profile:** BALANCED only (enforced)
- **Override Possible:** NO
- **Rationale:** CNS and force-velocity development still maturing; balanced exposure is developmental priority
- **Consequence of Violation:** Exercise quarantined, program regressed, Coach escalation required

### **Youth 17 Advanced (2+ years training age, documented)**
- **F-V Bias Profiles Allowed:** FORCE_BIASED only (conditional)
- **Restrictions:** 
  - Maximum 60/40 split (never 70/30 like adults)
  - Off-season and pre-season only (in-season = BALANCED enforced)
  - Requires Director approval and documentation of training age
- **Assessment Required:** CMJ profiling, squat 1RM ratio, or F-V slope testing
- **Consequence of Violation:** Bias profile rejected, BALANCED enforced, Director notification

### **Adult (18+, 2+ years training age)**
- **F-V Bias Profiles Allowed:** FORCE_BIASED, VELOCITY_BIASED, or BALANCED
- **Restrictions:**
  - In-season = BALANCED enforced (except Tier 3 low fixture density with approval)
  - Post-season = BALANCED enforced
  - Off-season and pre-season = all types allowed
- **Assessment Recommended:** CMJ profiling, squat 1RM ratio, F-V slope testing, or documented rationale
- **No Override:** If testing shows balanced profile (Squat 1.5-2.0x BW, RSI 1.5-1.8), BALANCED is default

### **R2P (Return to Performance)**
- **F-V Bias Profile:** BALANCED only (enforced for all R2P stages)
- **Rationale:** Tissue integrity and movement quality are primary; bias targeting adds unnecessary complexity
- **Override Possible:** NO (medical priority overrides performance optimization)

### **Season Override Rules (NEW)**
- **If season is IN_SEASON_TIER_1, IN_SEASON_TIER_2, IN_SEASON_TIER_3, or POST_SEASON:**
  - Force `fv_bias_profile = BALANCED` regardless of athlete's assessed bias profile
  - Ignore any scheduled FORCE_BIASED or VELOCITY_BIASED programming
  - Reason: Maintenance and resilience priority during competition; F-V targeting is off-season/prep-season strategy

---

# **Section 2: Legal Services & Offers (What EFL Actually Provides)**

## **2.1 Youth Lab (Ages 8–12)**

**Duration:** 45–50 minutes per session  
**Format:** Semi-private group (high frequency of change, gamified skills)  
**Focus:** Movement literacy, landing mechanics, coordination, balance, athletic foundations  
**Load Profile:** Low external load, high movement variety  
**F-V Bias Status:** ❌ **NO (BALANCED enforced, no bias targeting)**

**Plyometric Ceilings (Season-Aware):**
- **Session caps (absolute safety limits per Load Standards v2.2.0):**
  - MicroSession: 50 contacts maximum
  - Full Session: 80 contacts maximum
  - Max sprint sessions: 3 per week
- **Weekly volume governed by season_type** (Load Standards v2.2.0):
  - OFF_SEASON: 120-160 contacts/week
  - IN_SEASON_TIER_1: 0-80 contacts/week (maintenance only)
  - POST_SEASON: 0-80 contacts/week (recovery emphasis)

⚠️ **Critical Rule:** Session ceilings do NOT grant permission to exceed seasonal weekly ranges.  
**Elasticity:** E1-E2 allowed (Tier 1-2); E3-E4 (Tier 3) FORBIDDEN unless Director override  
**Session Structure:** PRIME (5–10m) → PREP (8–12m) → WORK (25–35m) → CLEAR (5–10m)  
**Program Assignment:** YLGENFND8WKGENERAL (8-week Foundation macro)  
**Strategic Role:** The Farm System — recurring base and community growth engine; parent referrals to SP Performance

**Pricing (Aug 2025):**
* 4 Pack: $80 ($20/session, 3 months)  
* 8 Pack: $140 ($17.50/session, 2 months)  
* 10 Pack: $170 ($17/session, 2 months)  
* 12 Pack: $190 ($15.83/session, 3 months)

---

## **2.2 SP Performance Lab (Ages 13+ competitive)**

**Duration:** 60 minutes per session  
**Format:** Semi-private performance training  
**Focus:** Strength, power, speed, resilience, elasticity, sport-specific overlays  
**Load Profile:** Earned exposure dictates intensity; formal plyometric tiers E1–E4  
**F-V Bias Status:** ⚠️ **CONDITIONAL** 
- Youth 13-16: ❌ NO (BALANCED enforced)
- Youth 17 Advanced: ✅ FORCE_BIASED only (60/40 max, off-season/pre-season only, Director approval)
- Adult: ✅ All types (off-season/pre-season); BALANCED enforced in-season/post-season

**Plyometric Ceilings (Season-Aware):**
- **Session caps (absolute safety limits per Load Standards v2.2.0):**
  - Youth 13-17 Full Session: 120 contacts maximum
  - Youth 13-17 MicroSession: 80 contacts maximum
  - Adult Full Session: 140 contacts maximum
  - Adult MicroSession: 60 contacts (E0-E1 only)
  - Max sprint sessions: 3 per week (all populations)
- **Weekly volume governed by season_type** (Load Standards v2.2.0):
  - Youth 13-17 OFF_SEASON: 140-200 contacts/week
  - Youth 13-17 IN_SEASON_TIER_1: 60-100 contacts/week
  - Adult OFF_SEASON: 160-240 contacts/week
  - Adult IN_SEASON_TIER_1: 120-160 contacts/week

⚠️ **Critical Rule:** Session ceilings do NOT grant permission to exceed seasonal weekly ranges.  
**Elasticity:** E1-E2 (Tier 1-2) always allowed; E3-E4 (Tier 3) allowed but ≤40% of session contacts for Youth 13-17  
**Session Structure:** PRIME (5–10m) → PREP (8–12m) → WORK (25–35m) → CLEAR (5–10m)  
**Program Assignment:** SPOFFDEV16WKHSBASKETBALL (or sport-specific variant; 16-week macro)  
**Strategic Role:** The Brand Drivers — premium service that builds authority; athletes wear the shirt and win on the field  
**Progression Gates:** Athletes must pass formal movement-quality and load-tolerance gates before advancing phases (documented in MesoMacro)  
**F-V Bias Assessment:** Prior to off-season/pre-season assignment, assess bias profile using CMJ profiling, squat 1RM ratio, or F-V slope testing per Governance v4.1 Section 8

**Pricing (Aug 2025):**
* 4 Pack: $140 ($35/session, 3 months)  
* 8 Pack: $265 ($33.13/session, 3 months)  
* 10 Pack: $310 ($31/session, 3 months)  
* 12 Pack: $365 ($30.42/session, 3 months)

---

## **2.3 Return to Performance (R2P) – Post-Injury Bridge**

**Duration:** 60–75 minutes per session  
**Format:** 1-on-1 integrated approach  
**Components:** Manual therapy (15–25 min) + Performance training (45–50 min)  
**Focus:** Bridge gap between PT discharge and full sport participation  
**Approach:** Constraints-led; pain-free ROM is the primary metric  
**Load Profile:** Graded exposure, tissue work, controlled intensity  
**F-V Bias Status:** ❌ **NO (BALANCED enforced, all stages)**

**Manual Therapy:** Hands-on joint access, tissue quality restoration (LMT-delivered)  
**Program:** R2P Progressive Build (phase-based, sport-dependent, per MesoMacro)  
**Strategic Role:** The Revenue Bridge — high-ticket service leveraging dual-credential coach expertise; captures market share from PT clinics lacking performance knowledge  
**Progression Pathway:** R2P Graduation to SP Performance Lab (tracked as core KPI)  
**Dual Credential Requirement:** Coach must hold both CSCS/performance cert and LMT (or equivalent manual therapy credential)  
**Safety Protocol:** No R2P athlete progresses to dynamic load without passing the positional isometric standard first

**Pricing (Aug 2025):**
* 4 Pack: $320 ($80/session, 3 months)  
* 8 Pack: $630 ($78.75/session, 3 months)

---

## **2.4 Elite Recovery Lab (ERL)**

**Duration:** 60–75 minutes per session  
**Format:** 1-on-1 hands-on manual therapy  
**Focus:** Tissue quality, joint access, durability, recovery support  
**Modality:** Licensed Massage Therapy (LMT-delivered)  
**Integration:** Pairs with SP Performance, R2P, or Mobility Lab as retention anchor  
**Program:** No formal programming; tissue-quality focus only  
**F-V Bias Status:** ❌ **NO (not applicable; tissue work only)**
**Strategic Role:** The Retention Anchor — keeps athletes healthy and adds revenue without programming overhead

**Pricing (Aug 2025):**
* 4 Pack: $320 ($80/session, 3 months)

---

## **2.5 Mobility Lab**

**Age Range:** Athletes (semi-private) and adults (private)  
**Duration:** 60 minutes per session  
**Format:**
* **Semi-Private (Athletes):** 15 minutes of hands-on tissue work on the table + 15–25 minutes of mobility and strength integration in a semi-private group
* **Private (Adults):** 60 minutes 1-on-1 targeted mobility and corrective strength

**Focus:** Joint-centric mobility, corrective exercise, pain-free movement, durability  
**Load Profile:** Low-to-moderate intensity; emphasis on leaving the session feeling better than arriving  
**F-V Bias Status:** ❌ **NO (BALANCED only, no bias targeting)**
**Session Structure:** PRIME (5–10m) → PREP (8–12m) → WORK (25–35m) → CLEAR (5–10m)  
**Program:** ADULTSTRGENFND8WKGENERAL (8-week Foundation macro) for adult strength; R2P-based for post-injury mobility  
**Strategic Role:** Retention and entry point for adult clients and athletes seeking joint-centric, durability-focused training and light recovery support

**Pricing (Aug 2025) — Mobility Lab:**
* 4 Pack: $250 ($62.50/session, 3 months)  
* 8 Pack: $480 ($60/session, 2 months)  
* 10 Pack: $600 ($60/session, 3 months)

---

## **2.6 Paused / Not Offered**

**Adult Group Strength**  
Status: PAUSED  
Reason: Prime evening hours reallocated to high-ROI athlete acquisition (SP Performance, Youth Lab) and high-ticket services (R2P, ERL)  
Future: May be revisited in FY2026 if operational capacity allows

---

## **Section 2.7: Contact & Sprint Counting Standards (Load Standards v2.2.0)**

### **2.7.1 Contact Counting Standard: Count Every Foot Strike (NSCA Standard)**

**From Load Standards v2.2.0 (NSCA Industry Standard):**  
Volume is measured by counting every individual foot strike to the ground.

**CRITICAL RULE:** Counting reps instead of contacts is a SAFETY VIOLATION.

**Contact Counting Law (Non-Negotiable):**
- Every foot strike = 1 contact
- Unilateral alternating = 2 contacts per rep (both feet strike)
- Formula: Sets × Reps × Foot_Strikes = Total Contacts

When exercises are prescribed "per leg," count BOTH legs in your total.

### **Examples for Coaches:**

| Exercise | What You Program | Pattern | How to Count | Total Contacts |
|---|---|---|---|---|
| Box Jump | 3 sets × 5 reps | Bilateral | 5 reps × 1 contact × 3 sets | **15 contacts** |
| Single Leg Bound L→R | 3 sets × 5 reps per leg | Unilateral | 5 reps × **2 feet** × 3 sets | **30 contacts** |
| Pogo Hops | 3 sets × 10 reps | Continuous | 10 strikes × 3 sets | **30 contacts** |

### **Common Coach Mistakes:**

❌ **WRONG:** "5 reps per leg = 5 contacts"  
✅ **CORRECT:** "5 reps per leg = 10 total foot strikes" (5 left + 5 right)

❌ **WRONG:** Counting exercise variations instead of total foot strikes  
✅ **CORRECT:** Sum ALL foot strikes across all plyometric exercises

---

### **2.7.2 Sprint Counting Standard: TRUE_SPRINT_METERS_ONLY**

**From Load Standards v2.2.0 (NSCA Industry Standard):**  
Only meters at ≥90% intensity count toward weekly sprint volume.

**SPRINT COUNTING RULE (MANDATORY):**
- Only sprint work ≥90% Vmax counts toward volume caps
- `intensity_percent_vmax` field is REQUIRED for all sprint exercises
- Missing intensity → QUARANTINE or count as ZERO
- Tempo ≠ Sprint
- Conditioning ≠ Sprint
- Warmup runs ≠ Sprint

**Key Rule:** Tempo runs, warmups, and low-intent shuttles **do NOT count** as sprint volume.

### **What Counts as Sprint:**

✅ Acceleration work ≥90% effort  
✅ Max velocity sprints  
✅ Flying sprints at ≥90% intensity  
✅ Resisted sprints (sled) if ≥90% effort

### **What Does NOT Count:**

❌ Warmup runs <90% intensity  
❌ Tempo runs (typically 70-85%)  
❌ Change-of-direction drills <90%  
❌ Conditioning shuttles

### **Intensity Guide for Coaches:**

| % Vmax | What It Feels Like | Counts? |
|---|---|---|
| 100% | Max effort, competition speed | ✅ YES |
| 95% | Near-max, building to top speed | ✅ YES |
| 90% | High effort threshold | ✅ YES |
| 85% | Sub-max effort | ❌ NO (conditioning) |
| 75% | Tempo pace | ❌ NO (tempo work) |

### **Coach Action Required:**

When programming sprints, **always specify intensity**:
- "10-yard Acceleration at 95% Vmax" ✅
- "40-yard Sprint at 100%" ✅
- "100m Tempo at 75%" ❌ (doesn't count toward sprint cap)

---

## **2.7.3 E-Node to Plyo Tier Mapping (Coach Reference)**

**From Governance v4.1:**  
E-nodes map to Plyometric Tiers as follows:

| E-Node | Plyo Tier | Intensity | Youth 8-12 | Youth 13-17 | Examples |
|---|---|---|---|---|---|
| **E0** | None | Non-plyometric | ✅ | ✅ | Squat, Lunge, Core |
| **E1** | Tier 1 | Low | ✅ | ✅ | Ankle Hops, Jump Rope |
| **E2** | Tier 2 | Moderate | ✅ | ✅ | Broad Jump, Box Jump 12-24" |
| **E3** | Tier 3 | High Shock | ❌ Forbidden* | ✅ ≤40%** | Depth Jump 12-18" |
| **E4** | Tier 3 | Max Shock | ❌ Forbidden* | ✅ ≤40%** | Depth Jump >18" |

*Youth 8-12: E3/E4 require Director override  
**Youth 13-17: E3/E4 combined must be ≤40% of total session contacts

**TIER 3 SHOCK WORK CAP (Youth 13-17):**
- Tier 3 (E3/E4) ≤ 40% of total session contacts
- Calculation: (E3_contacts + E4_contacts) / total_contacts ≤ 0.40
- Example: 120-contact session → max 48 Tier 3 contacts
- YELLOW readiness → Tier 3 FORBIDDEN (revert to E0-E2 only)
- RED readiness → ALL plyos forbidden (E0 only)

### **Coach Guidance:**

**Youth 8-12 Programs:**
- Stick to E1-E2 (Tier 1-2) only
- E3-E4 absolutely forbidden unless Austin approves with written justification

**Youth 13-17 Programs:**
- E1-E2 can be used freely
- E3-E4 allowed but track carefully: if session has 120 total contacts, max 48 can be E3/E4

**Adult Programs:**
- All E-nodes allowed within session/weekly caps

---

## **2.7.4 Season Block System (Load Standards v2.2.0)**

Programs should target season-appropriate volume ranges:

### **Youth 8-12:**

| Season Block | Weekly Contacts | Weekly Sprints | Notes |
|---|---|---|---|
| OFF_SEASON | 120-160 | 120-240m | Higher volume window |
| IN_SEASON_TIER_1 | 0-80 | 0-120m | High fixture density, maintenance |
| POST_SEASON | 0-80 | 0-120m | Recovery emphasis |

### **Youth 13-17:**

| Season Block | Weekly Contacts | Weekly Sprints | Notes |
|---|---|---|---|
| OFF_SEASON | 140-200 | 800-1200m | Aggressive development window |
| IN_SEASON_TIER_1 | 60-100 | 400-800m | High games/week, avoid maxing caps |
| POST_SEASON | 60-120 | 300-600m | Restore and deload |

### **Adult:**

| Season Block | Weekly Contacts | Weekly Sprints | Notes |
|---|---|---|---|
| OFF_SEASON | 160-240 | 1000-1600m | High capacity development |
| IN_SEASON_TIER_1 | 120-160 | 600-1000m | Maintenance during competition |
| POST_SEASON | 80-140 | 300-800m | Recovery period |

**Coach Note:** These are **recommended targets**. Absolute ceilings (80/120/140 per session) must NEVER be exceeded.

---

## **2.7.5 Common Seasonal Violations (Auto-DENY)**

These programming decisions must be **denied or escalated** regardless of athlete readiness:

### ❌ Volume Violations:
- **Off-season volumes during in-season:** Programming 140-200 contacts/week (OFF_SEASON range) during IN_SEASON_TIER_1
- **Maxing absolute ceilings in-season:** Using 120+120 = 240/week just because the absolute ceiling allows it
- **Sprint overreach:** Programming 800m/session during IN_SEASON_TIER_1 when range is 400-800m

### ❌ Intensity Violations:
- **Tier 3 plyometrics in POST_SEASON:** E3/E4 work during recovery phase
- **High-intensity work on maintenance phases:** Programming max-effort sprints during IN_SEASON_TIER_1

### ❌ Readiness Loopholes:
- **"GREEN readiness" exception:** Using GREEN status to justify off-season volume during in-season
- **Readiness modifiers apply AFTER seasonal ceilings, not before**
- Example: IN_SEASON_TIER_1 range is 60-100/week. GREEN readiness doesn't allow 200/week.

### ✅ Correct Seasonal Logic:

**Step 1:** Select season_type (determines weekly operating range)  
**Step 2:** Apply readiness modifier to that range (YELLOW = 75%, RED = 0%)  
**Step 3:** Program within adjusted range

**Example (Youth 13-17):**
- Season: IN_SEASON_TIER_1 → 60-100 contacts/week
- Readiness: YELLOW → 60-100 × 0.75 = 45-75 contacts/week
- Program: Target 50-70 contacts/week ✅

**NOT:**
- Athlete is GREEN → Use OFF_SEASON volume (140-200/week) ❌ ILLEGAL

---

# **Section 3: Session & Programming Rules (PRIME–PREP–WORK–CLEAR in BridgeAthletic)**

## **3.1 Universal Session Chassis (BridgeAthletic Workout Structure)**

In BridgeAthletic, every **Workout** (single training day) must follow this non-negotiable 4-block structure using **Blocks** (the components inside a workout).

## **PRIME (5–10 minutes) → BA Block #1**

* **BA Block Name:** `PRIME`  
* **Goal:** Open joints, organize positions, low-level activation  
* **Content:** Add exercises as individual items inside this block (e.g., joint mobility circuits, PVC pipe work, glute activation, soft-tissue prep)
* **Intensity:** Low  
* **Breathing Rule:** Natural breathing only. No dedicated breathwork drills. Breathing is organized through movement
* **Parameters:** Reps 5–10, RPE 3–4, tempo controlled

## **PREP (8–12 minutes) → BA Block #2**

* **BA Block Name:** `PREP`  
* **Goal:** Pattern rehearsal (Squat, Hinge, Push, Pull)  
* **Content:** Add exercises as individual items (e.g., tempo goblet squats, trap-bar hinges, push-up progressions, rowing patterns)
* **Intensity:** Low-to-Moderate; velocity and complexity increase, not load
* **Parameters:** Reps 6–8, RPE 4–5, tempo 3-1-1 or similar

## **WORK (25–35 minutes) → BA Blocks #3–5**

* **BA Block Names:** `WORK-A`, `WORK-B`, (optional) `WORK-C`  
* **Goal:** Primary training effect (Strength, Power, Speed, or Capacity)  
* **Structure:**  
  * **WORK-A (Primary Strength / Power):** 1–2 main lifts or plyometric patterns (e.g., bilateral squat, hinge, primary plyometric)
  * **WORK-B (Secondary / Accessory):** 1–2 secondary patterns or unilateral/accessory movements (e.g., lunge, single-leg work, horizontal push/pull)
  * **WORK-C (Optional Pod / Finisher):** Short, controlled density or capacity pod that stays within Appendix J laws for plyos, sprints, and fatigue
* **Parameters:** Reps/sets per MesoMacro; RPE 6–9 for primary, RPE 5–7 for accessory; track sets are key exercises

## **CLEAR (5–10 minutes) → BA Block #6**

* **BA Block Name:** `CLEAR`  
* **Goal:** Downshift and decompression  
* **Content:** Add exercises (e.g., 90/90 breathing, passive stretching, soft-tissue self-massage, quad-calf mobilization)
* **Intensity:** Low  
* **Breathing Rule:** Dedicated breathwork lives here (e.g., 90/90 breathing, long exhale drills)
* **Parameters:** Reps 5–8, RPE 2–3, long exhale tempo

**Rule:** Sub-blocks cannot be used to bypass any law (e.g., adding a "finisher" that pushes plyo contacts, sprint volume, or RPE beyond what the block/Appendix J allow). Sub-blocks are just **organization**, not extra volume permission.

---

## **3.2 Population Overlays (How Services Adapt the Chassis in BA)**

The PRIME–PREP–WORK–CLEAR structure is universal, but each population has specific constraints and focus areas within BridgeAthletic blocks:

## **Youth Lab (8–12)**

* **PRIME Block:** High frequency of change, novelty, coordination drills  
* **PREP Block:** Gamified pattern learning; fun movement variety  
* **WORK-A/B Blocks:** Landing mechanics, deceleration, multi-planar control; low external load; max 50 plyo contacts/session  
* **CLEAR Block:** Short decompression; light breathing and stretching  
* **Constraints (Two-Layer System):**
  * **Absolute ceilings:** 50 contacts/MS, 80/Full Session; E1-E2 only; sprint 80m/session, 240m/week
  * **Seasonal operating ranges:** Must program within season-appropriate weekly targets (e.g., IN_SEASON_TIER_1: 0-80/week)
  * **F-V Bias:** BALANCED only (no bias targeting)
  * **Critical:** Do not max absolute ceilings during in-season phases

## **SP Performance (13+)**

* **PRIME Block:** Sport-specific mobility and joint prep  
* **PREP Block:** Velocity-based pattern rehearsal; increasing complexity  
* **WORK-A/B/C Blocks:** Strength, power, speed, elasticity (E1–E4 tiers per block phase); sport-specific conditioning; HS max 80, Elite max 100 plyo contacts/session  
* **CLEAR Block:** Full parasympathetic reset; post-exertion breathing protocols  
* **Constraints (Two-Layer System):**
  * **Absolute ceilings:** Youth 13-17: 120/session, 240/week; Adult: 140/session, 280/week
  * **Seasonal operating ranges:** Must program within season-appropriate weekly targets
  * **Tier 3 limit:** Youth 13-17 ≤40% of session contacts for E3/E4 work
  * **F-V Bias:** Youth 13-16 = BALANCED only; Youth 17 = FORCE_BIASED only (60/40, off-season/pre-season); Adult = all types (off-season/pre-season), BALANCED in-season/post-season
  * **Gate 7 Validation (NEW):** Weekly program distribution must match F-V bias targets (±10% tolerance)
  * **Critical:** IN_SEASON_TIER_1 uses 60-100/week for Youth 13-17, not 240/week

## **R2P (Post-Injury)**

* **PRIME Block:** Careful joint mobilization; pain-free ROM assessment  
* **PREP Block:** Constraints-led; compensation pattern detection  
* **WORK-A/B Blocks:** Pain-free ROM is primary metric; graded load exposure; tissue work integration  
* **CLEAR Block:** Extended recovery breathing; tissue quality emphasis; 24-hour post-session check-in  
* **Constraints:** Stage-specific contraindications; no R2P Stage 1 plyos; progression gates before dynamic load; **F-V Bias = BALANCED only (no override)**

## **Mobility Lab (Adults/Athletes)**

* **PRIME Block:** Tissue quality (hands-on for athletes); joint prep  
* **PREP Block:** Corrective pattern emphasis; movement literacy  
* **WORK-A/B Blocks:** Durability focus; removed axial loading where risky; emphasis on leaving feeling better than arriving  
* **CLEAR Block:** Extended breathing; soft-tissue finish; parasympathetic priority  
* **Constraints:** No high-intensity running; no failure-to-fatigue training; low-to-moderate RPE 3–4; **F-V Bias = BALANCED only**

---

## **3.3 Appendix J Hard "Never" Rules (Absolute Violations in BA)**

These rules are non-negotiable and apply across all populations and services. Violating any of these is a **DENY** and must trigger escalation:

## **Youth (8–12) Violations**

* **High-Depth Shock/Depth Jumps (18–45 cm)**  
  Rationale: Youth CNS and tendon structure not developed for stretch-shortening cycle. Attempting forces crumple mechanics (valgus collapse, excessive flexion)  
  Allowed Alternative: Snap-downs, Drop Squats, low-box Pogo Stiffness

* **Tier 3 Plyometrics (E3-E4)**  
  Rationale: Youth 8-12 CNS and tendon maturity insufficient for high-shock work  
  Hard Block: E3-E4 (Tier 3) forbidden for ages 8-12 unless Director override. E1-E2 (Tier 1-2) allowed

* **Maximal Loading on Dysfunction**  
  Rationale: Never load a red-light joint (pain 2–10/10, instability, compensation)  
  Enforcement: Movement quality gate must pass before any load added

## **All Populations Violations**

* **Failure Training on Neural Lifts**  
  Lifts: Cleans, Snatches, all Plyometrics  
  Rationale: Sacrificing spinal position or landing mechanics for extra reps creates CNS fatigue and injury risk  
  Enforcement: RPE or RIR cap; stop before form breakdown

* **Ignoring Pain 2–10/10**  
  Action: Immediate pattern regression or session stop (Codex §8.2 Stop Rule)  
  Enforcement: Any athlete/parent/coach can call Stop if safety risk observed

* **Progression Tier Bypass**  
  Rationale: Earned Progression rule (Codex §1.2); advancement must be demonstrated, not assumed  
  Enforcement: POSITRON denies intent; auto-regress to legal exercise

* **Exceeding Weekly Pattern Quotas**  
  Rationale: SAID principle; overloading one pattern creates imbalance and injury risk  
  Enforcement: AETHER manifest stores weekly quotas per sport/population; Block Selector enforces; POSITRON denies overages

* **Exceeding Sprint & Running Volume**  
  Rationale: Appendix J Law 3 caps sprint and high-speed running exposure  
  Enforcement: Sprint ceiling per population per week (documented in MesoMacro)

---

## **3.4 Session Assembly Checklist (BridgeAthletic Build)**

Before any BA workout is built, confirm:

* **Service Line is Legal:** Is this client in Youth, SP, R2P, ERL, or Mobility? (No custom memberships)  
* **Program Block is Legal:** Is this BA Program from the MesoMacro v1.0.1 template folder? (No custom programs outside templates)  
* **Chassis Present:** Does the BA workout include PRIME, PREP, WORK-A, WORK-B, WORK-C, CLEAR blocks in the prescribed time ranges?  
* **Sub-Blocks Legal:** Are WORK sub-blocks only organizing, not adding extra volume beyond block caps?  
* **Population Overlays Applied:** Are constraints specific to this population (age, sport, injury status) respected?  
* **Exercise List is Legal:** Are all exercises in the BA exercise library and tagged with AETHER-compliant node, pattern, difficulty tags?  
* **Load is Legal:** Do all exercises respect Load Standards band ceilings for this population (via BA load assignment feature)?  
* **Plyometric Contacts Logged:** If plyo work, are contacts tracked against weekly ceiling (Appendix J Law 1) using BA tracking?  
* **F-V Bias Profile Set (NEW):** Is `fv_bias_profile` explicitly set in athlete profile (BALANCED, FORCE_BIASED, or VELOCITY_BIASED)?  
* **F-V Bias Legal (NEW):** Does the bias match the population/season rules (e.g., Youth ≤16 = BALANCED only)?  
* **Red Flags Checked:** Are there any pain, stress, or medical red flags that should trigger regression or escalation (Appendix J Law 6)?  
* **Breathing Sections Included:** Is CLEAR block included with parasympathetic breathing protocols?  
* **Gate 7 Validation (NEW):** If F-V bias is set, does weekly program distribution match targets (≤10% variance)?  
* **POSITRON Approval:** Does this session pass POSITRON enforcement (intent validation, clause binding, red-flag detection)?

**Default:** If any item above is unclear or missing data, **DEFAULT-DENY** and escalate to coach/Owner rather than guessing.

---

# **Section 4: Program Selection & Blocks (BridgeAthletic Implementation)**

## **4.1 What is a Block? (EFL Macro Block vs BA Workout Block)**

**EFL "Block" (MesoMacro):** A locked, pre-designed training phase of 4–16 weeks that defines duration, service line, phase, sport/goal, gates, and laws. These are **BA Programs** (top-level templates).

**BA "Block" (Workout Component):** Components inside a BA workout (PRIME, PREP, WORK-A, etc.). These are **BA Blocks** within workouts.

**Critical Rule:** All EFL macro blocks come from **MesoMacro Manifest v1.0.1 only**. Coaches and AI **cannot design custom BA Programs** outside these templates. The macro is the law.

---

## **4.2 Legal BA Programs (MesoMacro v1.0.1 Templates)**

In BridgeAthletic, create a **"Legal EFL Templates" folder**. Inside, create one BA **Program** per block tag:

### **Youth Lab Programs**

| BA Program Name | Duration | Focus | Gates | BA Tags |
| ----- | ----- | ----- | ----- | ----- |
| YLGENFND8WKGENERAL | 8 weeks | General athletic foundations | Movement quality pass | Service:Youth, Phase:Foundation, Population:8-12 |
| YLSPORTSPEC8WKSOCCER | 8 weeks | Soccer-specific prep | Footwork quality gate | Service:Youth, Phase:Sport-Specific, Sport:Soccer |
| YLSPORTSPEC8WKBASKETBALL | 8 weeks | Basketball-specific; vertical/multidirectional | Landing mechanics pass | Service:Youth, Phase:Sport-Specific, Sport:Basketball |

**Youth Program Rules in BA:**
* All Youth programs are C and D nodes only (no elasticity)
* Max 50 plyometric contacts per session (tracked via BA exercise parameters)
* No depth jumps 18–45 cm (exclude from exercise library for Youth)
* **F-V Bias = BALANCED only (enforced)**

### **SP Performance Programs**

| BA Program Name | Duration | Focus | Gates | BA Tags | F-V Bias |
| ----- | ----- | ----- | ----- | ----- | ----- |
| SPOFFDEV16WKHSBASKETBALL | 16 weeks | Off-season development | Bilateral squat benchmark; landing quality | Service:SP, Phase:Off-Season, Sport:Basketball | ⚠️ CONDITIONAL (Youth=BALANCED, Y17=FORCE 60/40, Adult=all) |
| SPOFFDEV16WKHSSOCCER | 16 weeks | Off-season; multidirectional | COD quality gate | Service:SP, Phase:Off-Season, Sport:Soccer | ⚠️ CONDITIONAL |
| SPPREPGAME8WKHSBASKETBALL | 8 weeks | Pre-season prep | Maintain strength gate | Service:SP, Phase:Pre-Season, Sport:Basketball | ⚠️ CONDITIONAL |
| SPINSEASON6WKHSBASKETBALL | 6 weeks | In-season maintenance | Weekly readiness check | Service:SP, Phase:In-Season, Sport:Basketball | ❌ BALANCED ONLY |
| SPPOSTSEASON4WKHSBASKETBALL | 4 weeks | Post-season deload | Soreness + fatigue assessment | Service:SP, Phase:Post-Season, Sport:Basketball | ❌ BALANCED ONLY |
| SPTAPER2WKHSBASKETBALL | 2 weeks | Championship taper | Final movement quality check | Service:SP, Phase:Taper, Sport:Basketball | ❌ BALANCED ONLY |

**SP Performance Program Rules in BA:**
* Formal node progression: E1 → E2 → E3 → E1 (Phase tags in BA)
* HS athletes max 80 plyo contacts/session; Elite max 100 (tracked via BA)
* Progression gates must be passed (documented in BA athlete notes/medical forms)
* **F-V Bias assessment required before off-season/pre-season assignment** (CMJ profiling, squat 1RM ratio, or F-V slope testing per Governance v4.1 Section 8)

### **R2P Programs**

| BA Program Name | Duration | Focus | Gates | BA Tags | F-V Bias |
| ----- | ----- | ----- | ----- | ----- | ----- |
| R2PSTAGE1REACTIVATION4WK | 4 weeks | Reactivation; pain-free ROM | Pain-free ROM gate (0–1/10) | Service:R2P, Phase:Stage1, Medical:PT-Clearance | ❌ BALANCED ONLY |
| R2PSTAGE2PROGRESSLOAD6WK | 6 weeks | Progressive loading | Bilateral pattern strength gate | Service:R2P, Phase:Stage2 | ❌ BALANCED ONLY |
| R2PSTAGE3SPORTINTEGRATION8WK | 8 weeks | Sport-specific exposure | Landing quality gate; plyometric tolerance | Service:R2P, Phase:Stage3 | ❌ BALANCED ONLY |
| R2PSTAGE4FULLRETURN4WK | 4 weeks | Full return to sport | Clearance from PT/medical; coach sign-off | Service:R2P, Phase:Stage4 | ❌ BALANCED ONLY |

**R2P Program Rules in BA:**
* All R2P programs include manual therapy (tracked as separate BA session or notes)
* Dual Credential Coach (LMT + performance cert) required (coach profile tag in BA)
* Pain-free ROM is primary metric (pain tracking in BA daily logs)
* No R2P Stage 1 plyometrics (hard block; exclude plyo exercises from library for Stage1)
* **F-V Bias = BALANCED only (medical priority overrides performance optimization, no override possible)**

### **Mobility Lab Programs**

| BA Program Name | Duration | Focus | Gates | BA Tags | F-V Bias |
| ----- | ----- | ----- | ----- | ----- | ----- |
| ADULTSTRGENFND8WKGENERAL | 8 weeks | General adult strength + mobility | Movement quality pass | Service:Mobility, Phase:Foundation, Population:Adult | ❌ BALANCED ONLY |
| ATHLETEMOBILITY4WKGENERAL | 4 weeks | Athlete mobility recovery | Mobility ROM gate | Service:Mobility, Phase:Recovery, Population:Athlete | ❌ BALANCED ONLY |
| ADULTCORRECTIVE8WKPOSTURAL | 8 weeks | Postural correction | Pain reduction gate (↓ 2–3 VAS) | Service:Mobility, Phase:Corrective, Population:Adult | ❌ BALANCED ONLY |

**Mobility Program Rules in BA:**
* No high-intensity running exercises in library for these programs
* Low-to-Moderate RPE (3–4/10) enforced via BA load assignment
* Emphasis on leaving feeling better (BA daily readiness survey)
* **F-V Bias = BALANCED only (no bias targeting)**

---

## **4.3 How to Select a Legal BA Program (Block Selector Logic)**

When a new athlete enters EFL or advances phases, use this deterministic flow in BridgeAthletic:

### **Step 1: Confirm Service Line in BA**

Ask:
* Is the client ages 8–12 seeking general athletic development? → **Youth Lab** (BA Program filter: Service:Youth)  
* Is the client ages 13+ seeking sport performance? → **SP Performance** (BA Program filter: Service:SP)  
* Is the client recovering from injury? → **R2P** (BA Program filter: Service:R2P)  
* Is the client seeking general mobility/durability? → **Mobility Lab** (BA Program filter: Service:Mobility)

**If service line is ambiguous**, default to **Discovery Call** (Codex §7.1) to screen for guardrails.

### **Step 2: Determine Phase & Context in BA**

Gather:
* **Age & sport** (if applicable)  
* **Injury status** (none, recent, chronic, post-PT)  
* **Season** (off-season, pre-season, in-season, post-season, tournament)  
* **Stress/readiness** (high game load, competition week, recovery week)  
* **Medical clearance** (if R2P, confirmed PT discharge?)  
* **F-V Bias Assessment (NEW):** For SP Performance off-season/pre-season, assess via CMJ profiling, squat 1RM ratio, or F-V slope testing (see Section 5.11)

### **Step 3: Map to Legal BA Program**

Using BA's **Library filter** by Service, Phase, Sport:

**Example 1:** 14-year-old basketball player, off-season, no injury history.  
→ Service: SP Performance  
→ Phase: Off-Season  
→ Sport: Basketball  
→ F-V Bias Assessment: Squat 1.3x BW, RSI 2.0 → FORCE_BIASED indicated  
→ BA Program: **SPOFFDEV16WKHSBASKETBALL** (set fv_bias_profile = FORCE_BIASED in athlete profile, 60/40 max because Youth 17... wait, they're 14, so BALANCED enforced)  
→ **Corrected:** BA Program = **SPOFFDEV16WKHSBASKETBALL** (fv_bias_profile = BALANCED enforced)

**Example 2:** 10-year-old soccer player, entering EFL for first time.  
→ Service: Youth Lab  
→ Phase: Foundation  
→ F-V Bias: BALANCED (enforced)  
→ BA Program: **YLGENFND8WKGENERAL**

**Example 3:** 18-year-old off-season, basketball, no injury.  
→ Service: SP Performance  
→ Phase: Off-Season  
→ F-V Bias Assessment: Squat 2.2x BW, RSI 1.2 → VELOCITY_BIASED indicated  
→ BA Program: **SPOFFDEV16WKHSBASKETBALL** (set fv_bias_profile = VELOCITY_BIASED in athlete profile)

**Example 4:** 16-year-old post-ACL, 12 weeks out, PT discharge cleared.  
→ Service: R2P  
→ Phase: Stage 2  
→ F-V Bias: BALANCED (enforced, medical priority)  
→ BA Program: **R2PSTAGE2PROGRESSLOAD6WK**

### **Step 4: POSITRON Enforcement Before BA Assignment**

Before assigning the BA Program, the system validates:

1. **Intent:** Is `assignProgram` a legal intent? (Yes, per intentlibrary.json)  
2. **Athlete Eligibility:** Does athlete's age, population, injury status match the program's BA tags? (AETHER checks)  
3. **Gate Readiness:** Are all prerequisite gates documented as passed in BA athlete notes/medical forms? (MesoMacro gate history)  
4. **F-V Bias Legality (NEW):** Does athlete's fv_bias_profile comply with population/season rules? (Governance v4.1 Section 2.8 check)  
5. **Conflict Check:** Any active red flags (pain 2–10/10, medical holds, stress overload) that prevent program entry? (THESIS scans BA daily logs)  
6. **Load Compatibility:** Do athlete's current metrics (stress, sleep, readiness from BA surveys) align with program's CNS demand? (GATE + THESIS check)

**Outcome:**
* **APPROVED:** Assign BA Program to athlete; they see it in their BA app. Set fv_bias_profile in athlete profile if bias-targeted program
* **DENIED:** Red flag or gate failure; system suggests prerequisite program or escalates to coach
* **ESCALATED:** Ambiguous or high-risk scenario; routed to COUNCIL for human review

---

## **4.4 Progression Gates in BridgeAthletic**

Each BA Program has **entry gates** and **exit gates**. Athletes must pass exit gates to advance to next BA Program.

### **Gate Tracking in BA:**

* **Entry Gate:** Documented in BA athlete profile → Medical Forms or Coach Notes
* **Mid-Block Gates:** Weeks 4, 8, 12 → BA Daily Readiness Survey + Coach Assessment notes
* **Exit Gate:** Week final → BA assessment form (movement quality, strength benchmarks) + Coach sign-off

### **BA Workflow Examples:**

**Youth Lab (8-week YLGENFND8WKGENERAL):**
* **Entry Gate:** Initial movement quality screen (landing, squat, hinge) → BA Medical/Assessment form
* **Mid-Gate (Week 4):** Landing mechanics check → video upload to BA, coach notes
* **Exit Gate (Week 8):** Landing mechanics pass → coach sign-off in BA notes; if pass, repeat YLGENFND8WKGENERAL or advance to sport-specific program

**SP Performance (16-week SPOFFDEV16WKHSBASKETBALL):**
* **Entry Gate:** Medical clearance; bilateral squat benchmark (1.0x BW x5) → BA Medical/Assessment form; **F-V Bias Assessment (CMJ, squat ratio, RSI)** documented
* **Mid-Gates (Weeks 4, 8, 12):** Strength progression check; movement quality reassess → BA Daily Readiness + Coach notes
* **Exit Gate (Week 16):** Bilateral + unilateral strength pass; landing quality; plyometric tolerance; CNS readiness; **F-V Bias Compliance Check (Gate 7)** → BA assessment form + coach sign-off
* **Advancement:** If pass → assign SPPREPGAME8WKHSBASKETBALL. If regress → reassign current block phase

---

## **4.5 F-V Bias & Block Selection (NEW)**

### **When Does Bias Get Set?**

**Timing:**
- **For SP Performance off-season/pre-season programs:** Before program assignment
- **For all other services:** Set to BALANCED (enforced, no override)
- **For seasonal transitions:** Re-enforce BALANCED if moving into in-season/post-season (override athlete's current bias)

### **Who Assesses the Bias?**

- **Coach** with movement quality data (CMJ, squat 1RM, F-V slope testing, or documented rationale)
- **AI can recommend** but must show reasoning (e.g., "Based on CMJ height 72cm and Squat 1.6x BW, BALANCED profile detected")

### **How to Set Bias in BA:**

1. In **Athlete Profile** → **Custom Fields** (or coach notes section)
2. Add field: `fv_bias_profile` with value: `BALANCED`, `FORCE_BIASED`, or `VELOCITY_BIASED`
3. Document field: `fv_bias_rationale` with assessment data or reason
4. Document field: `fv_bias_assessment_date` (e.g., "2025-12-20")
5. System validates bias against athlete's population/season on program assignment

### **What Happens if Bias is Missing?**

- **Default:** BALANCED (safe default)
- **In BA:** When athlete is assigned to a bias-targeted program without bias set, system prompts coach: "F-V Bias Assessment Required - Please set fv_bias_profile before program assignment"

### **Bias Legality Matrix (Quick Reference)**

| Population | Off-Season / Pre-Season | In-Season / Post-Season |
|---|---|---|
| Youth ≤16 | BALANCED only | BALANCED only |
| Youth 17 Advanced | FORCE_BIASED (60/40) or BALANCED | BALANCED only |
| Adult (18+) | All types (FORCE, VELOCITY, BALANCED) | BALANCED only |
| R2P (all stages) | BALANCED only | BALANCED only |

---

# **Section 5: Exercise Selection & Load Standards (AETHER + Gate 7)**

## **5.1 – 5.10 (Previous Content Intact)**

[All previous sections 5.1-5.10 remain unchanged from v0.4.0 — contact counting, sprint rules, E-node mapping, session assembly, etc.]

---

## **5.11 F-V Bias Coaching Decision Tree (NEW in v0.5.0)**

**When should you select a specific F-V bias for your athlete?**

This decision tree is binding for all SP Performance off-season/pre-season assignments. All other services = BALANCED (no override).

### **Step 1: Is your athlete Youth 16 or under?**
- **YES** → USE BALANCED (enforced by system, no override, hard block)
- **NO** → Continue to Step 2

### **Step 2: Is your athlete Youth 17 Advanced (2+ years training age)?**
- **YES** → Continue to Step 2A (conditional FORCE_BIASED only)
- **NO** → Continue to Step 3

### **Step 2A: Can you document training age ≥2 years AND tissue health screening passed?**
- **YES** → FORCE_BIASED is conditional option (60/40 max, Director approval, off-season/pre-season only)
- **NO** → USE BALANCED

### **Step 3: Is current season OFF_SEASON or PRE_SEASON?**
- **YES** → Continue to Step 4
- **NO** → USE BALANCED (in-season maintenance priority, bias not allowed)

### **Step 4: Do you have F-V diagnostic data (CMJ, squat 1RM, force plate, or F-V slope)?**
- **YES** → Continue to Step 5 (use testing data)
- **NO** → USE BALANCED (safe default without data)

### **Step 5: What does your diagnostic data indicate?**

| Finding | Indicator | Recommendation |
|---------|-----------|-----------------|
| **Force-Deficit** | Squat <1.5x BW, RSI >1.8, low peak force (<2.0x BW) | **FORCE_BIASED** — improve max strength |
| **Velocity-Deficit** | Squat >2.0x BW, RSI <1.5, high peak force but slow RFD | **VELOCITY_BIASED** — improve explosiveness |
| **Balanced** | Squat 1.5-2.0x BW, RSI 1.5-1.8, proportional metrics | **BALANCED** — general development |
| **Unclear / Conflicting** | Mixed indicators (e.g., high squat but high RSI) | **BALANCED** — default when uncertain |

### **Step 6: Document Your Rationale**

**Before assigning FORCE_BIASED or VELOCITY_BIASED, document:**

1. **Athlete Profile:** Age, training age, sport/position
2. **Diagnostic Data:** CMJ height (cm), RSI, squat 1RM (and body weight ratio), peak force (N), RFD (if available)
3. **Bias Selection:** Why this bias? (deficit observed, sport-specific need, test results indicate)
4. **Testing Date:** When was athlete assessed?
5. **Approval Status:** Coach approval logged? Director approval if required? (for Youth 17)

**Implementation in BA:**
```
fv_bias_profile: FORCE_BIASED
fv_bias_rationale: "Squat 1.4x BW, RSI 2.1, peak force 1680N - high reactivity, low absolute strength. Force-deficit profile. Sport: Basketball (guard). Needs max strength emphasis in off-season."
diagnostic_data:
  cmj_height_cm: 68
  rsi: 2.1
  squat_bw_ratio: 1.4
  peak_force_n: 1680
  rfd: "not tested"
  assessment_date: 2025-12-20
  assessment_type: CMJ_PROFILING + 1RM_TEST
fv_bias_restrictions:
  youth_16_under: BALANCED enforced, no override
  youth_17: FORCE_BIASED max 60/40, Director approval required
  adult_elite: All bias types allowed off-season, BALANCED in-season
  in_season: BALANCED enforced
approvals:
  coach_approved: true
  director_approval_required: false
  block_duration_weeks: 16
  block_season: Off_Season
```

---

# **Section 6: Red Flags & Readiness Adjustments**

## **6.1 – 6.6 (Previous Content Intact)**

[All previous sections 6.1-6.6 remain unchanged from v0.4.0]

---

## **6.7 Gate 7 F-V Bias Compliance Red Flags (NEW)**

**When:** After session publish, before athlete assignment (weekly validation)

**Trigger:** Weekly program distribution deviates from F-V bias targets

### **RED FLAG: Gate 7 YELLOW (Program Drift)**

**Threshold:** Program distribution 10-20% off bias targets  
**Status:** ⚠️ CAUTION - Program functional but off-target  
**Action:**
- Flag for coach review
- Recommend adjustments for next week
- Document in BA notes: "Gate 7 YELLOW - program 15% off FORCE_BIASED targets. Adjust week 2 to increase Band3-4 volume."
- Do NOT prevent athlete assignment (program still legal)

**Example:**
- **Bias Target:** FORCE_BIASED (70% Band2-4, 30% Band0-1)
- **Actual Program:** 65% Band2-4, 35% Band0-1
- **Variance:** 5% (within GREEN ≤10%)
- **Action:** PASS GREEN, no flag

### **RED FLAG: Gate 7 RED (Program Violation)**

**Threshold:** Program distribution >20% off bias targets OR safety gate violation  
**Status:** ❌ ILLEGAL - Program quarantined  
**Action:**
- **DO NOT ASSIGN** program to athlete
- Escalate to coach: "Gate 7 RED - program 28% off FORCE_BIASED targets. Cannot assign. Regenerate with stricter bias constraints or switch to BALANCED profile."
- Coach must rebuild program or change bias profile to BALANCED
- Document in BA notes with reason

**Example:**
- **Bias Target:** FORCE_BIASED (70% Band2-4, 30% Band0-1)
- **Actual Program:** 55% Band2-4, 45% Band0-1
- **Variance:** 15% (exceeds GREEN ≤10%)
- **Action:** YELLOW - flag for review OR RED if variance >20%

### **RED FLAG: Bias Profile Mismatch**

**Condition:** Athlete assigned to season that conflicts with bias profile

**Example 1:**
- **Athlete fv_bias_profile:** FORCE_BIASED
- **Season:** IN_SEASON_TIER_1
- **Conflict:** In-season requires BALANCED only
- **Action:** System overrides bias to BALANCED, flags coach: "In-season transition - bias reset to BALANCED per Load Standards v2.2.0"

**Example 2:**
- **Athlete fv_bias_profile:** VELOCITY_BIASED
- **Population:** Youth 16
- **Conflict:** Youth ≤16 allows BALANCED only
- **Action:** System denies program assignment, escalates: "Bias profile VELOCITY_BIASED not legal for Youth 16. Only BALANCED allowed."

### **How to Avoid Gate 7 Red Flags:**

1. **Build programs with bias in mind:**
   - FORCE_BIASED: Emphasize Band3-4 exercises (70% of volume)
   - VELOCITY_BIASED: Emphasize Band0-2 exercises (70% of volume)
   - BALANCED: Mix across all bands (50/50 spectrum)

2. **Use BA's band distribution tracker:**
   - When building WORK blocks, BA should show real-time band distribution %
   - Aim to keep within ±10% of bias targets

3. **Log weekly:**
   - After each week, coach documents: "Band distribution: Band0 15%, Band1 25%, Band2 30%, Band3 20%, Band4 10%. Target BALANCED - PASS GREEN"

---

# **Section 7: Escalation & Change Control**

[All previous sections 7.1-7.4 remain unchanged from v0.4.0]

---

# **APPENDIX F: F-V Bias Profiles Quick Reference (NEW)**

**Source:** Load Standards v2.2.0 Appendix C

---

## **FORCE_BIASED (Shift athlete rightward on F-V curve)**

**Target Athlete Profile:**
- Squat <1.5x BW
- RSI >1.8 (high reactivity, low force)
- Peak force <2.0x BW
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

## **VELOCITY_BIASED (Shift athlete leftward on F-V curve)**

**Target Athlete Profile:**
- Squat >2.0x BW
- RSI <1.5 (low reactivity, high force)
- Peak force >2.5x BW
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

## **BALANCED (General athletic development)**

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
- E0-E4: Equal emphasis, no specific ratio targets

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

# **APPENDIX G: Gate 7 Validation Quick Reference (NEW)**

**Source:** Governance v4.1 Appendix D

### **When Does Gate 7 Run?**

- After session publish (before athlete assignment)
- Weekly program review (coach audit)
- Monthly compliance check (automated)

### **What Does Gate 7 Check?**

1. **Band Distribution:** Actual % vs target % for bias profile
2. **Plyo Distribution:** Actual % vs target % for bias profile
3. **Critical Ratio:** Force:Velocity split (70:30 or 30:70 depending on bias)
4. **Safety Gates:** All v2.1.4 gates still pass (band ceilings, contact limits, etc.)

### **Validation Logic:**

```
IF athlete.fv_bias_profile IN [FORCE_BIASED, VELOCITY_BIASED]:
  
  Calculate actual band & plyo distribution from weekly program
  Compare to bias profile targets
  
  IF variance ≤ 10% AND critical_ratio >= 1.7 AND all safety gates PASS:
    Result: GREEN ✅
    Action: Approve program for assignment
    
  ELSE IF variance ≤ 20% AND all safety gates PASS:
    Result: YELLOW ⚠️
    Action: Flag for coach review, functional but off-target
    Recommendation: Adjust next week
    
  ELSE IF variance > 20% OR any safety gate FAILS:
    Result: RED ❌
    Action: QUARANTINE, do not assign
    Recommendation: Regenerate with bias constraints or switch to BALANCED

ELSE:
  Result: PASS (no distribution targets for BALANCED profile)
```

---

# **END EFL COACH & AI PLAYBOOK v0.5.0**

**Status:** PRODUCTION-READY  
**Effective Date:** January 1, 2026  
**Authority:** Load Standards v2.2.0 + Governance v4.1  
**All F-V Bias Integration Complete**

---

**Questions? Escalate to Owner: Austin Lawrence**

