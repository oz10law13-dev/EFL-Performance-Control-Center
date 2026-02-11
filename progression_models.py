"""
Evidence-based weekly progression models.
"""

PROGRESSION_MODELS = {
    "Linear_Strength": {
        # Classic linear periodization
        "week_1": {"intensity": 0.70, "volume": "3x8", "rpe": 7},
        "week_2": {"intensity": 0.75, "volume": "4x6", "rpe": 7.5},
        "week_3": {"intensity": 0.80, "volume": "3x5", "rpe": 8},
        "week_4": {"intensity": 0.65, "volume": "2x8", "rpe": 6},  # Deload
        "evidence": "Stone et al. 1999 - Linear progression effective for novices"
    },
    
    "Undulating_Power": {
        # Daily undulating for court sports
        "day_A": {"type": "strength", "intensity": 0.75, "volume": "3x6"},
        "day_B": {"type": "power", "intensity": 0.50, "volume": "3x3", "plyo_contacts": 60},
        "day_C": {"type": "hypertrophy", "intensity": 0.65, "volume": "4x10"},
        "evidence": "Rhea et al. 2002 - DUP superior for trained athletes"
    },
    
    "Block_Periodization": {
        # Accumulation → Intensification → Realization
        "block_1_accumulation": {
            "weeks": 3,
            "focus": "hypertrophy",
            "volume": "high",
            "intensity": "moderate",
            "plyos": "E1_only"
        },
        "block_2_intensification": {
            "weeks": 3,
            "focus": "strength",
            "volume": "moderate",
            "intensity": "high",
            "plyos": "E2_progressive"
        },
        "block_3_realization": {
            "weeks": 2,
            "focus": "power",
            "volume": "low",
            "intensity": "very_high",
            "plyos": "E3_gated"
        },
        "evidence": "Issurin 2010 - Block periodization for advanced athletes"
    }
}
