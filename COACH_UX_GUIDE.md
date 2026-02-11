# EPA v2.2 - COACH-FRIENDLY TOOLS USAGE GUIDE

**Date:** December 21, 2025  
**Version:** EPA v2.2 + Coach UX v1.0  
**Status:** Production-Ready

---

## 🎯 WHAT YOU JUST GOT

I've built **TWO powerful tools** to make EPA easier to use:

### **Tool 1: Coach-Friendly Message Wrapper**
Translates technical EPA responses into plain English with:
- ✅ Visual indicators (emojis)
- 📋 Clear problem explanations
- 💡 Actionable fix suggestions
- 📊 Weekly load tracking
- 🔧 Collapsible technical details

### **Tool 2: Interactive Session Builder**
No JSON required! Just answer questions:
- Step-by-step session creation
- Automatic validation
- Human-readable results
- Option to save sessions

---

## 📥 FILES YOU RECEIVED

Download these 3 new files from the chat outputs:

1. **`coach_messages.py`** - Message wrapper module
2. **`interactive_session_builder.py`** - Interactive tool
3. **`demo_coach_messages.py`** - Demo showing all features

**Save all to:** `C:\EFL-Governance-and-Programs\`

---

## 🚀 QUICK START GUIDE

### **Option A: Interactive Session Builder (Easiest)**

Perfect for coaches who don't want to write JSON.

**Step 1:** Run the interactive tool
```powershell
cd C:\EFL-Governance-and-Programs
python interactive_session_builder.py
```

**Step 2:** Answer the questions
```
Athlete name: Sarah Johnson
Age group: 2 (Youth 13-17)
Sport: Basketball
Current season: 1 (Off-Season)
Athlete readiness: 1 (GREEN)
...
```

**Step 3:** Get instant validation results
```
✅ SESSION APPROVED

This session meets all safety and compliance requirements.
You can proceed with programming this session.

📊 SESSION SUMMARY:
   Total Plyometric Contacts: 24
   Total Sprint Meters: 0
   CNS Demand: LOW

📈 WEEKLY LOAD TRACKING:
   Plyometric Contacts: 24 / 240 (10%) ✅
   Sprint Meters: 0 / 500 (0%) ✅
```

---

### **Option B: See All Examples (Demo)**

See the coach-friendly messages in action.

```powershell
python demo_coach_messages.py
```

**Shows 4 scenarios:**
1. ✅ Valid session (SUCCESS)
2. ❌ Weekly plyo cap exceeded (with fix suggestions)
3. ❌ RED readiness violation (with alternatives)
4. ❌ Adult MicroSession limit (with fixes)

---

### **Option C: Use in Your Own Scripts**

Add coach-friendly messages to your existing code.

```python
from epa_v2_2_full import EFLProgramArchitect
from coach_messages import format_epa_response
import json

# Initialize EPA
epa = EFLProgramArchitect(r"C:\EFL-Governance-and-Programs\EFL_Exercise_Library_v2_5.csv")

# Your session request (as JSON)
request = {
    "client_id": "ATHLETE_001",
    "population": "Youth_13_17",
    # ... rest of request
}

# Get EPA response
response_json = epa.process(json.dumps(request))

# Convert to coach-friendly message
friendly_message = format_epa_response(response_json)

# Display
print(friendly_message)
```

---

## 📊 BEFORE vs AFTER COMPARISON

### **BEFORE (Technical Output):**
```
{
  "status": "REJECTED_ILLEGAL",
  "reasons": [
    "WEEKLY_PLYO_CAP_EXCEEDED: Projected 262 > Cap 240"
  ],
  "validation_report": [
    {"gate_id": "5", "status": "FAIL"}
  ]
}
```

### **AFTER (Coach-Friendly Output):**
```
❌ SESSION REJECTED

📋 PROBLEM:

   Plyometric Contact Limit Exceeded:
   • Already used this week: 180 contacts
   • This session adds: 82 contacts
   • Total would be: 262 contacts
   • Your weekly limit: 240 contacts
   • Overage: 22 contacts

💡 HOW TO FIX:

   ✓ Reduce plyometric volume by 22 contacts:
     - Remove 1-2 sets from high-contact exercises
     - OR swap high-contact drills for lower-contact alternatives
     - OR move this session to next week

📈 WEEKLY LOAD TRACKING:
   Plyometric Contacts: 262 / 240 (109%) ❌
```

---

## 💡 EXAMPLE USE CASES

### **Use Case 1: Daily Session Validation**

**Scenario:** You plan tomorrow's session for 5 athletes

```powershell
# Run interactive builder for each athlete
python interactive_session_builder.py

# Or batch validate multiple sessions
python your_batch_script.py
```

**Result:** Get instant YES/NO for each session with specific fixes

---

### **Use Case 2: Weekly Planning Review**

**Scenario:** Sunday night, review all planned sessions for the week

```python
# Loop through all athletes
for athlete in athletes:
    for session in week_sessions:
        response = epa.process(session)
        friendly_msg = format_epa_response(response)
        
        if "REJECTED" in response:
            print(f"⚠️ {athlete.name} - Session {session.day}: NEEDS REVISION")
            print(friendly_msg)
```

**Result:** Catch compliance issues before the week starts

---

### **Use Case 3: Readiness-Based Adjustments**

**Scenario:** Athlete shows up RED readiness

```powershell
# Run interactive builder
# Select: RED readiness
# Tool automatically suggests recovery session
```

**Result:**
```
❌ RED Readiness Flag - No Plyometrics Allowed:
   • Athlete's readiness: RED (poor sleep/high stress/fatigue)
   • RED = Zero plyometric contacts allowed
   • Focus on mobility, skill work, and recovery only

