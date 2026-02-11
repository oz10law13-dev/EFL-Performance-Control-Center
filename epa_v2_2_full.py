"""
EFL PROGRAM ARCHITECT (EPA) v2.2 - Complete Implementation
============================================================

Deterministic Program Authoring Engine
Status: ENFORCEMENT-LOCKED (No discretionary overrides)
Effective: 2026-01-01

AUTHORITY PRECEDENCE:
1. EFL Load Standards v2.1.2 (Authoritative Safety Layer)
2. EFL Governance System v4.0
3. EFL Coach & AI Playbook v0.4.0
4. EFL Force-Velocity Schema
5. EFL Exercise Library / AETHER metadata

Architecture: Fail-fast gate validation
Output: Strict JSON (no markdown)
"""

import json
import csv
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
from enum import Enum


# ============================================================================
# PHASE 1: ENUMS & TYPE DEFINITIONS
# ============================================================================

class Population(Enum):
    YOUTH_8_12 = "Youth_8_12"
    YOUTH_13_17 = "Youth_13_17"
    ADULT = "Adult"
    R2P_STAGE_1 = "R2P_Stage_1"
    R2P_STAGE_2 = "R2P_Stage_2"
    R2P_STAGE_3 = "R2P_Stage_3"
    R2P_STAGE_4 = "R2P_Stage_4"


class SeasonType(Enum):
    OFF_SEASON = "OFF_SEASON"
    PRE_SEASON = "PRE_SEASON"
    IN_SEASON_TIER_1 = "IN_SEASON_TIER_1"
    IN_SEASON_TIER_2 = "IN_SEASON_TIER_2"
    IN_SEASON_TIER_3 = "IN_SEASON_TIER_3"
    POST_SEASON = "POST_SEASON"


class ReadinessFlag(Enum):
    GREEN = "GREEN"
    YELLOW = "YELLOW"
    RED = "RED"


class SessionType(Enum):
    FULL_SESSION = "FULL_SESSION"
    MICROSESSION = "MICROSESSION"


class ResponseStatus(Enum):
    SUCCESS = "SUCCESS"
    REJECTED_MISSING_FIELDS = "REJECTED_MISSING_FIELDS"
    REJECTED_ILLEGAL = "REJECTED_ILLEGAL"
    QUARANTINED_REVIEW = "QUARANTINED_REVIEW"


class BlockType(Enum):
    PRIME = "PRIME"
    PREP = "PREP"
    WORK = "WORK"
    CLEAR = "CLEAR"


# ============================================================================
# PHASE 2: DATA MODELS
# ============================================================================

@dataclass
class Exercise:
    """Exercise from AETHER library"""
    exercise_id: str
    exercise_name: str
    movement_pattern: str
    load_type: str
    equipment: List[str]
    stance: str
    complexity: str
    aether_pattern: str
    aether_node: str
    aether_difficulty: str
    contraindicated_populations: List[str]
    load_standard_band: str
    plyo_contacts: Optional[float]
    load_band_primary: str
    load_band_min: str
    load_band_max: str
    load_band_flexibility: str
    
    # Computed fields
    e_node: Optional[str] = None
    is_plyometric: bool = False
    is_sprint: bool = False
    intensity_percent_vmax: Optional[float] = None


@dataclass
class ExerciseInstance:
    """Exercise with session-specific parameters"""
    exercise_id: str
    exercise_name: str
    sets: int
    reps: int
    rest_seconds: int
    load: str
    rpe_target: Optional[int]
    coaching_cues: List[str]
    
    # Computed values
    total_contacts: int = 0
    total_sprint_meters: float = 0.0
    distance_m: Optional[float] = None
    intensity_percent_vmax: Optional[float] = None


@dataclass
class SessionBlock:
    """One block of a session (PRIME/PREP/WORK/CLEAR)"""
    block_type: str
    exercises: List[ExerciseInstance]
    duration_minutes_target: int


@dataclass
class SessionPlan:
    """Complete session plan"""
    session_id: str
    client_id: str
    week_id: str
    session_index: int
    session_type: str
    blocks: List[SessionBlock]
    total_plyo_contacts: int
    total_sprint_meters: float
    total_duration_minutes: int
    cns_category: str  # "HIGH" | "MODERATE" | "LOW"


@dataclass
class ValidationGateResult:
    """Result from a single validation gate"""
    gate_id: str
    gate_name: str
    status: str  # "PASS" | "FAIL" | "SKIP"
    reasons: List[str]


@dataclass
class WeeklyAggregation:
    """Weekly load tracking"""
    week_id: str
    completed_plyo_contacts: int
    completed_sprint_meters: float
    completed_sprint_sessions: int
    planned_plyo_contacts: int
    planned_sprint_meters: float
    planned_sprint_sessions: int
    projected_total_plyo_contacts: int
    projected_total_sprint_meters: float
    projected_total_sprint_sessions: int
    weekly_plyo_cap: int
    weekly_sprint_meters_cap: float
    weekly_sprint_sessions_cap: int


# ============================================================================
# PHASE 3: EXERCISE LIBRARY LOADER
# ============================================================================

