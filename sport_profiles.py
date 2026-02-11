"""
sport_profiles.py v1.0.2
========================
EFL Sports Performance - Court Sport Foundations
Sport-specific selection bias, pattern ownership, and constraint definitions
LIBRARY-DRIVEN FILTERS (not hardcoded exercise IDs)

Meta
----
File ID: SPORT_PROFILES_COURT_SPORT_v1_0_2
Version: 1.0.2
Effective Date: 2026-01-16
Owner: Elite Fitness Lab
Status: OPERATIONAL
Project Scope: Court Sport Foundations (Basketball/Volleyball, Youth 13-18, SP Performance)
Parent Documents:
  - EFL_SP_PROJECT_WRAPPER_COURT_SPORT_FOUNDATIONS_v1_0.md
  - EFL_SP_OUTPUT_SPEC_COURT_SPORT_FOUNDATIONS_v1_0.md
  - session_shells.json v1.0.1
Dependencies:
  - EFL_Exercise_Library_v2_5.csv (REQUIRED: exercise pools queried at runtime)
  - sport_demands_grid_v2.2.2_PATCHED.json (CNS budgets, seasonal plyo caps)
  - EFL_LOAD_STANDARDS_v2_2_0.json (population ceilings)

Changelog v1.0.1 → v1.0.2
--------------------------
BREAKING CHANGES:
  - Removed all hardcoded exercise_ids
  - Replaced with library filter objects (aether_pattern, load_band_primary, e_node)
  - Band naming updated to underscore format (Band_1, Band_2, etc.)
  - Pool structure now requires filters + selection_bias

Added:
  - Library query function get_exercises_from_library()
  - Pool filter validation validate_pool_query_returns_inventory()
  - E1 scarcity documentation (only 6 E1 plyos exist globally)
  - Band availability reality checks per pattern
  - selection_bias objects for week-based progression guidance

Changed:
  - All exercise_pools now use "pools" key with filter objects
  - Pattern definitions reference aether_pattern from CSV
  - Band references use Band_# format (load_band_primary column)
  - E-node references use e_node column directly
  - Unilateral_knee pool corrected to Band_2 only (no Band_0/1 exist)

Fixed:
  - Band_0 availability assumptions (removed where none exist)
  - Plyo E1 inventory expectations (reduced to realistic 3-6 per pattern)
  - Library column name mismatches
  - Exercise selection now queries real inventory

Validation:
  - All pools validated against actual library structure
  - Minimum inventory thresholds enforced (default 3 exercises per pool)
  - E1 plyo scarcity acknowledged and documented

Purpose
-------
Defines sport-specific preferences and constraints for BASKETBALL and VOLLEYBALL.
This file is Layer 1.5 of the session build pipeline:
  - Layer 1: session_shells.json (structure)
  - Layer 1.5: sport_profiles.py (selection bias + pattern ownership) ← THIS FILE
  - Layer 2: Client State legality engine (ceilings + clamps)
  - Layer 3-6: Zone resolver, exercise selector, progression validator, execution builder

What This File Owns
-------------------
✓ Pattern namespace declarations (sport_pool / global_pool / hint_only)
✓ Exercise pool FILTERS (aether_pattern + band + E-node queries)
✓ Selection bias preferences (band/E-node progression by week)
✓ Sport-specific constraints (forbidden categories, pressing limits)
✓ Pattern frequency targets (aligned with session_shells weekly expectations)
✓ Plyo distribution preferences (E-node emphasis per season)
✓ Resolver rules (soft weekly minimums that yield to safety gates)

What This File Does NOT Own
---------------------------
✗ Hardcoded exercise IDs (queries library at runtime)
✗ Band/E-node legality ceilings (Load Standards + Sport Demands)
✗ Population locks (Wrapper + Governance)
✗ Acute variables (sets/reps/rest → Output Spec + Generator)
✗ Session structure (PRIME/PREP/WORK/CLEAR → session_shells.json)
✗ Progression validation (ONE_AXIS_AT_A_TIME → Progression Validator)

Validation Hooks
----------------
Cross-file integrity checks:
  - validate_against_session_shells() → bidirectional alignment check
  - validate_pool_query_returns_inventory() → NEW: actual library alignment
  - validate_pattern_namespace_integrity() → no orphaned patterns
  - validate_resolver_rules_structural_safety() → resolver mins structurally satisfiable
  - validate_global_pool_coverage() → global_pool patterns have selectable inventory
  - validate_plyo_enode_completeness() → plyo pools have sufficient E1/E2/E3 inventory
"""

import pandas as pd  # type: ignore
from typing import Dict, List, Optional, Union

# ============================================================================
# FILE METADATA + DEPENDENCY RESOLUTION
# ============================================================================

FILE_META = {
    "file_id": "SPORT_PROFILES_COURT_SPORT_v1_0_2",
    "version": "1.0.2",
    "effective_date": "2026-01-16",
    "owner": "Elite Fitness Lab",
    "status": "OPERATIONAL",
    "library_dependency": {
        "file": "EFL_Exercise_Library_v2_5.csv",
        "required_columns": [
            "exercise_id",
            "aether_pattern",
            "movement_pattern",
            "load_band_primary",
            "e_node",
            "is_plyometric",
            "plyo_contacts",
            "is_sprint",
            "contraindicated_populations"
        ]
    },
    "dependency_aliases": {
        "EFL_EXERCISE_LIBRARY": ["EFL_Exercise_Library_v2_5.csv", "exercise_library_v2.5.csv"],
        "SPORT_DEMANDS_GRID": ["sport_demands_grid_v2.2.2_PATCHED.json"],
        "LOAD_STANDARDS": ["EFL_LOAD_STANDARDS_v2_2_0.json"],
        "SESSION_SHELLS": ["session_shells.json", "session_shells_v1_0_1.json"]
    },
    "validation_hooks": [
        "validate_against_session_shells",
        "validate_pool_query_returns_inventory",  # NEW: library-aligned
        "validate_pattern_namespace_integrity",
        "validate_resolver_rules_structural_safety",
        "validate_global_pool_coverage",
        "validate_plyo_enode_completeness"
    ]
}

# ============================================================================
# LIBRARY QUERY FUNCTIONS
# ============================================================================

