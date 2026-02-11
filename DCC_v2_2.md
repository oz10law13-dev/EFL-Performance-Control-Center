---
Meta
Field: Value
Document ID: EFLCONTROLCENTERDAILYCONSTRAINEDCONJUGATEV22
Version: 2.2
Effective Date: 2026-01-25
Release Date: 2026-01-25
Owner: Elite Fitness Lab, Director of Performance Systems
Status: OPERATIONAL
Project Scope: Daily Constrained Conjugate DCC Control Center for all SP Performance service lines
Supersedes: DCC v2.1 (2026-01-18)
Classification: PRIMARY ARCHITECTURAL CONTROL CENTER
Major Changes v2.2: Session Duration Contract, Block Time Budget, PRIME Day-Role Binding, PRIME Anti-Repetition Rule, PRIME Scope Lock, Session Abort Rule
---

# TITLE: EFL Control Center — Daily Constrained Conjugate Model Master Spec v2.2

## PART I: AUTHORITY SCOPE

### 0. What This Document Is and Is Not — Core Identity

The EFL Control Center (DCC) — Daily Constrained Conjugate is the foundational architectural framework that governs all daily training sessions and microcycles across Elite Fitness Lab's SP Performance service line. It defines:

- **Band and Node ceilings** — load classification and density
- **E-Node elasticity tiers** — plyometric complexity progression
- **Readiness modifiers** — YELLOW/RED envelope downgrades
- **Contact policies** — exposure accounting and caps
- **Day-role archetypes** — A/B/C patterns and responsibilities
- **Training Routes** — execution governors for fatigue tolerance, density, and termination
- **Session economics** — timing, block budgets, and failure protocols (NEW v2.2)
- **Always-illegal behaviors** — drift-killer rules that prevent coaching interpretation
- **Evidence-based rationale** — the why behind each constraint

**The DCC is NOT:**
- A stage-specific protocol (that is R2P-ACL Wrapper territory)
- A sport-specific specialization block (that is Child Wrapper territory)
- An exercise library or selection system (that is EPA Exercise Progression Law territory)
- A weekly meso template (that is Block Doc territory)

---

### 1. Hard Authority Stack — Non-Negotiable Dependencies

If this Control Center conflicts with any upstream document, the upstream document wins. This Control Center tightens constraints, never loosens them.

**Authority Hierarchy:**
1. **EFL Governance v4.1** — top-level organizational law
2. **EFL Load Standards v2.2.0** — Band/Node ceilings, youth rules, R2P-specific overlay
3. **DCC Master Spec v2.2** — daily operationalization, timing, block budgets, readiness modifiers, training routes, session economics
4. **Child Wrappers** (Court Sport, R2P-ACL, etc.) — sport/stage-specific constraints
5. **Block Documents** — meso templates, phase structure, progressions

**Conflict Resolution Rule:**  
Always apply the most restrictive rule. If Load Standards says Band 2 max and a downstream Block Doc requests Band 3 → Band 2 wins. If Readiness is RED and a coach prefers GREEN progress → RED wins, forcing downgrade or medical route.

---

## PART II: DCC RULES 0–8

### 2. Band and Node Classification System — What They Are

**Bands** define load magnitude (how much weight/resistance).  
**Nodes** define movement density (how many contacts/reps per minute, complexity of task).

#### Band Load Classification

| Band | Load Magnitude | Typical Application | Youth Overlay |
|------|---|---|---|
| **Band 0** | Bodyweight, light activation | Mobility, tissue prep, nervous system | Same, no modification |
| **Band 1** | Light to moderate, 25–50% 1RM | Foundational strength, unilateral work, control | Same, no modification |
| **Band 2** | Moderate to heavy, 50–80% 1RM | Primary compound lifts, hypertrophy, power prep | 25% load cap for youth 13–15 |
| **Band 3** | Heavy to maximal, 80%+ 1RM | Strength consolidation, 1RM testing | Forbidden for youth 13–17 |

#### E-Node Elasticity Complexity Scale

| E-Node | Task Complexity | Typical Application | Depth/Landing Load | Youth 13–15 Ceiling | Youth 16–17 Ceiling | Adult Ceiling |
|---|---|---|---|---|---|---|
| **E0** | Isometric, controlled pause | Glute activation, eccentric loading | None | Allowed | Allowed | Allowed |
| **E1** | Single-contact landing, straight | Box step-down, single-leg balance | 6" drop | Allowed | Allowed | Allowed |
| **E2** | Reactive landing, bilateral | Box drop, bilateral jump | 6–12" drop | Allowed, max 2/week | Allowed | Allowed |
| **E3** | Reactive single-leg landing | Single-leg hop, lateral bound | 12–18" drop | Forbidden | Allowed, readiness GREEN | Allowed |
| **E4** | High-velocity, multi-directional | Depth jump 18"+, reactive COD | 18"+ drop | Forbidden | Forbidden | Restricted, explicit clearance only |

---

### 3. Daily Session Constraints — Band-Node-E-Node Envelope + Session Economics (UPDATED v2.2)

#### 3.1 Session Duration Contract (NEW v2.2)

