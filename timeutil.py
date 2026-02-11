"""
UTC timestamp utility for EFL governance layer.
Provides timezone-aware timestamp generation.
"""

from datetime import datetime, timezone


def utc_now_z() -> str:
    """
    Return current UTC timestamp in ISO8601 format with 'Z' suffix.
    
    Returns:
        str: ISO8601 timestamp like '2026-01-15T23:52:00Z'
    """
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