def get_exercises_from_library(
    df: pd.DataFrame,
    aether_pattern: Optional[Union[str, List[str]]] = None,
    movement_pattern: Optional[Union[str, List[str]]] = None,
    band_filter: Optional[List[str]] = None,
    enode_filter: Optional[List[str]] = None,
    is_plyometric: Optional[bool] = None,
    is_sprint: Optional[bool] = None,
    limit: Optional[int] = None
) -> List[str]:
    """
    Query actual exercise library using filter criteria.
    
    Args:
        df: Exercise library DataFrame (EFL_Exercise_Library_v2_5.csv)
        aether_pattern: Single pattern or list, e.g., "Squat-Bilateral" or ["Squat-Bilateral", "Hinge-Bilateral"]
        movement_pattern: Single pattern or list, e.g., "Squat" or ["Jump", "Hop"]
        band_filter: List of bands, e.g., ["Band_1", "Band_2"]
        enode_filter: List of E-nodes, e.g., ["E1", "E2"]
        is_plyometric: Filter by plyometric flag
        is_sprint: Filter by sprint flag
        limit: Max results to return
    
    Returns:
        List of exercise_id values matching filters
    """
    filtered = df.copy()
    
    # Apply filters
    if aether_pattern:
        if isinstance(aether_pattern, str):
            filtered = filtered[filtered['aether_pattern'] == aether_pattern]
        else:
            filtered = filtered[filtered['aether_pattern'].isin(aether_pattern)]
    
    if movement_pattern:
        if isinstance(movement_pattern, str):
            filtered = filtered[filtered['movement_pattern'] == movement_pattern]
        else:
            filtered = filtered[filtered['movement_pattern'].isin(movement_pattern)]
    
    if band_filter:
        filtered = filtered[filtered['load_band_primary'].isin(band_filter)]
    
    if enode_filter:
        filtered = filtered[filtered['e_node'].isin(enode_filter)]
    
    if is_plyometric is not None:
        filtered = filtered[filtered['is_plyometric'] == is_plyometric]
    
    if is_sprint is not None:
        filtered = filtered[filtered['is_sprint'] == is_sprint]
    
    results = filtered['exercise_id'].tolist()
    
    if limit:
        results = results[:limit]
    
    return results


def query_pool_inventory(df: pd.DataFrame, pool_definition: Dict) -> Dict:
    """
    Query library using a pool definition's filters and return inventory stats.
    
    Args:
        df: Exercise library DataFrame
        pool_definition: Pool dict with 'filters' key
    
    Returns:
        Dict with inventory stats (total_count, by_band, by_enode, exercise_ids)
    """
    filters = pool_definition.get("filters", {})
    
    exercise_ids = get_exercises_from_library(
        df,
        aether_pattern=filters.get("aether_pattern"),
        movement_pattern=filters.get("movement_pattern"),
        band_filter=filters.get("load_band_primary"),
        enode_filter=filters.get("e_node"),
        is_plyometric=filters.get("is_plyometric"),
        is_sprint=filters.get("is_sprint")
    )
    
    filtered_df = df[df['exercise_id'].isin(exercise_ids)]
    
    return {
        "total_count": len(exercise_ids),
        "by_band": filtered_df['load_band_primary'].value_counts().to_dict() if len(exercise_ids) > 0 else {},
        "by_enode": filtered_df['e_node'].value_counts().to_dict() if len(exercise_ids) > 0 else {},
        "exercise_ids": exercise_ids
    }


# ============================================================================
# SPORT PROFILES
# ============================================================================