class ExerciseLibrary:
    """Loads and queries AETHER Exercise Library CSV"""
    
    def __init__(self, csv_path: str):
        self.exercises: Dict[str, Exercise] = {}
        self._load_csv(csv_path)
    
    def _load_csv(self, csv_path: str):
        """Load exercises from CSV"""
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                exercise = self._parse_row(row)
                self.exercises[exercise.exercise_id] = exercise
    
    def _parse_row(self, row: Dict) -> Exercise:
        """Parse CSV row into Exercise object"""
        # Parse equipment (comma-separated)
        equipment = []
        if row.get('equipment'):
            equipment = [e.strip() for e in row['equipment'].split(',')]
        
        # Parse contraindicated populations
        contraindicated = []
        if row.get('contraindicated_populations'):
            contraindicated = [p.strip() for p in row['contraindicated_populations'].split(',')]
        
        # Parse plyo contacts
        plyo_contacts = None
        if row.get('plyo_contacts'):
            try:
                plyo_contacts = float(row['plyo_contacts'])
            except (ValueError, TypeError):
                pass
        
        exercise = Exercise(
            exercise_id=row.get('exercise_id', ''),
            exercise_name=row.get('exercise_name', ''),
            movement_pattern=row.get('movement_pattern', ''),
            load_type=row.get('load_type', ''),
            equipment=equipment,
            stance=row.get('stance', ''),
            complexity=row.get('complexity', ''),
            aether_pattern=row.get('aether_pattern', ''),
            aether_node=row.get('aether_node', ''),
            aether_difficulty=row.get('aether_difficulty', ''),
            contraindicated_populations=contraindicated,
            load_standard_band=row.get('load_standard_band', ''),
            plyo_contacts=plyo_contacts,
            load_band_primary=row.get('load_band_primary', ''),
            load_band_min=row.get('load_band_min', ''),
            load_band_max=row.get('load_band_max', ''),
            load_band_flexibility=row.get('load_band_flexibility', '')
        )
        
        # Compute derived fields
        exercise.is_plyometric = (plyo_contacts is not None and plyo_contacts > 0)
        
        # Extract E-node from aether_difficulty (e.g., "E2" -> "E2")
        if exercise.aether_difficulty and exercise.aether_difficulty.startswith('E'):
            exercise.e_node = exercise.aether_difficulty[:2]  # "E0", "E1", "E2", etc.
        
        return exercise
    
    def get_exercise(self, exercise_id: str) -> Optional[Exercise]:
        """Get exercise by ID"""
        return self.exercises.get(exercise_id)
    
    def exists(self, exercise_id: str) -> bool:
        """Check if exercise exists"""
        return exercise_id in self.exercises


# ============================================================================
# PHASE 4: LIMIT MANAGER (LOAD STANDARDS v2.1.2)
# ============================================================================

class LimitManager:
    """
    Authoritative source for all caps, ceilings, and operating ranges
    from Load Standards v2.1.2
    """
    
    # Population-specific session caps
    POPULATION_SESSION_CAPS = {
        "Youth_8_12": {
            "plyo_contacts_per_session_full": 80,
            "plyo_contacts_per_session_microsession": 56,  # 80 * 0.7
            "sprint_meters_per_session": 150,
            "max_band": "Band_2",
            "max_node": "N2",
            "max_e_node": "E2"
        },
        "Youth_13_17": {
            "plyo_contacts_per_session_full": 100,
            "plyo_contacts_per_session_microsession": 70,  # 100 * 0.7
            "sprint_meters_per_session": 200,
            "max_band": "Band_3",
            "max_node": "N3",
            "max_e_node": "E4"
        },
        "Adult": {
            "plyo_contacts_per_session_full": 120,
            "plyo_contacts_per_session_microsession": 60,  # Special rule: 60 (not 84)
            "sprint_meters_per_session": 250,
            "max_band": "Band_4",
            "max_node": "N4",
            "max_e_node": "E4"
        }
    }
    
    # Population-specific weekly caps
    POPULATION_WEEKLY_CAPS = {
        "Youth_8_12": {
            "plyo_contacts_per_week": 200,
            "sprint_meters_per_week": 400,
            "max_sprint_sessions_per_week": 3
        },
        "Youth_13_17": {
            "plyo_contacts_per_week": 240,
            "sprint_meters_per_week": 500,
            "max_sprint_sessions_per_week": 3
        },
        "Adult": {
            "plyo_contacts_per_week": 300,
            "sprint_meters_per_week": 600,
            "max_sprint_sessions_per_week": 3
        }
    }
    
    # Seasonal operating ranges (weekly targets)
    SEASONAL_OPERATING_RANGES = {
        # Youth 8-12
        "Youth_8_12_OFF_SEASON": {"plyo_min": 80, "plyo_max": 160, "sprint_min": 150, "sprint_max": 300},
        "Youth_8_12_PRE_SEASON": {"plyo_min": 120, "plyo_max": 200, "sprint_min": 200, "sprint_max": 400},
        "Youth_8_12_IN_SEASON_TIER_1": {"plyo_min": 40, "plyo_max": 100, "sprint_min": 100, "sprint_max": 250},
        "Youth_8_12_IN_SEASON_TIER_2": {"plyo_min": 60, "plyo_max": 140, "sprint_min": 150, "sprint_max": 300},
        "Youth_8_12_IN_SEASON_TIER_3": {"plyo_min": 80, "plyo_max": 180, "sprint_min": 200, "sprint_max": 350},
        "Youth_8_12_POST_SEASON": {"plyo_min": 20, "plyo_max": 80, "sprint_min": 50, "sprint_max": 150},
        
        # Youth 13-17
        "Youth_13_17_OFF_SEASON": {"plyo_min": 120, "plyo_max": 240, "sprint_min": 200, "sprint_max": 500},
        "Youth_13_17_PRE_SEASON": {"plyo_min": 160, "plyo_max": 240, "sprint_min": 300, "sprint_max": 500},
        "Youth_13_17_IN_SEASON_TIER_1": {"plyo_min": 60, "plyo_max": 140, "sprint_min": 150, "sprint_max": 300},
        "Youth_13_17_IN_SEASON_TIER_2": {"plyo_min": 100, "plyo_max": 180, "sprint_min": 200, "sprint_max": 400},
        "Youth_13_17_IN_SEASON_TIER_3": {"plyo_min": 120, "plyo_max": 220, "sprint_min": 250, "sprint_max": 450},
        "Youth_13_17_POST_SEASON": {"plyo_min": 40, "plyo_max": 100, "sprint_min": 100, "sprint_max": 200},
        
        # Adult
        "Adult_OFF_SEASON": {"plyo_min": 150, "plyo_max": 300, "sprint_min": 250, "sprint_max": 600},
        "Adult_PRE_SEASON": {"plyo_min": 200, "plyo_max": 300, "sprint_min": 400, "sprint_max": 600},
        "Adult_IN_SEASON_TIER_1": {"plyo_min": 80, "plyo_max": 180, "sprint_min": 200, "sprint_max": 400},
        "Adult_IN_SEASON_TIER_2": {"plyo_min": 120, "plyo_max": 220, "sprint_min": 300, "sprint_max": 500},
        "Adult_IN_SEASON_TIER_3": {"plyo_min": 150, "plyo_max": 270, "sprint_min": 350, "sprint_max": 550},
        "Adult_POST_SEASON": {"plyo_min": 60, "plyo_max": 120, "sprint_min": 150, "sprint_max": 300}
    }
    
    # MicroSession special rules (Adult only)
    MICROSESSION_ADULT_RULES = {
        "max_contacts": 60,
        "allowed_e_nodes": ["E0", "E1"],
        "max_band": "Band_1",
        "true_sprinting_allowed": False,
        "duration_min": 10,
        "duration_max": 25
    }
    
    # Readiness modifiers
    READINESS_MODIFIERS = {
        "GREEN": {"multiplier": 1.0, "tier_restriction": None},
        "YELLOW": {"multiplier": 0.75, "tier_restriction": "E2_max"},  # Tier 2 max
        "RED": {"multiplier": 0.0, "tier_restriction": "mobility_only"}  # Zero plyo/sprint
    }
    
    # Youth 13-17 Tier 3 percentage cap
    TIER_3_PERCENTAGE_CAP_YOUTH_13_17 = 0.40  # 40% max
    
    @staticmethod
    def get_session_caps(population: str, session_type: str, readiness: str) -> Dict:
        """Get session-level caps for a given context"""
        base_caps = LimitManager.POPULATION_SESSION_CAPS.get(population, {})
        
        if not base_caps:
            return {}
        
        # Determine plyo contact cap based on session type
        if session_type == "FULL_SESSION":
            plyo_cap = base_caps["plyo_contacts_per_session_full"]
        else:  # MICROSESSION
            if population == "Adult":
                # Special rule: Adult MS = 60 contacts (not 0.7x)
                plyo_cap = LimitManager.MICROSESSION_ADULT_RULES["max_contacts"]
            else:
                # Athlete MS = 70% of full session cap
                plyo_cap = base_caps["plyo_contacts_per_session_microsession"]
        
        # Apply readiness modifier
        readiness_mod = LimitManager.READINESS_MODIFIERS.get(readiness, {})
        multiplier = readiness_mod.get("multiplier", 1.0)
        
        return {
            "plyo_contacts_cap": int(plyo_cap * multiplier),
            "sprint_meters_cap": int(base_caps["sprint_meters_per_session"] * multiplier),
            "max_band": base_caps["max_band"],
            "max_node": base_caps["max_node"],
            "max_e_node": base_caps["max_e_node"]
        }
    
    @staticmethod
    def get_weekly_caps(population: str) -> Dict:
        """Get weekly caps for a population"""
        return LimitManager.POPULATION_WEEKLY_CAPS.get(population, {})
    
    @staticmethod
    def get_seasonal_range(population: str, season_type: str) -> Dict:
        """Get seasonal operating range"""
        key = f"{population}_{season_type}"
        return LimitManager.SEASONAL_OPERATING_RANGES.get(key, {})


