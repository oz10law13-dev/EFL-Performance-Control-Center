"""
Request processing logic for EFL governance intents.
Implements GATE → STRATA → SIGIL → THESIS → VERITAS flow.
"""

import uuid
import os
from .authz import can_user_call_intent, INTENT_AUTHORIZATION_MATRIX
from .registry import UID_REGISTRY

# GENERATOR SELECTION: Use fake for tests, adapter for production
_USE_FAKE_GENERATOR = os.getenv("EFL_USE_FAKE_GENERATOR", "false").lower() == "true"

if _USE_FAKE_GENERATOR:
    from .generator_fake import fake_session_generator as _generator
    def _call_generator(client_id, project_id, session_date):
        return _generator(client_id, project_id, session_date)
else:
    from .generator_adapter import generate_session as _generator
    def _call_generator(client_id, project_id, session_date):
        return _generator(client_id, project_id, session_date, context={})


def process_request_session_generation(requestor_uid: str, payload: dict) -> dict:
    """
    Simulate GATE → STRATA → SIGIL → THESIS → VERITAS flow for one intent.
    
    Args:
        requestor_uid: UID of user making request
        payload: Request payload with client_id, project_id, session_date
    
    Returns:
        dict: Response with status, intent_id, and artifact (if approved)
    """
    intent_type = "REQUEST_SESSION_GENERATION"
    intent_id = str(uuid.uuid4())
    
    # Find user in registry
    user = None
    for u in UID_REGISTRY["users"]:
        if u["uid"] == requestor_uid:
            user = u
            break
    
    if not user:
        return {
            "status": "DENIED",
            "error_code": "USER_NOT_FOUND",
            "intent_id": intent_id
        }
    
    user_role = user["role"]
    
    # GATE: Role-based authorization
    if not can_user_call_intent(user_role, intent_type):
        return {
            "status": "DENIED",
            "error_code": "INTENT_ROLE_DENIED",
            "intent_id": intent_id,
            "user_role": user_role,
            "required_roles": list(INTENT_AUTHORIZATION_MATRIX[intent_type])
        }
    
    # STRATA: Input validation
    required_fields = ["client_id", "project_id", "session_date"]
    if any(field not in payload for field in required_fields):
        return {
            "status": "DENIED",
            "error_code": "INTENT_INPUT_INVALID",
            "intent_id": intent_id,
            "missing_fields": [f for f in required_fields if f not in payload]
        }
    
    client_id = payload["client_id"]
    
    # SIGIL: Eligibility check (athlete access control)
    if client_id not in user.get("assigned_athletes", []) and user_role == "Coach":
        return {
            "status": "DENIED",
            "error_code": "CLIENT_ACCESS_DENIED",
            "intent_id": intent_id
        }
    
    # THESIS: Generate artifact
    try:
        artifact = _call_generator(
            payload["client_id"],
            payload["project_id"],
            payload["session_date"]
        )
    except ValueError as e:
        return {
            "status": "FAILED",
            "error_code": "INVALID_PROJECT_ID",
            "intent_id": intent_id,
            "error": str(e)
        }
    except Exception as e:
        return {
            "status": "FAILED",
            "error_code": "GENERATOR_FAILURE",
            "intent_id": intent_id,
            "error": str(e)
        }
    
    # VERITAS: Return success with artifact
    return {
        "status": "APPROVED",
        "intent_id": intent_id,
        "artifact": artifact
    }
