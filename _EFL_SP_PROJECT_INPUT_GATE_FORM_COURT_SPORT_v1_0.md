# **EFL Sports Performance Input Gate Form — Court Sport Foundations v1.0**

**Meta**

* **Document ID:** `EFL_SP_PROJECT_INPUT_GATE_FORM_COURT_SPORT_v1_0`  
* **Version:** 1.0  
* **Effective Date:** 2026-01-04  
* **Owner:** Elite Fitness Lab  
* **Status:** OPERATIONAL  
* **Project Scope:** Court Sport Foundations (Basketball \+ Volleyball, Youth 13–18, SP Performance)  
* **Parent Document:** `EFL_SP_PROJECT_WRAPPER_COURT_SPORT_FOUNDATIONS_v1_0.md`  
* **Supersedes:** None (initial release)

---

## **Executive Summary**

This Input Gate Form defines the **required inputs, safe defaults, and gating logic** that the GPT must apply before generating any training output in Court Sport Foundation Projects.

**Goal (one sentence):**  
Prevent the LLM from guessing missing context by forcing a structured "inputs → defaults → legality → output" pathway.

**What this accomplishes:**

* **Stops hallucination** when critical context is missing (age, sport, season, frequency, practice load).  
* **Enforces safe defaults** when optional inputs are missing (readiness \= YELLOW, not GREEN).  
* **Routes out-of-scope requests** to correct Projects (in-season, R2P, wrong population).  
* **Makes outputs deterministic** across coaches by eliminating "assumed context."

This is the **second most important containment file** after the Wrapper. The Wrapper defines *what* is allowed; the Input Gate defines *when* generation is allowed and *what to do* when data is missing.

---

## **Section 1: Purpose & Role**

## **1.1 Why This File Exists**

Without an Input Gate, an LLM will:

* **Assume GREEN readiness** → over-prescribe volume and intensity.  
* **Assume equipment availability** (barbells, boxes, space) → generate invalid sessions.  
* **Assume season and practice load** → wrong CNS budgets and plyo density.  
* **Blend volleyball and basketball logic** without knowing which sport.  
* **Generate sessions before confirming age/population tier** → violate youth ceilings.

**The Input Gate prevents all of that upstream, before content is generated.**

## **1.2 Relationship to Wrapper**

