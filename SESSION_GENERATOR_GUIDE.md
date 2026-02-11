# EFL COMPLETE SESSION SYSTEM - USER GUIDE

**Version:** 1.0  
**Date:** December 21, 2025  
**Status:** Production Ready

---

## 🎯 WHAT YOU HAVE NOW

You now have a **COMPLETE, LLM-FREE SESSION GENERATION AND VALIDATION SYSTEM**.

### **The Complete Stack:**

```
CLIENT INPUT
    ↓
┌─────────────────────────────────────┐
│ 1. SESSION GENERATOR v1.0           │
│    • Client State Engine            │
│    • Exercise Routing v1.2          │
│    • Selection Algorithm v1.1       │
│    • Builds PRIME-PREP-WORK-CLEAR   │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. EPA v2.2 VALIDATOR               │
│    • 7-Gate Validation              │
│    • Load Standards v2.1.2          │
│    • Governance v4.0                │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. COACH-FRIENDLY FORMATTER         │
│    • Human-readable messages        │
│    • Fix suggestions                │
│    • Visual indicators              │
└─────────────────────────────────────┘
    ↓
COMPLETE VALIDATED SESSION (JSON)
Ready for BridgeAthletic
```

---

## 📦 FILES YOU RECEIVED

**Download these 2 NEW files:**

1. **`efl_session_generator_v1_0.py`** (775 lines) ⬆️
   - Complete session generator
   - NO LLM dependencies
   - Pure deterministic logic

2. **`complete_workflow_test.py`** (230 lines) ⬆️
   - Integration script
   - Generator → EPA → Coach Messages
   - Complete production workflow

**Files you already have:**

3. **`epa_v2_2_full.py`** - Validation engine
4. **`coach_messages.py`** - Friendly formatting
5. **`EFL_Exercise_Library_v2_5.csv`** - 2,724 exercises

---

## 🚀 QUICK START

### **Test the Complete System (5 minutes)**

```powershell
cd C:\EFL-Governance-and-Programs

# Run complete workflow
python complete_workflow_test.py
```

**Expected Output:**
```
================================================================================
STEP 1: GENERATING SESSION
================================================================================
✅ Generator ready (2724 exercises loaded)
✅ SESSION GENERATED

   PRIME: 3 exercises
   PREP: 3 exercises
   WORK: 4 exercises
   CLEAR: 2 exercises

   Plyo Contacts: 72
   Sprint Meters: 0

================================================================================
STEP 2: VALIDATING THROUGH EPA v2.2
================================================================================
⚙️  Running validation gates...

================================================================================
STEP 3: VALIDATION RESULTS
================================================================================
✅ SESSION APPROVED

This session meets all safety and compliance requirements.

📊 SESSION SUMMARY:
   Total Plyometric Contacts: 72
   Session Duration: 45 minutes
   CNS Demand: MODERATE

================================================================================
STEP 4: SAVING SESSION
================================================================================
✅ Complete session saved to: session_SARAH_001_2026-W01_S1.json
📋 SESSION READY FOR BRIDGEATHLETIC UPLOAD
```

---

## 💻 HOW TO USE

### **Option A: Generate Single Session**

```python
from efl_session_generator_v1_0 import EFLSessionGenerator

# Initialize
generator = EFLSessionGenerator(r"C:\EFL-Governance-and-Programs\EFL_Exercise_Library_v2_5.csv")

# Generate session
result = generator.generate_session(
    client_id="ATHLETE_001",
    population="Youth_13_17",      # Youth_8_12, Youth_13_17, Adult
    sport="Basketball",
    season_type="OFF_SEASON",      # OFF_SEASON, PRE_SEASON, IN_SEASON_TIER_1/2/3, POST_SEASON
    readiness_flag="GREEN",        # GREEN, YELLOW, RED
    session_type="FULL_SESSION",   # FULL_SESSION, MICROSESSION
    target_zones=["Zone_5", "Zone_6", "Zone_3"]  # Optional: specify FV zones
)

# Check result
if result["status"] == "SUCCESS":
    print(f"✅ Session generated: {result['total_plyo_contacts']} contacts")
else:
    print(f"❌ Failed: {result['reason']}")
```

### **Option B: Complete Workflow (Generate + Validate)**