**Core Rule:**  
**Athlete sessions must terminate between 50–60 minutes elapsed time, measured from the first PRIME drill to CLEAR completion.** If any block threatens to exceed its allocated time range, the coach must reduce volume or omit patterns **inside that block**. Session duration may not be extended beyond 60 minutes to "fit everything in."

**Containment Rule:**  
Sessions that overrun 60 minutes are **INVALID**. Reason code: `SESSION_DURATION_EXCEEDED`. The coach must restructure by reducing WORK volume, not by extending time.

---

#### 3.2 Block Time Budget (NEW v2.2)

All sessions in all Court Sport Foundation Projects must follow the **PRIME → PREP → WORK → CLEAR** structure with these **time ranges** (flexible within range, rigid across blocks):

| Block | Time Range | Purpose | RPE Cap |
|-------|---|---|---|
| **PRIME** | 8–10 min | Global warm-up, low-level elasticity (E0–E1 only), joint prep, tissue readiness | RPE ≤3 |
| **PREP** | 10–12 min | Pattern rehearsal at low load (Band 0–1), landing prep, stiffness priming | RPE ≤3 |
| **WORK** | 25–30 min | Main strength/plyo block, band and E-node progression per week, RPE peaks 4–7 (youth ≤4). **Minimum 24 min required for session validity.** | RPE peaks 4–7 |
| **CLEAR** | 5–8 min | Mobility, tissue work, trunk finishers, no added load beyond Band 0, parasympathetic activation | RPE ≤2 |

**Block Time Economics Rule:**  
Blocks may flex **within their time range** but may not exceed it. If PREP overruns to 15 minutes, WORK must compress or omit drills to stay within 25–30 min total. Sessions that violate block time budgets are **INVALID**.

**Containment Rule:**  
Sessions that skip phases, compress WORK below 24 minutes, or exceed youth RPE caps must be rejected or downgraded by the system. Sessions with WORK < 24 min are invalid. Reason code: `INSUFFICIENT_WORK_BLOCK`.

---

#### 3.3 The Pyramid Model — Band, Node, E-Node, Readiness Envelope

Each day occupies **ONE band ceiling** (Band 0–3).  
Within that band, **movement density varies** (Node 1–3).  
Within that day, **E-Node exposure varies** (E0–E4).  
**All are constrained by readiness state** (GREEN/YELLOW/RED).

**Training Route** determines execution economics within these boundaries.

---

### 4. Day-Role Archetypes and PRIME Binding (UPDATED v2.2)

#### 4.1 Day A — Strength Day (Bilateral, Vertical Jump, Capacity)

| Constraint | Rule |
|---|---|
| **Band ceiling** | Band 2–3 depends on training age, sport, prior LSI |
| **Node ceiling** | Node 2; Node 3 forbidden on strength days |
| **E-Node ceiling** | E0–E2 only; E3 forbidden on strength days |
| **Session contacts** | 20–40 contacts, avg 30 |
| **Pattern guarantee** | 5–8 compound movement blocks; accessory work must serve primary movement |
| **PRIME intent (NEW v2.2)** | Prepare tissues and joints for bilateral squat and vertical jump patterns; bias toward hip flexor, ankle, glute activation at E0–E1 |
| **Readiness GREEN** | Execute as planned |
| **Readiness YELLOW** | Reduce Band ceiling by 1 (Band 3→2, Band 2→1), reduce contact multiplier 0.8, hold pattern guarantees |
| **Readiness RED** | Collapse to Band 0, E0 only; force medical review or medical hold |

---

#### 4.2 Day B — Reactive/Plyo Day (Horizontal Power, Decel, Expression)

| Constraint | Rule |
|---|---|
| **Band ceiling** | Band 0–1; load is de-emphasized, elasticity is priority |
| **Node ceiling** | Node 1–2; Node 3 allowed only if readiness GREEN and training age ≥2y |
| **E-Node ceiling** | E1–E3; youth 13–15 E2 max; E4 restricted |
| **Session contacts** | 30–60 contacts, avg 45 |
| **Pattern guarantee** | 60% plyometric exposure, 40% strength/mobility balance; directional variety (vertical, horizontal, lateral) |
| **PRIME intent (NEW v2.2)** | Prepare tissues and joints for horizontal power and deceleration patterns; bias toward thoracic rotation, hamstring prep, hip extension at E0–E1 |
| **Readiness GREEN** | Execute as planned |
| **Readiness YELLOW** | Reduce E-Node by 1 (E3→E2, E2→E1), reduce contact multiplier 0.8 (~20% reduction), increase rest between sets |
| **Readiness RED** | Collapse to E0 only; medical route mandatory |

---

#### 4.3 Day C — Skill/Sport-Prep Day (Unilateral, Decel, Integration)

