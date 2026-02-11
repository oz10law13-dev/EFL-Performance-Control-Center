"""
Production generator adapter for EFL governance layer.
Routes to appropriate generator based on project_id.

This is the PRODUCTION entrypoint. Tests should import generator_fake directly.
"""

import uuid
from .timeutil import utc_now_z


def generate_session(client_id: str, project_id: str, session_date: str, context: dict = None) -> dict:
    """
    Production session generator adapter.
    
    Routes to appropriate project-specific generator based on project_id.
    Returns schema-compliant SESSION artifact.
    
    Args:
        client_id: Unique athlete/client identifier
        project_id: Project enum value from schema ('R2P_ACL', 'COURT_SPORT_FOUNDATIONS', etc.)
        session_date: ISO date when session is scheduled (YYYY-MM-DD)
        context: Optional dict with client_state, readiness, provider_notes, etc.
    
    Returns:
        dict: Schema-compliant SESSION artifact
    
    Raises:
        ValueError: If project_id is not supported
        RuntimeError: If generator fails
    """
    context = context or {}
    
    # Project routing
    if project_id in ("R2P-ACL", "R2P_ACL"):
        return _generate_r2p_acl_session(client_id, session_date, context)
    elif project_id in ("Court", "COURT_SPORT_FOUNDATIONS"):
        return _generate_court_sport_session(client_id, session_date, context)
    else:
        raise ValueError(
            f"Unsupported project_id: '{project_id}'. "
            f"Valid: R2P-ACL, R2P_ACL, Court, COURT_SPORT_FOUNDATIONS"
        )


def _generate_r2p_acl_session(client_id: str, session_date: str, context: dict) -> dict:
    """
    Generate R2P-ACL session artifact.
    
    TODO: Wire to real R2P-ACL stage-based generator.
    Currently returns minimal stub for testing adapter flow.
    """
    now = utc_now_z()
    
    # STUB: Replace with real R2P-ACL generator
    # Expected inputs from context:
    #   - client_state (stage, weeks_post_surgery, readiness, etc.)
    #   - provider_clearances
    #   - hardstop_flags
    
    return {
        "header": {
            "client_id": client_id,
            "artifact_id": str(uuid.uuid4()),
            "artifact_class": "SESSION",
            "target": "COACH_SHEET",
            "generated_at": now,
            "project_id": "R2P_ACL",
            "router_version": "ADAPTER_v0.0.1",
            "state_last_updated": now,
            "season_type": "OFF_SEASON",
            "eligible_for_training_today": True,
            "reason_codes": ["ADAPTER_STUB"]
        },
        "legality_snapshot": {
            "active_project": "R2P_ACL",
            "eligible": True,
            "reason_codes": ["ADAPTER_STUB"]
        },
        "cap_proof": {
            "caps_exist": True,
            "population_enforced": "Youth_13_16",
            "readiness_flag": "GREEN",
            "weekly_multiplier": 1.0,
            "session_multiplier": 1.0,
            "weekly_contacts_cap_base": 150,
            "weekly_contacts_cap_applied": 150,
            "session_contacts_cap_base": 60,
            "session_contacts_cap_applied": 60,
            "enode_accent_cap_pct": 0.40,
            "max_band_allowed_population": "Band3",
            "max_enode_allowed_population": "E3"
        },
        "exposure_summary": {
            "total_contacts": 0,  # STUB
            "total_sets": 0
        },
        "content_payload": {
            "session": {
                "session_id": str(uuid.uuid4()),
                "name": f"R2P-ACL Session - {client_id}",
                "session_date": session_date,
                "blocks": [],  # STUB: Real generator populates WORK blocks
                "total_sets": 0
            }
        },
        "metadata": {
            "generator_version": "ADAPTER_R2P_v0.0.1",
            "wrapper_version": "v1.1",
            "outputspec_version": "v1.0",
            "global_contract_version": "1.0.1",
            "validation_timestamp": now
        }
    }


def _generate_court_sport_session(client_id: str, session_date: str, context: dict) -> dict:
    """
    Generate Court Sport Foundations session artifact.
    Routes to real Court Sport generator.
    """
    from .generator_court import generate_court_sport_session
    return generate_court_sport_session(client_id, session_date, context)

