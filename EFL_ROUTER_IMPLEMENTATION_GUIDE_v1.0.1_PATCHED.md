# EFL Global Router Implementation Guide v1.0.1 (PATCHED)
**Companion to:** EFL_GLOBAL_CLIENT_STATE_v1.0.2.json

## Overview
This guide provides the exact implementation contract for the EFL Global Router — the legality engine that evaluates client state and produces routing decisions.

**v1.0.1 PATCHES:**
- Fixed: seasontype collapse no longer defaults to 'OFFSEASON' (respects "never default" rule)
- Updated: Schema reference to v1.0.2 (includes ACL-only R2P conditional, uniqueItems, minLength, projecthistory required fields)

---

## Router Function Signature

```javascript
/**
 * EFL Global Router - Legality Engine
 * @param {ClientState} inputState - Current client state (includes inputs + optional prior derived/decisions)
 * @param {string} routerVersion - Router version identifier (must be in allowlist)
 * @param {string} nowISO - Current timestamp in ISO8601 format
 * @returns {ClientState} - Fully populated state with atomic header+decisions update
 */
function routeClientState(inputState, routerVersion, nowISO) {
  // Implementation follows 3-phase validation + routing logic
}
```

---

## Three-Phase Validation Contract

### Phase 1: Schema Validation
**Purpose:** Validate output structure against JSON Schema v1.0.2  
**Validator:** Ajv v8+ with strict mode  
**On Failure:** Return collapse state with `ROUTEROUTPUTINCOMPLETE`

```javascript
const Ajv = require('ajv');
const addFormats = require('ajv-formats');

const ajv = new Ajv({
  strict: true,           // Enforce strict schema rules
  allErrors: true,        // Collect all validation errors
  validateFormats: true   // Validate date-time formats
});
addFormats(ajv);

const schema = require('./EFL_GLOBAL_CLIENT_STATE_v1.0.2.json');
const validate = ajv.compile(schema);

// Validate output
if (!validate(outputState)) {
  console.error('Schema validation failed:', validate.errors);
  return collapseState('ROUTEROUTPUTINCOMPLETE', inputState, nowISO);
}
```

**v1.0.2 Schema Enforcement:**
- ACL-only R2P conditional (weekspostop/grafttype only for ACL injuries)
- projecthistory items require projectid, startdate, exitreason
- uniqueItems on legal_projects and router_reasoncodes
- minLength=1 on all string IDs (clientid, routerversion, eventid, projectid, blockid)

### Phase 2: Coherence Validation
**Purpose:** Enforce atomic consistency rules  
**On Failure:** Return collapse state with `DEFAULTDENY_STATEHEADER_MISMATCH`

**Coherence Rules:**
1. `stateheader.lastupdated === lastupdated`
2. `stateheader.activeproject === decisions.activeproject`
3. `stateheader.routerversion === decisions.routerversion`
4. `stateheader.seasontype === inputs.trainingcontext_global.seasontype`
5. `stateheader.readinessflag === (inputs.trainingcontext_global.readinessflag ?? 'YELLOW')`

```javascript
function validateCoherence(state) {
  const checks = [
    state.stateheader.lastupdated === state.lastupdated,
    state.stateheader.activeproject === state.decisions.activeproject,
    state.stateheader.routerversion === state.decisions.routerversion,
    state.stateheader.seasontype === state.inputs.trainingcontext_global.seasontype,
    state.stateheader.readinessflag === (state.inputs.trainingcontext_global.readinessflag ?? 'YELLOW')
  ];

  if (!checks.every(Boolean)) {
    throw new Error('DEFAULTDENY_STATEHEADER_MISMATCH');
  }
}
```

### Phase 3: Invariant Validation
**Purpose:** Enforce Router-specific business rules  
**On Failure:** Return collapse state with `ROUTEROUTPUTINCOMPLETE`

**Router Invariants:**

**INV-001:** Youth E-node accent cap
```javascript
if (derived.populationoverrides.population_enforced === 'Youth812' || 
    derived.populationoverrides.population_enforced === 'Youth1316') {
  assert(derived.populationoverrides.enode_accent_cap_pct === 0.40);
} else {
  assert(derived.populationoverrides.enode_accent_cap_pct === null);
}
```

**INV-002:** Inputs immutability
```javascript
// Router must NEVER mutate inputs.* fields
// Only intake/update flows may modify inputs
```

**INV-003:** Derived existence
```javascript
if (decisions.eligible_for_training_today === true) {
  assert(derived !== null);
  assert(derived.populationoverrides !== null);
  assert(derived.readinessmultipliers !== null);
}
```

