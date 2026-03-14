"""Example 10-4. Guarded recursive agent generation with depth tracking.

A meta-agent loop with depth tracking, generation limits, validation gates,
and a kill switch to prevent runaway recursive agent creation.
"""

from dataclasses import dataclass, field
from typing import List, Optional
import json


@dataclass
class GeneratedAgent:
    """An agent created by the recursive generation process."""
    name: str
    depth: int
    parent: Optional[str]
    status: str  # "active", "failed", "killed"


class GuardedMetaAgent:
    """Meta-agent with depth tracking and generation limits."""

    MAX_DEPTH = 3
    MAX_TOTAL_AGENTS = 10

    def __init__(self):
        self.agents: List[GeneratedAgent] = []
        self.killed = False
        self.generation_log: List[str] = []

    def kill_switch(self) -> None:
        """Emergency stop for all generation."""
        self.killed = True
        self.generation_log.append("KILL SWITCH activated")

    def generate(self, name: str, depth: int = 0,
                 parent: Optional[str] = None) -> Optional[GeneratedAgent]:
        """Generate an agent with recursive depth protection."""

        # Gate 1: Kill switch
        if self.killed:
            self.generation_log.append(f"BLOCKED {name}: kill switch active")
            return None

        # Gate 2: Depth limit
        if depth > self.MAX_DEPTH:
            self.generation_log.append(
                f"BLOCKED {name}: depth {depth} exceeds max {self.MAX_DEPTH}")
            return None

        # Gate 3: Population limit
        if len(self.agents) >= self.MAX_TOTAL_AGENTS:
            self.generation_log.append(
                f"BLOCKED {name}: population limit {self.MAX_TOTAL_AGENTS} reached")
            self.kill_switch()
            return None

        # Gate 4: Validation (simulate — reject names containing "bad")
        if "bad" in name.lower():
            self.generation_log.append(f"REJECTED {name}: failed validation")
            return GeneratedAgent(name=name, depth=depth,
                                  parent=parent, status="failed")

        agent = GeneratedAgent(name=name, depth=depth,
                               parent=parent, status="active")
        self.agents.append(agent)
        self.generation_log.append(
            f"CREATED {name} at depth {depth} (parent: {parent or 'root'})")
        return agent


# --- Demo ---
if __name__ == "__main__":
    meta = GuardedMetaAgent()

    # Simulate recursive agent creation
    root = meta.generate("Deployer-v1", depth=0)
    child1 = meta.generate("Deployer-v1-retry", depth=1, parent="Deployer-v1")
    child2 = meta.generate("Deployer-v1-retry-fix", depth=2, parent="Deployer-v1-retry")
    child3 = meta.generate("Deployer-v1-deep", depth=3, parent="Deployer-v1-retry-fix")

    # This should be blocked — exceeds max depth
    blocked = meta.generate("Deployer-v1-too-deep", depth=4,
                            parent="Deployer-v1-deep")

    # This should be rejected — fails validation
    bad = meta.generate("bad-agent", depth=1, parent="Deployer-v1")

    print("=== Generation Log ===")
    for entry in meta.generation_log:
        print(f"  {entry}")

    print(f"\nActive agents: {len([a for a in meta.agents if a.status == 'active'])}")
    print(f"Blocked attempts: {sum(1 for e in meta.generation_log if 'BLOCKED' in e)}")
    print(f"Kill switch active: {meta.killed}")
