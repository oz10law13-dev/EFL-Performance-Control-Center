"""
Sport-specific training requirements based on movement analysis and evidence.
"""

SPORT_PROFILES = {
    "Basketball": {
        "description": "High-intensity intermittent sport with vertical jump emphasis",
        
        # Movement analysis
        "movement_demands": {
            "vertical_jump_frequency": "46 jumps/game (Abdelkrim 2007)",
            "sprint_distance": "664m high-intensity running/game (McInnes 1995)",
            "changes_of_direction": "997 per game (Scanlan 2011)",
            "play_duration": "2-6 second bursts"
        },
        
        # Volume distribution (% of total strength work)
        "strength_emphasis": {
            "squat_pattern": 0.35,      # Primary - vertical jump
            "hinge_pattern": 0.20,      # Support - sprint mechanics
            "unilateral": 0.25,         # High - decel demands
            "upper_push": 0.10,
            "upper_pull": 0.10
        },
        
        # Plyometric distribution (% of total plyo contacts)
        "plyo_emphasis": {
            "vertical": 0.50,           # Primary - jump training
            "lateral": 0.25,            # Support - defense slides
            "decel": 0.25               # Critical - injury prevention
        },
        
        # Training constraints
        "constraints": {
            "overhead_pressing": "LIMITED",    # Lower shoulder injury risk
            "max_weekly_contacts": 240,
            "plyo_session_cap": 80,
            "vertical_jump_priority": "HIGH"
        },
        
        # Evidence base
        "evidence": {
            "vertical_jump": "Flanagan & Comyns 2008 - Bilateral and unilateral loading both improve jump height",
            "acl_prevention": "Myer et al. 2013 - Neuromuscular training reduces ACL injury risk by 52%",
            "decel_training": "Dos Santos et al. 2019 - Eccentric strength critical for deceleration capacity"
        },
        
        # Exercise prioritization
        "exercise_priorities": {
            "squat": ["split squat", "step up", "bulgarian", "goblet"],  # Unilateral emphasis
            "hinge": ["rdl", "single leg rdl", "nordics"],
            "plyo": ["box jump", "vertical jump", "continuous jump", "lateral bound", "stick landing"]
        }
    },
    
    "Volleyball": {
        "description": "Repeated vertical jump sport with overhead hitting demands",
        
        # Movement analysis
        "movement_demands": {
            "vertical_jump_frequency": "300+ jumps/match (Sheppard 2007)",
            "overhead_hits": "80-120 per match (Seminati 2013)",
            "block_jumps": "40-60 per match",
            "continuous_play": "Repeated efforts with 5-10s rest"
        },
        
        # Volume distribution
        "strength_emphasis": {
            "squat_pattern": 0.30,
            "hinge_pattern": 0.15,
            "unilateral": 0.25,
            "upper_push": 0.10,         # Limited overhead
            "upper_pull": 0.20          # HIGH - scapular health
        },
        
        # Plyometric distribution
        "plyo_emphasis": {
            "vertical": 0.65,           # VERY HIGH - match demands
            "lateral": 0.15,
            "decel": 0.20
        },
        
        # Training constraints
        "constraints": {
            "overhead_pressing": "RESTRICTED",  # High shoulder injury risk
            "max_weekly_contacts": 280,         # Higher tolerance
            "plyo_session_cap": 90,
            "continuous_jump_training": "REQUIRED"
        },
        
        # Evidence base
        "evidence": {
            "shoulder_health": "Seminati & Minetti 2013 - Scapular dyskinesis in 67% of elite volleyball players",
            "vertical_jump": "Marques et al. 2009 - Depth jumps (60cm) most effective for volleyball athletes",
            "landing_asymmetry": "Lobietti et al. 2010 - Landing asymmetry >15% predicts patellar tendinopathy",
            "continuous_jumps": "Sheppard et al. 2008 - Repeated jump ability distinguishes elite vs sub-elite"
        },
        
        # Exercise prioritization
        "exercise_priorities": {
            "squat": ["front squat", "goblet", "trap bar", "split squat"],
            "hinge": ["rdl", "single leg rdl"],  # Less emphasis than basketball
            "plyo": ["continuous vertical", "repeated box jump", "depth jump", "approach jump", "block jump"],
            "scapular": ["band pull apart", "face pull", "scap push up", "y-raise", "prone t"]
        }
    }
}


def get_sport_profile(sport: str) -> dict:
    """Get evidence-based sport profile"""
    return SPORT_PROFILES.get(sport, SPORT_PROFILES["Basketball"])


def get_sport_emphasis(sport: str, category: str) -> dict:
    """Get emphasis percentages for a category (strength_emphasis or plyo_emphasis)"""
    profile = get_sport_profile(sport)
    return profile.get(category, {})