| Constraint | Rule |
|---|---|
| **Band ceiling** | Band 0–1; load not the focus |
| **Node ceiling** | Node 2–3 allowed; high complexity acceptable if readiness GREEN |
| **E-Node ceiling** | E2–E3; youth 13–15 E2 max; sport-reactive OK if in-season |
| **Session contacts** | 40–80 contacts, avg 60; higher for sport prep |
| **Pattern guarantee** | Sport-specific pattern exposure; game-speed decisions mandatory; no new max-load introductions |
| **PRIME intent (NEW v2.2)** | Prepare tissues and joints for unilateral and deceleration patterns; bias toward single-leg balance, foot/ankle stability, hip internal rotation at E0–E1 |
| **Readiness GREEN** | Execute as planned |
| **Readiness YELLOW** | Reduce E-Node by 1, reduce pattern complexity (slow decision-making, increase spacing), reduce contact multiplier 0.8 |
| **Readiness RED** | Fundamentals-only mode (ball handling, footwork, basic decision-making); no contact exposure |

---

### 5. PRIME Selection and Binding (NEW v2.2)

#### 5.1 PRIME Occurs After Day Role Is Set

**Core Rule:**  
PRIME content is selected **only after Day Role (A/B/C) is declared**. PRIME must **bias toward the dominant WORK patterns** for that day's role.

**PRIME Selection Logic:**
1. **Day Role determines WORK focus** (e.g., Day A = bilateral squat + vertical jump; Day B = horizontal power + decel; Day C = unilateral + sport-specific)
2. **PRIME is selected to prepare WORK patterns**, not as a standalone block
3. **PRIME must vary** across Day A, Day B, and Day C—no verbatim repetition

#### 5.2 PRIME Intent and Scope (NEW v2.2)

**What PRIME Is:**
- Movement preparation for WORK demands (not standalone activation or conditioning)
- Joint preparation for primary patterns in WORK block
- Low-level tissue readiness (E0–E1 elasticity only, no fatiguing work)
- 8–10 minute block at RPE ≤3

**What PRIME Is NOT (Always-Illegal):**
- Activation circuits or "core work" dosed at meaningful volume
- Conditioning sequences or repeated efforts that drive fatigue
- Elastic contacts that count toward plyo budgets
- Formal breathing protocols (those belong in CLEAR)
- Any drill that raises heart rate or causes muscular fatigue

**Legality Test for PRIME Content:**  
If it raises heart rate, causes fatigue, or is dosed at meaningful volume → **illegal PRIME content**.

#### 5.3 PRIME Anti-Repetition Rule (NEW v2.2)

**Core Rule:**  
**PRIME may not be identical across consecutive sessions.** Exercise rotation is allowed; intent repetition is forbidden.

**Example Violation:**
- Day A Session 1: Hip flexor mob + glute bridges + ankle mob + light pogos
- Day A Session 2: **Identical PRIME** → `PRIME_REPETITION_VIOLATION`

**Example Compliant Rotation:**
- Day A Session 1: Hip flexor half-kneeling mob + glute bridges + ankle dorsiflexion wall mob + light pogos
- Day A Session 2: Couch stretch + single-leg glute bridge + lacrosse ball ankle work + light skips
- Day A Session 3: Deep lunge hold + clamshells + 90/90 ankle prep + light box steps

**Containment Rule:**  
If PRIME content is identical across more than two consecutive sessions, the system must raise `PRIME_REPETITION_WARNING` and flag for coach review.

---

### 6. Contact Accounting and Exposure Ledger — Mandatory (FROM v2.1, UNCHANGED)

#### 6.1 What Is a Contact?

A contact is any single instance of foot strike, landing, or propulsion during plyometric, reactive, or sport-specific movement.

| Example | Count |
|---|---|
| Single-leg hop | 1 contact per leg per hop |
| Double-leg jump landing | 1 contact |
| Reactive box drop landing | 1 contact |
| Lateral bound (right land, left land) | 2 contacts |
| Cutting maneuver | 1 contact per directional change |
| **Non-contacts:** | |
| Band-resisted strength work | Counts as Band load, not contacts |
| Mobility, stretching, walking, isometric holds | No contact |
| Non-reactive balance work | No contact |

---

#### 6.2 Mandatory Contact Tracking

**Session Type** | **Typical Range** | **Mandatory Check**
---|---|---
Day A Strength | 20–40 | Do not exceed weekly cap
Day B Reactive/Plyo | 30–60 | Do not exceed weekly cap
Day C Skill/Sport | 40–80 | Do not exceed weekly cap; adjust if in-season

---

#### 6.3 Weekly Contact Caps — Youth Off-Season, GREEN Readiness

| Age/Population | Off-Season Cap | In-Season Cap | Notes |
|---|---|---|---|
| Youth 13–15 | 100 contacts/week | 80 contacts/week | Reduced in-season to preserve recovery |
| Youth 16–17 | 130 contacts/week | 100 contacts/week | Advanced athletes still protected |
| Adult 18+ | 180 contacts/week | 150 contacts/week | Higher capacity still monitored |

---

### 7. Readiness Classification System — Updated v2.0.1 (UNCHANGED)

#### 7.1 Readiness States and Modifiers

| Readiness State | Pain (0–10) | Swelling | Movement Quality | Session Status |
|---|---|---|---|---|
| **GREEN** | 0–2, no swelling | None | Symmetric, no compensation | Execute full envelope |
| **YELLOW** | 3–4, mild | Slight, not increasing | Slight asymmetry, mild compensation | Downgrade 0.8 multiplier |
| **RED** | 5–10 or effusion | Moderate or increasing | Significant asymmetry, giving way, major compensation | Collapse to Band 0, E0 only; medical hold |

