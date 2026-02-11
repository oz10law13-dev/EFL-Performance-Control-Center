"""
UID Registry: centralized user/role/athlete assignment data.

Authority: EFL_UID_ROLE_REGISTRY_SCHEMA_v1.0.1_PATCHED.json
"""

import uuid
from .timeutil import utc_now_z


# Extracted from test file (validated working registry)
UID_REGISTRY = {
    "schema_version": "1.0.1",
    "registry_metadata": {
        "lastupdated": utc_now_z(),
        "admin_contact": "admin@elitefitness.lab"
    },
    "roles": {
        "Coach": {
            "role_id": "ROLE_COACH",
            "role_name": "Coach",
            "tier": 1,
            "description": "Individual coach with own athlete access",
            "capabilities": [
                "REQUEST_SESSION_GENERATION",
                "SUBMIT_MANUAL_PROGRAM",
                "QUERY_ARTIFACT_HISTORY"
            ],
            "constraints": {
                "athlete_scope": "OWN_ONLY",
                "requires_mfa": False
            }
        },
        "SeniorCoach": {
            "role_id": "ROLE_SENIOR_COACH",
            "role_name": "SeniorCoach",
            "tier": 2,
            "description": "Facility-wide coach with approval authority",
            "capabilities": [
                "REQUEST_SESSION_GENERATION",
                "REQUEST_MESOCYCLE_GENERATION",
                "SUBMIT_MANUAL_PROGRAM",
                "REQUEST_OVERRIDE_STAGE",
                "APPROVE_OVERRIDE",
                "REQUEST_OVERRIDE_CAP",
                "QUERY_ARTIFACT_HISTORY",
                "QUERY_VIOLATIONS"
            ],
            "constraints": {
                "athlete_scope": "FACILITY_ALL",
                "requires_mfa": True
            }
        },
        "MedicalProvider": {
            "role_id": "ROLE_MEDICAL_PROVIDER",
            "role_name": "MedicalProvider",
            "tier": 3,
            "description": "Clinical authority for override approvals",
            "capabilities": [
                "SUBMIT_MANUAL_PROGRAM",
                "REQUEST_OVERRIDE_STAGE",
                "APPROVE_OVERRIDE",
                "QUERY_ARTIFACT_HISTORY",
                "QUERY_VIOLATIONS"
            ],
            "constraints": {
                "athlete_scope": "FACILITY_ALL",
                "requires_mfa": True
            }
        },
        "Admin": {
            "role_id": "ROLE_ADMIN",
            "role_name": "Admin",
            "tier": 5,
            "description": "System administrator",
            "capabilities": [
                "REQUEST_SESSION_GENERATION",
                "REQUEST_MESOCYCLE_GENERATION",
                "SUBMIT_MANUAL_PROGRAM",
                "REQUEST_OVERRIDE_STAGE",
                "APPROVE_OVERRIDE",
                "REQUEST_OVERRIDE_CAP",
                "DEPLOY_GENERATOR_VERSION",
                "UPDATE_PROJECT_SPEC",
                "UPDATE_ARTIFACT_SCHEMA",
                "QUERY_ARTIFACT_HISTORY",
                "QUERY_VIOLATIONS",
                "GENERATE_COMPLIANCE_REPORT"
            ],
            "constraints": {
                "athlete_scope": "SYSTEM_ALL",
                "requires_mfa": True,
                "max_concurrent_sessions": 10
            }
        },
        "QA": {
            "role_id": "ROLE_QA",
            "role_name": "QA",
            "tier": 4,
            "description": "QA and audit role",
            "capabilities": [
                "QUERY_ARTIFACT_HISTORY",
                "QUERY_VIOLATIONS"
            ],
            "constraints": {
                "athlete_scope": "SYSTEM_ALL",
                "requires_mfa": True
            }
        },
        "System": {
            "role_id": "ROLE_SYSTEM",
            "role_name": "System",
            "tier": 0,
            "description": "Automated system processes",
            "capabilities": [
                "REQUEST_SESSION_GENERATION",
                "REQUEST_MESOCYCLE_GENERATION"
            ],
            "constraints": {
                "athlete_scope": "SYSTEM_ALL"
            }
        }
    },
    "users": [
        {
            "uid": str(uuid.uuid4()),
            "username": "coach_alice",
            "email": "alice@example.com",
            "role": "Coach",
            "status": "ACTIVE",
            "registered_at": utc_now_z(),
            "assigned_athletes": ["CLIENT_001", "CLIENT_002"],
            "mfa_enabled": False
        },
        {
            "uid": str(uuid.uuid4()),
            "username": "senior_coach_bob",
            "email": "bob@example.com",
            "role": "SeniorCoach",
            "status": "ACTIVE",
            "registered_at": utc_now_z(),
            "assigned_athletes": [],
            "mfa_enabled": True
        },
        {
            "uid": str(uuid.uuid4()),
            "username": "provider_carol",
            "email": "carol@example.com",
            "role": "MedicalProvider",
            "status": "ACTIVE",
            "registered_at": utc_now_z(),
            "assigned_athletes": [],
            "mfa_enabled": True
        },
        {
            "uid": str(uuid.uuid4()),
            "username": "admin_dave",
            "email": "dave@example.com",
            "role": "Admin",
            "status": "ACTIVE",
            "registered_at": utc_now_z(),
            "assigned_athletes": [],
            "mfa_enabled": True
        }
    ]
}