**INV-004:** Atomic writes
```javascript
// stateheader + decisions must be written atomically
// Partial writes are invalid
```

**INV-005:** Default logging
```javascript
if (inputs.trainingcontext_global.readinessflag === null) {
  // Router defaults to YELLOW
  assert(decisions.rationale_stack.some(r => r.rule === 'DEFAULT_READINESS_YELLOW'));
}
```

**INV-006:** Reason code allowlist
```javascript
const allowedCodes = schema.definitions.ReasonCode.enum;
decisions.router_reasoncodes.forEach(code => {
  assert(allowedCodes.includes(code));
});
decisions.illegal_projects_with_reasons.forEach(item => {
  assert(allowedCodes.includes(item.reasoncode));
});
```

---

## Router Evaluation Order (Precedence Ladder)

Router evaluates rules in strict order. First match wins.

```javascript
function evaluateRouting(inputs, derived) {
  // 1. Version check
  if (!allowedVersions.includes(routerVersion)) {
    return collapse('DEFAULTDENY_VERSION_MISMATCH');
  }

  // 2. Critical inputs check
  if (!hasCriticalInputs(inputs)) {
    return collapse('DEFAULTDENY_MISSING_CRITICAL_INPUTS');
  }

  // 3. Medical lock (highest priority)
  if (inputs.medicalstatus.hardstopstatus.medicallocktriggered) {
    return collapse('DEFAULTDENY_MEDICAL_LOCK');
  }

  // 4. Hardstop (no route available)
  if (inputs.medicalstatus.hardstopstatus.hardstoptriggered && !hasR2PRoute(inputs)) {
    return collapse('DEFAULTDENY_HARDSTOP_NO_ROUTE');
  }

  // 5. R2P enrollment (locks all SP Performance)
  if (inputs.medicalstatus.isinr2pservice) {
    return routeToR2P(inputs, derived);
  }

  // 6. Age/population gates
  const legalByPopulation = filterByPopulation(allProjects, derived.populationoverrides);

  // 7. Season routing (ICP vs developmental)
  const legalBySeason = filterBySeason(legalByPopulation, inputs.trainingcontext_global.seasontype);

  // 8. Entry gates (Foundations exit → Specialization)
  const legalByGates = filterByEntryGates(legalBySeason, inputs.performancegates);

  // 9. Macro caps (annual specialization limits)
  const legalByMacro = filterByMacroCaps(legalByGates, derived.macrocounters);

  // 10. Select active project
  return selectActiveProject(legalByMacro, inputs);
}
```

---

## Collapse Behavior

When Router cannot evaluate, return full collapse state:

```javascript
function collapseState(reasonCode, inputState, nowISO) {
  const allProjects = schema.definitions.ProjectID.enum;

  return {
    clientid: inputState.clientid,
    lastupdated: nowISO,
    stateheader: {
      clientid: inputState.clientid,
      lastupdated: nowISO,
      activeproject: 'NONE',
      // PATCH: Do NOT default seasontype to 'OFFSEASON' - respect "never default" rule
      seasontype: inputState.inputs?.trainingcontext_global?.seasontype,
      readinessflag: 'YELLOW',
      routerversion: routerVersion,
      eligible_for_training_today: false
    },
    inputs: inputState.inputs, // Immutable - echo back unchanged
    derived: null,
    decisions: {
      activeproject: 'NONE',
      legal_projects: [],
      illegal_projects_with_reasons: allProjects.map(pid => ({
        projectid: pid,
        reasoncode: reasonCode
      })),
      eligible_for_training_today: false,
      router_reasoncodes: [reasonCode],
      routerversion: routerVersion,
      rationale_stack: []
    }
  };
}
```

**CRITICAL FIX:** Seasontype is NO LONGER defaulted to 'OFFSEASON' in collapse. The field echoes whatever was in inputs (may be undefined). This respects the "never default critical inputs" rule.

---

## Conservative Defaults (Unknown Handling)

Router applies conservative defaults ONLY to context fields, NEVER to critical inputs:

| Field | Default | Condition | Log Code |
|-------|---------|-----------|----------|
| `readinessflag` | `YELLOW` | Always if null | `DEFAULT_READINESS_YELLOW` |
| `daysuntilnextgame` | `2` | INSEASON only | `DEFAULT_ASSUME_GAME_PROXIMITY` |
| `practicegamesperweek` | `4` | INSEASON only | `DEFAULT_ASSUME_PRACTICE_VOLUME` |