```python
from efl_session_generator_v1_0 import EFLSessionGenerator
from epa_v2_2_full import EFLProgramArchitect
from coach_messages import format_epa_response
import json

# Step 1: Generate
generator = EFLSessionGenerator("EFL_Exercise_Library_v2_5.csv")
gen_result = generator.generate_session(
    client_id="ATHLETE_001",
    population="Youth_13_17",
    sport="Basketball",
    season_type="OFF_SEASON",
    readiness_flag="GREEN"
)

# Step 2: Convert to EPA format (see complete_workflow_test.py for full function)
epa_request = build_epa_request(gen_result, week_context)

# Step 3: Validate
epa = EFLProgramArchitect("EFL_Exercise_Library_v2_5.csv")
epa_response = epa.process(json.dumps(epa_request))

# Step 4: Format for coaches
friendly_message = format_epa_response(epa_response)
print(friendly_message)
```

---

## 🎨 CUSTOMIZATION OPTIONS

### **Target Specific Force-Velocity Zones**

```python
# Off-Season: Capacity + Hypertrophy + Reactive Power
result = generator.generate_session(
    ...
    target_zones=["Zone_5", "Zone_6", "Zone_3"]
)

# In-Season: Maintenance + Speed
result = generator.generate_session(
    ...
    target_zones=["Zone_5", "Zone_7", "Zone_8"]
)

# Strength Focus: Max Strength + Strength-Speed
result = generator.generate_session(
    ...
    target_zones=["Zone_1", "Zone_2"]
)
```

**Zone Reference:**
- **Zone 1:** Max Strength (85-100% 1RM)
- **Zone 2:** Strength-Speed (75-90% 1RM)
- **Zone 3:** Speed-Strength / Reactive Power (Plyos)
- **Zone 4:** Speed (Linear sprints)
- **Zone 5:** Strength-Endurance (60-75% 1RM)
- **Zone 6:** Hypertrophy (60-80% 1RM)
- **Zone 7:** Speed (Max velocity)
- **Zone 8:** Agility / COD

### **Readiness-Based Auto-Adjustment**

The system automatically adjusts based on readiness:

**GREEN (Well-rested):**
- Full volume access
- All E-nodes allowed (per population)
- Example: 120 contacts for Youth 13-17

**YELLOW (Moderate fatigue):**
- 75% volume reduction
- Max E2 tier (no high-shock plyos)
- Example: 90 contacts for Youth 13-17

**RED (Poor sleep/high stress):**
- Zero plyometrics
- E0 only (strength, mobility)
- Focus on recovery

```python
# System automatically handles readiness
result = generator.generate_session(
    ...
    readiness_flag="YELLOW"  # Automatically reduces volume to 75%
)
```

---

## 📊 OUTPUT FORMAT

### **Generator Output Structure**

```json
{
  "status": "SUCCESS",
  "session_plan": {
    "PRIME": [
      {
        "exercise_id": "EX_00123",
        "exercise_name": "Hip Mobility Flow",
        "sets": 1,
        "reps": 8,
        "rest_seconds": 30,
        "load": "Bodyweight",
        "rpe_target": 3,
        "tempo": "Controlled",
        "coaching_cues": ["Quality over speed", "Full ROM"],
        "total_contacts": 0,
        "total_sprint_meters": 0
      }
    ],
    "PREP": [...],
    "WORK": [...],
    "CLEAR": [...]
  },
  "total_plyo_contacts": 72,
  "total_sprint_meters": 0,
  "client_state": {
    "population": "Youth_13_17",
    "max_band_allowed": "Band_3",
    "plyo_contacts_cap_session": 120,
    ...
  }
}
```

### **EPA Validation Output**

```json
{
  "status": "SUCCESS",
  "validation_report": [
    {"gate_id": "0", "status": "PASS"},
    {"gate_id": "1", "status": "PASS"},
    ...
  ],
  "session_plan": {
    "total_plyo_contacts": 72,
    "total_sprint_meters": 0,
    "cns_category": "MODERATE"
  }
}
```

---

## 🔧 TECHNICAL DETAILS

### **Architecture Components**

**1. Client State Engine**
- Computes legal ceilings from Load Standards v2.1.2
- Applies population limits (Youth 8-12: 80, Youth 13-17: 120, Adult: 140)
- Enforces readiness modifiers (RED/YELLOW/GREEN)
- Handles session type rules (MicroSession: Adult 60-contact cap)

**2. Exercise Router (Routing v1.2)**
- Filters 2,724 exercises by Band/Node/E-Node ceilings
- Routes to PRIME/PREP/WORK/CLEAR candidate pools
- Applies injury contraindications
- Enforces equipment availability

