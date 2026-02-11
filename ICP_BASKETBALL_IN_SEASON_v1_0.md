# ICP_BASKETBALL_IN_SEASON_v1_0

**Document ID**: ICP_BASKETBALL_IN_SEASON_v1_0  
**Version**: v1.0 (PATCHED-2)  
**Effective Date**: 2026-01-07  
**Owner**: Elite Fitness Lab  
**Status**: OPERATIONAL  
**Document Type**: In-Season ICP (State-Based)  
**Population**: Youth 13–15 (HS/MS)  
**Season**: IN_SEASON ONLY  
**Frequency**: 1–2 sessions/week (**NEVER 0**)  
**F-V Bias**: BALANCED (locked for youth ≤16)  
**Core Rule**: **NO PROGRESSION — STATE CONTROL ONLY**

---

## Dependencies (Hard Authority)

- Parent Wrapper: `EFL_SP_PROJECT_WRAPPER_COURT_SPORT_FOUNDATIONS_v1_0.md`
- MDP: `EFL_MDP_COURT_VERTICAL_v1_4.json`
- Governance: `EFL_Governance_v4_1.md`
- Load Standards: `EFL_LOAD_STANDARDS_v2_2_0.json`
- Sport Demands: `sport_demands_grid_v2.2.2.json`
- ICP Definitions: `EFL_ICP_Definitions_v2_3_1.json`
- Exercise Library: `EFL_Exercise_Library_v2_5.csv`
- Prerequisite: `HS_BASKETBALL_ELASTIC_SPECIALIZATION_MESO_v1_0` OR `HS_BASKETBALL_FOUNDATIONS_MESO_v1_0`

---

## 0. What This Document IS (And Is NOT)

### 0.1 This is an IN-SEASON ICP

- **IS state-based** (GREEN / YELLOW / RED) — not progression-based
- **IS basketball-specific** (court vertical MDP, game-day proximity rules)
- **IS business-safe** — every week has ≥1 session (no cancellations)
- **NOT** a foundations block (no volume progression)
- **NOT** a specialization meso (no elastic development)
- **NOT** off-season (in-season rules apply whenever games are scheduled or team calendar governs training density)

### 0.2 Core Function

Protects **elastic quality, tissue health, and performance readiness** during in-season using **state-driven session selection** governed by:

- Athlete readiness (GREEN / YELLOW / RED)
- Practice density (3–6/week)
- Game density (0–3/week)
- Tournament presence (Y/N)

### 0.3 Key Principle

**Sessions always occur. Stress adapts, never cancels.**

If facility training is blocked → **IS-D Micro (Remote)** is mandatory. No week ends with 0 sessions.

---

## 1. Block Identity & Purpose

### 1.1 Identity Matrix

| Attribute | Value |
| --- | --- |
| Document Type | In-Season ICP (State-Based) |
| Population | Youth 13–15 (HS/MS) |
| Season | IN_SEASON ONLY |
| Frequency | 1–2 sessions/week (NEVER 0) |
| F-V Bias | BALANCED (locked for ≤16) |
| Parent Authority | Court Sport In-Season ICP Family |
| MDP | MDP_COURT_VERTICAL |
| Sport | Basketball |
| Prerequisite | Elastic Specialization OR Foundations |

### 1.2 Purpose Matrix

| Problem | ICP Solution |
| --- | --- |
| High practice + game density | State-based session selection (IS-A/B/C/D) |
| CNS overload risk | Remove elastic when density ≥ threshold |
| Tissue breakdown | Downgrade to recovery sessions (IS-C/D) |
| Business continuity | IS-D Micro ensures no "off" weeks |
| Youth CNS protection | BALANCED lock, E3/E4 forbidden |
| Performance maintenance | Minimal elastic dose (E1/E2 only, if GREEN) |

---

## 2. Block-Level Invariants (Never Change)

These rules apply to **ALL weeks** of this ICP:

| Invariant | Value | Reason |
| --- | --- | --- |
| F-V Bias | BALANCED only | Youth ≤16 lock |
| E3 exposure | ❌ Forbidden | In-season CNS protection |
| E4 exposure | ❌ Forbidden | Basketball node + youth |
| Season | IN_SEASON only | Games scheduled or team calendar governs density |
| Weekly sessions | ≥1 always | Business continuity law |
| Session cap (elastic) | ≤60 contacts | Youth + in-season ceiling |
| Weekly cap (elastic) | ≤60 contacts total | In-season hard limit |
| IS-A + IS-B elastic rule | If IS-A occurs this week → IS-B elastic = 0 | Enforces weekly cap (no micro-dose in IS-B) |
| Band 4 | ❌ Forbidden | Youth hard ban |
| Band 3 max | 10% WORK (GREEN only) | In-season constraint |
| Progression model | ❌ None | State control, not time control |
| Back-to-back elastic | ❌ Forbidden | 48h minimum rest |
| Elastic <72h pre-game | ❌ Forbidden | Game-day proximity rule |