**Never Default (Always Collapse):**
- `seasontype`
- `age`
- `sport`
- `athletetrack`
- `isinr2pservice`
- `injurytype`

---

## Population Enforcement (INV-001)

```javascript
function computePopulationOverrides(age, athletetrack) {
  let population_enforced, enode_accent_cap_pct;

  if (age >= 8 && age <= 12) {
    population_enforced = 'Youth812';
    enode_accent_cap_pct = 0.40;
  } else if (age >= 13 && age <= 16) {
    population_enforced = 'Youth1316';
    enode_accent_cap_pct = 0.40;
  } else if (age === 17) {
    population_enforced = 'Youth17Advanced';
    enode_accent_cap_pct = null;
  } else if (age >= 18 && athletetrack === 'GENERAL') {
    population_enforced = 'Adult_GENERAL';
    enode_accent_cap_pct = null;
  } else if (age >= 18 && athletetrack === 'ATHLETE') {
    population_enforced = 'Adult_ATHLETE';
    enode_accent_cap_pct = null;
  }

  return { population_enforced, enode_accent_cap_pct };
}
```

---

## Readiness Multipliers

```javascript
function computeReadinessMultipliers(readinessFlag) {
  const multipliers = {
    'GREEN': { weekly: 1.0, session: 1.0 },
    'YELLOW': { weekly: 0.75, session: 0.8 },
    'RED': { weekly: 0.0, session: 0.0 }
  };

  return {
    weeklymultiplier: multipliers[readinessFlag].weekly,
    sessionmultiplier: multipliers[readinessFlag].session
  };
}
```

---

## Test Fixtures

Six reference test cases are provided in separate file:
- `EFL_ROUTER_TEST_FIXTURES_v1.0.json`

**Collapse Cases:**
1. Missing critical inputs
2. Version mismatch
3. Medical lock
4. Stateheader mismatch

**Legal Cases:**
5. Youth 13-16, OFFSEASON, non-R2P → COURT_SPORT_FOUNDATIONS
6. R2P enrolled → R2P_ACL (locks SP)

**Note:** These fixtures should be validated against schema v1.0.2 to ensure compliance with surgical patches (uniqueItems, minLength, projecthistory required fields, ACL-only conditional).

---

## Error Handling

Router must NEVER throw exceptions during evaluation. All failures return structured collapse state.

```javascript
function safeRoute(inputState, routerVersion, nowISO) {
  try {
    const result = routeClientState(inputState, routerVersion, nowISO);

    // Phase 1: Schema validation
    if (!validate(result)) {
      return collapseState('ROUTEROUTPUTINCOMPLETE', inputState, nowISO);
    }

    // Phase 2: Coherence validation
    validateCoherence(result);

    // Phase 3: Invariant validation
    validateInvariants(result);

    return result;

  } catch (error) {
    console.error('Router evaluation failed:', error);
    return collapseState('ROUTEROUTPUTINCOMPLETE', inputState, nowISO);
  }
}
```

---

## Production Checklist

Before deploying Router:

- [ ] Schema validation configured with Ajv strict mode
- [ ] All three validation phases implemented
- [ ] Coherence rules enforced
- [ ] Router invariants validated (INV-001 through INV-006)
- [ ] Conservative defaults logged in rationale_stack
- [ ] All reason codes in allowlist
- [ ] Inputs partition never mutated by Router
- [ ] Atomic writes (stateheader + decisions together)
- [ ] Seasontype never defaulted in collapse (PATCHED)
- [ ] All six test fixtures pass against v1.0.2 schema
- [ ] Collapse behavior returns complete state with derived:null

---

## Schema v1.0.2 Surgical Patches (Reference)

**PATCH 1:** ACL-only R2P conditional
- Only require weekspostop/grafttype/providerclearance when isinr2pservice=true AND injurytype ∈ {ACLRECONSTRUCTION, ACLHIGHGRADESPRAIN}

**PATCH 2:** projecthistory required fields
- Items require: projectid, startdate, exitreason
- minLength=1 on projectid and blockid

**PATCH 3:** uniqueItems enforcement
- legal_projects: uniqueItems=true
- router_reasoncodes: uniqueItems=true

**PATCH 4:** minLength on string IDs
- clientid, routerversion, eventid, projectid, blockid all require minLength=1

---

**Version:** 1.0.1 (PATCHED)  
**Status:** PRODUCTION-READY  
**Schema:** EFL_GLOBAL_CLIENT_STATE_v1.0.2.json  
**Date:** 2026-01-15  
**Patches:** Seasontype collapse fixed, schema reference updated to v1.0.2