# ============================================================================
# PHASE 5: INPUT VALIDATOR
# ============================================================================

class InputValidator:
    """Validates input JSON contract"""
    
    REQUIRED_FIELDS = [
        "client_id",
        "population",
        "sport",
        "season_type",
        "readiness_flag",
        "injury_flags",
        "week_id",
        "planned_sessions_this_week",
        "completed_sessions_this_week",
        "session_index",
        "session_type",
        "planned_sprint_sessions_this_week",
        "completed_sprint_sessions_this_week"
    ]
    
    @staticmethod
    def validate(input_data: Dict) -> Tuple[bool, List[str]]:
        """
        Validate input JSON
        Returns: (is_valid, missing_fields)
        """
        missing = []
        
        for field in InputValidator.REQUIRED_FIELDS:
            if field not in input_data or input_data[field] is None:
                missing.append(field)
        
        return (len(missing) == 0, missing)


# ============================================================================
# PHASE 6: VALIDATION GATES (FAIL-FAST)
# ============================================================================

class ValidationGates:
    """
    Implements all 7 validation gates (0-6)
    Architecture: FAIL-FAST (first failure stops all downstream gates)
    """
    
    def __init__(self, library: ExerciseLibrary, limits: LimitManager):
        self.library = library
        self.limits = limits
    
    def run_all_gates(self, input_data: Dict, session_plan: Optional[SessionPlan]) -> List[ValidationGateResult]:
        """
        Run all gates in sequence (fail-fast)
        Returns list of gate results
        """
        results = []
        
        # Gate 0: Exercise Library Metadata Validation
        gate0 = self._gate_0_library_metadata(input_data, session_plan)
        results.append(gate0)
        if gate0.status == "FAIL":
            return results  # STOP - metadata missing/invalid
        
        # Gate 1: Population Band/Node Ceiling
        gate1 = self._gate_1_population_ceiling(input_data, session_plan)
        results.append(gate1)
        if gate1.status == "FAIL":
            return results  # STOP - exceeds population limits
        
        # Gate 2: Season/Fixture Legality
        gate2 = self._gate_2_season_legality(input_data, session_plan)
        results.append(gate2)
        if gate2.status == "FAIL":
            return results  # STOP - illegal for season
        
        # Gate 3: Readiness Modifier Application
        gate3 = self._gate_3_readiness_modifiers(input_data, session_plan)
        results.append(gate3)
        if gate3.status == "FAIL":
            return results  # STOP - readiness violation
        
        # Gate 4: Session Type Rules
        gate4 = self._gate_4_session_type_rules(input_data, session_plan)
        results.append(gate4)
        if gate4.status == "FAIL":
            return results  # STOP - session type violation
        
        # Gate 5: Weekly Caps Projection
        gate5 = self._gate_5_weekly_caps(input_data, session_plan)
        results.append(gate5)
        if gate5.status == "FAIL":
            return results  # STOP - weekly cap exceeded
        
        # Gate 6: Tier 3 Percentage (Youth 13-17 only)
        gate6 = self._gate_6_tier_3_percentage(input_data, session_plan)
        results.append(gate6)
        if gate6.status == "FAIL":
            return results  # STOP - Tier 3 percentage exceeded
        
        return results
    
    def _gate_0_library_metadata(self, input_data: Dict, session_plan: Optional[SessionPlan]) -> ValidationGateResult:
        """Gate 0: Exercise Library Metadata Validation"""
        if not session_plan:
            return ValidationGateResult(
                gate_id="0",
                gate_name="Exercise_Library_Metadata",
                status="SKIP",
                reasons=["No session plan provided"]
            )
        
        reasons = []
        
        for block in session_plan.blocks:
            for ex in block.exercises:
                # Check exercise exists in library
                library_ex = self.library.get_exercise(ex.exercise_id)
                
                if not library_ex:
                    reasons.append(f"MISSING_EXERCISE: {ex.exercise_id} not found in library")
                    continue
                
                # Check for required metadata (plyometric exercises)
                if library_ex.is_plyometric:
                    if library_ex.plyo_contacts is None or library_ex.plyo_contacts == 0:
                        reasons.append(f"MISSING_PLYO_CONTACTS: {ex.exercise_id}")
                
                # Check for sprint intensity metadata
                if library_ex.is_sprint and ex.intensity_percent_vmax is None:
                    reasons.append(f"MISSING_INTENSITY_VMAX: {ex.exercise_id} (sprint requires intensity)")
        
        status = "FAIL" if reasons else "PASS"
        
        return ValidationGateResult(
            gate_id="0",
            gate_name="Exercise_Library_Metadata",
            status=status,
            reasons=reasons
        )
    
    def _gate_1_population_ceiling(self, input_data: Dict, session_plan: Optional[SessionPlan]) -> ValidationGateResult:
        """Gate 1: Population Band/Node Ceiling"""
        if not session_plan:
            return ValidationGateResult(
                gate_id="1",
                gate_name="Population_Band_Node_Ceiling",
                status="SKIP",
                reasons=["No session plan provided"]
            )
        
        population = input_data.get("population")
        session_type = input_data.get("session_type")
        readiness = input_data.get("readiness_flag")
        
        caps = self.limits.get_session_caps(population, session_type, readiness)
        max_band = caps.get("max_band", "Band_4")
        max_e_node = caps.get("max_e_node", "E4")
        
        reasons = []
        
        for block in session_plan.blocks:
            for ex in block.exercises:
                library_ex = self.library.get_exercise(ex.exercise_id)
                if not library_ex:
                    continue
                
                # Check band
                ex_band = library_ex.load_standard_band
                if self._compare_bands(ex_band, max_band) > 0:
                    reasons.append(f"BAND_EXCEEDED: {ex.exercise_id} requires {ex_band}, max allowed {max_band}")
                
                # Check E-node
                if library_ex.e_node:
                    if self._compare_e_nodes(library_ex.e_node, max_e_node) > 0:
                        reasons.append(f"E_NODE_EXCEEDED: {ex.exercise_id} requires {library_ex.e_node}, max allowed {max_e_node}")
        
        status = "FAIL" if reasons else "PASS"
        
        return ValidationGateResult(
            gate_id="1",
            gate_name="Population_Band_Node_Ceiling",
            status=status,
            reasons=reasons
        )
    
    def _gate_2_season_legality(self, input_data: Dict, session_plan: Optional[SessionPlan]) -> ValidationGateResult:
        """Gate 2: Season/Fixture Legality"""
        if not session_plan:
            return ValidationGateResult(
                gate_id="2",
                gate_name="Season_Fixture_Legality",
                status="SKIP",
                reasons=["No session plan provided"]
            )
        
        season_type = input_data.get("season_type")
        reasons = []
        
        # IN_SEASON restrictions (example - would need full rules from Governance v4.0)
        if "IN_SEASON" in season_type:
            # Check for high-CNS exercises in Tier 1
            if season_type == "IN_SEASON_TIER_1":
                for block in session_plan.blocks:
                    for ex in block.exercises:
                        library_ex = self.library.get_exercise(ex.exercise_id)
                        if library_ex and library_ex.e_node in ["E3", "E4"]:
                            reasons.append(f"ILLEGAL_TIER_1_E_NODE: {ex.exercise_id} ({library_ex.e_node}) illegal in Tier 1")
        
        status = "FAIL" if reasons else "PASS"
        
        return ValidationGateResult(
            gate_id="2",
            gate_name="Season_Fixture_Legality",
            status=status,
            reasons=reasons
        )
    
    def _gate_3_readiness_modifiers(self, input_data: Dict, session_plan: Optional[SessionPlan]) -> ValidationGateResult:
        """Gate 3: Readiness Modifier Application"""
        if not session_plan:
            return ValidationGateResult(
                gate_id="3",
                gate_name="Readiness_Modifiers",
                status="SKIP",
                reasons=["No session plan provided"]
            )
        
        readiness = input_data.get("readiness_flag")
        reasons = []
        
        # RED readiness: zero plyometrics and zero true sprinting
        if readiness == "RED":
            if session_plan.total_plyo_contacts > 0:
                reasons.append(f"RED_READINESS_PLYO_VIOLATION: {session_plan.total_plyo_contacts} contacts (must be 0)")
            
            if session_plan.total_sprint_meters > 0:
                reasons.append(f"RED_READINESS_SPRINT_VIOLATION: {session_plan.total_sprint_meters}m (must be 0)")
        
        # YELLOW readiness: max E2 (Tier 2)
        if readiness == "YELLOW":
            for block in session_plan.blocks:
                for ex in block.exercises:
                    library_ex = self.library.get_exercise(ex.exercise_id)
                    if library_ex and library_ex.e_node:
                        if self._compare_e_nodes(library_ex.e_node, "E2") > 0:
                            reasons.append(f"YELLOW_READINESS_TIER_VIOLATION: {ex.exercise_id} ({library_ex.e_node}) exceeds E2 limit")
        
        status = "FAIL" if reasons else "PASS"
        
        return ValidationGateResult(
            gate_id="3",
            gate_name="Readiness_Modifiers",
            status=status,
            reasons=reasons
        )
    
    def _gate_4_session_type_rules(self, input_data: Dict, session_plan: Optional[SessionPlan]) -> ValidationGateResult:
        """Gate 4: Session Type Rules (MicroSession vs Full)"""
        if not session_plan:
            return ValidationGateResult(
                gate_id="4",
                gate_name="Session_Type_Rules",
                status="SKIP",
                reasons=["No session plan provided"]
            )
        
        session_type = input_data.get("session_type")
        population = input_data.get("population")
        reasons = []
        
        if session_type == "MICROSESSION":
            # Adult MicroSession special rules
            if population == "Adult":
                ms_rules = self.limits.MICROSESSION_ADULT_RULES
                
                # Check contacts (60 max)
                if session_plan.total_plyo_contacts > ms_rules["max_contacts"]:
                    reasons.append(f"ADULT_MS_CONTACTS_EXCEEDED: {session_plan.total_plyo_contacts} > {ms_rules['max_contacts']}")
                
                # Check E-nodes (E0-E1 only)
                for block in session_plan.blocks:
                    for ex in block.exercises:
                        library_ex = self.library.get_exercise(ex.exercise_id)
                        if library_ex and library_ex.e_node:
                            if library_ex.e_node not in ms_rules["allowed_e_nodes"]:
                                reasons.append(f"ADULT_MS_E_NODE_VIOLATION: {ex.exercise_id} ({library_ex.e_node}) not in {ms_rules['allowed_e_nodes']}")
                
                # Check sprinting (not allowed)
                if session_plan.total_sprint_meters > 0:
                    reasons.append(f"ADULT_MS_SPRINT_VIOLATION: {session_plan.total_sprint_meters}m (sprinting not allowed)")
        
        status = "FAIL" if reasons else "PASS"
        
        return ValidationGateResult(
            gate_id="4",
            gate_name="Session_Type_Rules",
            status=status,
            reasons=reasons
        )
    
    def _gate_5_weekly_caps(self, input_data: Dict, session_plan: Optional[SessionPlan]) -> ValidationGateResult:
        """Gate 5: Weekly Caps Projection"""
        if not session_plan:
            return ValidationGateResult(
                gate_id="5",
                gate_name="Weekly_Caps_Projection",
                status="SKIP",
                reasons=["No session plan provided"]
            )
        
        population = input_data.get("population")
        weekly_caps = self.limits.get_weekly_caps(population)
        
        # Get practice exposure tracking (optional)
        practice_exposure = input_data.get("practice_exposure", {})
        tracked_plyo = practice_exposure.get("tracked_plyo_contacts_this_week", 0)
        tracked_sprint = practice_exposure.get("tracked_true_sprint_meters_this_week", 0)
        
        # Completed sessions (already done)
        completed_sessions = input_data.get("completed_sessions_this_week", 0)
        completed_sprint_sessions = input_data.get("completed_sprint_sessions_this_week", 0)
        
        # Planned sessions (including current)
        planned_sessions = input_data.get("planned_sessions_this_week", 0)
        planned_sprint_sessions = input_data.get("planned_sprint_sessions_this_week", 0)
        
        reasons = []
        
        # Gate 5.1: Weekly plyo contact cap
        projected_plyo = tracked_plyo + session_plan.total_plyo_contacts
        weekly_plyo_cap = weekly_caps.get("plyo_contacts_per_week", 999999)
        
        if projected_plyo > weekly_plyo_cap:
            reasons.append(f"WEEKLY_PLYO_CAP_EXCEEDED: Projected {projected_plyo} > Cap {weekly_plyo_cap}")
        
        # Gate 5.2: Weekly sprint meters cap
        projected_sprint = tracked_sprint + session_plan.total_sprint_meters
        weekly_sprint_cap = weekly_caps.get("sprint_meters_per_week", 999999)
        
        if projected_sprint > weekly_sprint_cap:
            reasons.append(f"WEEKLY_SPRINT_METERS_CAP_EXCEEDED: Projected {projected_sprint} > Cap {weekly_sprint_cap}")
        
        # Gate 5.3: Sprint session count cap
        current_session_has_sprint = (session_plan.total_sprint_meters > 0)
        projected_sprint_sessions = completed_sprint_sessions
        if current_session_has_sprint:
            projected_sprint_sessions += 1
        
        max_sprint_sessions = weekly_caps.get("max_sprint_sessions_per_week", 3)
        
        if projected_sprint_sessions > max_sprint_sessions:
            reasons.append(f"SPRINT_SESSION_CAP_EXCEEDED: Projected {projected_sprint_sessions} > Cap {max_sprint_sessions}")
        
        status = "FAIL" if reasons else "PASS"
        
        return ValidationGateResult(
            gate_id="5",
            gate_name="Weekly_Caps_Projection",
            status=status,
            reasons=reasons
        )
    
    def _gate_6_tier_3_percentage(self, input_data: Dict, session_plan: Optional[SessionPlan]) -> ValidationGateResult:
        """Gate 6: Tier 3 Percentage Cap (Youth 13-17 only)"""
        if not session_plan:
            return ValidationGateResult(
                gate_id="6",
                gate_name="Tier_3_Percentage_Cap",
                status="SKIP",
                reasons=["No session plan provided"]
            )
        
        population = input_data.get("population")
        
        # Only applies to Youth 13-17
        if population != "Youth_13_17":
            return ValidationGateResult(
                gate_id="6",
                gate_name="Tier_3_Percentage_Cap",
                status="SKIP",
                reasons=["Not applicable to this population"]
            )
        
        reasons = []
        
        # Calculate Tier 3 contacts (E3 + E4)
        tier_3_contacts = 0
        total_plyo_contacts = session_plan.total_plyo_contacts
        
        for block in session_plan.blocks:
            for ex in block.exercises:
                library_ex = self.library.get_exercise(ex.exercise_id)
                if library_ex and library_ex.e_node in ["E3", "E4"]:
                    tier_3_contacts += ex.total_contacts
        
        if total_plyo_contacts > 0:
            tier_3_percentage = tier_3_contacts / total_plyo_contacts
            max_percentage = self.limits.TIER_3_PERCENTAGE_CAP_YOUTH_13_17
            
            if tier_3_percentage > max_percentage:
                reasons.append(
                    f"TIER_3_PERCENTAGE_EXCEEDED: {tier_3_percentage:.1%} > {max_percentage:.1%} "
                    f"({tier_3_contacts}/{total_plyo_contacts} contacts)"
                )
        
        status = "FAIL" if reasons else "PASS"
        
        return ValidationGateResult(
            gate_id="6",
            gate_name="Tier_3_Percentage_Cap",
            status=status,
            reasons=reasons
        )
    
    # Helper methods
    def _compare_bands(self, band1: str, band2: str) -> int:
        """Compare two bands (-1: band1 < band2, 0: equal, 1: band1 > band2)"""
        band_order = ["Band_0", "Band_1", "Band_2", "Band_3", "Band_4"]
        
        try:
            idx1 = band_order.index(band1)
            idx2 = band_order.index(band2)
            
            if idx1 < idx2:
                return -1
            elif idx1 > idx2:
                return 1
            else:
                return 0
        except ValueError:
            return 0
    
    def _compare_e_nodes(self, e1: str, e2: str) -> int:
        """Compare two E-nodes (-1: e1 < e2, 0: equal, 1: e1 > e2)"""
        e_order = ["E0", "E1", "E2", "E3", "E4"]
        
        try:
            idx1 = e_order.index(e1)
            idx2 = e_order.index(e2)
            
            if idx1 < idx2:
                return -1
            elif idx1 > idx2:
                return 1
            else:
                return 0
        except ValueError:
            return 0


