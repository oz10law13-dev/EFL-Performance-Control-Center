"""
Court Sport exercise pattern mapper v2 - adjusted for Exercise Library v2.5 reality.
"""

from typing import List, Dict, Optional
import pandas as pd

class CourtSportExerciseMapper:
    """Map Court Sport patterns to Exercise Library exercises (reality-based)"""
    
    # Pattern mapping rules adjusted for actual library structure
    PATTERN_MAP = {
        "bilateral_squat": {
            "movement_pattern": "Squat",
            "name_exclude": ["single", "1 leg", "pistol"],
            "band_max": 2  # Reality: squats are Band_1-2
        },
        "hip_hinge": {
            "movement_pattern": "Deadlift",
            "name_exclude": ["single", "1 leg", "1 arm"],
            "band_max": 2  # Reality: deadlifts are Band_1-2
        },
        "unilateral_knee": {
            "movement_pattern": "Lunge",
            "name_include": ["lunge", "split", "step up", "bulgarian"],
            "band_max": 2  # Reality: lunges are Band_2 (not Band_0-1!)
        },
        "unilateral_hip": {
            "movement_pattern": "Deadlift",
            "name_include": ["single", "1 leg", "SL"],
            "band_max": 2
        },
        "trunk_anti_ext": {
            "movement_pattern": None,
            "name_include": ["plank", "dead bug", "fallout", "rollout", "anti-extension"],
            "band_max": 1  # Reality: planks are Band_1 (not Band_0!)
        },
        "trunk_anti_rot": {
            "movement_pattern": None,
            "name_include": ["pallof", "anti-rotation", "chop", "lift", "bird dog"],
            "band_max": 1
        },
        "calf_ankle": {
            "movement_pattern": None,
            "name_include": ["calf", "heel raise", "toe raise", "ankle"],
            "band_max": 1
        },
        "horizontal_pull": {
            "movement_pattern": "Row",
            "band_max": 2
        },
        "vertical_pull": {
            "movement_pattern": "Pull",
            "name_include": ["pull up", "chin", "lat", "pulldown"],
            "band_max": 2
        },
        "horizontal_push": {
            "movement_pattern": "Push",
            "name_include": ["push up", "bench", "floor press"],
            "name_exclude": ["overhead", "vertical"],
            "band_max": 2
        },
        # E1 plyos - use specific exercise names (no "Hop" pattern with E1!)
        "plyo_e1_pogo": {
            "movement_pattern": None,
            "name_include": ["pogo", "ankle bound", "ankle skip"],
            "enode_required": "E1"
        },
        # E2 plyos - use "Hop" pattern
        "plyo_e2_vertical": {
            "movement_pattern": "Hop",
            "name_include": ["jump", "vertical", "box", "squat jump"],
            "enode_required": "E2"
        },
        "plyo_e2_lateral": {
            "movement_pattern": "Hop",
            "name_include": ["lateral", "side", "bound"],
            "enode_required": "E2"
        }
    }
    
    @staticmethod
    def find_exercises(
        df: pd.DataFrame,
        court_pattern: str,
        readiness_band_override: Optional[int] = None,
        readiness_enode_override: Optional[str] = None,
        exclude_youth: bool = True,
        limit: int = 10
    ) -> List[Dict]:
        """Find exercises for a Court Sport pattern"""
        
        if court_pattern not in CourtSportExerciseMapper.PATTERN_MAP:
            return []
        
        rules = CourtSportExerciseMapper.PATTERN_MAP[court_pattern]
        
        # Start with all exercises
        mask = pd.Series([True] * len(df))
        
        # Filter by movement pattern if specified
        if rules.get("movement_pattern"):
            mask &= df['movement_pattern'] == rules["movement_pattern"]
        
        # Filter by name includes
        if rules.get("name_include"):
            name_mask = pd.Series([False] * len(df))
            for keyword in rules["name_include"]:
                name_mask |= df['exercise_name'].str.contains(keyword, case=False, na=False)
            mask &= name_mask
        
        # Filter by name excludes
        if rules.get("name_exclude"):
            for keyword in rules["name_exclude"]:
                mask &= ~df['exercise_name'].str.contains(keyword, case=False, na=False)
        
        # Filter by band ceiling (use override if provided, else use rule default)
        band_max = readiness_band_override if readiness_band_override is not None else rules.get("band_max")
        if band_max is not None:
            df['band_num'] = df['load_band_primary'].str.extract(r'Band_(\d+)')[0].astype('Int64')
            mask &= (df['band_num'] <= band_max) & (df['band_num'].notna())
        
        # Filter by E-node
        enode = readiness_enode_override if readiness_enode_override else rules.get("enode_required")
        if enode:
            mask &= df['e_node'] == enode
        
        # Exclude youth contraindications
        if exclude_youth:
            mask &= ~df['contraindicated_populations'].str.contains('Youth', case=False, na=False)
        
        # Get results
        results = df[mask].head(limit)
        return results.to_dict('records')


def get_court_sport_mapper():
    """Get mapper instance"""
    return CourtSportExerciseMapper()
