"""
EFL SESSION GENERATOR v1.0
===========================

Complete deterministic session generator for Elite Fitness Lab.
Builds PRIME → PREP → WORK → CLEAR sessions using:
- Exercise Selection Routing v1.2
- Exercise Selection Algorithm v1.1
- EPA v2.2 validation

NO LLM DEPENDENCIES - Pure deterministic logic.

Authority Stack:
1. EFL Load Standards v2.1.2
2. EFL Governance System v4.0
3. EFL Coach AI Playbook v0.4.0
4. EFL Force-Velocity Schema v2.0
5. EFL Exercise Library v2.5
"""

import json
import csv
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# ENUMS & DATA STRUCTURES
# ============================================================================

class Population(Enum):
    YOUTH_8_12 = "Youth_8_12"
    YOUTH_13_17 = "Youth_13_17"
    ADULT = "Adult"


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


@dataclass
class Exercise:
    """Exercise from library with all metadata"""
    exercise_id: str
    exercise_name: str
    movement_pattern: str
    aether_pattern: str
    aether_node: str
    aether_difficulty: str
    load_standard_band: str
    contraindicated_populations: str
    fv_zones: str
    e_node_classification: str
    plyo_contacts: float
    is_plyometric: bool
    is_sprint: bool
    intensity_percent_vmax: float
    equipment: str


@dataclass
class ClientState:
    """Client state with computed legal ceilings"""
    client_id: str
    population: Population
    sport: str
    season_type: SeasonType
    readiness_flag: ReadinessFlag
    injury_flags: List[str]
    
    # Computed ceilings
    max_band_allowed: str
    max_node_allowed: str
    max_e_node_allowed: str
    plyo_contacts_cap_session: int
    plyo_contacts_cap_weekly: int
    sprint_meters_cap_session: int
    sprint_meters_cap_weekly: int
    max_sprint_sessions_per_week: int
    
    # Weekly tracking
    completed_sessions_this_week: int
    completed_sprint_sessions_this_week: int
    weekly_contacts_accumulated: int
    weekly_sprint_meters_accumulated: int


# ============================================================================
# EXERCISE LIBRARY LOADER
# ============================================================================

class ExerciseLibrary:
    """Loads and manages Exercise Library v2.5"""
    
    def __init__(self, csv_path: str):
        self.exercises: Dict[str, Exercise] = {}
        self.load_library(csv_path)
    
    def load_library(self, csv_path: str):
        """Load exercises from CSV"""
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                exercise = Exercise(
                    exercise_id=row['exercise_id'],
                    exercise_name=row['exercise_name'],
                    movement_pattern=row['movement_pattern'],
                    aether_pattern=row['aether_pattern'],
                    aether_node=row['aether_node'],
                    aether_difficulty=row.get('aether_difficulty', ''),
                    load_standard_band=row['load_standard_band'],
                    contraindicated_populations=row.get('contraindicated_populations', ''),
                    fv_zones=row.get('fv_zones', ''),
                    e_node_classification=row.get('e_node_classification', ''),
                    plyo_contacts=float(row.get('plyo_contacts', 0) or 0),
                    is_plyometric=row.get('is_plyometric', 'false').lower() == 'true',
                    is_sprint=row.get('is_sprint', 'false').lower() == 'true',
                    intensity_percent_vmax=float(row.get('intensity_percent_vmax', 0) or 0),
                    equipment=row.get('equipment', '')
                )
                self.exercises[exercise.exercise_id] = exercise
    
    def get(self, exercise_id: str) -> Optional[Exercise]:
        """Get exercise by ID"""
        return self.exercises.get(exercise_id)
    
    def filter(self, **criteria) -> List[Exercise]:
        """Filter exercises by criteria"""
        results = []
        for ex in self.exercises.values():
            match = True
            for key, value in criteria.items():
                if not hasattr(ex, key):
                    match = False
                    break
                if getattr(ex, key) != value:
                    match = False
                    break
            if match:
                results.append(ex)
        return results