---

## 3. Weekly Inputs (Queried Every Week)

The system queries these **before** generating the week's session plan:

1. **Practices/week** (3–6 range typical)
2. **Games/week** (0–3 range typical)
3. **Tournament present** (Y/N)
4. **Days since last game** (0–7)
5. **Days until next game** (0–7)
6. **Athlete state** (GREEN / YELLOW / RED)

### 3.1 Deterministic Definitions

**Tournament** = TRUE if:

- Tournament flag = TRUE, OR
- Games/week ≥2, OR
- Back-to-back games within ≤48h

**Practice Spike** = TRUE if:

- `practices_this_week ≥ practices_last_week + 1`
- If `last_week` unknown → no spike applied

**Unknown Handling** (Conservative Bias):

- If `days_until_next_game` unknown → treat as **<72h** (no elastic allowed)
- If `days_since_last_game` unknown → treat as **<48h** (recovery priority)

---

## 4. ICP State Map (Single Source of Truth)

### 4.1 State Definitions

| State | Definition | Allowed Action |
| --- | --- | --- |
| GREEN | No pain, soreness ≤48h, practices tolerated, no fatigue flags | Maintain elastic + strength (low dose) |
| YELLOW | Soreness >48h OR practice spike OR fatigue accumulation | Limit elastic (E1 only), protect CNS |
| RED | Pain, joint irritation, performance breakdown, illness | Recovery-only session (IS-C or IS-D) |

### 4.2 State Precedence Rule

RED > YELLOW > GREEN

- No averaging (e.g., "mostly GREEN" = GREEN, not YELLOW)
- No discretion (if any RED flag exists → RED)
- One-way transitions within a week (no re-upgrade)

### 4.3 No Re-Upgrade Rule

Once downgraded in a week (e.g., GREEN → YELLOW on Tuesday) → **no re-upgrade within that week**.

**Rationale**: Prevents oscillation and enforces conservative bias during season.

---

## 5. Load Density Map (Schedule Ceiling)

Schedule defines the **maximum stress ceiling** allowed that week, independent of athlete state.

| Load Density | Practices | Games | Tournament | Stress Ceiling |
| --- | --- | --- | --- | --- |
| LOW | ≤3 | 0 | No | IS-A or IS-B allowed |
| MODERATE | 3–4 | 1 | No | IS-B primary; IS-A only if timing allows |
| HIGH | ≥5 | ≥1 | No | IS-B downgraded or IS-C |
| PEAK | Any | ≥2 | Yes | IS-C or IS-D only |

### 5.1 Precedence Rule

**Tournament / PEAK ceiling overrides athlete state.**

- If tournament week → force IS-C or IS-D, even if athlete = GREEN.
- If ≥2 games/week → force IS-B or IS-C, even if athlete = GREEN.

---

## 6. Session Type Map (In-Season Only)

| Session Type | Purpose | Elastic Allowed | Strength Allowed | CNS Load |
| --- | --- | --- | --- | --- |
| IS-A | Elastic maintenance (GREEN only) | Yes (limited: E1/E2, 30–50 contacts) | Yes (low: Band 0–2) | Low–Moderate |
| IS-B | Strength + durability | No (elastic = 0 if IS-A occurred this week) | Yes (per state matrix) | Low |
| IS-C | CNS-light durability | ❌ None | Band 0–1 only | Very Low |
| IS-D Micro (Remote) | Business continuity / travel | ❌ None | Bodyweight only | Minimal |

### 6.1 Hard Business Rule

**No week results in 0 sessions.**

If facility training is blocked → **IS-D Micro is mandatory** and counts as the week's session.

---

## 7. Weekly Session Allocation Map