---

#### 7.2 Readiness Modifier Application (FROM v2.1)

| Readiness State | Band Adjustment | E-Node Adjustment | Contact Adjustment | Session Status |
|---|---|---|---|---|
| **GREEN** | Full ceiling | Full ceiling | 100% of weekly cap | Execute |
| **YELLOW** | −1 (Band 3→2, Band 2→1) | −1 (E3→E2, E2→E1) | 80% of weekly cap (0.8× multiplier) | Downgrade |
| **RED** | Band 0–1 only | E0 only | 0%, no contacts | Hold, medical route |

**Contact Multiplier Formula:**  
Session contacts = base contacts × readiness modifier  
Example: 40 contact session, YELLOW readiness → 40 × 0.8 = 32 contacts max

---

#### 7.3 Accepted Readiness Inputs — Context Only (FROM v2.0.1)

**Primary Triggers (Authority):**
- Pain (0–10 scale)
- Swelling/effusion presence
- Movement quality (symmetry, compensation)

**Secondary Context (Supportive, do NOT override core decision):**
- Session RPE / sRPE
- Jump-based metrics (CMJ, RSI)
- External practice load (proxy for fatigue)

**Hard Rule:**  
Pain, swelling, and movement quality remain **authoritative**. Additional inputs provide context but do not override core readiness decision matrix.

---

### 8. Always-Illegal Behaviors — Drift-Killer Rules (UPDATED v2.2)

**No Exceptions. No Coach Override. No Interpretation.**

| Behavior | Why It's Illegal | Consequence |
|---|---|---|
| **Band 3 + Node 3 simultaneously** | Overload fatigue injury | Session illegal; downgrade to Band 2/Node 2 |
| **E4 in youth 13–17** | Skeletal immaturity cannot absorb load | Session illegal; collapse to E3 max |
| **Contact cap exceeded** | Cumulative injury risk | Session illegal; cap at population max |
| **Readiness RED + full load** | Ignores inflammation, cartilage damage | Session illegal; force medical route |
| **Hardstop ignored** | Symptom escalation → permanent injury | All training halted; medical review mandatory |
| **Day-role pattern broken** (e.g., Day A with 80% plyometric) | Violates structural guarantee | Session illegal; restructure day |
| **Stage authority overridden** | Objective gates exist; subjectivity fails | Session illegal; use computed stage |
| **Two hardstops in 14 days** | Pattern of escalation | Athlete locked to medical review; training blocked |
| **PRIME + activation/conditioning/breathing** (NEW v2.2) | PRIME is prep-only; no fatigue, no volumes, no recovery work | Session illegal; move drills to WORK or CLEAR |
| **PRIME identical across sessions** (NEW v2.2) | Boring, ineffective, drift-prone | Flag `PRIME_REPETITION_WARNING`; coach must rotate |
| **Session overruns 60 minutes** (NEW v2.2) | Blocks time budgets are inviolable | Session illegal; reduce WORK volume, not extend time |

---

## PART II-A: TRAINING ROUTES — EXECUTION GOVERNORS (FROM v2.1, UNCHANGED)

### 9. Training Routes System Definition — What Is a Training Route?

A **Training Route** is a DCC execution governor that determines:
- **How close to ceilings** work is driven (proximity to Band/Node/E-Node caps)
- **How fatigue is treated** (forbidden, tolerated, sought)
- **How density behaves** over time (static, progressive, regressive)
- **What ends the block** (output drop, quality loss, planned volume, time)

**Routes are orthogonal to:**
- Exercise legality (EPL governs ONE-AXIS-AT-A-TIME)
- Safety ceilings (Load Standards govern Band/Node/E-Node caps)
- Medical permission (R2P governs stage progression and hardstops)
- Day-role architecture (DCC Day A/B/C remain structural foundation)

**Key Principle:**  
Routes control **execution intensity**, not **safety boundaries**. Routes operate **inside** the safety envelope, never expanding it.

---

### 9.1 Route Intent-Output Matrix (FROM v2.1)

| Route | Intent | Output Expectation | Output Decay Allowed? |
|---|---|---|---|
| **Max Performance** | Absolute | Near-maximum output | Forbidden |
| **Submax Performance** | Maximum intent, capped output | 85–92% of max | Forbidden |
| **Capacity Accumulation** | Moderate | 70–80% of max | Allowed, bounded |
| **Regeneration** | Low | Smooth, effortless output | Forbidden |

**Critical Distinction:**  
Max Performance and Submax Performance both require **high intent**. The difference is **output cap**, not effort.

---

### 9.2 Route Fatigue Economics (FROM v2.1)

| Route | Fatigue Policy | Why |
|---|---|---|
| **Max Performance** | Zero tolerance | Output expression requires full neural capacity |
| **Submax Performance** | Zero tolerance | Quality preservation requires freshness |
| **Capacity Accumulation** | Bounded tolerance | Tissue adaptation requires progressive overload |
| **Regeneration** | Zero tolerance | Recovery requires parasympathetic dominance |