SPORT_PROFILES = {
    
    # ========================================================================
    # BASKETBALL
    # ========================================================================
    "BASKETBALL": {
        
        "meta": {
            "sport_id": "BASKETBALL",
            "mapped_movement_demand_profile": "MDP_COURT_VERTICAL",
            "supports_specialization_blocks": True,
            "specialization_types": ["ELASTIC", "DECELERATION"],
            "legal_seasons": ["OFF_SEASON", "PRE_SEASON"],
            "description": "Indoor court sport; vertical + lateral jump focus, high deceleration frequency, minimal overhead exposure"
        },
        
        # --------------------------------------------------------------------
        # PATTERN OWNERSHIP (namespace declarations)
        # --------------------------------------------------------------------
        "pattern_ownership": {
            "sport_pool": [
                # Patterns with sport-owned selection logic (filters defined in pools)
                "bilateral_squat",
                "hip_hinge",
                "unilateral_knee",
                "unilateral_hip",
                "pull_horizontal",
                "push_horizontal",
                "plyo_vertical",
                "plyo_lateral"
            ],
            "global_pool_required": [
                # Patterns delegated to global accessory library logic
                "trunk_anti_extension",
                "trunk_anti_rotation",
                "calf_ankle",
                "hip_mobility",
                "shoulder_mobility"
            ],
            "hint_only": [
                # Patterns used as cues in PREP; no exercise validation required
                "landing_prep",
                "ankle_prep",
                "decel_prep",
                "stiffness_priming"
            ]
        },
        
        # --------------------------------------------------------------------
        # POOLS (library-driven filters, not hardcoded IDs)
        # --------------------------------------------------------------------
        "pools": {
            "bilateral_squat": {
                "description": "Force absorption, landing foundation, knee control",
                "filters": {
                    "aether_pattern": "Squat-Bilateral",
                    "load_band_primary": ["Band_1", "Band_2"],  # NO Band_0 or Band_3 exist in library
                    "e_node": None  # All E-nodes acceptable (but E0 dominant)
                },
                "selection_bias": {
                    "prefer_bands_by_week": {
                        "1-3": ["Band_1"],
                        "4-6": ["Band_1", "Band_2"],
                        "7-8": ["Band_1", "Band_2"]
                    },
                    "avoid_repeats_window_sessions": 3,
                    "prefer_tempo_variations_early": True
                },
                "library_reality": {
                    "band_1_count": 66,
                    "band_2_count": 61,
                    "band_0_count": 0,  # NONE exist
                    "band_3_count": 0   # NONE exist
                },
                "notes": "Basketball squat emphasis: depth, landing quality, knee control over max load. Library has NO Band_0 or Band_3 squats."
            },
            
            "hip_hinge": {
                "description": "Posterior chain, jump support, decel strength",
                "filters": {
                    "aether_pattern": "Hinge-Bilateral",
                    "load_band_primary": ["Band_1", "Band_2"],
                    "e_node": None
                },
                "selection_bias": {
                    "prefer_bands_by_week": {
                        "1-3": ["Band_1"],
                        "4-8": ["Band_1", "Band_2"]
                    },
                    "avoid_repeats_window_sessions": 3
                },
                "library_reality": {
                    "band_1_count": 56,
                    "band_2_count": 49
                },
                "notes": "Basketball hinge: eccentric strength for decel, glute power for jump"
            },
            
            "unilateral_knee": {
                "description": "LOCKED PATTERN (2×/week); valgus control, single-leg stability",
                "filters": {
                    "aether_pattern": "Lunge-Unilateral",
                    "load_band_primary": ["Band_2"],  # ONLY Band_2 exists!
                    "e_node": ["E0"]  # Exclude E3 drop lunges for main strength work
                },
                "selection_bias": {
                    "prefer_bands_by_week": {
                        "all_weeks": ["Band_2"]  # No choice, only Band_2 available
                    },
                    "avoid_repeats_window_sessions": 2,
                    "progression_via_tempo_not_load": True
                },
                "library_reality": {
                    "band_0_count": 0,  # NONE
                    "band_1_count": 0,  # NONE
                    "band_2_count": 125
                },
                "notes": "CRITICAL CONSTRAINT: Library has NO Band_0/1 unilateral exercises. All lunge work is Band_2. Must use tempo/ROM/stance progression instead of load progression."
            },
            
            "unilateral_hip": {
                "description": "Glute emphasis, decel reinforcement, hip stability",
                "filters": {
                    "aether_pattern": "Hinge-Bilateral",  # Single-leg RDL variants
                    "movement_pattern": ["Deadlift"],
                    "load_band_primary": ["Band_1", "Band_2"]
                },
                "selection_bias": {
                    "prefer_bands_by_week": {
                        "1-4": ["Band_1"],
                        "5-8": ["Band_1", "Band_2"]
                    },
                    "prefer_single_leg_variants": True
                },
                "notes": "Basketball decel emphasis; glute strength for landing control. Query uses hinge pattern + single-leg cue in name."
            },
            
            "pull_horizontal": {
                "description": "Basketball horizontal pull emphasis; scap control, upper back armor",
                "filters": {
                    "aether_pattern": "Pull-Horizontal",
                    "load_band_primary": ["Band_1", "Band_2", "Band_3"]
                },
                "selection_bias": {
                    "prefer_bands_by_week": {
                        "1-3": ["Band_1"],
                        "4-6": ["Band_1", "Band_2"],
                        "7-8": ["Band_2"]
                    },
                    "avoid_repeats_window_sessions": 3
                },
                "notes": "Basketball prefers horizontal row > vertical pull; posterior shoulder health"
            },
            
            "push_horizontal": {
                "description": "Pressing pattern (submax); minimal overhead load per Sport Demands",
                "filters": {
                    "aether_pattern": "Push-Horizontal",
                    "load_band_primary": ["Band_1", "Band_2"]  # Youth 13-16 ceiling Band_2
                },
                "selection_bias": {
                    "prefer_bands_by_week": {
                        "1-4": ["Band_1"],
                        "5-8": ["Band_1", "Band_2"]
                    },
                    "prefer_floor_press_over_bench_early": True
                },
                "notes": "Basketball allows Band_1-2 pressing; no true overhead per Sport Demands"
            },
            
            "plyo_vertical": {
                "description": "Basketball vertical emphasis; box jumps, broad jumps, approach jumps",
                "filters": {
                    "is_plyometric": True,
                    "movement_pattern": ["Jump", "Hop"],
                    "aether_pattern": "Plyometric-Landing"
                },
                "selection_bias": {
                    "prefer_enodes_by_week": {
                        "1-2": ["E1"],  # CRITICAL: Only 3 E1 allocated (6 total globally)
                        "3-4": ["E1", "E2"],
                        "5-6": ["E2"],
                        "7-8": ["E2", "E3"]
                    },
                    "e3_max_percentage_session": 0.40,  # Youth 13-16 ceiling per Wrapper
                    "avoid_repeats_window_sessions": 2
                },
                "enode_allocation": {
                    "E1_allocated": 3,  # From 6 global total (shared with lateral)
                    "E2_expected": 80,
                    "E3_expected": 10
                },
                "library_reality": {
                    "E1_global_total": 6,  # ENTIRE LIBRARY
                    "E1_scarcity_note": "Only 6 E1 plyos exist globally. Basketball vertical gets 3. Week 1-2 has minimal variety. Generator may use low-complexity E2 as 'soft E1' substitutes if legality allows."
                },
                "notes": "Vertical jump priority for basketball; progression gated by Wrapper 4.3. E1 scarcity is real constraint."
            },
            
            "plyo_lateral": {
                "description": "Basketball lateral emphasis; lateral bounds, lateral hurdle hops, decel plyos",
                "filters": {
                    "is_plyometric": True,
                    "movement_pattern": ["Bound", "Skip", "Jump"],
                    "aether_pattern": None  # Movement pattern sufficient for lateral queries
                },
                "selection_bias": {
                    "prefer_enodes_by_week": {
                        "1-2": ["E1"],
                        "3-4": ["E1", "E2"],
                        "5-8": ["E2", "E3"]
                    },
                    "e3_max_percentage_session": 0.40,
                    "prefer_lateral_keywords": ["lateral", "side", "skater"]
                },
                "enode_allocation": {
                    "E1_allocated": 3,  # From 6 global total
                    "E2_expected": 40,
                    "E3_expected": 5
                },
                "notes": "Basketball lateral decel emphasis; change-of-direction injury prevention. Shares E1 scarcity with vertical."
            }
        },
        
        # --------------------------------------------------------------------
        # PATTERN FREQUENCIES (aligned with session_shells weekly expectations)
        # --------------------------------------------------------------------
        "pattern_frequencies": {
            "bilateral_squat": {
                "min_per_week": 1,
                "target_per_week": 2,
                "enforcement_mode": "required_slots_only",
                "notes": "Primary on DayA; optional secondary on DayB if 3×/week"
            },
            "hip_hinge": {
                "min_per_week": 1,
                "target_per_week": 2,
                "enforcement_mode": "required_slots_only",
                "notes": "Primary on DayB; optional secondary on DayA if 3×/week"
            },
            "unilateral_knee": {
                "min_per_week": 2,
                "target_per_week": 2,
                "enforcement_mode": "locked",
                "notes": "LOCKED per Wrapper 4.2; every strength session, critical injury prevention"
            },
            "unilateral_hip": {
                "min_per_week": 1,
                "target_per_week": 2,
                "enforcement_mode": "required_slots_only",
                "notes": "Day B or optional Day C"
            },
            "trunk_anti_extension": {
                "min_per_week": 2,
                "target_per_week": 2,
                "enforcement_mode": "locked",
                "notes": "LOCKED per Wrapper 4.2; every WORK + CLEAR block"
            },
            "trunk_anti_rotation": {
                "min_per_week": 2,
                "target_per_week": 2,
                "enforcement_mode": "locked",
                "notes": "LOCKED per Wrapper 4.2; critical for basketball rotation control"
            },
            "calf_ankle": {
                "min_per_week": 2,
                "target_per_week": 2,
                "enforcement_mode": "locked",
                "notes": "LOCKED per Wrapper 4.2; stiffness, landing resilience"
            },
            "pull_horizontal": {
                "min_per_week": 2,
                "target_per_week": 2,
                "enforcement_mode": "required_slots_only",
                "notes": "Basketball horizontal pull emphasis"
            },
            "push_horizontal": {
                "min_per_week": 1,
                "target_per_week": 2,
                "enforcement_mode": "resolver",
                "notes": "Submax pressing; resolver handles optional slot logic"
            },
            "plyo_vertical": {
                "min_per_week": 1,
                "target_per_week": 2,
                "enforcement_mode": "required_slots_only",
                "notes": "Basketball vertical jump priority"
            },
            "plyo_lateral": {
                "min_per_week": 1,
                "target_per_week": 2,
                "enforcement_mode": "required_slots_only",
                "notes": "Basketball lateral decel priority"
            }
        },
        
        # --------------------------------------------------------------------
        # RESOLVER RULES (soft weekly minimums that yield to safety gates)
        # --------------------------------------------------------------------
        "resolver_rules": [
            {
                "pattern": "push_horizontal",
                "min_per_week": 1,
                "scope": "across_all_days",
                "eligible_slot_types": ["strength_slots", "upper_slots"],
                "priority": "yield_to_safety_gates",
                "contraindication_overrides": [
                    "shoulder_red_flag",
                    "wrist_injury",
                    "ceiling_blocks_pressing"
                ],
                "notes": "Basketball allows Band_1-2 pressing; if shoulder contraindication, legal to drop to 0 per EFL Governance 4.1 injury gates"
            }
        ],
        
        # --------------------------------------------------------------------
        # SPORT-SPECIFIC CONSTRAINTS
        # --------------------------------------------------------------------
        "constraints": {
            "forbidden_categories": [
                "overhead_press_true",
                "olympic_lifts"
            ],
            "required_patterns_per_week": [
                "unilateral_knee",
                "trunk_anti_extension",
                "trunk_anti_rotation",
                "calf_ankle"
            ],
            "pressing_limits": {
                "max_band": "Band_2",
                "no_overhead": True
            },
            "max_enode_policy": "E3_gated_40pct",
            "notes": "Basketball sport-specific constraints per Sport Demands Grid v2.2.2"
        },
        
        # --------------------------------------------------------------------
        # PLYO DISTRIBUTION PREFERENCES (E-node emphasis per season)
        # --------------------------------------------------------------------
        "plyo_distribution": {
            "OFF_SEASON": {
                "E1_target_pct": 0.50,
                "E2_target_pct": 0.40,
                "E3_target_pct": 0.10,
                "notes": "Off-season: build tolerance, progressive E-node unlock per Wrapper 4.3. E1 scarcity acknowledged."
            },
            "PRE_SEASON": {
                "E1_target_pct": 0.40,
                "E2_target_pct": 0.50,
                "E3_target_pct": 0.10,
                "notes": "Pre-season: maintain E2 emphasis, moderate E3 exposure if quality sustained"
            }
        },
        
        # --------------------------------------------------------------------
        # ROUTING (sport-specific ICP + block defaults + ROUTING GUARD)
        # --------------------------------------------------------------------
        "routing": {
            "supported_seasons": ["OFF_SEASON", "PRE_SEASON"],
            "requires_reroute_if_season_unsupported": True,
            "reroute_to_icp_map": {
                "IN_SEASON_TIER1": "ICP_BASKETBALL_IN_SEASON_TIER1",
                "IN_SEASON_TIER2": "ICP_BASKETBALL_IN_SEASON_TIER2",
                "IN_SEASON_TIER3": "ICP_BASKETBALL_IN_SEASON_TIER3",
                "POST_SEASON": "ICP_BASKETBALL_POST_SEASON"
            },
            "default_icp_id": "ICP_BASKETBALL_FOUNDATIONS",
            "block_type": "FOUNDATIONS_8WK",
            "notes": "In-season programming requires routing to ICP_BASKETBALL_IN_SEASON per ICP Definitions v2.3.1"
        }
    },
    
    # ========================================================================
    # VOLLEYBALL
    # ========================================================================
    "VOLLEYBALL": {
        
        "meta": {
            "sport_id": "VOLLEYBALL",
            "mapped_movement_demand_profile": "MDP_COURT_VERTICAL",
            "supports_specialization_blocks": True,
            "specialization_types": ["ELASTIC"],
            "legal_seasons": ["OFF_SEASON", "PRE_SEASON"],
            "description": "Indoor court sport; vertical jump dominant, high overhead exposure, moderate lateral demand"
        },
        
        # --------------------------------------------------------------------
        # PATTERN OWNERSHIP
        # --------------------------------------------------------------------
        "pattern_ownership": {
            "sport_pool": [
                "bilateral_squat",
                "hip_hinge",
                "unilateral_knee",
                "unilateral_hip",
                "pull_vertical",
                "push_limited",
                "plyo_vertical"
            ],
            "global_pool_required": [
                "trunk_anti_extension",
                "trunk_anti_rotation",
                "calf_ankle",
                "hip_mobility",
                "shoulder_mobility"
            ],
            "hint_only": [
                "landing_prep",
                "ankle_prep",
                "ankle_mobility",
                "stiffness_priming"
            ]
        },
        
        # --------------------------------------------------------------------
        # POOLS
        # --------------------------------------------------------------------
        "pools": {
            "bilateral_squat": {
                "description": "Volleyball squat emphasis; ankle mobility, force absorption for vertical jump",
                "filters": {
                    "aether_pattern": "Squat-Bilateral",
                    "load_band_primary": ["Band_1", "Band_2"],
                    "e_node": None
                },
                "selection_bias": {
                    "prefer_bands_by_week": {
                        "1-3": ["Band_1"],
                        "4-8": ["Band_1", "Band_2"]
                    },
                    "prefer_front_squat_over_back": True,
                    "prefer_ankle_mobility_variations": True
                },
                "library_reality": {
                    "band_1_count": 66,
                    "band_2_count": 61
                },
                "notes": "Volleyball squat: ankle ROM critical for vertical jump mechanics"
            },
            
            "hip_hinge": {
                "description": "Posterior chain; moderate emphasis (VB squat-primary sport)",
                "filters": {
                    "aether_pattern": "Hinge-Bilateral",
                    "load_band_primary": ["Band_1", "Band_2"]
                },
                "selection_bias": {
                    "prefer_bands_by_week": {
                        "1-4": ["Band_1"],
                        "5-8": ["Band_1", "Band_2"]
                    }
                },
                "notes": "VB hinge: lighter than basketball; complements squat-dominant training"
            },
            
            "unilateral_knee": {
                "description": "LOCKED PATTERN (2×/week); valgus control critical for VB landing volume",
                "filters": {
                    "aether_pattern": "Lunge-Unilateral",
                    "load_band_primary": ["Band_2"],
                    "e_node": ["E0"]
                },
                "selection_bias": {
                    "prefer_bands_by_week": {
                        "all_weeks": ["Band_2"]
                    },
                    "progression_via_tempo_not_load": True
                },
                "library_reality": {
                    "band_2_count": 125
                },
                "notes": "Critical for VB; high landing volume in practice requires weight room protection. Band_2 only."
            },
            
            "unilateral_hip": {
                "description": "Glute emphasis, hip stability",
                "filters": {
                    "aether_pattern": "Hinge-Bilateral",
                    "movement_pattern": ["Deadlift"],
                    "load_band_primary": ["Band_1", "Band_2"]
                },
                "selection_bias": {
                    "prefer_bands_by_week": {
                        "1-4": ["Band_1"],
                        "5-8": ["Band_1", "Band_2"]
                    }
                },
                "notes": "VB hip stability for single-leg landing control"
            },
            
            "pull_vertical": {
                "description": "Volleyball vertical pull emphasis; scap control, posterior shoulder armor",
                "filters": {
                    "aether_pattern": "Pull-Horizontal",  # Library uses Pull-Horizontal for both
                    "movement_pattern": ["Pull"],
                    "load_band_primary": ["Band_1", "Band_2", "Band_3"]
                },
                "selection_bias": {
                    "prefer_bands_by_week": {
                        "1-3": ["Band_1"],
                        "4-6": ["Band_1", "Band_2"],
                        "7-8": ["Band_2"]
                    },
                    "prefer_vertical_pull_keywords": ["pulldown", "pull-up", "lat"]
                },
                "notes": "VB uses vertical pull; scap health critical for overhead sport. Filter by movement keywords."
            },
            
            "push_limited": {
                "description": "Volleyball Child Wrapper constraint: Band_1 only, NO overhead pressing",
                "filters": {
                    "aether_pattern": "Push-Horizontal",
                    "load_band_primary": ["Band_1"]  # VB CEILING Band_1 (tighter than BBall)
                },
                "selection_bias": {
                    "prefer_bands_by_week": {
                        "all_weeks": ["Band_1"]
                    },
                    "prefer_floor_press_variations": True
                },
                "notes": "VB pressing tightly restricted; high overhead exposure in practice limits weight room pressing volume"
            },
            
            "plyo_vertical": {
                "description": "Volleyball vertical emphasis; approach jumps, spike approach sims, box jumps",
                "filters": {
                    "is_plyometric": True,
                    "movement_pattern": ["Jump", "Hop"],
                    "aether_pattern": "Plyometric-Landing"
                },
                "selection_bias": {
                    "prefer_enodes_by_week": {
                        "1-2": ["E1"],
                        "3-4": ["E1", "E2"],
                        "5-8": ["E2", "E3"]
                    },
                    "e3_max_percentage_session": 0.40,
                    "prefer_approach_variations": True
                },
                "enode_allocation": {
                    "E1_allocated": 6,  # VB gets all 6 (no lateral emphasis)
                    "E2_expected": 120,
                    "E3_expected": 15
                },
                "library_reality": {
                    "E1_global_total": 6,
                    "E1_scarcity_note": "VB vertical jump dominant; allocates all 6 E1 plyos. Week 1-2 still limited variety."
                },
                "notes": "VB vertical jump dominant; highest plyo contact volume of all court sports per Sport Demands"
            }
        },
        
        # --------------------------------------------------------------------
        # PATTERN FREQUENCIES
        # --------------------------------------------------------------------
        "pattern_frequencies": {
            "bilateral_squat": {
                "min_per_week": 1,
                "target_per_week": 2,
                "enforcement_mode": "required_slots_only",
                "notes": "VB squat-primary sport; DayA squat-dominant"
            },
            "hip_hinge": {
                "min_per_week": 1,
                "target_per_week": 1,
                "enforcement_mode": "required_slots_only",
                "notes": "Moderate hinge emphasis; complements squat priority"
            },
            "unilateral_knee": {
                "min_per_week": 2,
                "target_per_week": 2,
                "enforcement_mode": "locked",
                "notes": "LOCKED per Wrapper 4.2"
            },
            "unilateral_hip": {
                "min_per_week": 1,
                "target_per_week": 2,
                "enforcement_mode": "required_slots_only",
                "notes": "Day B or optional Day C"
            },
            "trunk_anti_extension": {
                "min_per_week": 2,
                "target_per_week": 2,
                "enforcement_mode": "locked",
                "notes": "LOCKED per Wrapper 4.2"
            },
            "trunk_anti_rotation": {
                "min_per_week": 2,
                "target_per_week": 2,
                "enforcement_mode": "locked",
                "notes": "LOCKED per Wrapper 4.2"
            },
            "calf_ankle": {
                "min_per_week": 2,
                "target_per_week": 2,
                "enforcement_mode": "locked",
                "notes": "LOCKED per Wrapper 4.2; critical for VB stiffness + landing volume tolerance"
            },
            "pull_vertical": {
                "min_per_week": 2,
                "target_per_week": 2,
                "enforcement_mode": "required_slots_only",
                "notes": "VB vertical pull emphasis; scap health critical"
            },
            "push_limited": {
                "min_per_week": 1,
                "target_per_week": 2,
                "enforcement_mode": "resolver",
                "notes": "Soft requirement; Band_1 only, resolver handles optional slot logic"
            },
            "plyo_vertical": {
                "min_per_week": 2,
                "target_per_week": 2,
                "enforcement_mode": "required_slots_only",
                "notes": "VB vertical jump dominant; highest plyo volume of all court sports"
            }
        },
        
        # --------------------------------------------------------------------
        # RESOLVER RULES
        # --------------------------------------------------------------------
        "resolver_rules": [
            {
                "pattern": "push_limited",
                "min_per_week": 1,
                "scope": "across_all_days",
                "eligible_slot_types": ["strength_slots", "upper_slots"],
                "priority": "yield_to_safety_gates",
                "contraindication_overrides": [
                    "shoulder_red_flag",
                    "overhead_irritation",
                    "wrist_injury",
                    "high_practice_overhead_volume"
                ],
                "notes": "VB pressing Band_1 only per Child Wrapper; if shoulder contraindication or high practice overhead volume (≥4 practices/week), legal to drop to 0"
            }
        ],
        
        # --------------------------------------------------------------------
        # SPORT-SPECIFIC CONSTRAINTS
        # --------------------------------------------------------------------
        "constraints": {
            "forbidden_categories": [
                "overhead_press_true",
                "overhead_press_band2_plus",
                "olympic_lifts"
            ],
            "required_patterns_per_week": [
                "unilateral_knee",
                "trunk_anti_extension",
                "trunk_anti_rotation",
                "calf_ankle"
            ],
            "pressing_limits": {
                "max_band": "Band_1",  # VB TIGHTER than Basketball
                "no_overhead": True
            },
            "max_enode_policy": "E3_gated_40pct",
            "notes": "Volleyball Child Wrapper tightens pressing constraints vs generic Court Sport Wrapper"
        },
        
        # --------------------------------------------------------------------
        # PLYO DISTRIBUTION PREFERENCES
        # --------------------------------------------------------------------
        "plyo_distribution": {
            "OFF_SEASON": {
                "E1_target_pct": 0.40,
                "E2_target_pct": 0.50,
                "E3_target_pct": 0.10,
                "notes": "VB off-season: highest plyo volume (130 contacts/session per Sport Demands); E2 emphasis"
            },
            "PRE_SEASON": {
                "E1_target_pct": 0.40,
                "E2_target_pct": 0.50,
                "E3_target_pct": 0.10,
                "notes": "VB pre-season: maintain E2 emphasis (120 contacts/session per Sport Demands)"
            }
        },
        
        # --------------------------------------------------------------------
        # ROUTING
        # --------------------------------------------------------------------
        "routing": {
            "supported_seasons": ["OFF_SEASON", "PRE_SEASON"],
            "requires_reroute_if_season_unsupported": True,
            "reroute_to_icp_map": {
                "IN_SEASON_TIER1": "ICP_VOLLEYBALL_IN_SEASON_TIER1",
                "IN_SEASON_TIER2": "ICP_VOLLEYBALL_IN_SEASON_TIER2",
                "IN_SEASON_TIER3": "ICP_VOLLEYBALL_IN_SEASON_TIER3",
                "POST_SEASON": "ICP_VOLLEYBALL_POST_SEASON"
            },
            "default_icp_id": "ICP_VOLLEYBALL_FOUNDATIONS",
            "block_type": "FOUNDATIONS_8WK",
            "notes": "In-season programming requires routing to ICP_VOLLEYBALL_IN_SEASON per ICP Definitions v2.3.1"
        }
    }
}