# ============================================================================
# PHASE 7: SESSION BUILDER
# ============================================================================

class SessionBuilder:
    """Builds SessionPlan from input blocks"""
    
    def __init__(self, library: ExerciseLibrary):
        self.library = library
    
    def build_session(self, input_data: Dict) -> SessionPlan:
        """
        Build session plan from input blocks
        Computes totals (contacts, sprint meters, etc.)
        """
        blocks_data = input_data.get("blocks", [])
        
        blocks = []
        total_plyo_contacts = 0
        total_sprint_meters = 0.0
        total_duration = 0
        
        for block_data in blocks_data:
            block = self._build_block(block_data)
            blocks.append(block)
            
            # Aggregate totals
            for ex in block.exercises:
                total_plyo_contacts += ex.total_contacts
                total_sprint_meters += ex.total_sprint_meters
            
            total_duration += block.duration_minutes_target
        
        # Determine CNS category (simplified - would use more sophisticated logic)
        cns_category = self._determine_cns_category(total_plyo_contacts, total_sprint_meters)
        
        return SessionPlan(
            session_id=input_data.get("session_id", ""),
            client_id=input_data.get("client_id", ""),
            week_id=input_data.get("week_id", ""),
            session_index=input_data.get("session_index", 1),
            session_type=input_data.get("session_type", "FULL_SESSION"),
            blocks=blocks,
            total_plyo_contacts=total_plyo_contacts,
            total_sprint_meters=total_sprint_meters,
            total_duration_minutes=total_duration,
            cns_category=cns_category
        )
    
    def _build_block(self, block_data: Dict) -> SessionBlock:
        """Build single session block"""
        exercises_data = block_data.get("items", [])
        exercises = []
        
        for ex_data in exercises_data:
            ex = self._build_exercise(ex_data)
            exercises.append(ex)
        
        return SessionBlock(
            block_type=block_data.get("name", "WORK"),
            exercises=exercises,
            duration_minutes_target=block_data.get("duration_minutes_target", 20)
        )
    
    def _build_exercise(self, ex_data: Dict) -> ExerciseInstance:
        """Build single exercise instance with computed totals"""
        exercise_id = ex_data.get("exercise_id", "")
        library_ex = self.library.get_exercise(exercise_id)
        
        sets = ex_data.get("sets", 0)
        reps = ex_data.get("reps", 0)
        
        # Compute plyo contacts
        total_contacts = 0
        if library_ex and library_ex.is_plyometric:
            contacts_per_rep = library_ex.plyo_contacts or 0
            total_contacts = int(sets * reps * contacts_per_rep)
        
        # Compute sprint meters
        total_sprint_meters = 0.0
        distance_m = ex_data.get("distance_m")
        intensity_vmax = ex_data.get("intensity_percent_vmax")
        
        if distance_m and intensity_vmax and intensity_vmax >= 90:
            total_sprint_meters = sets * reps * distance_m
        
        return ExerciseInstance(
            exercise_id=exercise_id,
            exercise_name=ex_data.get("exercise_name", library_ex.exercise_name if library_ex else ""),
            sets=sets,
            reps=reps,
            rest_seconds=ex_data.get("rest_seconds", 60),
            load=ex_data.get("load", "Bodyweight"),
            rpe_target=ex_data.get("rpe_target"),
            coaching_cues=ex_data.get("coaching_cues", []),
            total_contacts=total_contacts,
            total_sprint_meters=total_sprint_meters,
            distance_m=distance_m,
            intensity_percent_vmax=intensity_vmax
        )
    
    def _determine_cns_category(self, plyo_contacts: int, sprint_meters: float) -> str:
        """Determine CNS category (simplified logic)"""
        if plyo_contacts >= 100 or sprint_meters >= 200:
            return "HIGH"
        elif plyo_contacts >= 50 or sprint_meters >= 100:
            return "MODERATE"
        else:
            return "LOW"