---

### 9.3 Route Density Behavior (FROM v2.1)

| Route | Density Behavior | Adjustment Direction |
|---|---|---|
| **Max Performance** | Minimal | Never increases; rest is priority |
| **Submax Performance** | Fixed | May decrease if quality degrades |
| **Capacity Accumulation** | Progressive | Planned increase over block |
| **Regeneration** | Minimal | Fixed; time-based, no progression |

**Rule:**  
Only **Capacity** is allowed to intentionally increase density over time.

---

### 9.4 Route Termination Logic (FROM v2.1)

| Route | Primary Termination | Secondary Termination |
|---|---|---|
| **Max Performance** | Output drop (velocity loss ≥5%, bar speed decay) | Time cap (prevent grinding) |
| **Submax Performance** | Quality loss (form breakdown, compensation) | Early stop if quality cannot be maintained |
| **Capacity Accumulation** | Planned volume completion | Time cap if volume cannot be achieved safely |
| **Regeneration** | Time-based planned duration | NA; no performance goal |

---

### 9.5 Route Day-Role Intensity Envelope (FROM v2.1)

| Route | Day A Strength | Day B Reactive/Plyo | Day C Skill/Sport |
|---|---|---|---|
| **Max Performance** | Near Band/Node ceilings, E2–E3 elastic focus | Forbidden | Forbidden |
| **Submax Performance** | Band 1–2, Node 1–2, E0–E2 controlled elastic | Zero-impact skill work only | Zero-impact skill work only |
| **Capacity Accumulation** | Band 0–1 foundational | Band 0–1, E0–E1 low elastic load | Forbidden |
| **Regeneration** | Band 0 mobility | Band 0 only, E0 activation | Skill acquisition, low chaos |

---

### 9.6 Route Readiness Adaptation (FROM v2.1)

| Route | GREEN | YELLOW | RED |
|---|---|---|---|
| **Max Performance** | Allowed | Forbidden | Forbidden |
| **Submax Performance** | Allowed | Reduced ceiling (Band −1, E-node −1) | Forbidden |
| **Capacity Accumulation** | Allowed | Reduced volume (0.8× contacts) | Forbidden |
| **Regeneration** | Allowed | Allowed | Allowed (preferred) |

---

### 9.7 Route Selection Decision Tree (FROM v2.1)

How DCC selects the route for today's session:

1. **Is R2P active?** YES → Restrict routes (Max forbidden, Capacity forbidden). NO → Continue.
2. **What day is it (A/B/C)?** Day A, B, C routes available. Day C: Regeneration preferred.
3. **What is readiness state?** GREEN: All routes available. YELLOW: Max forbidden; Submax/Capacity downgraded. RED: Only Regeneration allowed.
4. **Select highest-performance route allowed.** Apply route execution rules. Validate exercises with EPL. Generate session.

**Principle:**  
Performance is earned, not chosen.

---

### 9.8 Executive Lock-In — Training Routes (FROM v2.1)

DCC Training Routes define how training stress is expressed, not how much stress is allowed. By separating intent, fatigue tolerance, and termination logic, routes enable maximal and submaximal performance adaptations without violating:
- Safety ceilings (Load Standards)
- Exercise legality (EPL)
- Medical permission (R2P)
- Day-role architecture (DCC Day A/B/C)

Routes are execution governors, not permission granters. Routes operate inside the safety envelope—never expanding it.

---

## PART III: SESSION FAILURE AND ABORT PROTOCOLS (NEW v2.2)

### 10. Session Abort Rule — Single Valve (NEW v2.2)

#### 10.1 When Sessions Collapse

**Core Rule:**  
If any of the following occur during a session, the session **immediately collapses to CLEAR only**. No scoring. No thresholds. One valve.

| Trigger | Behavior |
|---|---|
| **Pain escalates beyond baseline** | 3+ points above athlete's normal pain level during session |
| **Coordination/movement quality degrades** | Visible valgus collapse, asymmetry, or compensation that cannot be restored with rest or exercise modification |
| **Athlete cannot meet quality standards** | Unable to execute prescribed movement pattern with form integrity after one rest period |
| **Coach observes safety red flag** | Giving way, sharp joint pain, acute swelling, persistent limp, or behavioral change (pain avoidance, fatigue signs) |

#### 10.2 Session Collapse Protocol

**Immediate Actions:**
1. Stop the current exercise or block.
2. Shift to CLEAR-only activities: mobility, easy stretching, parasympathetic activation, no added load.
3. Document why the session collapsed (trigger reason).
4. Do **not** resume WORK, even after rest.
5. Do **not** complete WORK volume on another day to "make up" the collapsed session.

**Session Structure After Collapse:**
- PRIME: Execute as planned (already complete or omit)
- PREP: Omit or reduce to light movement prep
- WORK: **Omitted entirely**
- CLEAR: Extended 10–15 min focus on downshift and recovery

**Recording and Routing:**
- Flag session as **COLLAPSED** in session log.
- Log trigger reason (e.g., pain escalation, coordination loss, valgus collapse).
- **Do not** re-attempt WORK block in next session automatically. Reassess readiness at next session.
- If collapse occurs two or more times in 5 days, flag for readiness re-evaluation or medical review.

