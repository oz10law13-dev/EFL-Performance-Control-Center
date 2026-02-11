"""
Sport-specific exercise selection with evidence-based prioritization.
"""

import pandas as pd
from typing import List, Dict
from .sport_profiles import get_sport_profile
from .court_sport_exercise_map import CourtSportExerciseMapper


class SportSpecificExerciseSelector:
    """Select and prioritize exercises based on sport demands"""
    
    @staticmethod
    def select_for_basketball(
        df: pd.DataFrame,
        mapper: CourtSportExerciseMapper,
        band_allowed: int,
        enode_allowed: str,
        limit: int = 5
    ) -> Dict[str, List[Dict]]:
        """
        Basketball-specific exercise selection.
        Priorities: Vertical power, decel, unilateral strength
        """
        
        # Squat: Prioritize unilateral (more sport-specific)
        all_squats = mapper.find_exercises(df, "bilateral_squat", readiness_band_override=band_allowed, limit=20)
        squat_primary = [ex for ex in all_squats if "goblet" in ex["exercise_name"].lower() or "trap" in ex["exercise_name"].lower()][:limit]
        
        # Unilateral: Prioritize split squats and step-ups (decel/acceleration)
        all_unilateral = mapper.find_exercises(df, "unilateral_knee", readiness_band_override=band_allowed, limit=30)
        unilateral = [
            ex for ex in all_unilateral 
            if any(kw in ex["exercise_name"].lower() for kw in ["split", "step up", "bulgarian", "lunge"])
        ][:limit]
        
        # Plyos: Vertical emphasis with decel component
        if enode_allowed == "E2":
            all_vertical = mapper.find_exercises(df, "plyo_e2_vertical", readiness_enode_override="E2", limit=30)
            # Prioritize box jumps and vertical jumps
            vertical_primary = [ex for ex in all_vertical if any(kw in ex["exercise_name"].lower() for kw in ["box", "vertical", "squat jump"])][:limit]
            # Add decel-specific
            decel = [ex for ex in all_vertical if any(kw in ex["exercise_name"].lower() for kw in ["stick", "stabilize", "land"])][:3]
        else:  # E1
            vertical_primary = mapper.find_exercises(df, "plyo_e1_pogo", readiness_enode_override="E1", limit=limit)
            decel = []
        
        # Lateral: For defense
        lateral = mapper.find_exercises(df, "plyo_e2_lateral", readiness_enode_override=enode_allowed, limit=limit) if enode_allowed == "E2" else []
        
        return {
            "squat_primary": squat_primary,
            "unilateral": unilateral,
            "vertical_plyos": vertical_primary,
            "decel_plyos": decel,
            "lateral_plyos": lateral
        }
    
    @staticmethod
    def select_for_volleyball(
        df: pd.DataFrame,
        mapper: CourtSportExerciseMapper,
        band_allowed: int,
        enode_allowed: str,
        limit: int = 5
    ) -> Dict[str, List[Dict]]:
        """
        Volleyball-specific exercise selection.
        Priorities: Repeated vertical jumps, scapular health, rotational power
        """
        
        # Squat: Front rack emphasis (thoracic position)
        all_squats = mapper.find_exercises(df, "bilateral_squat", readiness_band_override=band_allowed, limit=20)
        squat_primary = [ex for ex in all_squats if any(kw in ex["exercise_name"].lower() for kw in ["front", "goblet", "high bar"])][:limit]
        
        # Unilateral: Standard priority
        unilateral = mapper.find_exercises(df, "unilateral_knee", readiness_band_override=band_allowed, limit=limit)
        
        # Plyos: CONTINUOUS/REPEATED emphasis (match demands)
        if enode_allowed == "E2":
            all_vertical = mapper.find_exercises(df, "plyo_e2_vertical", readiness_enode_override="E2", limit=30)
            # Prioritize continuous and repeated jumps
            vertical_primary = [
                ex for ex in all_vertical 
                if any(kw in ex["exercise_name"].lower() for kw in ["continuous", "repeated", "multiple", "approach"])
            ][:limit]
            if len(vertical_primary) < limit:
                vertical_primary.extend([ex for ex in all_vertical if ex not in vertical_primary][:limit - len(vertical_primary)])
        else:  # E1
            vertical_primary = mapper.find_exercises(df, "plyo_e1_pogo", readiness_enode_override="E1", limit=limit)
        
        # Rotational: For hitting mechanics
        all_rotational = mapper.find_exercises(df, "trunk_anti_rot", readiness_band_override=min(band_allowed, 1), limit=20)
        rotational = [
            ex for ex in all_rotational 
            if any(kw in ex["exercise_name"].lower() for kw in ["rotation", "chop", "lift", "throw"])
        ][:limit]
        
        # Scapular: Critical for shoulder health
        all_pull = mapper.find_exercises(df, "horizontal_pull", readiness_band_override=band_allowed, limit=30)
        scapular = [
            ex for ex in all_pull 
            if any(kw in ex["exercise_name"].lower() for kw in ["row", "retraction", "scap", "face pull"])
        ][:limit]
        
        return {
            "squat_primary": squat_primary,
            "unilateral": unilateral,
            "vertical_plyos": vertical_primary,
            "rotational": rotational,
            "scapular": scapular
        }
    
    @staticmethod
    def select_exercises(
        df: pd.DataFrame,
        mapper: CourtSportExerciseMapper,
        sport: str,
        band_allowed: int,
        enode_allowed: str,
        limit: int = 5
    ) -> Dict[str, List[Dict]]:
        """Route to sport-specific selector"""
        
        if sport == "Basketball":
            return SportSpecificExerciseSelector.select_for_basketball(
                df, mapper, band_allowed, enode_allowed, limit
            )
        elif sport == "Volleyball":
            return SportSpecificExerciseSelector.select_for_volleyball(
                df, mapper, band_allowed, enode_allowed, limit
            )
        else:
            # Default to basketball
            return SportSpecificExerciseSelector.select_for_basketball(
                df, mapper, band_allowed, enode_allowed, limit
            )


def get_sport_exercise_selector():
    """Get singleton selector"""
    return SportSpecificExerciseSelector()
