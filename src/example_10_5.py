"""Example 10-5. MetaAgentGovernor enforcing approval policies and audit trails.

A governance layer that enforces approval policies, checks against an
allowed-tools registry, and requires human approval above certain
autonomy thresholds. All agent creation events are logged.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from datetime import datetime
from enum import Enum
import json


class AutonomyLevel(Enum):
    LOW = "low"          # read-only operations
    MEDIUM = "medium"    # write to non-prod
    HIGH = "high"        # write to production


@dataclass
class ToolRegistryEntry:
    name: str
    autonomy_level: AutonomyLevel
    requires_approval: bool


@dataclass
class CreationRequest:
    requester: str
    agent_name: str
    requested_tools: List[str]
    purpose: str


@dataclass
class AuditEntry:
    timestamp: str
    action: str
    requester: str
    agent_name: str
    details: str
    approved: bool


class MetaAgentGovernor:
    """Governance layer for meta-agent operations."""

    def __init__(self, approval_threshold: AutonomyLevel = AutonomyLevel.HIGH):
        self.tool_registry: Dict[str, ToolRegistryEntry] = {}
        self.audit_log: List[AuditEntry] = []
        self.approval_threshold = approval_threshold
        self.pending_approvals: List[CreationRequest] = []

    def register_tool(self, name: str, level: AutonomyLevel) -> None:
        self.tool_registry[name] = ToolRegistryEntry(
            name=name,
            autonomy_level=level,
            requires_approval=(
                list(AutonomyLevel).index(level)
                >= list(AutonomyLevel).index(self.approval_threshold)
            ),
        )

    def _log(self, action: str, request: CreationRequest,
             details: str, approved: bool) -> None:
        self.audit_log.append(AuditEntry(
            timestamp=datetime.now().strftime("%H:%M:%S"),
            action=action,
            requester=request.requester,
            agent_name=request.agent_name,
            details=details,
            approved=approved,
        ))

    def evaluate(self, request: CreationRequest) -> Dict[str, object]:
        """Evaluate an agent creation request against policies."""
        # Check all requested tools against registry
        unknown_tools = [t for t in request.requested_tools
                         if t not in self.tool_registry]
        if unknown_tools:
            self._log("REJECTED", request,
                      f"Unknown tools: {unknown_tools}", False)
            return {"approved": False, "reason": f"Unknown tools: {unknown_tools}"}

        # Determine max autonomy level
        max_level = max(
            (self.tool_registry[t].autonomy_level for t in request.requested_tools),
            key=lambda x: list(AutonomyLevel).index(x),
        )

        # Check if approval is required
        needs_approval = any(
            self.tool_registry[t].requires_approval
            for t in request.requested_tools
        )

        if needs_approval:
            self.pending_approvals.append(request)
            self._log("PENDING_APPROVAL", request,
                      f"Max autonomy: {max_level.value}", False)
            return {"approved": False,
                    "reason": f"Requires approval: {max_level.value} autonomy",
                    "pending": True}

        self._log("APPROVED", request,
                  f"Max autonomy: {max_level.value}", True)
        return {"approved": True, "autonomy_level": max_level.value}

    def approve_pending(self, agent_name: str, approver: str) -> bool:
        """Manually approve a pending request."""
        for req in self.pending_approvals:
            if req.agent_name == agent_name:
                self.pending_approvals.remove(req)
                self._log("MANUALLY_APPROVED", req,
                          f"Approved by {approver}", True)
                return True
        return False


# --- Demo ---
if __name__ == "__main__":
    gov = MetaAgentGovernor(approval_threshold=AutonomyLevel.HIGH)

    # Register tools with autonomy levels
    gov.register_tool("code_reader", AutonomyLevel.LOW)
    gov.register_tool("test_runner", AutonomyLevel.MEDIUM)
    gov.register_tool("staging_deploy", AutonomyLevel.MEDIUM)
    gov.register_tool("production_push", AutonomyLevel.HIGH)

    # Request 1: Low-risk agent (should auto-approve)
    r1 = CreationRequest("alice", "ReadOnlyAnalyzer",
                         ["code_reader"], "Analyze code quality")
    result1 = gov.evaluate(r1)
    print(f"Request 1 ({r1.agent_name}): {result1}")

    # Request 2: High-risk agent (should need approval)
    r2 = CreationRequest("bob", "HotfixDeployer",
                         ["code_reader", "production_push"],
                         "Deploy hotfixes to prod")
    result2 = gov.evaluate(r2)
    print(f"Request 2 ({r2.agent_name}): {result2}")

    # Request 3: Unknown tool (should reject)
    r3 = CreationRequest("charlie", "RogueAgent",
                         ["code_reader", "secret_stealer"],
                         "Definitely not malicious")
    result3 = gov.evaluate(r3)
    print(f"Request 3 ({r3.agent_name}): {result3}")

    # Approve pending request
    approved = gov.approve_pending("HotfixDeployer", "vp_diana")
    print(f"\nManual approval for HotfixDeployer: {approved}")

    # Print audit trail
    print(f"\n=== Audit Trail ({len(gov.audit_log)} entries) ===")
    for entry in gov.audit_log:
        print(f"  [{entry.timestamp}] {entry.action}: "
              f"{entry.agent_name} by {entry.requester} "
              f"- {entry.details} (approved={entry.approved})")