#### 10.3 Containment Rule

Sessions that collapse to CLEAR are **VALID executions** of DCC protocol, not failures. The collapse rule prevents digging holes—attempting to push through degraded quality, pain, or movement compromise.

This is the **single safety valve** between "I'm tired" and "I'm injured."

---

## PART IV: EVIDENCE-BASED REASONING (FROM v2.1, REFRESHED)

### 11. Why Session Duration Is 50–60 Minutes (NEW v2.2 Rationale)

**The Problem:**
- Sessions with vague or open-ended length drift to 70–90 minutes.
- "Fitting everything in" creates silent volume accumulation.
- Coaches lose situational awareness of total fatigue and CNS load.
- Athletes experience recovery debt and readiness collapse.

**The Evidence:**
- Court sport (basketball, volleyball) training research shows optimal stimulus delivery occurs in 45–60 min blocks (Bompa & Buzzichelli, 2023).
- Session exceeding 60 min shows diminishing returns for adaptation and increased injury risk (Halson & Jeong, 2023).
- Youth athletes (13–17) show accelerated fatigue accumulation in sessions >60 min (Faigenbaum et al., 2024).

**The Fix:**
- Hard duration boundary (50–60 min) makes volume predictable and auditable.
- Block time budgets (8–10 / 10–12 / 25–30 / 5–8) distribute work logically without math.
- Coaches adjust WORK volume, not session length, when time is tight.

---

### 12. Why Block Time Budgets Exist (NEW v2.2 Rationale)

**The Problem:**
- Blocks with assumed time ranges (e.g., "WORK is 30 min") create silent overrun.
- Coaches spend 20 min on PRIME and compress WORK to 18 min without noticing.
- Session validity depends on WORK ≥24 min; compressed WORK is illegal.

**The Evidence:**
- Warm-up physiology shows optimal nervous system priming occurs in 8–12 min (Grgic et al., 2024).
- Movement quality rehearsal (PREP) requires 10–12 min to address motor learning (Wulf & Lewthwaite, 2023).
- Main stimulus (WORK) requires 25–30 min to deliver adequate volume and density for adaptation (Suchomel et al., 2023).
- Cool-down (CLEAR) requires 5–8 min to lower heart rate and engage parasympathetic system (Bourdon et al., 2024).

**The Fix:**
- Fixed time ranges for each block make structure visible and auditable.
- Blocks flex within range (8–10 not 8–15) but never across blocks.
- If time is tight, reduce WORK drills (e.g., drop one exercise), never shorten blocks.

---

### 13. Why PRIME Is Day-Role Dependent (NEW v2.2 Rationale)

**The Problem:**
- PRIME as a "global warm-up" leads to templating and copy-paste.
- Athletes perform identical prep across Day A, B, C sessions → boring, ineffective.
- Coaches don't align PRIME to the day's WORK demands → missed adaptation.

**The Evidence:**
- Motor learning requires context-specific preparation; general warm-ups show 30–50% less transfer to task-specific performance (Grgic et al., 2024).
- Sport preparation research shows prep that aligns with upcoming WORK demands improves power output by 5–15% vs. generic prep (Suchomel et al., 2023).
- Youth athletes show better injury prevention when prep addresses the specific movement patterns they're about to execute (Myer et al., 2024).

**The Fix:**
- PRIME selection occurs **after** Day Role is declared.
- PRIME biases toward tissues and joints required for that day's WORK (hip flexor prep for Day A squat, thoracic rotation for Day B power, etc.).
- PRIME rotates across sessions → variety keeps engagement high and adaptation fresh.

---

### 14. Why PRIME Anti-Repetition Exists (NEW v2.2 Rationale)

**The Problem:**
- Identical PRIME across sessions is efficient for coaches but creates neural adaptation (habituation).
- Athletes "zone out" during identical prep; attention drops; quality suffers.
- Repetitive PRIME doesn't challenge proprioception or motor variability.

**The Evidence:**
- Proprioceptive training research shows **variation** in stimulus (different movement angles, speeds, stabilization demands) drives greater neuromuscular adaptation than repetitive identical drills (Wulf & Lewthwaite, 2023).
- Youth athlete boredom during identical warm-ups correlates with reduced engagement and higher injury rates (Faigenbaum et al., 2024).

**The Fix:**
- PRIME may include different exercises each session but cannot be identical in sequence and intent.
- Example: Day A PRIME Session 1 = [hip mob, glute bridge, ankle prep, pogos] vs. Day A PRIME Session 2 = [deep lunge, clamshells, lacrosse ball ankle, light skips] → different exercises, same intent (hip, glute, ankle, low-level plyos).
- Rotation is lightweight (coach-level decision) but non-negotiable.

---

### 15. Why PRIME Scope Is Locked (NEW v2.2 Rationale)

**The Problem:**
- PRIME "creep" expands prep into a second WORK block via "activation circuits."
- Breathing protocols (formal parasympathetic drills) appear in PRIME, not CLEAR, creating confusion.
- Conditioning is disguised as "dynamic prep."

