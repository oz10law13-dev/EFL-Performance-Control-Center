"""
EPA v2.2 - COACH-FRIENDLY MESSAGE WRAPPER
==========================================

Translates technical EPA responses into human-readable messages with:
- Plain English explanations
- Visual indicators (✅ ❌ ⚠️)
- Actionable fix suggestions
- Collapsible technical details
"""

import json
from typing import Dict, List


class CoachMessageBuilder:
    """Builds coach-friendly messages from EPA responses"""
    
    # Emoji mappings
    EMOJI = {
        "SUCCESS": "✅",
        "REJECTED_ILLEGAL": "❌",
        "REJECTED_MISSING_FIELDS": "⚠️",
        "QUARANTINED_REVIEW": "🔍",
        "PASS": "✅",
        "FAIL": "❌",
        "SKIP": "⊘"
    }
    
    def __init__(self, epa_response: Dict):
        """Initialize with raw EPA JSON response"""
        self.response = epa_response
        self.status = epa_response.get('status', 'UNKNOWN')
        self.reasons = epa_response.get('reasons', [])
        self.session_plan = epa_response.get('session_plan')
        self.validation_report = epa_response.get('validation_report', [])
        self.weekly_agg = epa_response.get('weekly_aggregation', {})
        self.computed_limits = epa_response.get('computed_limits', {})
    
    def build_message(self, include_technical: bool = True) -> str:
        """Build complete coach-friendly message"""
        lines = []
        
        # Header
        lines.append("=" * 80)
        lines.append(self._build_header())
        lines.append("=" * 80)
        
        # Main message
        if self.status == "SUCCESS":
            lines.append(self._build_success_message())
        elif self.status == "REJECTED_ILLEGAL":
            lines.append(self._build_rejection_message())
        elif self.status == "REJECTED_MISSING_FIELDS":
            lines.append(self._build_missing_fields_message())
        elif self.status == "QUARANTINED_REVIEW":
            lines.append(self._build_quarantine_message())
        
        # Session summary (if success)
        if self.status == "SUCCESS" and self.session_plan:
            lines.append(self._build_session_summary())
        
        # Weekly load tracking
        if self.weekly_agg:
            lines.append(self._build_weekly_tracking())
        
        # Technical details (collapsible)
        if include_technical:
            lines.append(self._build_technical_details())
        
        lines.append("=" * 80)
        
        return "\n".join(lines)
    
    def _build_header(self) -> str:
        """Build message header with status"""
        emoji = self.EMOJI.get(self.status, "⚠️")
        
        headers = {
            "SUCCESS": f"{emoji} SESSION APPROVED",
            "REJECTED_ILLEGAL": f"{emoji} SESSION REJECTED",
            "REJECTED_MISSING_FIELDS": f"{emoji} INCOMPLETE REQUEST",
            "QUARANTINED_REVIEW": f"{emoji} REVIEW REQUIRED"
        }
        
        return headers.get(self.status, f"{emoji} {self.status}")
    
    def _build_success_message(self) -> str:
        """Build success message"""
        msg = ["\n✅ This session meets all safety and compliance requirements."]
        msg.append("   You can proceed with programming this session.\n")
        return "\n".join(msg)
    
    def _build_rejection_message(self) -> str:
        """Build rejection message with fixes"""
        msg = ["\n❌ This session cannot be programmed as designed.\n"]
        
        # Categorize reasons
        plyo_violations = []
        sprint_violations = []
        readiness_violations = []
        population_violations = []
        other_violations = []
        
        for reason in self.reasons:
            if "PLYO" in reason or "CONTACT" in reason:
                plyo_violations.append(reason)
            elif "SPRINT" in reason or "METERS" in reason:
                sprint_violations.append(reason)
            elif "READINESS" in reason:
                readiness_violations.append(reason)
            elif "BAND" in reason or "NODE" in reason or "E_NODE" in reason:
                population_violations.append(reason)
            else:
                other_violations.append(reason)
        
        # Build problem section
        msg.append("📋 PROBLEM:\n")
        
        if plyo_violations:
            msg.append(self._explain_plyo_violation(plyo_violations[0]))
        
        if sprint_violations:
            msg.append(self._explain_sprint_violation(sprint_violations[0]))
        
        if readiness_violations:
            msg.append(self._explain_readiness_violation(readiness_violations[0]))
        
        if population_violations:
            msg.append(self._explain_population_violation(population_violations[0]))
        
        if other_violations:
            for violation in other_violations:
                msg.append(f"   • {violation}\n")
        
        # Build fix suggestions
        msg.append("\n💡 HOW TO FIX:\n")
        msg.append(self._build_fix_suggestions())
        
        return "\n".join(msg)
    
    def _explain_plyo_violation(self, reason: str) -> str:
        """Explain plyometric violations in plain English"""
        if "WEEKLY_PLYO_CAP_EXCEEDED" in reason:
            # Extract numbers from reason
            parts = reason.split()
            projected = int(parts[parts.index("Projected") + 1]) if "Projected" in parts else "?"
            cap = int(parts[parts.index("Cap") + 1]) if "Cap" in parts else "?"
            
            completed = self.weekly_agg.get('completed_plyo_contacts', 0)
            session = self.weekly_agg.get('planned_plyo_contacts', 0)
            overage = projected - cap if isinstance(projected, int) and isinstance(cap, int) else "?"
            
            return (
                f"   Plyometric Contact Limit Exceeded:\n"
                f"   • Already used this week: {completed} contacts\n"
                f"   • This session adds: {session} contacts\n"
                f"   • Total would be: {projected} contacts\n"
                f"   • Your weekly limit: {cap} contacts\n"
                f"   • Overage: {overage} contacts\n"
            )
        
        elif "ADULT_MS_CONTACTS_EXCEEDED" in reason:
            parts = reason.split()
            actual = parts[1] if len(parts) > 1 else "?"
            return (
                f"   Adult MicroSession Contact Limit Exceeded:\n"
                f"   • This session: {actual} contacts\n"
                f"   • MicroSession limit: 60 contacts (special rule)\n"
                f"   • Regular Adult sessions allow 120 contacts\n"
                f"   • But MicroSessions are capped at 60\n"
            )
        
        else:
            return f"   • {reason}\n"
    
    def _explain_sprint_violation(self, reason: str) -> str:
        """Explain sprint violations in plain English"""
        if "SPRINT_SESSION_CAP_EXCEEDED" in reason:
            return (
                f"   Sprint Session Limit Exceeded:\n"
                f"   • You've already done 3 sprint sessions this week\n"
                f"   • Weekly limit: 3 sessions with true sprinting (≥90% max speed)\n"
                f"   • This protects against overtraining\n"
            )
        else:
            return f"   • {reason}\n"
    
    def _explain_readiness_violation(self, reason: str) -> str:
        """Explain readiness violations in plain English"""
        if "RED_READINESS_PLYO_VIOLATION" in reason:
            return (
                f"   RED Readiness Flag - No Plyometrics Allowed:\n"
                f"   • Athlete's readiness: RED (poor sleep/high stress/fatigue)\n"
                f"   • RED = Zero plyometric contacts allowed\n"
                f"   • Focus on mobility, skill work, and recovery only\n"
            )
        
        elif "YELLOW_READINESS_TIER_VIOLATION" in reason:
            return (
                f"   YELLOW Readiness Flag - Reduced Intensity Required:\n"
                f"   • Athlete's readiness: YELLOW (moderate fatigue)\n"
                f"   • YELLOW = Max E2 tier (no high-impact plyos)\n"
                f"   • Load reduced to 75% of normal volume\n"
            )
        
        else:
            return f"   • {reason}\n"
    
    def _explain_population_violation(self, reason: str) -> str:
        """Explain population limit violations"""
        if "E_NODE_EXCEEDED" in reason:
            parts = reason.split()
            return (
                f"   Exercise Intensity Too High for Age Group:\n"
                f"   • {' '.join(parts)}\n"
                f"   • Age-appropriate training is critical for safety\n"
            )
        else:
            return f"   • {reason}\n"
    
    def _build_fix_suggestions(self) -> str:
        """Build actionable fix suggestions"""
        suggestions = []
        
        for reason in self.reasons:
            if "WEEKLY_PLYO_CAP_EXCEEDED" in reason:
                overage = self._calculate_plyo_overage()
                suggestions.append(f"   ✓ Reduce plyometric volume by {overage} contacts:")
                suggestions.append(f"     - Remove 1-2 sets from high-contact exercises")
                suggestions.append(f"     - OR swap high-contact drills for lower-contact alternatives")
                suggestions.append(f"     - OR move this session to next week")
            
            elif "RED_READINESS" in reason:
                suggestions.append(f"   ✓ Switch to mobility/recovery session:")
                suggestions.append(f"     - Focus on foam rolling, stretching, breathing")
                suggestions.append(f"     - Light movement only (walking, yoga, swimming)")
                suggestions.append(f"     - Re-assess readiness tomorrow")
            
            elif "YELLOW_READINESS_TIER_VIOLATION" in reason:
                suggestions.append(f"   ✓ Reduce exercise intensity:")
                suggestions.append(f"     - Use E0-E2 tier exercises only")
                suggestions.append(f"     - Swap E3/E4 exercises for lower-tier alternatives")
                suggestions.append(f"     - Reduce volume by 25%")
            
            elif "ADULT_MS_CONTACTS_EXCEEDED" in reason:
                current = self.weekly_agg.get('planned_plyo_contacts', 0)
                remove = current - 60
                suggestions.append(f"   ✓ Reduce MicroSession contacts to 60 or below:")
                suggestions.append(f"     - Remove {remove} contacts (about 1-2 sets)")
                suggestions.append(f"     - OR convert to FULL_SESSION if appropriate")
            
            elif "SPRINT_SESSION_CAP_EXCEEDED" in reason:
                suggestions.append(f"   ✓ Move sprint work to next week")
                suggestions.append(f"   ✓ OR replace sprints with tempo runs (<90% speed)")
            
            elif "E_NODE_EXCEEDED" in reason or "BAND_EXCEEDED" in reason:
                suggestions.append(f"   ✓ Use age-appropriate exercise alternatives")
                suggestions.append(f"   ✓ Consult exercise library for legal substitutes")
        
        if not suggestions:
            suggestions.append(f"   ✓ Review technical details below for specific violations")
            suggestions.append(f"   ✓ Contact head coach for guidance")
        
        return "\n".join(suggestions) + "\n"
    
    def _calculate_plyo_overage(self) -> int:
        """Calculate how many contacts over the limit"""
        projected = self.weekly_agg.get('projected_total_plyo_contacts', 0)
        cap = self.weekly_agg.get('weekly_plyo_cap', 0)
        return max(0, projected - cap)
    
    def _build_missing_fields_message(self) -> str:
        """Build message for missing required fields"""
        msg = ["\n⚠️ Your request is missing required information.\n"]
        msg.append("📋 MISSING FIELDS:\n")
        
        for reason in self.reasons:
            if "MISSING_REQUIRED_FIELD" in reason:
                field = reason.replace("MISSING_REQUIRED_FIELD:", "").strip()
                msg.append(f"   • {field}")
        
        msg.append("\n💡 WHAT TO DO:\n")
        msg.append("   ✓ Provide all required client information")
        msg.append("   ✓ See technical details below for complete field list\n")
        
        return "\n".join(msg)
    
    def _build_quarantine_message(self) -> str:
        """Build message for quarantined sessions"""
        msg = ["\n🔍 This session requires manual review before programming.\n"]
        msg.append("📋 ISSUES FOUND:\n")
        
        for reason in self.reasons:
            if "MISSING_EXERCISE" in reason:
                msg.append(f"   • Exercise not found in library")
            elif "MISSING_INTENSITY" in reason:
                msg.append(f"   • Sprint exercise missing intensity data")
            else:
                msg.append(f"   • {reason}")
        
        msg.append("\n💡 NEXT STEPS:\n")
        msg.append("   ✓ Contact head coach for exercise verification")
        msg.append("   ✓ Check exercise IDs against library")
        msg.append("   ✓ Add missing metadata to exercise library\n")
        
        return "\n".join(msg)
    
    def _build_session_summary(self) -> str:
        """Build session summary for approved sessions"""
        msg = ["\n📊 SESSION SUMMARY:\n"]
        
        plan = self.session_plan
        msg.append(f"   Total Plyometric Contacts: {plan.get('total_plyo_contacts', 0)}")
        msg.append(f"   Total Sprint Meters: {plan.get('total_sprint_meters', 0)}")
        msg.append(f"   Session Duration: {plan.get('total_duration_minutes', 0)} minutes")
        msg.append(f"   CNS Demand: {plan.get('cns_category', 'N/A')}")
        
        return "\n".join(msg) + "\n"
    
    def _build_weekly_tracking(self) -> str:
        """Build weekly load tracking summary"""
        msg = ["\n📈 WEEKLY LOAD TRACKING:\n"]
        
        agg = self.weekly_agg
        
        # Plyo contacts
        plyo_projected = agg.get('projected_total_plyo_contacts', 0)
        plyo_cap = agg.get('weekly_plyo_cap', 0)
        plyo_pct = (plyo_projected / plyo_cap * 100) if plyo_cap > 0 else 0
        plyo_emoji = "✅" if plyo_projected <= plyo_cap else "❌"
        
        msg.append(f"   Plyometric Contacts: {plyo_projected} / {plyo_cap} ({plyo_pct:.0f}%) {plyo_emoji}")
        
        # Sprint meters
        sprint_projected = agg.get('projected_total_sprint_meters', 0)
        sprint_cap = agg.get('weekly_sprint_meters_cap', 0)
        sprint_pct = (sprint_projected / sprint_cap * 100) if sprint_cap > 0 else 0
        sprint_emoji = "✅" if sprint_projected <= sprint_cap else "❌"
        
        msg.append(f"   Sprint Meters: {sprint_projected} / {sprint_cap} ({sprint_pct:.0f}%) {sprint_emoji}")
        
        # Sprint sessions
        sessions_projected = agg.get('projected_total_sprint_sessions', 0)
        sessions_cap = agg.get('weekly_sprint_sessions_cap', 3)
        sessions_emoji = "✅" if sessions_projected <= sessions_cap else "❌"
        
        msg.append(f"   Sprint Sessions: {sessions_projected} / {sessions_cap} {sessions_emoji}")
        
        return "\n".join(msg) + "\n"
    
    def _build_technical_details(self) -> str:
        """Build collapsible technical details section"""
        msg = ["\n" + "─" * 80]
        msg.append("🔧 TECHNICAL DETAILS (For Advanced Users)")
        msg.append("─" * 80 + "\n")
        
        # Validation gates
        msg.append("Validation Gates:\n")
        for gate in self.validation_report:
            emoji = self.EMOJI.get(gate.get('status', 'SKIP'), "⊘")
            msg.append(f"   {emoji} Gate {gate.get('gate_id')}: {gate.get('gate_name')} ({gate.get('status')})")
            
            if gate.get('reasons'):
                for reason in gate.get('reasons')[:2]:
                    msg.append(f"      - {reason}")
        
        # Computed limits
        msg.append("\n\nComputed Limits:\n")
        session_caps = self.computed_limits.get('session_caps', {})
        msg.append(f"   Population: {self.computed_limits.get('population', 'N/A')}")
        msg.append(f"   Session Type: {self.computed_limits.get('session_type', 'N/A')}")
        msg.append(f"   Readiness: {self.computed_limits.get('readiness_flag', 'N/A')}")
        msg.append(f"   Max Band: {session_caps.get('max_band', 'N/A')}")
        msg.append(f"   Max E-Node: {session_caps.get('max_e_node', 'N/A')}")
        
        msg.append("\n" + "─" * 80 + "\n")
        
        return "\n".join(msg)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

def format_epa_response(epa_json_response: str) -> str:
    """
    Convert raw EPA JSON response to coach-friendly message
    
    Args:
        epa_json_response: JSON string from EPA.process()
    
    Returns:
        Formatted human-readable message
    """
    response_dict = json.loads(epa_json_response)
    builder = CoachMessageBuilder(response_dict)
    return builder.build_message(include_technical=True)


if __name__ == "__main__":
    print("EPA v2.2 Coach-Friendly Message Wrapper")
    print("This module formats EPA responses for human readability")
    print("\nUsage:")
    print("  from coach_messages import format_epa_response")
    print("  friendly_message = format_epa_response(epa_response_json)")
    print("  print(friendly_message)")