| Schedule | Sessions/week | Allowed Types | Notes |
| --- | --- | --- | --- |
| 3–4 practices, 0 games | 2 | IS-A + IS-B | Normal off-week in-season; IS-B has no elastic |
| 3–5 practices, 1 game | 1–2 | IS-B primary; IS-A only if ≥72h pre-game | If IS-A used, IS-B = no elastic |
| ≥5 practices + games | 1 | IS-C or downgraded IS-B | High-density week |
| Tournament week / ≥2 games | 1 | IS-C or IS-D Micro | Peak density |

### 7.1 Never Allowed

- 2× IS-A in the same week
- Elastic on back-to-back days
- Elastic inside **72h pre-game** window
- IS-B elastic if IS-A occurred that week (weekly cap enforcement)

---

## 8. Elastic (Plyometric) Matrix — By State

### 8.1 Elastic Contacts per Session

| State | Contacts / Session | E-Nodes Allowed |
| --- | --- | --- |
| GREEN | 30–50 | E1 (60%) + E2 (40%) |
| YELLOW | 10–25 | E1 only (100%) |
| RED | 0 | ❌ None |

### 8.2 Elastic Distribution (If Allowed)

| State | E1% | E2% | E3% | E4% |
| --- | --- | --- | --- | --- |
| GREEN | 60 | 40 | ❌ | ❌ |
| YELLOW | 100 | 0 | ❌ | ❌ |
| RED | — | — | — | — |

### 8.3 Absolute Elastic Laws (In-Season)

| Rule | Status | Reason |
| --- | --- | --- |
| E3 exposure | ❌ **ILLEGAL** | In-season CNS protection |
| E4 exposure | ❌ **ILLEGAL** | Youth + basketball node profile |
| Session cap | ≤60 contacts | In-season ceiling |
| Weekly cap | ≤60 contacts total | Maintenance dose only |
| Back-to-back elastic | ❌ **ILLEGAL** | 48h minimum rest |
| Elastic <72h pre-game | ❌ **ILLEGAL** | Game-day proximity rule |
| Elastic under YELLOW | ✅ Allowed (E1 only, 10–25 contacts, timing rules apply) | Conservative maintenance |
| Elastic under RED | ❌ **ILLEGAL** | Recovery priority |

---

## 9. Strength (Band) Matrix — By State

### 9.1 Band Distribution (WORK only)

| State | Band 0–1 | Band 2 | Band 3 |
| --- | --- | --- | --- |
| GREEN | 55% | 35% | 10% |
| YELLOW | 65% | 35% | 0% |
| RED | 80% | 20% | 0% |

### 9.2 Hard Laws

| Rule | Status | Reason |
| --- | --- | --- |
| Band 4 | ❌ **ILLEGAL** | Youth hard ban |
| Band 3 in-season | ≤10% WORK, GREEN only | CNS protection |
| Band 3 grinding | ❌ **ILLEGAL** | Rate/intent only (2–4 reps, fast) |
| Fatigue-based strength sets | ❌ **ILLEGAL** | Elastic/game quality protection |

---

## 10. Day-Level Session Blueprints

### 10.1 IS-A — Elastic Maintenance (GREEN Only; Ceiling Must Allow)

**When to Use:**

- Athlete = GREEN
- Load density = LOW or MODERATE
- ≥72h until next game
- ≥48h since last game
- **No more than 1× per week**

**Session Structure:**

| Element | Rule |
| --- | --- |
| Elastic | 30–50 contacts (E1 60% / E2 40%) |
| Strength | Band 0–2 only |
| Focus | Vertical expression, decel mechanics, rotation |
| Duration | 45–55 minutes |
| CNS Load | Low–Moderate |

**Weekly Cap Enforcement:**  
If IS-A occurs this week → all other sessions (IS-B) have **0 elastic**.

**Example Day:**

- PRIME: Movement prep + ankle/calf (5 min)
- PREP: Box jumps E2 (20 contacts) + Single-leg line hops E1 (20 contacts)
- WORK: Goblet squat 3×6 (Band 1), Split squat 3×6/leg (Band 1), DB RDL 3×8 (Band 1)
- CLEAR: Med ball rotational throws 3×4, Pallof press 3×8, Calf raise 3×12

---

### 10.2 IS-B — Strength + Durability (All States)

**When to Use:**

- Any state (GREEN / YELLOW / RED)
- Primary session type for game weeks
- Can occur <72h pre-game (no elastic, reduced volume)

**Session Structure:**

| Element | Rule |
| --- | --- |
| Elastic | ❌ None (always 0 in IS-B to preserve weekly cap) |
| Strength | Per state matrix (Band 0–2, or 0–1 if YELLOW/RED) |
| Focus | Unilateral knee, hinge, trunk, posterior chain |
| Duration | 40–50 minutes |
| CNS Load | Low |

