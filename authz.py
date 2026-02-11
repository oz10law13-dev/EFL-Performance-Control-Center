"""
Authorization matrix and intent permission logic for EFL governance.
"""

# Intent → Allowed Roles mapping (default-deny policy)
INTENT_AUTHORIZATION_MATRIX = {
    "REQUEST_SESSION_GENERATION": {"Coach", "SeniorCoach", "Admin", "System"},
    "REQUEST_MESOCYCLE_GENERATION": {"SeniorCoach", "Admin"},
    "SUBMIT_MANUAL_PROGRAM": {"Coach", "SeniorCoach", "MedicalProvider", "Admin"},
    "REQUEST_OVERRIDE_STAGE": {"SeniorCoach", "MedicalProvider", "Admin"},
    "APPROVE_OVERRIDE": {"SeniorCoach", "MedicalProvider", "Admin"},
    "REQUEST_OVERRIDE_CAP": {"SeniorCoach", "Admin"},
    "DEPLOY_GENERATOR_VERSION": {"Admin"},
    "UPDATE_PROJECT_SPEC": {"Admin"},
    "UPDATE_ARTIFACT_SCHEMA": {"Admin"},
    "QUERY_ARTIFACT_HISTORY": {"Coach", "SeniorCoach", "MedicalProvider", "Admin", "QA"},
    "QUERY_VIOLATIONS": {"Admin", "QA"},
    "GENERATE_COMPLIANCE_REPORT": {"Admin"}
}


def can_user_call_intent(user_role: str, intent: str) -> bool:
    """
    Check if user role is authorized for intent.
    
    Args:
        user_role: Role name (e.g., 'Coach', 'Admin')
        intent: Intent name (e.g., 'REQUEST_SESSION_GENERATION')
    
    Returns:
        bool: True if authorized, False otherwise
    """
    return user_role in INTENT_AUTHORIZATION_MATRIX.get(intent, set())