# ============================================================================
# CLIENT STATE ENGINE (Governance v4.0)
# ============================================================================

class ClientStateEngine:
    """Computes legal ceilings based on Load Standards v2.1.2"""
    
    # Load Standards v2.1.2 - Population Ceilings
    POPULATION_CEILINGS = {
        Population.YOUTH_8_12: {
            "session_full": 80,
            "session_micro": 50,
            "weekly": 160,
            "sprint_session": 80,
            "sprint_weekly": 240,
            "max_band": "Band_2",
            "max_node": "N2",
            "max_e_node": "E2"
        },
        Population.YOUTH_13_17: {
            "session_full": 120,
            "session_micro": 80,
            "weekly": 240,
            "sprint_session": 200,
            "sprint_weekly": 500,
            "max_band": "Band_3",
            "max_node": "N3",
            "max_e_node": "E4"
        },
        Population.ADULT: {
            "session_full": 140,
            "session_micro": 60,  # Adult MicroSession special rule
            "weekly": 280,
            "sprint_session": 200,
            "sprint_weekly": 500,
            "max_band": "Band_4",
            "max_node": "N4",
            "max_e_node": "E4"
        }
    }
    
    @classmethod
    def compute_state(cls, 
                      client_id: str,
                      population: Population,
                      sport: str,
                      season_type: SeasonType,
                      readiness_flag: ReadinessFlag,
                      injury_flags: List[str],
                      session_type: SessionType,
                      completed_sessions_this_week: int = 0,
                      completed_sprint_sessions_this_week: int = 0,
                      weekly_contacts_accumulated: int = 0,
                      weekly_sprint_meters_accumulated: int = 0) -> ClientState:
        """Compute client state with legal ceilings"""
        
        # Get population base ceilings
        pop_ceilings = cls.POPULATION_CEILINGS[population]
        
        # Session type determines session ceiling
        if session_type == SessionType.FULL_SESSION:
            session_plyo_cap = pop_ceilings["session_full"]
        else:
            session_plyo_cap = pop_ceilings["session_micro"]
        
        # Readiness modifiers (Governance v4.0)
        if readiness_flag == ReadinessFlag.RED:
            # RED = no plyos
            session_plyo_cap = 0
            max_e_node = "E0"
        elif readiness_flag == ReadinessFlag.YELLOW:
            # YELLOW = 0.75x volume, max E2
            session_plyo_cap = int(session_plyo_cap * 0.75)
            max_e_node = "E2"
        else:
            # GREEN = full access
            max_e_node = pop_ceilings["max_e_node"]
        
        return ClientState(
            client_id=client_id,
            population=population,
            sport=sport,
            season_type=season_type,
            readiness_flag=readiness_flag,
            injury_flags=injury_flags,
            max_band_allowed=pop_ceilings["max_band"],
            max_node_allowed=pop_ceilings["max_node"],
            max_e_node_allowed=max_e_node,
            plyo_contacts_cap_session=session_plyo_cap,
            plyo_contacts_cap_weekly=pop_ceilings["weekly"],
            sprint_meters_cap_session=pop_ceilings["sprint_session"],
            sprint_meters_cap_weekly=pop_ceilings["sprint_weekly"],
            max_sprint_sessions_per_week=3,
            completed_sessions_this_week=completed_sessions_this_week,
            completed_sprint_sessions_this_week=completed_sprint_sessions_this_week,
            weekly_contacts_accumulated=weekly_contacts_accumulated,
            weekly_sprint_meters_accumulated=weekly_sprint_meters_accumulated
        )


# ============================================================================
# EXERCISE SELECTION ROUTING v1.2
# ============================================================================