**The Evidence:**
- PRIME-level activation (e.g., 3×20 band walks) creates significant CNS and metabolic fatigue, reducing power output in subsequent WORK by 5–10% (Schoenfeld & Grgic, 2024).
- Formal breathing protocols (structured respiratory drills) require parasympathetic dominance and low arousal; executing during warm-up (high arousal) reduces efficacy (Halson & Jeong, 2023).
- PRIME as true "prep" should account for <10% of session CNS budget; PRIME exceeding 15 min shows diminishing prep returns and competes with WORK stimulus.

**The Fix:**
- PRIME is **prep-only**: tissue mobilization, joint prep, low-level elasticity (E0–E1), neural priming.
- PRIME is **not**: activation circuits, core work, conditioning, breathing protocols, elastic contact budgets.
- Legality test: "Does this raise heart rate or cause fatigue?" → If yes, it's illegal in PRIME.

---

### 16. Why Session Abort Prevents Injury Cascade (NEW v2.2 Rationale)

**The Problem:**
- Sessions continue despite pain escalation, coordination loss, or quality breakdown.
- Athletes and coaches "push through," creating accumulated damage and extended injury timelines.
- Injury prevention culture demands **stopping early**, not grinding through.

**The Evidence:**
- Return-to-sport research shows early cessation when pain or movement quality degrades prevents injury cascade escalation by 40–60% (Paterno et al., 2024).
- Movement quality degradation (valgus collapse, asymmetry) during fatigue is a primary ACL re-injury predictor in youth athletes (Myer et al., 2024).
- Sessions continued under pain >3 points above baseline show 3–5× higher risk of re-injury within 7 days (Kapreli et al., 2023).

**The Fix:**
- Single, clear abort rule: **If pain escalates, coordination degrades, or quality cannot be restored → collapse to CLEAR immediately.**
- No scoring, no thresholds, no judgment calls.
- This is the DCC's **safety valve**—quick exit from risk without complexity.

---

### 17. Why Evidence Currency Is Critical (FROM v2.1, UNCHANGED)

| Topic | Key Sources |
|---|---|
| Plyometric dose and youth elasticity | Ramirez-Campillo et al. 2023, 2024; Suchomel et al. 2023 |
| Motor learning and skill acquisition | Wulf & Lewthwaite 2023; Faigenbaum et al. 2024 |
| Readiness monitoring and injury prediction | Halson & Jeong 2023; Saw et al. 2024; Bourdon et al. 2024 |
| Return-to-sport algorithms and gates | Caulfield et al. 2024; Paterno et al. 2024; Myer et al. 2024 |
| Injury cascade and prevention | Lohmander et al. 2024; Kapreli et al. 2023 |
| Velocity-based training and fatigue | Suchomel et al. 2023; Schoenfeld & Grgic 2024 |
| Periodization and overload | Issurin 2024; Bompa & Buzzichelli 2023 |
| Youth biomechanics and development | Faigenbaum et al. 2024; Myer et al. 2024 |

All references in this document reflect **2023–2025 research consensus.**

---

## PART IV: APPENDIX AND REFERENCE

### A. Readiness Multiplier Quick-Reference v2.2 (FROM v2.1, UNCHANGED)

| Readiness State | Pain (0–10) | Examples | Session Cap Adjustment |
|---|---|---|---|
| **GREEN** | 0–2, no swelling | Pain-free range, symmetric movement, zero limp | 1.0x full cap |
| **YELLOW** | 3–4, mild swelling | Slight pain, mild asymmetry, no compensation | 0.8x cap (20% reduction) |
| **RED** | 5–10, moderate/severe swelling or effusion | Pain at rest, significant limp, giving way | 0.0x → Band 0, E0 only |

---

### B. Training Route Quick-Reference v2.2 (FROM v2.1, UNCHANGED)

| Route | Intent | Fatigue Policy | Termination | Typical Day |
|---|---|---|---|---|
| **Max Performance** | Absolute output | Zero tolerance | Output drop | Day A, select windows |
| **Submax Performance** | Max intent, capped output | Zero tolerance | Quality loss | Day A, Day B |
| **Capacity Accumulation** | Moderate, progressive | Bounded tolerance | Planned volume | Day B, Day C |
| **Regeneration** | Low, effortless | Zero tolerance | Time-based | Day C, recovery days |

---

### C. Key Definitions (FROM v2.1, UPDATED v2.2)