# ============================================================================
# PHASE 8: RESPONSE BUILDER
# ============================================================================

class ResponseBuilder:
    """Builds final JSON response"""
    
    @staticmethod
    def build_success(
        input_data: Dict,
        session_plan: SessionPlan,
        validation_results: List[ValidationGateResult],
        weekly_agg: WeeklyAggregation,
        computed_limits: Dict
    ) -> Dict:
        """Build SUCCESS response"""
        return {
            "status": ResponseStatus.SUCCESS.value,
            "reasons": [],
            "inputs_echo": ResponseBuilder._sanitize_inputs(input_data),
            "computed_limits": computed_limits,
            "session_plan": ResponseBuilder._serialize_session(session_plan),
            "validation_report": ResponseBuilder._serialize_gates(validation_results),
            "weekly_aggregation": ResponseBuilder._serialize_weekly_agg(weekly_agg)
        }
    
    @staticmethod
    def build_rejected_missing_fields(missing_fields: List[str]) -> Dict:
        """Build REJECTED_MISSING_FIELDS response"""
        return {
            "status": ResponseStatus.REJECTED_MISSING_FIELDS.value,
            "reasons": [f"MISSING_REQUIRED_FIELD: {f}" for f in missing_fields],
            "inputs_echo": None,
            "computed_limits": None,
            "session_plan": None,
            "validation_report": None,
            "weekly_aggregation": None
        }
    
    @staticmethod
    def build_rejected_illegal(
        input_data: Dict,
        validation_results: List[ValidationGateResult],
        computed_limits: Dict
    ) -> Dict:
        """Build REJECTED_ILLEGAL response"""
        all_reasons = []
        for gate in validation_results:
            all_reasons.extend(gate.reasons)
        
        return {
            "status": ResponseStatus.REJECTED_ILLEGAL.value,
            "reasons": all_reasons,
            "inputs_echo": ResponseBuilder._sanitize_inputs(input_data),
            "computed_limits": computed_limits,
            "session_plan": None,
            "validation_report": ResponseBuilder._serialize_gates(validation_results),
            "weekly_aggregation": None
        }
    
    @staticmethod
    def build_quarantined(
        input_data: Dict,
        validation_results: List[ValidationGateResult],
        computed_limits: Dict
    ) -> Dict:
        """Build QUARANTINED_REVIEW response"""
        all_reasons = []
        for gate in validation_results:
            all_reasons.extend(gate.reasons)
        
        return {
            "status": ResponseStatus.QUARANTINED_REVIEW.value,
            "reasons": all_reasons,
            "inputs_echo": ResponseBuilder._sanitize_inputs(input_data),
            "computed_limits": computed_limits,
            "session_plan": None,
            "validation_report": ResponseBuilder._serialize_gates(validation_results),
            "weekly_aggregation": None
        }
    
    @staticmethod
    def _sanitize_inputs(input_data: Dict) -> Dict:
        """Sanitize input data for echo"""
        return {k: v for k, v in input_data.items()}
    
    @staticmethod
    def _serialize_session(session: SessionPlan) -> Dict:
        """Serialize session plan to dict"""
        return {
            "session_id": session.session_id,
            "client_id": session.client_id,
            "week_id": session.week_id,
            "session_index": session.session_index,
            "session_type": session.session_type,
            "blocks": [
                {
                    "block_type": block.block_type,
                    "duration_minutes_target": block.duration_minutes_target,
                    "exercises": [
                        {
                            "exercise_id": ex.exercise_id,
                            "exercise_name": ex.exercise_name,
                            "sets": ex.sets,
                            "reps": ex.reps,
                            "rest_seconds": ex.rest_seconds,
                            "load": ex.load,
                            "rpe_target": ex.rpe_target,
                            "coaching_cues": ex.coaching_cues,
                            "total_contacts": ex.total_contacts,
                            "total_sprint_meters": ex.total_sprint_meters
                        }
                        for ex in block.exercises
                    ]
                }
                for block in session.blocks
            ],
            "total_plyo_contacts": session.total_plyo_contacts,
            "total_sprint_meters": session.total_sprint_meters,
            "total_duration_minutes": session.total_duration_minutes,
            "cns_category": session.cns_category
        }
    
    @staticmethod
    def _serialize_gates(gates: List[ValidationGateResult]) -> List[Dict]:
        """Serialize gate results to list of dicts"""
        return [
            {
                "gate_id": gate.gate_id,
                "gate_name": gate.gate_name,
                "status": gate.status,
                "reasons": gate.reasons
            }
            for gate in gates
        ]
    
    @staticmethod
    def _serialize_weekly_agg(agg: WeeklyAggregation) -> Dict:
        """Serialize weekly aggregation to dict"""
        return {
            "week_id": agg.week_id,
            "completed_plyo_contacts": agg.completed_plyo_contacts,
            "completed_sprint_meters": agg.completed_sprint_meters,
            "completed_sprint_sessions": agg.completed_sprint_sessions,
            "planned_plyo_contacts": agg.planned_plyo_contacts,
            "planned_sprint_meters": agg.planned_sprint_meters,
            "planned_sprint_sessions": agg.planned_sprint_sessions,
            "projected_total_plyo_contacts": agg.projected_total_plyo_contacts,
            "projected_total_sprint_meters": agg.projected_total_sprint_meters,
            "projected_total_sprint_sessions": agg.projected_total_sprint_sessions,
            "weekly_plyo_cap": agg.weekly_plyo_cap,
            "weekly_sprint_meters_cap": agg.weekly_sprint_meters_cap,
            "weekly_sprint_sessions_cap": agg.weekly_sprint_sessions_cap
        }


