"""
Exercise Library v2.5 loader and validator for EFL Court Sport generator.
Provides exercise selection, validation, and contraindication checking.
"""

import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional

class ExerciseLibrary:
    """Exercise Library v2.5 interface for Court Sport Foundations"""
    
    def __init__(self, csv_path: str = None):
        if csv_path is None:
            csv_path = Path(__file__).parent.parent / "data" / "EFL_Exercise_Library_v2_5.csv"
        
        self.df = pd.read_csv(csv_path)
        print(f"✅ Loaded {len(self.df)} exercises from Exercise Library v2.5")
    
    def find_exercises(
        self,
        movement_pattern: str,
        band_max: Optional[int] = None,
        enode: Optional[str] = None,
        exclude_youth: bool = True,
        limit: int = 10
    ) -> List[Dict]:
        """Find exercises matching criteria"""
        
        # Start with movement pattern match
        mask = self.df['movement_pattern'] == movement_pattern
        
        # Filter by band ceiling (any band <= max)
        if band_max is not None:
            # Extract band number from 'Band_X' string
            self.df['band_num'] = self.df['load_band_primary'].str.extract(r'Band_(\d+)')[0].astype('Int64')
            mask &= (self.df['band_num'] <= band_max) & (self.df['band_num'].notna())
        
        # Filter by E-node
        if enode:
            mask &= self.df['e_node'] == enode
        
        # Exclude youth contraindications
        if exclude_youth:
            mask &= ~self.df['contraindicated_populations'].str.contains('Youth', case=False, na=False)
        
        # Get results
        results = self.df[mask].head(limit)
        
        # Convert to dict list
        return results.to_dict('records')
    
    def get_exercise_by_name(self, name: str) -> Optional[Dict]:
        """Get single exercise by exact name match"""
        match = self.df[self.df['exercise_name'] == name]
        if len(match) > 0:
            return match.iloc[0].to_dict()
        return None
    
    def get_court_sport_exercises(self, readiness: str = "YELLOW", sport: str = "Basketball") -> Dict[str, List[Dict]]:
        """Get curated exercise selection for Court Sport Foundations"""
        
        # Determine band ceiling by readiness
        if readiness == "RED":
            max_band = 1
            enode_allowed = "E0"
        elif readiness == "YELLOW":
            max_band = 1
            enode_allowed = "E1"
        else:  # GREEN
            max_band = 2
            enode_allowed = "E2"
        
        return {
            "squat": self.find_exercises("Squat", band_max=max_band, limit=5),
            "hinge": self.find_exercises("Deadlift", band_max=max_band, limit=5),
            "lunge": self.find_exercises("Lunge", band_max=1, limit=5),
            "push": self.find_exercises("Push", band_max=1, limit=5),
            "pull": self.find_exercises("Pull", band_max=1, limit=5),
            "row": self.find_exercises("Row", band_max=1, limit=5),
            "plyo_e1": self.find_exercises("Hop", enode="E1", limit=10),
            "plyo_e2": self.find_exercises("Hop", enode="E2", limit=10) if enode_allowed == "E2" else []
        }


# Singleton instance
_library = None

def get_exercise_library() -> ExerciseLibrary:
    """Get singleton exercise library instance"""
    global _library
    if _library is None:
        _library = ExerciseLibrary()
    return _library

