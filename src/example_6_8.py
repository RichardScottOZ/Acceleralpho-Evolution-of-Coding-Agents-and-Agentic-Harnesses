"""Example 6-8. The pull request as the agent's unit of work.

Models a PR with the four key properties: atomic, reviewable,
testable, revertible — and a lifecycle from draft to merged.
"""
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List
import hashlib


class PRStatus(Enum):
    DRAFT = auto()
    OPEN = auto()
    CI_PASSING = auto()
    APPROVED = auto()
    MERGED = auto()
    REVERTED = auto()


@dataclass
class FileDiff:
    path: str
    additions: int
    deletions: int


@dataclass
class PullRequest:
    title: str
    branch: str
    diffs: List[FileDiff] = field(default_factory=list)
    status: PRStatus = PRStatus.DRAFT
    ci_passed: bool = False
    approvals: int = 0

    @property
    def diff_hash(self) -> str:
        """Content hash for atomicity — the PR is one logical unit."""
        content = "".join(f"{d.path}+{d.additions}-{d.deletions}" for d in self.diffs)
        return hashlib.sha256(content.encode()).hexdigest()[:12]

    @property
    def is_reviewable(self) -> bool:
        return len(self.diffs) > 0 and self.status != PRStatus.DRAFT

    @property
    def is_mergeable(self) -> bool:
        return self.ci_passed and self.approvals >= 1

    def open_pr(self) -> None:
        self.status = PRStatus.OPEN
        print(f"  PR opened: '{self.title}' on branch {self.branch}")

    def run_ci(self, passes: bool) -> None:
        self.ci_passed = passes
        self.status = PRStatus.CI_PASSING if passes else PRStatus.OPEN
        print(f"  CI {'PASSED' if passes else 'FAILED'} for {self.diff_hash}")

    def approve(self) -> None:
        self.approvals += 1
        self.status = PRStatus.APPROVED
        print(f"  Approved ({self.approvals} approval(s))")

    def merge(self) -> None:
        if not self.is_mergeable:
            print(f"  BLOCKED: ci_passed={self.ci_passed}, approvals={self.approvals}")
            return
        self.status = PRStatus.MERGED
        print(f"  MERGED: {len(self.diffs)} file(s), hash={self.diff_hash}")

    def revert(self) -> None:
        self.status = PRStatus.REVERTED
        print(f"  REVERTED: '{self.title}' rolled back in one action")


# --- Lifecycle demo ---
pr = PullRequest(
    title="Add farewell() feature",
    branch="feature/farewell",
    diffs=[
        FileDiff("utils.py", additions=15, deletions=0),
        FileDiff("tests/test_utils.py", additions=25, deletions=0),
        FileDiff("README.md", additions=3, deletions=1),
    ],
)

print("=== PR Lifecycle ===")
pr.open_pr()
print(f"  Reviewable: {pr.is_reviewable}")
pr.run_ci(passes=True)
pr.approve()
pr.merge()
print(f"  Final status: {pr.status.name}")

# Demonstrate revert
print("\n=== Revert scenario ===")
pr.revert()
print(f"  Final status: {pr.status.name}")