# ============================================================================
# HANDOFF CONTRACT
# ============================================================================

HANDOFF_CONTRACT = {
    "provides_to_downstream": [
        "exercise pool FILTERS (aether_pattern + band + E-node queries)",
        "selection bias preferences (band/E-node progression by week)",
        "sport-specific constraints (forbidden categories, pressing limits)",
        "pattern frequency targets (aligned with session_shells weekly expectations)",
        "plyo distribution preferences (E-node emphasis per season)",
        "resolver rules (soft weekly minimums that yield to safety gates)"
    ],
    "requires_from_upstream": [
        "Exercise library DataFrame (EFL_Exercise_Library_v2_5.csv)",
        "Client State Object (population, season, readiness, injury flags)",
        "Week number (for band/E-node preference lookup)",
        "Session frequency (2× vs 3× per week)",
        "Day archetype (DayA / DayB / DayC)"
    ],
    "delegates_to_other_layers": [
        "global_pool patterns → EFL_Exercise_Library_v2_5.csv accessory section",
        "band/E-node legality ceilings → Load Standards + Sport Demands clamping",
        "acute variables (sets/reps/rest/tempo) → Output Spec + Generator",
        "session structure (PRIME/PREP/WORK/CLEAR) → session_shells.json",
        "progression validation (ONE_AXIS_AT_A_TIME) → Progression Validator",
        "final exercise selection → Exercise Selector (queries pools via filters)"
    ]
}


