"""Example 6-6. Modelling the autocomplete-to-agent evolution.

Shows how the unit of work expands from a single line suggestion
to a full multi-file change set as agents mature.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import List


class GenerationEra(Enum):
    AUTOCOMPLETE = "autocomplete"
    CHAT = "chat"
    WORKSPACE = "workspace"


@dataclass
class FileChange:
    path: str
    diff_summary: str


@dataclass
class CopilotOutput:
    era: GenerationEra
    description: str
    files_touched: List[FileChange] = field(default_factory=list)

    @property
    def scope(self) -> str:
        n = len(self.files_touched)
        if n == 0:
            return "single cursor position"
        elif n == 1:
            return "single file"
        return f"{n} files (PR-level)"


# --- Simulate each generation ---
autocomplete = CopilotOutput(
    era=GenerationEra.AUTOCOMPLETE,
    description="Suggest next line after 'def farewell('",
)

chat = CopilotOutput(
    era=GenerationEra.CHAT,
    description="Generate farewell() body in chat panel",
    files_touched=[FileChange("utils.py", "+farewell()")],
)

workspace = CopilotOutput(
    era=GenerationEra.WORKSPACE,
    description="Implement farewell feature across codebase",
    files_touched=[
        FileChange("utils.py", "+farewell()"),
        FileChange("tests/test_utils.py", "+test_farewell()"),
        FileChange("README.md", "+farewell docs"),
    ],
)

for output in [autocomplete, chat, workspace]:
    print(f"[{output.era.value:>12}] scope={output.scope:>25}  |  {output.description}")