💡 HOW TO FIX:
   ✓ Switch to mobility/recovery session:
     - Focus on foam rolling, stretching, breathing
     - Light movement only (walking, yoga, swimming)
     - Re-assess readiness tomorrow
```

---

## 🎨 MESSAGE FEATURES EXPLAINED

### **Visual Indicators**
- ✅ = Approved / Within limits
- ❌ = Rejected / Exceeded limits
- ⚠️ = Warning / Review needed
- 🔍 = Quarantined / Manual review
- 📋 = Problem description
- 💡 = Fix suggestions
- 📊 = Session summary
- 📈 = Weekly tracking
- 🔧 = Technical details

### **Problem Explanations**

The wrapper automatically translates technical reason codes:

| Technical Code | Coach-Friendly Explanation |
|----------------|---------------------------|
| `WEEKLY_PLYO_CAP_EXCEEDED` | "Plyometric Contact Limit Exceeded: You've used X contacts, this adds Y, total would be Z. Your limit is W." |
| `RED_READINESS_PLYO_VIOLATION` | "RED Readiness - No Plyometrics Allowed: Focus on mobility and recovery only." |
| `ADULT_MS_CONTACTS_EXCEEDED` | "Adult MicroSession Contact Limit Exceeded: MicroSessions capped at 60 contacts (not 84)." |
| `SPRINT_SESSION_CAP_EXCEEDED` | "Sprint Session Limit Exceeded: Already completed 3 sprint sessions this week." |

### **Fix Suggestions**

For each violation, the wrapper provides 2-3 actionable fixes:

**Example (Weekly Plyo Cap):**
```
💡 HOW TO FIX:
   ✓ Reduce plyometric volume by 22 contacts:
     - Remove 1-2 sets from high-contact exercises
     - OR swap high-contact drills for lower-contact alternatives
     - OR move this session to next week
```

---

## 🔧 ADVANCED USAGE

### **Customize Messages**

You can modify `coach_messages.py` to add your own explanations:

```python
# In coach_messages.py

def _explain_custom_violation(self, reason: str) -> str:
    if "MY_CUSTOM_RULE" in reason:
        return (
            f"   Custom Rule Violation:\n"
            f"   • Your custom explanation here\n"
        )
```

### **Hide Technical Details**

Don't want technical details shown?

```python
# In your script
builder = CoachMessageBuilder(response_dict)
message = builder.build_message(include_technical=False)  # No tech details
```

### **Extract Specific Info**

Need just the fix suggestions?

```python
builder = CoachMessageBuilder(response_dict)
fixes = builder._build_fix_suggestions()
print(fixes)
```

---

## 📋 INTERACTIVE BUILDER WORKFLOW

### **Full Session Creation Flow:**

```
1. CLIENT INFO
   - Name: Sarah Johnson
   - Age: Youth 13-17
   - Sport: Basketball

2. TRAINING CONTEXT
   - Season: Off-Season
   - Readiness: GREEN

3. WEEKLY PLAN
   - Week: 2026-W01
   - Sessions planned: 3
   - Sessions completed: 0

4. CURRENT LOAD
   - Plyo contacts: 0
   - Sprint meters: 0

5. EXERCISES
   - Exercise 1: Lateral Bound (3x8)
   - Exercise 2: Lateral Jumps (3x6)

6. VALIDATION
   ⚙️ Processing...
   ✅ SESSION APPROVED
```

---

## 🎯 BEST PRACTICES

### **For Coaches:**

1. **Start with Interactive Builder**
   - Learn the validation rules
   - See what gets rejected and why

2. **Use Demo for Training**
   - Show new coaches the 4 scenarios
   - Understand common violations

3. **Integrate into Workflow**
   - Validate sessions before entering in BridgeAthletic
   - Review weekly plans on Sundays

### **For Programmers:**

1. **Import the Wrapper**
   ```python
   from coach_messages import format_epa_response
   ```

2. **Always Format Responses**
   ```python
   raw_response = epa.process(request)
   friendly_response = format_epa_response(raw_response)
   ```

3. **Save Both Versions**
   ```python
   # For coaches
   with open("session_coach.txt", "w") as f:
       f.write(friendly_response)
   
   # For system
   with open("session_raw.json", "w") as f:
       f.write(raw_response)
   ```

---

## ❓ TROUBLESHOOTING

### **Issue: "Module not found: coach_messages"**

**Solution:**
```powershell
# Make sure coach_messages.py is in the same directory
cd C:\EFL-Governance-and-Programs
ls coach_messages.py  # Should show the file
```

### **Issue: Interactive builder crashes**

**Solution:**
```powershell
# Run with error details
python interactive_session_builder.py 2>&1
```

### **Issue: Messages not showing emojis**

**Solution:**
```powershell
# Windows PowerShell might not show emojis
# Use Windows Terminal instead
# Or run: [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

---

## 📞 NEXT STEPS

**You now have 3 ways to use EPA:**

1. **✅ Technical (JSON)** - `epa_v2_2_full.py`
2. **✅ Coach-Friendly (Wrapper)** - `coach_messages.py`
3. **✅ Interactive (No Code)** - `interactive_session_builder.py`

**Try them all and see which fits your workflow best!**

---

## 🎉 SUMMARY

**What Changed:**
- ❌ Before: Technical JSON output only
- ✅ After: Human-readable messages + interactive tool

**What You Can Do Now:**
- Build sessions without writing JSON
- Get plain English validation results
- See actionable fix suggestions
- Track weekly load visually

**Production Status:** ✅ Ready to use immediately

---

**END OF GUIDE**
