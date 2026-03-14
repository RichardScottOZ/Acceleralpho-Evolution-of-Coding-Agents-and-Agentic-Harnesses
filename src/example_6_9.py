"""Example 6-9. Automated review heuristics for agent-generated code.

Scans a simulated agent-generated PR for common failure modes:
intent drift, hallucinated imports, and shallow tests.
"""
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class ReviewFinding:
    severity: str  # "error", "warning", "info"
    rule: str
    message: str


def check_hallucinated_imports(code: str, available_modules: set) -> List[ReviewFinding]:
    """Flag imports that reference modules not in the project."""
    findings = []
    for line in code.splitlines():
        stripped = line.strip()
        if stripped.startswith("import ") or stripped.startswith("from "):
            tokens = stripped.replace("from ", "").replace("import ", "").split(".")
            module = tokens[0].split()[0]
            if module not in available_modules:
                findings.append(ReviewFinding(
                    severity="error",
                    rule="hallucinated-import",
                    message=f"Module '{module}' not found in project or stdlib",
                ))
    return findings


def check_shallow_tests(test_code: str) -> List[ReviewFinding]:
    """Flag test assertions that are too weak."""
    findings = []
    weak_patterns = ["is not None", "is True", "is False", "!= None"]
    for i, line in enumerate(test_code.splitlines(), 1):
        for pattern in weak_patterns:
            if f"assert" in line and pattern in line:
                findings.append(ReviewFinding(
                    severity="warning",
                    rule="shallow-assertion",
                    message=f"Line {i}: Weak assertion using '{pattern}'",
                ))
    return findings


def check_intent_drift(issue_keywords: set, code: str) -> List[ReviewFinding]:
    """Warn if none of the issue keywords appear in the implementation."""
    code_lower = code.lower()
    matched = {kw for kw in issue_keywords if kw.lower() in code_lower}
    if len(matched) < len(issue_keywords) / 2:
        return [ReviewFinding(
            severity="warning",
            rule="intent-drift",
            message=f"Only {len(matched)}/{len(issue_keywords)} issue keywords found in code",
        )]
    return []


# --- Simulated agent PR ---
agent_code = """
from utils import greet
from magic_helpers import autofix  # does not exist!
import json

def farewell(name: str) -> str:
    return f"Goodbye, {name}!"
"""

agent_tests = """
def test_farewell_returns():
    result = farewell("Alice")
    assert result is not None  # too weak!

def test_farewell_content():
    result = farewell("Bob")
    assert result == "Goodbye, Bob!"
"""

known_modules = {"utils", "json", "os", "sys", "typing", "dataclasses"}
issue_keywords = {"farewell", "goodbye", "name"}

# --- Run checks ---
all_findings: List[Tuple[str, List[ReviewFinding]]] = [
    ("Hallucinated imports", check_hallucinated_imports(agent_code, known_modules)),
    ("Shallow tests", check_shallow_tests(agent_tests)),
    ("Intent drift", check_intent_drift(issue_keywords, agent_code)),
]

print("=== Agent PR Review Report ===\n")
total = 0
for check_name, findings in all_findings:
    print(f"[{check_name}]")
    if not findings:
        print("  No issues found.")
    for f in findings:
        print(f"  {f.severity.upper():>7}: ({f.rule}) {f.message}")
        total += 1
    print()

print(f"Total findings: {total}")