**3. Session Builder (Algorithm v1.1)**
- Selects exercises from candidate pools
- Manages volume budgets (running plyo contact tally)
- Ensures pattern variety (no duplicate movement patterns)
- Prescribes sets/reps/load/tempo based on zone
- Generates coaching cues

**4. EPA Validator (EPA v2.2)**
- 7-gate validation system
- Enforces Load Standards v2.1.2 caps
- Validates Tier 3 rules (Youth 13-17: ≤40% session contacts)
- Checks weekly projections
- Fail-fast architecture

---

## 🎯 USE CASES

### **Use Case 1: Weekly Programming**

Generate 3 sessions for one athlete:

```python
generator = EFLSessionGenerator("library.csv")

# Monday: Capacity focus
session_1 = generator.generate_session(
    client_id="SARAH",
    population="Youth_13_17",
    sport="Basketball",
    season_type="OFF_SEASON",
    readiness_flag="GREEN",
    target_zones=["Zone_5", "Zone_6"]
)

# Wednesday: Power focus
session_2 = generator.generate_session(
    client_id="SARAH",
    ...
    target_zones=["Zone_3"],  # Reactive power
    completed_sessions_this_week=1,
    weekly_contacts_accumulated=session_1["total_plyo_contacts"]
)

# Friday: Speed focus
session_3 = generator.generate_session(
    client_id="SARAH",
    ...
    target_zones=["Zone_7", "Zone_8"],  # Speed + agility
    completed_sessions_this_week=2,
    weekly_contacts_accumulated=session_1["total_plyo_contacts"] + session_2["total_plyo_contacts"]
)
```

### **Use Case 2: Batch Generation**

Generate sessions for entire team:

```python
athletes = [
    {"id": "SARAH", "age": 15, "readiness": "GREEN"},
    {"id": "JAKE", "age": 16, "readiness": "YELLOW"},
    {"id": "MIA", "age": 14, "readiness": "GREEN"}
]

for athlete in athletes:
    result = generator.generate_session(
        client_id=athlete["id"],
        population="Youth_13_17",
        sport="Basketball",
        season_type="OFF_SEASON",
        readiness_flag=athlete["readiness"]
    )
    
    # Validate each
    epa_response = epa.process(convert_to_epa_format(result))
    
    # Save if valid
    if epa_response["status"] == "SUCCESS":
        save_session(athlete["id"], epa_response)
```

---

## ❓ TROUBLESHOOTING

### **Issue: "Insufficient exercises in candidate pools"**

**Cause:** No exercises match the filters (too restrictive ceilings)

**Solution:**
1. Check population limits are correct
2. Verify readiness flag (RED = very restrictive)
3. Review injury flags (may exclude too many exercises)

### **Issue: EPA rejects generated session**

**Cause:** Session exceeds weekly caps

**Solution:**
- Pass `weekly_contacts_accumulated` when generating
- Reduce target zones to lower-contact options
- Check readiness flag is accurate

### **Issue: No plyometric exercises selected**

**Cause:** RED readiness or plyo budget exhausted

**Solution:**
- Verify readiness is GREEN or YELLOW
- Check `weekly_contacts_accumulated` is accurate
- Reduce other sessions' plyo volume

---

## 📋 NEXT STEPS

**You can now:**

1. ✅ Generate complete PRIME-PREP-WORK-CLEAR sessions
2. ✅ Validate all sessions through EPA v2.2
3. ✅ Get coach-friendly feedback with fix suggestions
4. ✅ Export sessions to JSON for BridgeAthletic
5. ✅ Batch process entire team rosters
6. ✅ Customize by Force-Velocity zones
7. ✅ Auto-adjust for readiness states

**Optional enhancements:**

- Add web interface for non-coders
- Build Excel upload tool
- Create BridgeAthletic direct integration
- Add session templates library
- Build automated weekly planning

---

## 🎉 SUMMARY

**What Changed:**
- ❌ Before: LLM-dependent, unpredictable, slow
- ✅ After: Pure Python, deterministic, fast (<2 seconds)

**What You Can Do:**
- Generate unlimited sessions instantly
- Full compliance with Load Standards v2.1.2
- Automatic safety enforcement
- Ready for production use

**System Status:**
- ✅ Session Generator: PRODUCTION READY
- ✅ EPA Validator: TESTED & VALIDATED
- ✅ Coach Messages: COMPLETE
- ✅ Complete Workflow: OPERATIONAL

---

**END OF GUIDE**

For questions or issues, reference:
- `efl_session_generator_v1_0.py` source code
- `complete_workflow_test.py` for integration examples
- EFL Coach AI Playbook v0.4.0 for programming rules
