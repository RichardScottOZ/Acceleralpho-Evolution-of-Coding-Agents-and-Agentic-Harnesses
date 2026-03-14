"""Example 6-10. CI feedback loop with automatic retry.

Simulates an agent that pushes code, reads CI results, and
iterates fixes until tests pass or the retry budget runs out.
"""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CIResult:
    passed: bool
    failing_test: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class Commit:
    message: str
    fixes_applied: List[str] = field(default_factory=list)


def simulate_ci(commit: Commit, failing_until_attempt: int, attempt: int) -> CIResult:
    """Simulate CI that fails until a specific attempt number."""
    if attempt < failing_until_attempt:
        return CIResult(
            passed=False,
            failing_test="test_farewell_format",
            error_message=f"AssertionError: expected 'Goodbye, Alice!' got 'Bye, Alice!'",
        )
    return CIResult(passed=True)


def agent_generate_fix(ci_result: CIResult) -> str:
    """Simulate the agent reading CI logs and proposing a fix."""
    if ci_result.failing_test and "farewell_format" in ci_result.failing_test:
        return "Fix: change 'Bye' prefix to 'Goodbye' in farewell()"
    return "Fix: generic correction based on error log"


@dataclass
class CIFeedbackLoop:
    max_retries: int = 3
    commits: List[Commit] = field(default_factory=list)

    def run(self, initial_commit: Commit, failing_until: int = 2) -> bool:
        """Run the push -> CI -> fix loop."""
        current_commit = initial_commit
        self.commits.append(current_commit)

        for attempt in range(1, self.max_retries + 1):
            print(f"\n--- Attempt {attempt}/{self.max_retries} ---")
            print(f"  Push: {current_commit.message}")

            ci = simulate_ci(current_commit, failing_until, attempt)

            if ci.passed:
                print(f"  CI: PASSED")
                print(f"  -> PR marked ready for review")
                return True

            print(f"  CI: FAILED")
            print(f"  Failing test: {ci.failing_test}")
            print(f"  Error: {ci.error_message}")

            if attempt < self.max_retries:
                fix = agent_generate_fix(ci)
                print(f"  Agent fix: {fix}")
                current_commit = Commit(
                    message=f"fix: address CI failure (attempt {attempt})",
                    fixes_applied=[fix],
                )
                self.commits.append(current_commit)
            else:
                print(f"  -> Retry budget exhausted, flagging for human help")

        return False


# --- Run the loop ---
print("=== CI Feedback Loop Simulation ===")
loop = CIFeedbackLoop(max_retries=3)

initial = Commit(message="feat: add farewell() function")
success = loop.run(initial, failing_until=3)

print(f"\nResult: {'SUCCESS' if success else 'NEEDS HUMAN HELP'}")
print(f"Total commits: {len(loop.commits)}")
for i, c in enumerate(loop.commits, 1):
    fixes = f" (fixes: {c.fixes_applied})" if c.fixes_applied else ""
    print(f"  {i}. {c.message}{fixes}")