**Example Day (GREEN):**

- PRIME: Movement prep (5 min)
- PREP: None
- WORK: Trap bar deadlift 4×5 (Band 2), Reverse lunge 3×6/leg (Band 1), DB bench 3×6 (Band 2), Inverted row 3×8
- CLEAR: Plank 3×30s, Side plank 3×20s/side, Calf raise 3×15

**Example Day (YELLOW):**

- PRIME: Movement prep (5 min)
- PREP: None
- WORK: Goblet squat 3×8 (Band 1), Split squat 3×8/leg (Band 0), DB RDL 3×10 (Band 1), Push-up 3×10
- CLEAR: Dead bug 3×10, Bird dog 3×8/side, Ankle mobility

---

### 10.3 IS-C — CNS-Light Durability

**When to Use:**

- Athlete = RED
- Load density = HIGH or PEAK
- Back-to-back games
- Tournament week

**Session Structure:**

| Element | Rule |
| --- | --- |
| Elastic | ❌ None |
| Strength | Band 0–1 only |
| Focus | Isometrics, tempo bodyweight, trunk, ankle, mobility |
| Duration | 30–40 minutes |
| CNS Load | Very Low |

**Example Day:**

- PRIME: Breathing + soft tissue (5 min)
- PREP: None
- WORK: Goblet squat iso-hold 3×20s (Band 0), Split squat 3×8/leg (tempo 3-1-1, Band 0), Glute bridge 3×12
- CLEAR: Plank 3×30s, Side plank 3×20s, Calf stretch, Hip flexor stretch

---

### 10.4 IS-D Micro (Remote)

**When to Use:**

- Facility closed
- Travel week
- Illness (non-pain)
- Business continuity override

**Session Structure:**

| Element | Rule |
| --- | --- |
| Elastic | ❌ None |
| Strength | Bodyweight only (no external load) |
| Focus | Breathing, mobility, trunk, hips, shoulder/scap |
| Duration | 10–25 minutes |
| CNS Load | Minimal |

**Example Day:**

- Breathing reset 3 min
- Cat-cow 2×8
- Glute bridge 3×12
- Dead bug 3×10
- Push-up 2×8
- Hip flexor stretch 2×30s/side
- Calf stretch 2×30s/side

**Counts as the week's session.**

---

## 11. Game Proximity Laws

### 11.1 Within 72h BEFORE a Game

| Rule | Action |
| --- | --- |
| Elastic | ❌ Remove entirely |
| Band 3 | ❌ Remove entirely |
| Session type | IS-B only (no IS-A) |
| Volume | Reduce IS-B by 20% (fewer sets) |

### 11.2 Within 48h AFTER a Game

| Condition | Action |
| --- | --- |
| Soreness present | IS-C or IS-D |
| No soreness | IS-B allowed (no elastic) |

### 11.3 Back-to-Back Games

| Rule | Action |
| --- | --- |
| Session type | IS-C or IS-D only |
| Never | "Off" or skip |

---

## 12. Practice / Game Override Matrix

| Condition | Mandatory Action |
| --- | --- |
| Practice = 5/week | Remove IS-A entirely |
| ≥2 games/week | 1 session max (IS-B or IS-C) |
| Tournament week | IS-C or IS-D only |
| Practice spike (+1/week) | Remove elastic (force IS-B/C/D) |
| Pain flag | Force RED state (IS-C or IS-D) |

---

## 13. Pattern Guarantee Matrix (Weekly Minimums)

| Pattern | Min / Week | Notes |
| --- | --- | --- |
| Unilateral knee | 2 | Split squat, lunge, step-up |
| Hinge | 2 | RDL, KB swing, trap bar deadlift |
| Trunk anti-extension | 2 | Plank, dead bug, fallout |
| Trunk anti-rotation | 2 | Pallof, chop, bird dog |
| Upper pull | 2 | Row, pull-up, lat pulldown |
| Upper push | 1 | Push-up, DB press, landmine press |
| Calf / ankle | 2 | Calf raises, ankle stiffness drills |
| Decel mechanics | 1–2 | Landing drills (technique only, not E-node) |
| Med ball rotation | 1 | Rotational throws (basketball-specific) |
| Plyo | 0–1 | State + game dependent (E1/E2 only if GREEN) |

### 13.1 Decel Technique Touch Definition (NOT Elastic)