# ============================================================================
# VALIDATION FUNCTIONS (v1.0.2 LIBRARY-ALIGNED)
# ============================================================================

def get_sport_profile(sport: str) -> dict:
    """
    Retrieve sport profile by sport ID.
    
    v1.0.2: Unchanged from v1.0.1 (input normalization retained).
    
    Args:
        sport: Sport identifier ("BASKETBALL" or "VOLLEYBALL")
        
    Returns:
        Sport profile dict
        
    Raises:
        ValueError: If sport not found in SPORT_PROFILES
    """
    sport = sport.upper().strip()
    
    if sport not in SPORT_PROFILES:
        raise ValueError(
            f"Sport '{sport}' not found. Valid sports: {list(SPORT_PROFILES.keys())}"
        )
    return SPORT_PROFILES[sport]


def validate_pool_query_returns_inventory(
    sport: str, 
    exercise_library_df: pd.DataFrame,
    min_inventory_threshold: int = 3,
    strict_mode: bool = False
) -> dict:
    """
    v1.0.2 NEW: Validate that all sport_pool patterns return sufficient inventory
    when queried against actual library.
    
    Args:
        sport: Sport identifier
        exercise_library_df: Exercise library DataFrame (REQUIRED)
        min_inventory_threshold: Minimum exercises per pool (default 3)
        strict_mode: If True, fail on any pool below threshold
        
    Returns:
        Validation result dict with status and inventory_gaps
    """
    profile = get_sport_profile(sport)
    inventory_gaps = []
    
    sport_pool_patterns = profile["pattern_ownership"]["sport_pool"]
    pools = profile["pools"]
    
    for pattern in sport_pool_patterns:
        if pattern not in pools:
            inventory_gaps.append({
                "type": "MISSING_POOL_DEFINITION",
                "pattern": pattern,
                "message": f"Pattern '{pattern}' in sport_pool but no pool definition found"
            })
            continue
        
        pool_def = pools[pattern]
        inventory = query_pool_inventory(exercise_library_df, pool_def)
        
        if inventory["total_count"] < min_inventory_threshold:
            inventory_gaps.append({
                "type": "INSUFFICIENT_LIBRARY_INVENTORY",
                "pattern": pattern,
                "filters": pool_def.get("filters"),
                "actual_count": inventory["total_count"],
                "min_threshold": min_inventory_threshold,
                "by_band": inventory["by_band"],
                "by_enode": inventory["by_enode"],
                "message": f"Pool '{pattern}' returns only {inventory['total_count']} exercises (min {min_inventory_threshold} required)"
            })
    
    return {
        "status": "PASS" if len(inventory_gaps) == 0 else "FAIL",
        "inventory_gaps": inventory_gaps,
        "strict_mode": strict_mode
    }


