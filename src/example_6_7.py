"""Example 6-7. The workspace pipeline as a state machine.

Models the spec -> plan -> implement -> review pipeline
with explicit state transitions and artifact tracking.
"""
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, Optional


class Stage(Enum):
    SPEC = auto()
    PLAN = auto()
    IMPLEMENT = auto()
    REVIEW = auto()
    MERGED = auto()


TRANSITIONS = {
    Stage.SPEC: Stage.PLAN,
    Stage.PLAN: Stage.IMPLEMENT,
    Stage.IMPLEMENT: Stage.REVIEW,
    Stage.REVIEW: Stage.MERGED,
}


@dataclass
class Pipeline:
    issue_title: str
    current: Stage = Stage.SPEC
    artifacts: Dict[str, str] = field(default_factory=dict)

    def advance(self, artifact_key: str, artifact_value: str) -> None:
        next_stage = TRANSITIONS.get(self.current)
        if next_stage is None:
            raise RuntimeError(f"Cannot advance past {self.current.name}")
        self.artifacts[artifact_key] = artifact_value
        prev = self.current.name
        self.current = next_stage
        print(f"  {prev:>10} -> {self.current.name:<10}  artifact: {artifact_key}")

    def revise(self, back_to: Stage) -> None:
        """Return to an earlier stage (e.g., review sends back to plan)."""
        print(f"  {'REVISE':>10}: {self.current.name} -> {back_to.name}")
        self.current = back_to


# --- Run the pipeline ---
pipe = Pipeline(issue_title="Add farewell() feature")
print(f"Pipeline: {pipe.issue_title}")
print(f"  Starting at: {pipe.current.name}\n")

pipe.advance("spec", "Must add farewell(name) returning 'Goodbye, {name}!'")
pipe.advance("plan", "Edit utils.py, add tests/test_utils.py")
pipe.advance("implementation", "Branch feature/farewell with 2 file changes")

# Reviewer requests changes -> back to plan
pipe.revise(back_to=Stage.PLAN)
pipe.advance("plan_v2", "Also update README.md")
pipe.advance("implementation_v2", "Branch feature/farewell-v2 with 3 file changes")
pipe.advance("approval", "LGTM — merging")

print(f"\nFinal state: {pipe.current.name}")
print(f"Artifacts: {list(pipe.artifacts.keys())}")