Decel mechanics may occur even when plyo = 0, provided they meet these criteria:

- Drop step + stick (low amplitude)
- Snap-down to stick
- Low box step-off to stick (no rebound)

**Legal constraints:**

- No rebound
- No continuous contacts
- No reactive series

**If any rebound or continuous contacts occur → it becomes elastic and must follow Section 8.**

---

## 14. Automatic Downgrade Matrix

| Trigger | Action | Reason Code |
| --- | --- | --- |
| Soreness >48h | GREEN → YELLOW | `SORENESS_FLAG` |
| Game performance drop | GREEN → YELLOW | `PERFORMANCE_DROP` |
| Pain flag | Any → RED | `PAIN_FLAG` |
| Practice spike (+1/week) | Remove elastic | `PRACTICE_SPIKE` |
| Tournament / ≥2 games | Force IS-C / IS-D | `PEAK_DENSITY` |

### 14.1 Downgrade Rules

- **No re-upgrade within the same week** (once YELLOW → stays YELLOW until next week)
- RED always forces recovery session (IS-C or IS-D)
- Tournament week **overrides athlete state** (force IS-C/D even if GREEN)

---

## 15. Weekly Decision Tree (EPA Integration)

### Step 1: Query Inputs

- Practices/week
- Games/week
- Tournament (Y/N) — apply deterministic definition from Section 3.1
- Days since last game (if unknown → <48h)
- Days until next game (if unknown → <72h)
- Athlete state (GREEN / YELLOW / RED)

### Step 2: Determine Load Density

- If tournament OR ≥2 games → **PEAK**
- Else if ≥5 practices OR games + high practice → **HIGH**
- Else if 3–4 practices + 1 game → **MODERATE**
- Else → **LOW**

### Step 3: Apply State + Density Ceiling

| State + Density | Session Type |
| --- | --- |
| GREEN + LOW | IS-A + IS-B (2 sessions; IS-B has 0 elastic) |
| GREEN + MODERATE | IS-B primary; IS-A if ≥72h pre-game (if IS-A used, IS-B = 0 elastic) |
| GREEN + HIGH | IS-B downgraded or IS-C (1 session) |
| GREEN + PEAK | IS-C or IS-D (1 session) |
| YELLOW + any | IS-B or IS-C (no IS-A; elastic allowed only in IS-B if YELLOW + timing allows) |
| RED + any | IS-C or IS-D only |

### Step 4: Apply Game Proximity Rules

- If <72h pre-game → no elastic, no Band 3
- If <48h post-game + soreness → IS-C or IS-D
- If back-to-back games → IS-C or IS-D only

### Step 5: Generate Session

- Select session type (IS-A / IS-B / IS-C / IS-D)
- Apply elastic matrix (contacts + E-node %)
- Apply band matrix (% distribution)
- Apply pattern guarantees (weekly minimums)
- Enforce weekly elastic cap (if IS-A occurred → IS-B elastic = 0)

---

## 16. Exit Routing

| Condition | Route |
| --- | --- |
| Season ends | `ICP_BASKETBALL_POST_SEASON_v1_0` (future doc) |
| Extended break ≥3 weeks | `HS_BASKETBALL_FOUNDATIONS_MESO_v1_0` (Week 3 entry) |
| Injury / pain >72h | R2P Project (immediate handoff) |

---

## 17. Integration Notes

### For Coaches

- **This is a STATE-BASED ICP** — not progression-based, not time-based
- **Sessions always occur** — if facility blocked, use IS-D Micro
- **Elastic is rare** — only IS-A (GREEN + low density + ≥72h pre-game)
- **E3/E4 forbidden** — in-season CNS protection (E1/E2 only if GREEN)
- **Tournament week overrides state** — force IS-C/D even if athlete feels great
- **No re-upgrade within a week** — conservative bias during season
- **Band 3 rare** — only GREEN state, ≤10% WORK, rate/intent only
- **Weekly elastic cap enforced** — if IS-A occurs, IS-B has 0 elastic

### For EPA v2.2

- **Query inputs weekly** before generating session (practices, games, tournament, state, game proximity)
- **Apply deterministic definitions** (tournament, practice spike, unknown handling per Section 3.1)
- **Apply load density ceiling first** (PEAK overrides athlete state)
- **Enforce game proximity rules** (no elastic <72h pre-game, reduce volume)
- **Enforce state precedence** (RED > YELLOW > GREEN, no averaging)
- **Enforce weekly elastic cap** (if IS-A occurs → all IS-B sessions have 0 elastic)
- **Enforce business continuity** (if no facility session possible → generate IS-D Micro)
- **Respect pattern guarantees** (weekly minimums must appear even in IS-C/D)
- **Track downgrade triggers** (soreness, pain, performance drop → force state change)