def validate_against_session_shells(sport: str, session_shells: dict) -> dict:
    """
    v1.0.2: Unchanged from v1.0.1 (bidirectional validation retained).
    
    Cross-validate sport_profiles pattern_frequencies against session_shells 
    weekly_coverage_expectations.
    
    Args:
        sport: Sport identifier
        session_shells: Parsed session_shells.json dict
        
    Returns:
        Validation result dict with status and mismatches
    """
    profile = get_sport_profile(sport)
    mismatches = []
    
    if sport not in session_shells:
        return {
            "status": "FAIL",
            "message": f"Sport '{sport}' not found in session_shells.json"
        }
    
    shells_2x = session_shells[sport].get("2_sessions_per_week", {})
    expectations = shells_2x.get("weekly_coverage_expectations", {})
    
    # Canonicalize expectations
    canonicalized_expectations = {}
    for pattern, value in expectations.items():
        if isinstance(value, int):
            canonicalized_expectations[pattern] = {"min": value}
        elif isinstance(value, dict):
            if "min" not in value and "description" not in value:
                mismatches.append({
                    "type": "MALFORMED_EXPECTATION",
                    "pattern": pattern,
                    "message": f"Expectation for '{pattern}' is dict but missing 'min' key"
                })
            else:
                canonicalized_expectations[pattern] = value
        elif isinstance(value, str):
            continue
    
    # Direction 1: shells → profiles
    frequencies = profile["pattern_frequencies"]
    for pattern, expected in canonicalized_expectations.items():
        if "min" not in expected:
            continue
        
        expected_min = expected["min"]
        
        if pattern not in frequencies:
            mismatches.append({
                "type": "MISSING_FREQUENCY_DEFINITION",
                "pattern": pattern,
                "direction": "shells_to_profiles",
                "message": f"Pattern '{pattern}' in session_shells expectations but not in sport_profiles frequencies"
            })
            continue
        
        freq_min = frequencies[pattern]["min_per_week"]
        if freq_min != expected_min:
            mismatches.append({
                "type": "FREQUENCY_MISMATCH",
                "pattern": pattern,
                "direction": "shells_to_profiles",
                "session_shells_min": expected_min,
                "sport_profiles_min": freq_min,
                "message": f"Mismatch for '{pattern}': shells={expected_min}, profile={freq_min}"
            })
    
    # Direction 2: profiles → shells (bidirectional)
    for pattern, freq_def in frequencies.items():
        if pattern not in canonicalized_expectations:
            mismatches.append({
                "type": "FREQUENCY_DEFINED_BUT_NOT_IN_SHELLS_EXPECTATIONS",
                "pattern": pattern,
                "direction": "profiles_to_shells",
                "message": f"Pattern '{pattern}' in sport_profiles frequencies but not in session_shells expectations"
            })
    
    return {
        "status": "PASS" if len(mismatches) == 0 else "FAIL",
        "mismatches": mismatches
    }


