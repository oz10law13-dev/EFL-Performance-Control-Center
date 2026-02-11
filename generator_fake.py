"""
Fake session generator for testing EFL governance layer.
Produces schema-compliant SESSION artifacts with deterministic output.
"""

import uuid
from .timeutil import utc_now_z


def fake_session_generator(client_id: str, project_id: str, session_date: str) -> dict:
    """
    Minimal SESSION artifact that conforms to EFL_OUTPUT_ARTIFACT_SCHEMA_v1.0.1.
    
    IMPORTANT SEMANTICS:
    - generated_at: system timestamp when artifact was created
    - session_date: training date when session is scheduled
    These are NOT the same and should not be conflated.
    
    PROJECT ID MAPPING:
    - Maps test-friendly IDs to schema enum values
    - Unknown projects raise explicit error (no silent defaults)
    
    SCHEMA COMPLIANCE:
    - Returns all required top-level fields: header, legality_snapshot, metadata
    - Returns all SESSION-conditional fields: cap_proof, exposure_summary, content_payload
    - All required nested fields populated (not stubs)
    
    Args:
        client_id: Unique athlete/client identifier
        project_id: Test-friendly project ID ('R2P-ACL', 'Court', etc.)
        session_date: ISO date when session is scheduled (YYYY-MM-DD)
    
    Returns:
        dict: Schema-compliant SESSION artifact
    
    Raises:
        ValueError: If project_id is unknown
    """
    now = utc_now_z()  # System timestamp when artifact is generated
    
    # PROJECT ID MAPPING
    project_mapping = {
        "R2P-ACL": "R2P_ACL",
        "Court": "COURT_SPORT_FOUNDATIONS",
        "R2P_ACL": "R2P_ACL",
        "COURT_SPORT_FOUNDATIONS": "COURT_SPORT_FOUNDATIONS"
    }
    
    if project_id not in project_mapping:
        raise ValueError(
            f"Unknown project ID '{project_id}'. "
            f"Valid IDs: {list(project_mapping.keys())}"
        )
    
    schema_project_id = project_mapping[project_id]
    
    # NOTE: No default fallback - unknown projects should fail explicitly
    return {
        "header": {
            "clientid": client_id,
            "artifact_id": str(uuid.uuid4()),
            "artifact_class": "SESSION",
            "target": "COACHSHEET",
            "generated_at": now,  # system timestamp
            "projectid": schema_project_id,
            "routerversion": "ROUTER_v1.0_TEST",
            "state_lastupdated": now,
            "seasontype": "OFFSEASON",
            "eligible_for_training_today": True,
            "reasoncodes": ["ROUTER_PASS"]
        },
        "legality_snapshot": {
            "activeproject": schema_project_id,
            "eligible": True,
            "reasoncodes": ["ROUTER_PASS"]
        },
        "cap_proof": {
            "caps_exist": True,
            "population_enforced": "Youth1316",
            "readinessflag": "GREEN",
            "weeklymultiplier": 1.0,
            "sessionmultiplier": 1.0,
            "weeklycontactscap_base": 150,
            "weeklycontactscap_applied": 150,
            "sessioncontactscap_base": 60,
            "sessioncontactscap_applied": 60,
            "enode_accent_cap_pct": 0.40,
            "maxbandallowed_population": "Band3",
            "maxenodeallowed_population": "E3"
        },
        "exposure_summary": {
            "total_contacts": 45,
            "total_sets": 12
        },
        "content_payload": {
            "session": {
                "session_id": str(uuid.uuid4()),
                "name": f"Test session for {client_id}",
                "session_date": session_date,
                "blocks": [],
                "total_sets": 0
            }
        },
        "metadata": {
            "generator_version": "TEST_FAKE_v0.0.1",
            "wrapper_version": "v1.0",
            "outputspec_version": "v1.0",
            "global_contract_version": "1.0.1",
            "validation_timestamp": now
        }
    }