### For System Architects

- This ICP is **state-driven**, not time-driven (no "Week 1, Week 2" progression)
- **Load density + athlete state** are the dual governors (neither alone determines session type)
- **Tournament/PEAK overrides athlete state** (business + safety rule)
- **IS-D Micro** solves business continuity (no "off" weeks, even if facility closed)
- **Game proximity rules** are deterministic (72h/48h thresholds, no discretion)
- **No re-upgrade rule** prevents oscillation (conservative bias)
- **Elastic rare by design** (only GREEN + low density + timing window)
- **Weekly cap enforcement** is explicit (IS-A → IS-B elastic = 0)
- **Unknown handling** is conservative (treat as <72h pre-game, <48h post-game)

---

## 18. Why This Document is Critical

Once this ICP exists:

✅ **Basketball in-season pathway complete** (Foundations → Specialization → In-Season)  
✅ **Youth CNS protected** (BALANCED lock, E3/E4 forbidden, elastic rare)  
✅ **Business continuity enforced** (IS-D Micro = no "off" weeks)  
✅ **State-based control** (GREEN/YELLOW/RED governs session type)  
✅ **Game proximity safe** (72h/48h rules prevent CNS overload)  
✅ **Tournament override** (PEAK density forces recovery session)  
✅ **Pattern guarantees maintained** (weekly minimums even in IS-C/D)  
✅ **Exit routing clear** (post-season ICP, foundations re-entry, R2P)  
✅ **Weekly cap enforced deterministically** (IS-A → IS-B elastic = 0)  
✅ **Decel mechanics defined** (no elastic "backdoor")  
✅ **Unknown handling conservative** (EPA never guesses)

---

## 19. Version Control

**v1.0 (PATCHED-2)** (2026-01-07)

- **Status**: OPERATIONAL | Ready for EPA integration and coach deployment
- All contradictions resolved, all determinism gaps closed
- Parent Wrapper: Added `EFL_SP_PROJECT_WRAPPER_COURT_SPORT_FOUNDATIONS_v1_0.md` dependency
- Aligned to Load Standards v2.2.0, Governance v4.1, ICP Definitions v2.3.1
- MDP: Court Vertical v1_4.json
- Sport Demands Grid: v2.2.2 (basketball IN_SEASON profile)
- Prerequisite: Elastic Specialization OR Foundations
- State map: GREEN / YELLOW / RED (RED > YELLOW > GREEN precedence)
- Load density: LOW / MODERATE / HIGH / PEAK (PEAK overrides state)
- Session types: IS-A (elastic maintenance, GREEN only), IS-B (strength + durability, 0 elastic if IS-A occurred), IS-C (CNS-light), IS-D Micro (remote/business continuity)
- Elastic cap: ≤60 contacts/session, ≤60/week total, E1/E2 only (E3/E4 forbidden)
- **Weekly cap enforcement**: If IS-A occurs → IS-B elastic = 0 (no micro-dose)
- YELLOW elastic: ✅ Allowed (E1 only, 10–25 contacts, timing rules apply)
- RED elastic: ❌ Forbidden
- Band cap: Band 3 ≤10% (GREEN only), Band 4 forbidden
- Game proximity: No elastic <72h pre-game, reduce volume, IS-C/D for back-to-back games
- Tournament definition: Flag OR games/week ≥2 OR back-to-back ≤48h
- Practice spike definition: `practices_this_week ≥ practices_last_week + 1`
- Unknown handling: Conservative (unknown days_until_next_game → <72h; unknown days_since_last_game → <48h)
- Decel mechanics definition: No rebound, no continuous contacts, low amplitude only (otherwise elastic)
- Business rule: NEVER 0 sessions (IS-D Micro mandatory if facility blocked)
- Exit routing: Post-Season ICP, Foundations (Week 3), R2P

**Next Review**: 2026-04-07 or upon Load Standards v2.2.1 release

---

**End of Document**  
**Status**: OPERATIONAL (FACTORY-GRADE, PATCHED-2) | Basketball in-season ICP complete  
**System Integration**: Basketball factory now 90% complete (Foundations → Specialization → In-Season → [Post-Season pending]) -