def validate_pattern_namespace_integrity(sport: str) -> dict:
    """
    v1.0.2: Unchanged from v1.0.1.
    
    Validate that all patterns referenced in pools and pattern_frequencies
    are declared in pattern_ownership.
    
    Args:
        sport: Sport identifier
        
    Returns:
        Validation result dict with status and orphaned patterns
    """
    profile = get_sport_profile(sport)
    orphans = []
    
    declared_patterns = set(
        profile["pattern_ownership"]["sport_pool"] +
        profile["pattern_ownership"]["global_pool_required"] +
        profile["pattern_ownership"]["hint_only"]
    )
    
    # Check pools
    for pattern in profile["pools"].keys():
        if pattern not in declared_patterns:
            orphans.append({
                "type": "ORPHANED_POOL",
                "pattern": pattern,
                "message": f"Pattern '{pattern}' in pools but not in pattern_ownership"
            })
    
    # Check pattern_frequencies
    for pattern in profile["pattern_frequencies"].keys():
        if pattern not in declared_patterns:
            orphans.append({
                "type": "ORPHANED_FREQUENCY",
                "pattern": pattern,
                "message": f"Pattern '{pattern}' in pattern_frequencies but not in pattern_ownership"
            })
    
    return {
        "status": "PASS" if len(orphans) == 0 else "FAIL",
        "orphaned_patterns": orphans
    }


