"""Example 10-1. Meta-agent generating an agent configuration from a task specification.

A meta-agent that takes a high-level task specification (name, goal, tools,
constraints) and produces a complete agent configuration: system prompt,
tool definitions, and loop parameters.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
import json
import uuid
from datetime import datetime


@dataclass
class TaskSpecification:
    """High-level description of a desired agent."""
    name: str
    goal: str
    tools: List[str]
    constraints: List[str]
    max_iterations: int = 10


@dataclass
class AgentConfiguration:
    """Complete configuration for a new agent instance."""
    agent_id: str
    system_prompt: str
    tool_definitions: List[Dict[str, Any]]
    loop_config: Dict[str, Any]
    created_at: str
    source_spec: str


class MetaAgent:
    """An agent whose output is another agent's configuration."""

    def generate(self, spec: TaskSpecification) -> AgentConfiguration:
        # Build system prompt from specification
        constraint_block = "\n".join(f"- {c}" for c in spec.constraints)
        system_prompt = (
            f"You are {spec.name}. Your goal: {spec.goal}\n\n"
            f"Constraints you MUST follow:\n{constraint_block}\n\n"
            f"Available tools: {', '.join(spec.tools)}.\n"
            f"Always explain your reasoning before acting."
        )

        # Generate tool definitions
        tool_defs = [
            {"name": tool, "description": f"Tool for {tool} operations",
             "parameters": {"type": "object", "properties": {}}}
            for tool in spec.tools
        ]

        # Configure execution loop
        loop_config = {
            "max_iterations": spec.max_iterations,
            "stop_on_error": True,
            "require_human_approval": any(
                "never auto" in c.lower() or "human" in c.lower()
                for c in spec.constraints
            ),
        }

        return AgentConfiguration(
            agent_id=str(uuid.uuid4())[:8],
            system_prompt=system_prompt,
            tool_definitions=tool_defs,
            loop_config=loop_config,
            created_at=datetime.now().isoformat(),
            source_spec=spec.name,
        )


# --- Demo ---
if __name__ == "__main__":
    meta = MetaAgent()

    spec = TaskSpecification(
        name="SecurityReviewer",
        goal="Review Python PRs for security vulnerabilities",
        tools=["ast_analyzer", "bandit_scanner"],
        constraints=[
            "Never auto-merge pull requests",
            "Flag but do not fix security issues",
            "Report findings in structured JSON",
        ],
        max_iterations=5,
    )

    config = meta.generate(spec)
    print(f"Generated agent: {config.source_spec} ({config.agent_id})")
    print(f"Tools: {[t['name'] for t in config.tool_definitions]}")
    print(f"Human approval required: {config.loop_config['require_human_approval']}")
    print(f"Max iterations: {config.loop_config['max_iterations']}")
    print(f"\nSystem prompt preview:")
    print(config.system_prompt[:200] + "...")