# ============================================================================
# PHASE 9: MAIN ORCHESTRATOR
# ============================================================================

class EFLProgramArchitect:
    """
    Main EPA v2.2 Orchestrator
    Coordinates all phases: validation â†’ session building â†’ gate checking â†’ response
    """
    
    def __init__(self, library_csv_path: str):
        self.library = ExerciseLibrary(library_csv_path)
        self.limits = LimitManager()
        self.gates = ValidationGates(self.library, self.limits)
        self.session_builder = SessionBuilder(self.library)
    
    def process(self, json_input: str) -> str:
        """
        Main entry point
        Input: JSON string
        Output: JSON string (strict, no markdown)
        """
        try:
            input_data = json.loads(json_input)
        except json.JSONDecodeError as e:
            return json.dumps({
                "status": "REJECTED_MISSING_FIELDS",
                "reasons": [f"INVALID_JSON: {str(e)}"],
                "inputs_echo": None,
                "computed_limits": None,
                "session_plan": None,
                "validation_report": None,
                "weekly_aggregation": None
            }, indent=2)
        
        # Step 1: Validate input contract
        is_valid, missing_fields = InputValidator.validate(input_data)
        if not is_valid:
            response = ResponseBuilder.build_rejected_missing_fields(missing_fields)
            return json.dumps(response, indent=2)
        
        # Step 2: Compute limits
        computed_limits = self._compute_limits(input_data)
        
        # Step 3: Build session plan (if blocks provided)
        session_plan = None
        if "blocks" in input_data:
            session_plan = self.session_builder.build_session(input_data)
        
        # Step 4: Run all validation gates (fail-fast)
        validation_results = self.gates.run_all_gates(input_data, session_plan)
        
        # Step 5: Check if any gate failed
        failed_gates = [g for g in validation_results if g.status == "FAIL"]
        
        if failed_gates:
            # Check if it's a QUARANTINE situation (Gate 0 failure)
            if validation_results[0].status == "FAIL":
                response = ResponseBuilder.build_quarantined(input_data, validation_results, computed_limits)
            else:
                response = ResponseBuilder.build_rejected_illegal(input_data, validation_results, computed_limits)
            
            return json.dumps(response, indent=2)
        
        # Step 6: Build weekly aggregation
        weekly_agg = self._build_weekly_aggregation(input_data, session_plan)
        
        # Step 7: SUCCESS - return complete response
        response = ResponseBuilder.build_success(
            input_data,
            session_plan,
            validation_results,
            weekly_agg,
            computed_limits
        )
        
        return json.dumps(response, indent=2)
    
    def _compute_limits(self, input_data: Dict) -> Dict:
        """Compute all applicable limits for this context"""
        population = input_data.get("population")
        session_type = input_data.get("session_type")
        season_type = input_data.get("season_type")
        readiness = input_data.get("readiness_flag")
        
        session_caps = self.limits.get_session_caps(population, session_type, readiness)
        weekly_caps = self.limits.get_weekly_caps(population)
        seasonal_range = self.limits.get_seasonal_range(population, season_type)
        
        return {
            "population": population,
            "session_type": session_type,
            "season_type": season_type,
            "readiness_flag": readiness,
            "session_caps": session_caps,
            "weekly_caps": weekly_caps,
            "seasonal_operating_range": seasonal_range
        }
    
    def _build_weekly_aggregation(self, input_data: Dict, session_plan: Optional[SessionPlan]) -> WeeklyAggregation:
        """Build weekly load aggregation"""
        population = input_data.get("population")
        weekly_caps = self.limits.get_weekly_caps(population)
        
        # Practice exposure (optional)
        practice_exposure = input_data.get("practice_exposure", {})
        tracked_plyo = practice_exposure.get("tracked_plyo_contacts_this_week", 0)
        tracked_sprint = practice_exposure.get("tracked_true_sprint_meters_this_week", 0)
        
        completed_sprint_sessions = input_data.get("completed_sprint_sessions_this_week", 0)
        
        # Current session values
        current_plyo = session_plan.total_plyo_contacts if session_plan else 0
        current_sprint = session_plan.total_sprint_meters if session_plan else 0
        current_has_sprint = (current_sprint > 0)
        
        return WeeklyAggregation(
            week_id=input_data.get("week_id", ""),
            completed_plyo_contacts=tracked_plyo,
            completed_sprint_meters=tracked_sprint,
            completed_sprint_sessions=completed_sprint_sessions,
            planned_plyo_contacts=current_plyo,
            planned_sprint_meters=current_sprint,
            planned_sprint_sessions=1 if current_has_sprint else 0,
            projected_total_plyo_contacts=tracked_plyo + current_plyo,
            projected_total_sprint_meters=tracked_sprint + current_sprint,
            projected_total_sprint_sessions=completed_sprint_sessions + (1 if current_has_sprint else 0),
            weekly_plyo_cap=weekly_caps.get("plyo_contacts_per_week", 0),
            weekly_sprint_meters_cap=weekly_caps.get("sprint_meters_per_week", 0),
            weekly_sprint_sessions_cap=weekly_caps.get("max_sprint_sessions_per_week", 3)
        )


# ============================================================================
# MAIN EXECUTION (for testing)
# ============================================================================

if __name__ == "__main__":
    print("EFL Program Architect v2.2 - Loaded")
    print("Use: epa = EFLProgramArchitect('path/to/library.csv')")
    print("Then: response = epa.process(json_string)")