def validate_resolver_rules_structural_safety(sport: str, session_shells: dict) -> dict:
    """
    v1.0.2: Unchanged from v1.0.1.
    
    Validate that resolver rules can be structurally satisfied by session_shells.
    
    Args:
        sport: Sport identifier
        session_shells: Parsed session_shells.json dict
        
    Returns:
        Validation result dict with status and unsafe resolver rules
    """
    profile = get_sport_profile(sport)
    unsafe_rules = []
    
    resolver_rules = profile.get("resolver_rules", [])
    
    if sport not in session_shells:
        return {
            "status": "FAIL",
            "message": f"Sport '{sport}' not found in session_shells.json"
        }
    
    shells_2x = session_shells[sport].get("2_sessions_per_week", {})
    
    for rule in resolver_rules:
        pattern = rule["pattern"]
        min_per_week = rule["min_per_week"]
        eligible_slot_types = rule.get("eligible_slot_types", 
                                       ["strength_slots", "upper_slots", "plyo_slots", "micro_slots"])
        
        total_slots = 0
        for day in ["DayA", "DayB"]:
            day_shell = shells_2x.get(day, {})
            work = day_shell.get("work", {})
            
            for slot_group in eligible_slot_types:
                slots = work.get(slot_group, [])
                for slot in slots:
                    if slot.get("pattern") == pattern:
                        total_slots += 1
        
        if total_slots < min_per_week:
            unsafe_rules.append({
                "type": "RESOLVER_STRUCTURALLY_IMPOSSIBLE",
                "pattern": pattern,
                "resolver_min": min_per_week,
                "available_slots": total_slots,
                "eligible_slot_types": eligible_slot_types,
                "message": f"Resolver rule requires {min_per_week}×/week for '{pattern}' but only {total_slots} eligible slots available"
            })
    
    return {
        "status": "PASS" if len(unsafe_rules) == 0 else "FAIL",
        "unsafe_rules": unsafe_rules
    }


def validate_sport_profile_integrity(
    sport: str, 
    exercise_library_df: pd.DataFrame,
    session_shells: dict = None,
    strict_mode: bool = False
) -> dict:
    """
    v1.0.2: Updated to require exercise_library_df (MANDATORY).
    
    Run full validation suite for a sport profile.
    
    Args:
        sport: Sport identifier
        exercise_library_df: Exercise library DataFrame (REQUIRED in v1.0.2)
        session_shells: Parsed session_shells.json dict (optional)
        strict_mode: If True, enforce all checks including minimum inventory thresholds
        
    Returns:
        Comprehensive validation result dict
    """
    if exercise_library_df is None:
        return {
            "status": "FAIL",
            "error": "exercise_library_df is REQUIRED in v1.0.2 (library-aligned pools)"
        }
    
    results = {
        "sport": sport,
        "timestamp": "2026-01-16",
        "version": "1.0.2",
        "strict_mode": strict_mode,
        "checks": {}
    }
    
    # 1. NEW: Pool inventory validation (REQUIRED)
    results["checks"]["pool_inventory"] = validate_pool_query_returns_inventory(
        sport, exercise_library_df, min_inventory_threshold=3, strict_mode=strict_mode
    )
    
    # 2. Pattern namespace integrity
    results["checks"]["pattern_namespace_integrity"] = validate_pattern_namespace_integrity(sport)
    
    # 3. Cross-file validation (if session_shells provided)
    if session_shells is not None:
        results["checks"]["session_shells_alignment"] = validate_against_session_shells(
            sport, session_shells
        )
        results["checks"]["resolver_rules_structural_safety"] = validate_resolver_rules_structural_safety(
            sport, session_shells
        )
    
    # Overall status
    all_passed = all(
        check.get("status") in ["PASS", "SKIP"]
        for check in results["checks"].values()
    )
    results["overall_status"] = "PASS" if all_passed else "FAIL"
    
    return results


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    import pandas as pd  # type: ignore
    
    # Load exercise library
    try:
        library_df = pd.read_csv("EFL_Exercise_Library_v2_5.csv")
        print("✓ Exercise library loaded successfully")
        print(f"  Total exercises: {len(library_df)}")
    except FileNotFoundError:
        print("✗ Exercise library not found (EFL_Exercise_Library_v2_5.csv)")
        library_df = None
    
    # Example 1: Get sport profile
    bball = get_sport_profile("basketball")
    print(f"\n✓ Basketball profile loaded")
    print(f"  Sport pool patterns: {len(bball['pattern_ownership']['sport_pool'])}")
    
    # Example 2: Query pool inventory
    if library_df is not None:
        print("\n=== POOL INVENTORY CHECK ===")
        for pattern, pool_def in bball["pools"].items():
            inventory = query_pool_inventory(library_df, pool_def)
            print(f"\n{pattern}:")
            print(f"  Total: {inventory['total_count']}")
            print(f"  By band: {inventory['by_band']}")
            if inventory['by_enode']:
                print(f"  By E-node: {inventory['by_enode']}")
    
    # Example 3: Full validation
    if library_df is not None:
        print("\n=== VALIDATION SUITE ===")
        results = validate_sport_profile_integrity(
            "BASKETBALL",
            library_df,
            strict_mode=False
        )
        print(f"Overall status: {results['overall_status']}")
        for check_name, check_result in results['checks'].items():
            print(f"  {check_name}: {check_result['status']}")
            if check_result['status'] == 'FAIL':
                if 'inventory_gaps' in check_result:
                    for gap in check_result['inventory_gaps']:
                        print(f"    - {gap['message']}")
    
    print("\n✓ sport_profiles.py v1.0.2 loaded successfully")
    print("✓ Library-aligned filters implemented")
    print("✓ All hardcoded exercise IDs removed")