class ExerciseRouter:
    """Filters exercises into PRIME/PREP/WORK/CLEAR candidate pools"""
    
    BAND_ORDER = {"Band_0": 0, "Band_1": 1, "Band_2": 2, "Band_3": 3, "Band_4": 4}
    NODE_ORDER = {"N0": 0, "N1": 1, "N2": 2, "N3": 3, "N4": 4, "A": 1, "B": 2, "C": 3, "D": 4}
    E_NODE_ORDER = {"E0": 0, "E1": 1, "E2": 2, "E3": 3, "E4": 4}
    
    def __init__(self, library: ExerciseLibrary):
        self.library = library
    
    def route(self, client_state: ClientState) -> Dict[str, List[Exercise]]:
        """Route exercises to PRIME/PREP/WORK/CLEAR pools"""
        
        # Apply global filters first
        legal_exercises = self._apply_global_filters(client_state)
        
        # Route to blocks
        pools = {
            "PRIME": self._filter_prime(legal_exercises),
            "PREP": self._filter_prep(legal_exercises),
            "WORK": self._filter_work(legal_exercises, client_state),
            "CLEAR": self._filter_clear(legal_exercises)
        }
        
        return pools
    
    def _apply_global_filters(self, client_state: ClientState) -> List[Exercise]:
        """Global filters: Band/Node/E-Node ceilings, injuries"""
        legal = []
        
        max_band_level = self.BAND_ORDER.get(client_state.max_band_allowed, 0)
        max_node_level = self.NODE_ORDER.get(client_state.max_node_allowed, 0)
        max_e_level = self.E_NODE_ORDER.get(client_state.max_e_node_allowed, 0)
        
        for ex in self.library.exercises.values():
            # Check band ceiling
            ex_band_level = self.BAND_ORDER.get(ex.load_standard_band, 0)
            if ex_band_level > max_band_level:
                continue
            
            # Check node ceiling
            ex_node_level = self.NODE_ORDER.get(ex.aether_node, 0)
            if ex_node_level > max_node_level:
                continue
            
            # Check E-node ceiling
            ex_e_level = self.E_NODE_ORDER.get(ex.e_node_classification, 0)
            if ex_e_level > max_e_level:
                continue
            
            # Check injury contraindications
            if client_state.injury_flags:
                contraindicated = ex.contraindicated_populations.split(',')
                if any(flag in contraindicated for flag in client_state.injury_flags):
                    continue
            
            legal.append(ex)
        
        return legal
    
    def _filter_prime(self, exercises: List[Exercise]) -> List[Exercise]:
        """PRIME block: Mobility, activation, breathing (E0, Band_0-1)"""
        prime_patterns = [
            "Joint-Mobility", "Mobility", "Stability", "Balance-Proprioception",
            "Breathing-Work", "Muscle-Activation", "Foot-Ankle-Work"
        ]
        
        return [
            ex for ex in exercises
            if (ex.aether_pattern in prime_patterns or ex.movement_pattern in prime_patterns)
            and ex.load_standard_band in ["Band_0", "Band_1"]
            and ex.e_node_classification == "E0"
            and not ex.is_plyometric
            and not ex.is_sprint
        ]
    
    def _filter_prep(self, exercises: List[Exercise]) -> List[Exercise]:
        """PREP block: Pattern rehearsal (E0-E1, Band_0-2)"""
        prep_patterns = [
            "Squat", "Hinge", "Lunge", "Push", "Pull",
            "Core", "Carry", "Balance"
        ]
        
        return [
            ex for ex in exercises
            if any(p in ex.movement_pattern or p in ex.aether_pattern for p in prep_patterns)
            and ex.load_standard_band in ["Band_0", "Band_1", "Band_2"]
            and ex.e_node_classification in ["E0", "E1"]
            and not ex.is_sprint  # No sprints in PREP
        ]
    
    def _filter_work(self, exercises: List[Exercise], client_state: ClientState) -> List[Exercise]:
        """WORK block: Main training stimulus"""
        # WORK gets all legal exercises that aren't purely mobility/breathing
        excluded_patterns = ["Breathing-Work", "Joint-Mobility"]
        
        return [
            ex for ex in exercises
            if ex.aether_pattern not in excluded_patterns
            and ex.movement_pattern not in excluded_patterns
        ]
    
    def _filter_clear(self, exercises: List[Exercise]) -> List[Exercise]:
        """CLEAR block: Cool-down, recovery (E0, Band_0-1)"""
        clear_patterns = [
            "Mobility", "Breathing-Work", "Joint-Mobility",
            "Stretching", "Recovery"
        ]
        
        return [
            ex for ex in exercises
            if (ex.aether_pattern in clear_patterns or ex.movement_pattern in clear_patterns)
            and ex.load_standard_band in ["Band_0", "Band_1"]
            and ex.e_node_classification == "E0"
            and not ex.is_plyometric
            and not ex.is_sprint
        ]


