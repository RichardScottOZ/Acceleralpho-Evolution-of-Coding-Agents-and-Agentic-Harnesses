"""Example 10-3. AgentFactory producing specialized agents from templates.

A factory class that takes a template name + parameters, validates constraints,
and produces configured agents. Demonstrates creating 3 different specialized
agents from one factory.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import json
from datetime import datetime


@dataclass
class AgentTemplate:
    """A reusable template for agent creation."""
    name: str
    base_prompt: str
    required_params: List[str]
    allowed_tools: List[str]
    constraints: Dict[str, Any]


@dataclass
class ProducedAgent:
    """An agent produced by the factory."""
    agent_id: str
    template_name: str
    system_prompt: str
    tools: List[str]
    parameters: Dict[str, Any]
    created_at: str


class AgentFactory:
    """Factory that stamps out validated agents from templates."""

    def __init__(self):
        self.templates: Dict[str, AgentTemplate] = {}
        self.produced: List[ProducedAgent] = []
        self._counter = 0

    def register_template(self, template: AgentTemplate) -> None:
        self.templates[template.name] = template

    def create(self, template_name: str, params: Dict[str, Any]) -> ProducedAgent:
        """Create an agent from a template with validation."""
        if template_name not in self.templates:
            raise ValueError(f"Unknown template: {template_name}")

        tmpl = self.templates[template_name]

        # Validate required parameters
        missing = [p for p in tmpl.required_params if p not in params]
        if missing:
            raise ValueError(f"Missing required params: {missing}")

        # Validate constraints
        for key, bounds in tmpl.constraints.items():
            if key in params:
                val = params[key]
                if isinstance(bounds, dict):
                    if "min" in bounds and val < bounds["min"]:
                        raise ValueError(f"{key}={val} below min {bounds['min']}")
                    if "max" in bounds and val > bounds["max"]:
                        raise ValueError(f"{key}={val} above max {bounds['max']}")

        # Build system prompt with parameters
        prompt = tmpl.base_prompt
        for k, v in params.items():
            prompt = prompt.replace(f"{{{k}}}", str(v))

        self._counter += 1
        agent = ProducedAgent(
            agent_id=f"{template_name}-{self._counter:04d}",
            template_name=template_name,
            system_prompt=prompt,
            tools=tmpl.allowed_tools,
            parameters=params,
            created_at=datetime.now().isoformat(),
        )
        self.produced.append(agent)
        return agent


# --- Demo ---
if __name__ == "__main__":
    factory = AgentFactory()

    # Register three templates
    factory.register_template(AgentTemplate(
        name="code_reviewer",
        base_prompt="Review {language} code for {focus_area}. Be thorough but concise.",
        required_params=["language", "focus_area"],
        allowed_tools=["ast_parser", "linter"],
        constraints={},
    ))
    factory.register_template(AgentTemplate(
        name="test_generator",
        base_prompt="Generate {language} tests targeting {coverage_target}% coverage.",
        required_params=["language", "coverage_target"],
        allowed_tools=["test_runner", "coverage_tool"],
        constraints={"coverage_target": {"min": 50, "max": 100}},
    ))
    factory.register_template(AgentTemplate(
        name="doc_writer",
        base_prompt="Write {doc_format} documentation for {language} projects.",
        required_params=["language", "doc_format"],
        allowed_tools=["markdown_renderer"],
        constraints={},
    ))

    # Create three specialized agents
    agents_to_create = [
        ("code_reviewer", {"language": "Python", "focus_area": "security"}),
        ("test_generator", {"language": "Python", "coverage_target": 90}),
        ("doc_writer", {"language": "Go", "doc_format": "markdown"}),
    ]

    for tmpl_name, params in agents_to_create:
        agent = factory.create(tmpl_name, params)
        print(f"Created: {agent.agent_id}")
        print(f"  Prompt: {agent.system_prompt}")
        print(f"  Tools:  {agent.tools}")
        print()

    print(f"Total agents produced: {len(factory.produced)}")

    # Demonstrate constraint validation
    try:
        factory.create("test_generator", {"language": "Rust", "coverage_target": 150})
    except ValueError as e:
        print(f"Validation caught: {e}")