| Term | Definition |
|---|---|
| **Contact** | Single foot strike, landing, or propulsion in plyometric/reactive movement |
| **Band** | Load magnitude classification (Band 0–3) |
| **Node** | Movement density within band (Node 1–3) |
| **E-Node** | Plyometric/elasticity complexity tier (E0–E4) |
| **Readiness** | Acute joint/movement quality state (GREEN/YELLOW/RED) |
| **Hardstop** | Symptom (effusion, giving way, sharp pain) triggering immediate training halt |
| **Envelope** | Combined Band + Node + E-Node + readiness constraints for a single day |
| **Computed Stage** | AI system-calculated training stage based on objective gates (not coach override) |
| **Guardrail** | Maximum safe exposure limit (not prescription) |
| **Multiplier** | Readiness-based reduction factor applied to session caps (1.0, 0.8, or 0.0) |
| **Training Route** | Execution governor defining fatigue tolerance, density behavior, termination logic within safety boundaries |
| **Fatigue Economics** | How fatigue is treated (forbidden, tolerated, sought) within a training route |
| **Density Governor** | Rule determining if/how movement density changes over time within a route |
| **Termination Logic** | Primary and secondary criteria that end a training block within a route |
| **Session Duration Contract** (NEW v2.2) | Hard boundary: athlete sessions must terminate 50–60 min |
| **Block Time Budget** (NEW v2.2) | Fixed time ranges per block: PRIME 8–10, PREP 10–12, WORK 25–30, CLEAR 5–8 |
| **PRIME Day-Role Binding** (NEW v2.2) | PRIME selection occurs after Day Role is declared; PRIME must prepare tissues/joints for WORK |
| **PRIME Anti-Repetition** (NEW v2.2) | PRIME content may not be identical across consecutive sessions |
| **PRIME Scope Lock** (NEW v2.2) | PRIME may not include activation/conditioning/breathing/elastic contacts |
| **Session Collapse** (NEW v2.2) | When pain escalates, quality degrades, or safety risk appears → session shifts to CLEAR only |

---

### D. DCC Audit Checklist (NEW v2.2)

Before publishing any session, verify:

- [ ] Session duration: 50–60 min ✓
- [ ] Block time ranges within budget (PRIME 8–10, PREP 10–12, WORK 25–30, CLEAR 5–8) ✓
- [ ] WORK duration ≥24 min ✓
- [ ] PRIME selected after Day Role declared ✓
- [ ] PRIME does not repeat from prior session (or repeats only identical in structure, not intent) ✓
- [ ] PRIME contains no activation circuits, conditioning, breathing protocols, or elastic contacts ✓
- [ ] PRIME is 8–10 min at RPE ≤3 ✓
- [ ] PRIME → PREP → WORK → CLEAR in order ✓
- [ ] Contact totals do not exceed weekly cap for readiness state ✓
- [ ] Readiness modifier applied (GREEN 1.0x, YELLOW 0.8x, RED 0.0x) ✓
- [ ] No Band 3 + Node 3 simultaneously ✓
- [ ] No E4 in youth 13–17 ✓
- [ ] Readiness RED does not receive full load ✓
- [ ] No Day-role pattern violated (Day A ≥5 compound blocks, etc.) ✓
- [ ] If pain escalates, quality drops, or safety flag → session collapses to CLEAR ✓
- [ ] Session abort triggered → WORK omitted, CLEAR extended ✓

---

## PART V: CLOSING NOTE AND VERSION CONTROL

### DCC Operational Philosophy (FROM v2.1, AFFIRMED v2.2)

The DCC operates as a **containment system**, not an optimization system.

**Its purpose:**
- Prevent harm (not maximize adaptation)
- Enforce consistency (not honor coach preferences over data)
- Make training auditable and predictable (not clever or "efficient")

**What DCC guarantees:**
- Two different coaches building the same session will produce nearly identical outputs
- Missing inputs → system stops and asks (never guesses)
- Requests outside scope → system explains why with legal alternative or routing
- Outputs feel predictable, safe, and repeatable (not creative, not novel, not risky)

This is not a bug. **This is the design.**

---

### Version Control Log

| Version | Date | Changes | Author | Status |
|---|---|---|---|---|
| **1.0** | 2026-01-11 | Initial operational release | EFL Director | Superseded |
| **2.0** | 2026-01-11 | Initial operational release | EFL Director | Superseded |
| **2.0.1** | 2026-01-18 | Readiness standardization (0.8 canonical, monitoring inputs clarification 6A), evidence citation refresh (2023–2025 sources), dose language clarifier (guardrails vs prescriptions), research language precision (softened risk percentages) | Austin Lawrence | Superseded |
| **2.1** | 2026-01-18 | **MAJOR** Training Routes execution governors (Max/Submax/Capacity/Regeneration routes with fatigue economics, density governors, termination logic, integration with Day A/B/C, Readiness, EPL, Population Safety) | Austin Lawrence | Superseded |
| **2.2** | 2026-01-25 | **MAJOR** Session Duration Contract (50–60 min hard boundary), Block Time Budget (PRIME 8–10, PREP 10–12, WORK 25–30, CLEAR 5–8), PRIME Day-Role Binding (PRIME selected after Day Role, must prepare WORK patterns), PRIME Anti-Repetition Rule (no identical PRIME across sessions), PRIME Scope Lock (no activation/conditioning/breathing/contacts), Session Abort Rule (collapse to CLEAR if pain escalates, quality degrades, safety risk appears) | Austin Lawrence | **CURRENT** |

---

### Authorization and Effective Date

| Field | Value |
|---|---|
| **Document Classification** | PRIMARY ARCHITECTURAL CONTROL CENTER |
| **Authorization** | EFL Director of Performance Systems |
| **Effective Date** | 2026-01-25 |
| **Next Review Date** | 2026-07-25 (6-month cycle) |

---

## END OF DCC v2.2