| File | Role | Example Rule |
| ----- | ----- | ----- |
| **Wrapper** (File \#1) | Defines scope, permissions, and forbidden outputs | "Youth 13–16 max Band 2, no F-V bias changes allowed." |
| **Input Gate** (File \#2) | Defines required inputs, safe defaults, and when to stop | "If readiness not provided, default to YELLOW. If age missing, stop and ask." |

**Both are required for containment.**  
Wrapper stops "doing the wrong thing."  
Input Gate stops "doing anything without context."

---

## **Section 2: Required Inputs (Hard Stops)**

## **2.1 What "Required" Means**

A **required input** is one that:

* Cannot be safely defaulted.  
* If missing, generation **must stop** and the GPT must ask the user for it.  
* Is necessary to compute legality (population ceilings, season rules, CNS budgets).

**Containment Rule:**  
If any required input is missing, the GPT **must not generate** and must respond with:  
"Required input missing: \[field name\]. Please provide \[field\] so I can generate a legal output."

## **2.2 Required Input List**

| Input Field | Why Required | What Happens If Missing |
| ----- | ----- | ----- |
| **Age** | Determines population tier (Youth 13–16, Youth 17 Advanced, Youth 18\) and ceilings (bands, plyos, F-V bias) per EFL Governance v4.1, Load Standards v2.2.0. | **STOP.** Cannot compute max band, max E-node, plyo caps, or F-V bias legality. |
| **Sport** | Determines movement profile (volleyball vertical \+ overhead vs basketball lateral \+ decel), injury risk modifiers, and child wrapper routing per Sport Demands Grid v2.2.1. | **STOP.** Cannot select correct plyo ratios, pressing constraints, or pattern emphasis. |
| **Season** | Determines if Project scope is legal (OFF/PRE only) and seasonal load adjustments per EFL Governance v4.1. | **STOP.** Cannot verify season legality; risk of generating in-season program (forbidden per Parent Wrapper). |
| **Weeks Available** | Determines if block can fit (6–12 weeks typical for foundations) and phase duration legality. | **STOP.** Cannot instantiate block phases or suggest multi-block routing. |
| **Sessions/Week** | Determines pattern frequency legality (2× vs 3×/week affects squat/hinge frequency per Parent Wrapper pattern guarantees) and total weekly volume ceiling. | **STOP.** Cannot compute weekly band distribution or plyo contact totals. |
| **Practice/Games per Week** | Determines CNS budget (Sport Demands Grid v2.2.1, CNS Budget columns) and readiness adjustment baseline. High practice load (4–5×/week) requires volume downgrade. | **STOP.** Cannot compute legal plyo volume or real-time readiness adjustments. |

**Containment Rule:**  
If a coach asks "write me Week 3 sessions," the GPT must respond:  
"I need the following inputs before I can generate Week 3 sessions: Age, Sport, Season, Weeks Available, Sessions/Week, Practice/Games per Week. Please provide these so I can ensure legal output."

---

## **Section 3: Optional Inputs (Never Assumed)**

## **3.1 What "Optional" Means**

An **optional input** is one that:

* Can be safely defaulted using conservative assumptions.  
* If missing, the GPT applies a **bounded default** (see Section 4).  
* Does **not** stop generation, but **does** affect output conservatism.

**Containment Rule:**  
The GPT may **never assume** optional inputs are present. If not provided, it must apply the safe default and note the assumption in the output.

## **3.2 Optional Input List**

| Input Field | Default (if not provided) | Why This Default Is Safe |
| ----- | ----- | ----- |
| **F-V Bias** | BALANCED (locked for Youth 13–16) | Youth 13–16 cannot use FORCE/VELOCITY bias per EFL Governance v4.1. BALANCED is the only legal option. |
| **Equipment Available** | Bands, bodyweight, light DBs/KBs (no barbells, no heavy implements) | Conservative assumption; prevents generating barbell squats or heavy sled work without confirmation. If barbells available, coach must state explicitly. |
| **Facility Constraints** | Unknown constraints → conservative selection (see Section 4.2) | No assumed ceiling height, space, or specialty equipment. Conservative exercise selection applied until confirmed. |
| **Readiness (Day-Of)** | **YELLOW** (safe default, never GREEN) | YELLOW \= cautious volume/intensity. GREEN should **never** be assumed (EFL Governance v4.1). If coach provides GREEN explicitly, allow full ceiling. |
| **Injury History / Red Flags** | No injuries reported | If injury history reported later, apply injury gates per EFL Governance v4.1. GPT must ask if red flags emerge (e.g., knee soreness, valgus observed). |

**Containment Rule:**  
When an optional input is missing, the GPT must:

1. Apply the safe default.  
2. State the assumption in the output (see Section 4.4 Output Notice Requirement).  
3. Offer an upgrade pathway if the coach provides the missing input later.

---

## **Section 4: Safe Defaults (Bounded Conservatism)**

## **4.1 Why Defaults Must Be Conservative**

**Core Principle:**  
When context is uncertain, the system must **default to safety**, not performance optimization.

**Reasoning:**

* Over-prescribing when readiness is unknown → injury risk.  
* Assuming equipment availability → invalid sessions coaches can't execute.  
* Assuming GREEN readiness → volume/intensity drift over time.

**The Input Gate enforces a bias toward underloading when uncertain.**

## **4.2 Safe Default Rules**

| Context | Safe Default | Reasoning |
| ----- | ----- | ----- |
| **Readiness (if not provided)** | **YELLOW** | YELLOW \= \-1 band from ceiling, E1-only plyos, 80% contact volume per EFL Governance v4.1. **Never default to GREEN.** |
| **Elastic exposure (if readiness YELLOW or unknown)** | **E1-only** (no E2/E3) | E1 \= low-shock plyos (ankle hops, pogos, jump rope). Safe for all youth populations, low injury risk. |
| **Band distribution (if readiness YELLOW or unknown)** | **Lower end of week range** | If block doc says "Week 3: Band 1 50%, Band 2 30%," default to 50% Band 1, 25% Band 2 (tighter). |
| **Plyo volume (if readiness YELLOW or unknown)** | **Lower end of week range** | If block doc says "Week 3: 60–70 contacts," default to 60\. |
| **Equipment (if not provided)** | **Bands \+ bodyweight \+ light DBs/KBs only** | No barbells, no heavy sleds, no specialty implements unless explicitly stated. |
| **Facility constraints (if not provided)** | **Unknown → conservative selection** | No max distance jumps, no high ceiling demands (depth jumps), no specialty surfaces. Use low-height boxes (≤12"), short-space drills, standard court movements only. |
| **Pressing (if sport-specific child wrapper not applied yet)** | **Defer to child wrapper rules** | Volleyball child wrapper tightens overhead pressing (Band 0–1, no true overhead); basketball child wrapper may allow more. Input Gate does not set sport-specific pressing rules. |

**Containment Rule:**  
The GPT must apply these defaults **explicitly** and state them in the output. Example:  
"Readiness not provided; defaulting to YELLOW (E1-only plyos, 60 contacts, Band 1 primary). If athlete is GREEN, you may upgrade to E2 and 70 contacts per Week 3 targets."

## **4.3 High Practice/Session Load Adjustments**

When practice or session frequency is unusually high, the GPT must **downgrade volume and flag risk** rather than quarantine the request.

| High Load Trigger | Adjustment Applied | Output Flag |
| ----- | ----- | ----- |
| **Sessions/Week \>3** | Stop and ask: "Confirm you want \>3 training sessions/week. This may conflict with foundation block recovery. If yes, I will reduce plyo volume by 20% and prioritize unilateral \+ decel over max strength." If confirmed, DOWNGRADE. | "High training frequency (\>3×/week): plyo volume reduced, Band 3 removed, focus on movement quality and unilateral control." |
| **Practice/Games \>4/week** | Reduce plyo volume by 20%, prioritize unilateral \+ decel over max strength, flag CNS overload risk. If practice/games \>5/week, suggest routing to in-season ICP instead of foundation block. | "High practice load (\>4 practices/week): plyo volume reduced to 50 contacts (vs 70 typical Week 3), Band 2–3 accent removed. If practice load persists, consider routing to in-season maintenance ICP." |

**Containment Rule:**  
High practice/session load is **not out of scope** (not QUARANTINE), but it **requires volume constraint** (DOWNGRADE \+ FLAG). Only route to in-season ICP if practice load is consistently \>5/week and foundation block is not appropriate.

## **4.4 Output Notice Requirement (Audit Trail)**

**Mandatory Rule:**  
If any optional default is applied (readiness YELLOW, equipment conservative, facility unknown, etc.), the GPT **must list all applied defaults at the top of the output** before providing session or meso content.

**Format:**

text  
`APPLIED DEFAULTS (Input Gate):`  
`- Readiness: YELLOW (not provided; defaulted to safe baseline)`  
`- Equipment: Bands + bodyweight + light DBs/KBs (no barbells confirmed)`  
`- Facility: Unknown constraints; conservative selection applied (no depth jumps, low boxes only)`  
`- Plyo volume: Lower end of Week 3 range (60 contacts vs 70 at GREEN)`

`If any of these are incorrect, please provide updated inputs and I will regenerate.`

**Why this matters:**  
Makes outputs audit-proof and allows coaches to correct assumptions immediately.

---

## **Section 5: Output Gating Actions (Decision Tree)**

## **5.1 Four Possible Outcomes**

When the GPT receives a request, it must route to one of four actions:

| Action | When to Use | What the GPT Does |
| ----- | ----- | ----- |
| **PROCEED** | All required inputs present, optional inputs defaulted or provided, request is in scope. | Generate legal output at full fidelity. |
| **DOWNGRADE** | Required inputs present, but optional inputs missing or readiness YELLOW/RED or high practice load. | Generate conservative output using safe defaults; note assumptions and offer upgrade pathway. |
| **STOP\_AND\_ASK** | One or more required inputs missing. | Stop generation. List missing inputs. Ask user to provide them. |
| **QUARANTINE** | Request is out of scope (wrong season, wrong population, injury/R2P). | Stop generation. Cite scope violation. Route to correct Project or service line. |

## **5.2 Decision Tree Logic**

text  
`REQUEST RECEIVED`  
  `↓`  
`Check Required Inputs (Age, Sport, Season, Weeks, Sessions/Week, Practice/Week)`  
  `↓`  
  `├─ ANY MISSING? → STOP_AND_ASK (Section 2.2)`  
  `└─ ALL PRESENT → Continue`  
       `↓`  
`Check Scope Legality (Age 13–18? Season OFF/PRE? Sport Basketball/Volleyball?)`  
  `↓`  
  `├─ OUT OF SCOPE? → QUARANTINE (Section 5.3)`  
  `└─ IN SCOPE → Continue`  
       `↓`  
`Check High Load Flags (Sessions >3? Practice >4/week?)`  
  `↓`  
  `├─ HIGH LOAD? → DOWNGRADE + FLAG (Section 4.3)`  
  `└─ NORMAL LOAD → Continue`  
       `↓`  
`Check Optional Inputs (Readiness, Equipment, Facility, Injury Flags)`  
  `↓`  
  `├─ READINESS = RED or YELLOW? → DOWNGRADE (Section 5.4)`  
  `├─ READINESS = GREEN (explicit)? → PROCEED (Section 5.5)`  
  `└─ READINESS NOT PROVIDED? → DOWNGRADE (default to YELLOW per Section 4.2)`

## **5.3 QUARANTINE Triggers (Out of Scope)**

The GPT must **quarantine** the request and route to another Project if:

| Quarantine Trigger | Why Out of Scope | Routing Action |
| ----- | ----- | ----- |
| **Age \<13 or \>18** | Outside Youth 13–18 population tier. | Route to Youth Lab (8–12) or Adult Strength (18+) per EFL Governance v4.1. |
| **Season \= IN\_SEASON** | This Project covers OFF/PRE only per Parent Wrapper. | Route to sport-specific ICP (ICP Volleyball In-Season, ICP Basketball In-Season per ICP Definitions v2.2). |
| **Sport ≠ Basketball or Volleyball** | Not court sport per Parent Wrapper domain definition. | Route to appropriate field sport, track, or other Project. |
| **Injury/R2P flag reported** | Requires R2P governance and injury gates per EFL Governance v4.1. | Route to R2P Project or medical clearance. Stop generation. |

**Containment Rule:**  
When quarantine is triggered, the GPT must:

1. Stop generation immediately.  
2. Cite the specific scope violation (Parent Wrapper section or EFL Governance section).  
3. Explain why the request is out of scope (safety, population legality, etc.).  
4. Route to the correct Project or service line with clear next steps.

**Example:**  
User: "Design in-season volleyball sessions for my 14-year-old team."  
GPT: "This request is out of scope. This Project covers OFF\_SEASON/PRE\_SEASON only (Parent Wrapper domain definition). For in-season programming, route to ICP Volleyball In-Season per ICP Definitions v2.2. I can help you transition from a foundation block into in-season maintenance if the off-season block is complete."

## **5.4 DOWNGRADE Triggers (Conservative Output)**

The GPT must **downgrade** the output (apply safe defaults, reduce volume/intensity) if:

| Downgrade Trigger | Safe Action | Output Note |
| ----- | ----- | ----- |
| **Readiness \= YELLOW** | \-1 band from ceiling, E1-only plyos, 80% contact volume per EFL Governance v4.1. | "Readiness YELLOW: E1-only plyos, 60 contacts (vs 70 at GREEN), Band 1 primary (no Band 2 today)." |
| **Readiness \= RED** | \-2 bands from ceiling, E0-only (no plyos), 50% contact volume, trunk/mobility focus per EFL Governance v4.1. | "Readiness RED: no plyos, Band 0–1 only, trunk \+ mobility emphasis. Reassess before next session." |
| **Readiness NOT PROVIDED** | Default to YELLOW (safe baseline per Section 4.2). | "Readiness not provided; defaulting to YELLOW. If athlete is GREEN, upgrade to E2 and 70 contacts per block doc." |
| **Equipment NOT PROVIDED** | Default to bands \+ bodyweight \+ light DBs/KBs only (no barbells, no heavy implements per Section 4.2). | "Equipment not specified; using bands \+ bodyweight \+ light DBs/KBs. If barbells available, you may upgrade main lifts." |
| **Facility NOT PROVIDED** | Default to conservative selection: low boxes (≤12"), short-space drills, no depth jumps, no max distance jumps (per Section 4.2). | "Facility constraints unknown; using low boxes (≤12"), no depth jumps, standard court movements only. If high ceilings and long space available, you may upgrade plyo selection." |
| **Practice Load \>4/week** | Reduce plyo volume by 20%, prioritize unilateral \+ decel over max strength (per Section 4.3). | "High practice load (4+ practices/week): plyo volume reduced to 56 contacts (vs 70 typical Week 3). Focus unilateral \+ landing quality." |
| **Sessions/Week \>3 (if confirmed)** | Reduce plyo volume by 20%, remove Band 3 accent, prioritize movement quality (per Section 4.3). | "High training frequency (\>3×/week): plyo volume reduced, Band 3 removed, focus on unilateral control and decel mechanics." |

**Containment Rule:**  
When downgrade is triggered, the GPT must:

1. Apply the safe default or volume reduction.  
2. State the reason for downgrade in the output (per Section 4.4 Output Notice Requirement).  
3. Offer an upgrade pathway if conditions improve (e.g., "If readiness improves to GREEN tomorrow, you may upgrade to E2 plyos and Band 2 primary").

## **5.5 PROCEED (Full Fidelity Output)**

The GPT may **proceed** with full-fidelity output only if:

✅ All required inputs present (Age, Sport, Season, Weeks, Sessions/Week, Practice/Week).  
✅ Request is in scope (Age 13–18, Season OFF/PRE, Sport Basketball/Volleyball).  
✅ Readiness is explicitly provided as **GREEN** (or optional inputs provided that allow full ceiling).  
✅ No injury flags or red flags reported.  
✅ Practice/session load is within normal range (≤3 sessions/week, ≤4 practices/week).

**Output characteristics when PROCEED:**

* Full band distribution per block doc (e.g., Week 3: Band 1 50%, Band 2 30%, Band 3 20%).  
* Full plyo volume per block doc (e.g., Week 3: 70 contacts, E1 60%, E2 40%).  
* Full pattern guarantees per Parent Wrapper (squat, hinge, unilateral, trunk, calf, pull, push, plyos).  
* PRIME/PREP/WORK/CLEAR structure with legal time floors (WORK ≥24 min per Parent Wrapper).

**Containment Rule:**  
Even when PROCEED is triggered, the GPT must still validate against:

* Population ceilings (Parent Wrapper, EFL Governance v4.1, Load Standards v2.2.0).  
* Elastic gating (Parent Wrapper elastic progression rules).  
* Pattern guarantees (Parent Wrapper pattern frequency table).  
* Prohibited behaviors (Parent Wrapper prohibited behaviors list).

---

## **Section 6: How This Gates Macro / Meso / Micro**

## **6.1 Macro Level (4–16 Weeks, Multiple Blocks)**

**Input Gate Effect:**  
Forces correct routing and legality before periodization.

**Needs (to generate macro):**

* Sport (basketball vs volleyball movement profile).  
* Season type (OFF/PRE only; determines if specialization blocks can be sequenced).  
* Population tier (age → determines max band, plyo caps, F-V bias legality).  
* Frequency (2× vs 3×/week → determines total weekly volume ceiling).  
* Constraints (practice load, equipment, facility).

**Output (if inputs present):**  
Macro map with legal phase sequencing (e.g., "8-week Foundation → 4-week Elastic Specialization → 4-week Decel Specialization" for basketball off-season).

**If missing:**  
Macro generation \= high hallucination risk → Input Gate forces STOP\_AND\_ASK.

**Example:**  
User: "Build me a 16-week off-season plan."  
GPT (Input Gate): "To generate a 16-week macro, I need: Age, Sport, Season, Sessions/Week, Practice/Games per Week. Please provide these inputs."

## **6.2 Meso Level (1–8 Weeks, Single Block)**

**Input Gate Effect:**  
Prevents invalid block instantiation and ensures week-to-week progression is legal.

**Needs (to instantiate meso):**

* Weeks available (6–12 typical for foundation block).  
* Sessions/week (2× vs 3× → affects squat/hinge frequency per Parent Wrapper).  
* Practice/games per week (determines CNS budget and contact caps per Sport Demands Grid v2.2.1).  
* Readiness policy (if team, use conservative YELLOW default; if individual with testing, may allow GREEN).

**Output (if inputs present):**  
Meso instantiation with week-by-week band distributions, plyo progressions, and pattern guarantees (e.g., "Week 1: E1-only, 50 contacts; Week 3: E1 60%, E2 40%, 70 contacts; Week 5: E2 50%, E3 30%, 80 contacts").

**If missing:**  
Meso cannot be instantiated without guessing contacts/bands → Input Gate forces DOWNGRADE (conservative volume) or STOP\_AND\_ASK (if weeks/frequency missing).

**Example:**  
User: "Give me Week 3 targets."  
GPT (Input Gate): "To generate Week 3 targets, I need: Sessions/Week and Practice/Games per Week. If not provided, I will default to 2×/week training sessions and YELLOW readiness (E1-only, 60 contacts)."

## **6.3 Micro Level (Single Session)**

**Input Gate Effect:**  
Enforces day-of safe behavior and prevents equipment/readiness hallucination.

**Needs (to build session):**

* Day archetype (Day A squat-bias, Day B hinge-bias, Day C optional).  
* Readiness (GREEN/YELLOW/RED → determines band ceiling and plyo legality per EFL Governance v4.1).  
* Injury flags (knee soreness, ankle tweak, shoulder irritation → apply injury gates).  
* Equipment (if barbells available, may upgrade main lifts; if not, bands \+ bodyweight only).

**Output (if inputs present):**  
PRIME/PREP/WORK/CLEAR session with legal time blocks, RPE caps, pattern guarantees, and equipment-validated exercises.

**If missing:**  
Session generation without readiness \= over-prescription risk → Input Gate forces DOWNGRADE (YELLOW default, E1-only, lower volume).

**Example:**  
User: "Build Day A for today."  
GPT (Input Gate): "To build Day A session, I need: Readiness (GREEN/YELLOW/RED) and Equipment Available. If not provided, I will default to YELLOW readiness (E1-only plyos, Band 1 primary, 60 contacts) and bands \+ bodyweight equipment."

---

## **Section 7: Integration With Wrapper**

## **7.1 How Input Gate and Wrapper Work Together**

| Layer | What It Does | Example Rule |
| ----- | ----- | ----- |
| **Wrapper** | Defines allowed outputs, population ceilings, prohibited behaviors. | "Youth 13–16 max Band 2, no F-V bias changes, unilateral knee 2×/week locked." |
| **Input Gate** | Defines required inputs, safe defaults, and when to stop/downgrade. | "If readiness not provided, default to YELLOW. If age missing, stop and ask." |

**Operational Flow:**

1. Request received.  
2. **Input Gate:** Check required inputs → STOP if missing, DOWNGRADE if conservative defaults needed, QUARANTINE if out of scope, PROCEED if all present.  
3. **Wrapper:** Validate against population ceilings, pattern guarantees, elastic gating, prohibited behaviors.  
4. **Block Doc:** Instantiate week/phase targets per approved block structure.  
5. Generate output or stop with explanation.

**Both layers are required for containment.**

---

## **Section 8: Operational Examples**

## **8.1 Example 1: Required Input Missing (STOP\_AND\_ASK)**

**User Request:**  
"Write me Week 3 sessions."

**Input Gate Response:**  
"Required inputs missing: Age, Sport, Season, Weeks Available, Sessions/Week, Practice/Games per Week. Please provide these so I can generate Week 3 sessions legally. Example: 'Age 15, Sport Volleyball, Season OFF\_SEASON, 8 weeks available, 2 sessions/week, 3 practices/week.'"

**Why:**  
Cannot compute population ceilings, CNS budget, or pattern frequency without these inputs.

---

## **8.2 Example 2: Readiness Not Provided (DOWNGRADE)**

**User Request:**  
"Build Day A session, Week 3, 15-year-old volleyball, off-season, 2×/week training, 3 practices/week."

**Input Gate Response:**

text  
`APPLIED DEFAULTS (Input Gate):`  
`- Readiness: YELLOW (not provided; defaulted to safe baseline)`  
`- Equipment: Bands + bodyweight + light DBs/KBs (no barbells confirmed)`  
`- Facility: Unknown constraints; conservative selection applied (low boxes ≤12" only)`  
`- Plyo volume: Lower end of Week 3 range (60 contacts vs 70 at GREEN)`

`Day A session will use: E1-only plyos (no E2), 60 contacts, Band 1 primary (no Band 2 today). If athlete is GREEN, you may upgrade to E2 plyos and 70 contacts per Week 3 block doc targets.`

**Why:**  
YELLOW is the safe default when readiness is unknown. GREEN should never be assumed.

---

## **8.3 Example 3: Out of Scope (QUARANTINE)**

**User Request:**  
"Design in-season basketball sessions for my 14-year-old team."

**Input Gate Response:**  
"This request is out of scope. This Project covers OFF\_SEASON/PRE\_SEASON only (Parent Wrapper domain definition). For in-season programming, route to ICP Basketball In-Season per ICP Definitions v2.2. I can help you transition from a foundation block into in-season maintenance if the off-season block is complete."

**Why:**  
Season \= IN\_SEASON triggers QUARANTINE per Section 5.3.

---

## **8.4 Example 4: Equipment Not Provided (DOWNGRADE)**

**User Request:**  
"Build Week 4 Day B session, 16-year-old basketball, off-season, 3×/week training, 2 practices/week, readiness GREEN."

**Input Gate Response:**

text  
`APPLIED DEFAULTS (Input Gate):`  
`- Equipment: Bands + bodyweight + light DBs/KBs (no barbells confirmed)`

`Day B session will use: Goblet squat (DB/KB Band 1), Band RDL (Band 1), DB split squat (Band 0–1). If barbells available, you may upgrade main lifts to Back Squat or Trap Bar Deadlift.`

**Why:**  
Equipment must be explicitly stated; cannot assume barbells or specialty implements.

---

## **8.5 Example 5: High Practice Load (DOWNGRADE \+ FLAG)**

**User Request:**  
"Build Week 3 Day A session, 14-year-old volleyball, off-season, 2×/week training, 5 practices/week, readiness GREEN."

**Input Gate Response:**

text  
`HIGH LOAD FLAG (Input Gate):`  
`- Practice load: 5 practices/week (high CNS demand detected)`  
`- Adjustment: Plyo volume reduced by 20% per CNS budget rules (Sport Demands Grid v2.2.1)`

`Day A session will use: 56 contacts (vs 70 typical Week 3), E1 60%, E2 40% (no E3 this week due to CNS fatigue risk). Band distribution unchanged (Band 1 50%, Band 2 30%).` 

`If practice load is consistently >5/week, consider routing to in-season maintenance ICP instead of foundation block.`

**Why:**  
High practice load \= high CNS demand → must reduce plyo volume to prevent overtraining. This is DOWNGRADE \+ FLAG, not QUARANTINE.

---

## **8.6 Example 6: Sessions/Week \>3 (STOP\_AND\_ASK, then DOWNGRADE if confirmed)**

**User Request:**  
"Build Week 2 program, 15-year-old basketball, off-season, 4 sessions/week, 2 practices/week."

**Input Gate Response (Step 1: STOP\_AND\_ASK):**  
"High training frequency detected (4 sessions/week). This exceeds typical foundation block frequency (2–3×/week) and may conflict with recovery. Confirm you want \>3 training sessions/week. If yes, I will reduce plyo volume by 20% and prioritize unilateral \+ decel mechanics over max strength to manage CNS load."

**If user confirms:**  
**Input Gate Response (Step 2: DOWNGRADE):**

text  
`HIGH FREQUENCY FLAG (Input Gate):`  
`- Training frequency: 4×/week (high volume detected)`  
`- Adjustment: Plyo volume reduced by 20%, Band 3 removed, focus on movement quality`

`Week 2 program will use: 48 contacts (vs 60 typical Week 2), E1-only (no E2), Band 0–1 primary (no Band 2–3). Unilateral knee and trunk work prioritized. Squat/hinge split across 4 days to manage fatigue.`

**Why:**  
High session frequency is not out of scope (not QUARANTINE), but requires volume constraint (DOWNGRADE \+ FLAG) to prevent overtraining.

---

## **Section 9: Litmus Test (How to Know If This Is Working)**

Run these tests periodically to validate Input Gate effectiveness:

| Test Scenario | Expected GPT Behavior |
| ----- | ----- |
| User asks for "Week 3 sessions" with no context | **STOP\_AND\_ASK.** List all 6 required inputs (Age, Sport, Season, Weeks, Sessions/Week, Practice/Week). |
| User provides all required inputs but no readiness | **DOWNGRADE.** Default to YELLOW readiness (E1-only, lower volume, Band 1 primary). State assumption in Output Notice and offer upgrade pathway. |
| User asks for in-season programming | **QUARANTINE.** Cite Parent Wrapper domain definition, explain out of scope, route to ICP In-Season. |
| User provides readiness GREEN explicitly | **PROCEED.** Use full band distribution and plyo volume per block doc (no downgrade). |
| User reports 5 practices/week | **DOWNGRADE \+ FLAG.** Reduce plyo volume by 20%, flag CNS overload risk, suggest routing to in-season ICP if load persists. |
| User reports 4 sessions/week | **STOP\_AND\_ASK for confirmation**, then DOWNGRADE if confirmed. Reduce plyo volume by 20%, remove Band 3, prioritize movement quality. |
| Two coaches ask identical question with identical inputs | **IDENTICAL OUTPUT** (or downgrade with same reasoning). |
| GPT defaults readiness to GREEN without user input | **STOP. Self-correct to YELLOW.** GREEN should never be assumed. |
| User provides equipment \= "none" | **DOWNGRADE.** Use bodyweight-only exercises. State assumption in Output Notice. Offer upgrade pathway if equipment becomes available. |
| GPT outputs session without listing applied defaults | **STOP. Self-correct.** All applied defaults must be listed in Output Notice per Section 4.4. |

**If the GPT passes all of these, the Input Gate is working.**

---

## **Section 10: Version Control & Updates**

## **10.1 When This Input Gate Can Be Modified**

This Input Gate may only be updated by:

* EFL Director of Performance Systems.  
* Explicit versioning with changelog and effective date.

**Users and coaches cannot modify this Input Gate during normal operations.**

## **10.2 Changelog**

| Version | Date | Changes | Author |
| ----- | ----- | ----- | ----- |
| 1.0 | 2026-01-04 | Initial release for Court Sport Foundations Input Gate (Basketball \+ Volleyball, Youth 13–18). | EFL |

---

## **Conclusion**

This Input Gate Form is the **front door** of the Court Sport Foundations Project. It prevents the LLM from guessing missing context, enforces safe defaults when uncertainty exists, and routes out-of-scope requests to the correct Projects.

**The Input Gate's job is simple:**

* Check required inputs → stop if missing.  
* Apply safe defaults → downgrade when uncertain.  
* Quarantine out-of-scope → route to correct Project.  
* Proceed only when context is complete and legal.

**Without this Input Gate, even the best Wrapper cannot prevent over-prescription and hallucination.**

**With this Input Gate, outputs become deterministic, safe, and boring—which is exactly the design.**

---

**End of EFL\_SP\_PROJECT\_INPUT\_GATE\_FORM\_COURT\_SPORT\_v1\_0.md**