# ============================================================================
# EXERCISE SELECTION ALGORITHM v1.1
# ============================================================================

class SessionBuilder:
    """Builds complete PRIME-PREP-WORK-CLEAR sessions with volume control"""
    
    def __init__(self, router: ExerciseRouter):
        self.router = router
    
    def build_session(self, client_state: ClientState, target_zones: List[str] = None) -> Dict:
        """Build complete session"""
        
        # Get candidate pools
        pools = self.router.route(client_state)
        
        # Check if we have enough exercises
        if not all(pools.values()):
            return {
                "status": "QUARANTINED_REVIEW",
                "reason": "Insufficient exercises in candidate pools",
                "pools_summary": {k: len(v) for k, v in pools.items()}
            }
        
        # Build each block
        session = {
            "PRIME": self._build_prime_block(pools["PRIME"]),
            "PREP": self._build_prep_block(pools["PREP"]),
            "WORK": self._build_work_block(pools["WORK"], client_state, target_zones),
            "CLEAR": self._build_clear_block(pools["CLEAR"])
        }
        
        # Calculate totals
        total_plyo_contacts = sum(
            item.get("total_contacts", 0)
            for block in session.values()
            for item in block
        )
        
        total_sprint_meters = sum(
            item.get("total_sprint_meters", 0)
            for block in session.values()
            for item in block
        )
        
        return {
            "status": "SUCCESS",
            "session_plan": session,
            "total_plyo_contacts": total_plyo_contacts,
            "total_sprint_meters": total_sprint_meters,
            "pools_used": {k: len(v) for k, v in pools.items()}
        }
    
    def _build_prime_block(self, candidates: List[Exercise]) -> List[Dict]:
        """Build PRIME block (5-10 min): 2-3 exercises"""
        selected = candidates[:3] if len(candidates) >= 3 else candidates
        
        return [
            {
                "exercise_id": ex.exercise_id,
                "exercise_name": ex.exercise_name,
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
            for ex in selected
        ]
    
    def _build_prep_block(self, candidates: List[Exercise]) -> List[Dict]:
        """Build PREP block (8-12 min): 2-3 exercises"""
        selected = candidates[:3] if len(candidates) >= 3 else candidates
        
        return [
            {
                "exercise_id": ex.exercise_id,
                "exercise_name": ex.exercise_name,
                "sets": 2,
                "reps": 6,
                "rest_seconds": 45,
                "load": "Light" if ex.load_standard_band in ["Band_1", "Band_2"] else "Bodyweight",
                "rpe_target": 4,
                "tempo": "3-1-1",
                "coaching_cues": ["Control descent", "Explosive concentric"],
                "total_contacts": int(2 * 6 * ex.plyo_contacts) if ex.is_plyometric else 0,
                "total_sprint_meters": 0
            }
            for ex in selected
        ]
    
    def _build_work_block(self, candidates: List[Exercise], 
                          client_state: ClientState,
                          target_zones: List[str] = None) -> List[Dict]:
        """Build WORK block (25-35 min): 3-5 exercises with volume control"""
        
        # Filter by target zones if specified
        if target_zones:
            candidates = [
                ex for ex in candidates
                if any(zone in ex.fv_zones for zone in target_zones)
            ]
        
        # Select exercises ensuring pattern variety
        selected = []
        patterns_used = set()
        plyo_contacts_accumulated = 0
        
        for ex in candidates:
            # Skip if pattern already used (ensure variety)
            base_pattern = ex.movement_pattern.split('-')[0] if '-' in ex.movement_pattern else ex.movement_pattern
            if base_pattern in patterns_used:
                continue
            
            # Check plyo contact budget
            if ex.is_plyometric:
                potential_contacts = int(3 * 8 * ex.plyo_contacts)
                if plyo_contacts_accumulated + potential_contacts > client_state.plyo_contacts_cap_session:
                    continue
                plyo_contacts_accumulated += potential_contacts
            
            selected.append(ex)
            patterns_used.add(base_pattern)
            
            if len(selected) >= 4:
                break
        
        # Build items
        items = []
        for ex in selected:
            if ex.is_plyometric:
                # Plyometric exercises: lower reps, more sets
                sets, reps = 3, 8
                rest = 90
                rpe = 7
            elif ex.load_standard_band in ["Band_3", "Band_4"]:
                # Heavy strength: lower reps
                sets, reps = 4, 5
                rest = 180
                rpe = 8
            else:
                # Moderate work
                sets, reps = 3, 8
                rest = 90
                rpe = 7
            
            total_contacts = int(sets * reps * ex.plyo_contacts) if ex.is_plyometric else 0
            
            items.append({
                "exercise_id": ex.exercise_id,
                "exercise_name": ex.exercise_name,
                "sets": sets,
                "reps": reps,
                "rest_seconds": rest,
                "load": self._prescribe_load(ex.load_standard_band),
                "rpe_target": rpe,
                "tempo": "Explosive" if ex.is_plyometric else "Controlled",
                "coaching_cues": self._generate_cues(ex),
                "total_contacts": total_contacts,
                "total_sprint_meters": 0
            })
        
        return items
    
    def _build_clear_block(self, candidates: List[Exercise]) -> List[Dict]:
        """Build CLEAR block (5-10 min): 2 exercises"""
        selected = candidates[:2] if len(candidates) >= 2 else candidates
        
        return [
            {
                "exercise_id": ex.exercise_id,
                "exercise_name": ex.exercise_name,
                "sets": 1,
                "reps": 8,
                "rest_seconds": 0,
                "load": "Bodyweight",
                "rpe_target": 2,
                "tempo": "Slow/Relaxed",
                "coaching_cues": ["Deep breathing", "Relax into stretch"],
                "total_contacts": 0,
                "total_sprint_meters": 0
            }
            for ex in selected
        ]
    
    def _prescribe_load(self, band: str) -> str:
        """Prescribe load description based on band"""
        load_map = {
            "Band_0": "Bodyweight",
            "Band_1": "Light (60-70% 1RM)",
            "Band_2": "Moderate (70-80% 1RM)",
            "Band_3": "Heavy (80-90% 1RM)",
            "Band_4": "Max (90-100% 1RM)"
        }
        return load_map.get(band, "Bodyweight")
    
    def _generate_cues(self, exercise: Exercise) -> List[str]:
        """Generate coaching cues based on exercise type"""
        if exercise.is_plyometric:
            return ["Stick landing", "Quick ground contact", "Drive through hips"]
        elif "Squat" in exercise.movement_pattern:
            return ["Chest up", "Knees out", "Full depth"]
        elif "Hinge" in exercise.movement_pattern:
            return ["Flat back", "Push hips back", "Drive through heels"]
        elif "Push" in exercise.movement_pattern:
            return ["Tight core", "Full lockout", "Control eccentric"]
        elif "Pull" in exercise.movement_pattern:
            return ["Retract scaps", "Pull to chest", "Control tempo"]
        else:
            return ["Quality movement", "Full ROM", "Control breathing"]


# ============================================================================
# MAIN SESSION GENERATOR
# ============================================================================

class EFLSessionGenerator:
    """Main session generator combining all components"""
    
    def __init__(self, library_path: str):
        self.library = ExerciseLibrary(library_path)
        self.router = ExerciseRouter(self.library)
        self.builder = SessionBuilder(self.router)
    
    def generate_session(self,
                        client_id: str,
                        population: str,
                        sport: str,
                        season_type: str,
                        readiness_flag: str = "GREEN",
                        session_type: str = "FULL_SESSION",
                        injury_flags: List[str] = None,
                        target_zones: List[str] = None,
                        **kwargs) -> Dict:
        """Generate complete session"""
        
        # Convert strings to enums
        pop_enum = Population(population)
        season_enum = SeasonType(season_type)
        readiness_enum = ReadinessFlag(readiness_flag)
        session_enum = SessionType(session_type)
        
        # Compute client state
        client_state = ClientStateEngine.compute_state(
            client_id=client_id,
            population=pop_enum,
            sport=sport,
            season_type=season_enum,
            readiness_flag=readiness_enum,
            injury_flags=injury_flags or [],
            session_type=session_enum,
            **kwargs
        )
        
        # Build session
        result = self.builder.build_session(client_state, target_zones)
        
        # Add client context to result
        result["client_state"] = {
            "client_id": client_state.client_id,
            "population": client_state.population.value,
            "sport": client_state.sport,
            "season_type": client_state.season_type.value,
            "readiness_flag": client_state.readiness_flag.value,
            "max_band_allowed": client_state.max_band_allowed,
            "max_e_node_allowed": client_state.max_e_node_allowed,
            "plyo_contacts_cap_session": client_state.plyo_contacts_cap_session,
            "plyo_contacts_cap_weekly": client_state.plyo_contacts_cap_weekly
        }
        
        return result


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("EFL SESSION GENERATOR v1.0 - TEST")
    print("=" * 80)
    
    # Initialize generator
    library_path = r"C:\EFL-Governance-and-Programs\EFL_Exercise_Library_v2_5.csv"
    generator = EFLSessionGenerator(library_path)
    
    print(f"\n✅ Generator initialized")
    print(f"   Library loaded: {len(generator.library.exercises)} exercises")
    
    # Generate test session
    print("\n" + "=" * 80)
    print("GENERATING SESSION: Youth 13-17, Basketball, Off-Season")
    print("=" * 80)
    
    result = generator.generate_session(
        client_id="TEST_ATHLETE_001",
        population="Youth_13_17",
        sport="Basketball",
        season_type="OFF_SEASON",
        readiness_flag="GREEN",
        session_type="FULL_SESSION",
        target_zones=["Zone_5", "Zone_6", "Zone_3"]  # Capacity + Reactive Power
    )
    
    # Display results
    if result["status"] == "SUCCESS":
        print("\n✅ SESSION GENERATED SUCCESSFULLY")
        print(f"\n📊 TOTALS:")
        print(f"   Plyo Contacts: {result['total_plyo_contacts']}")
        print(f"   Sprint Meters: {result['total_sprint_meters']}")
        
        print(f"\n🏋️ SESSION STRUCTURE:")
        for block_name, items in result["session_plan"].items():
            print(f"\n   {block_name} ({len(items)} exercises):")
            for item in items:
                contacts = f" ({item['total_contacts']} contacts)" if item['total_contacts'] > 0 else ""
                print(f"      • {item['exercise_name']}: {item['sets']}x{item['reps']}{contacts}")
        
        print(f"\n💾 Full session JSON ready for EPA validation")
        
    else:
        print(f"\n❌ SESSION GENERATION FAILED")
        print(f"   Status: {result['status']}")
        print(f"   Reason: {result.get('reason', 'Unknown')}")
