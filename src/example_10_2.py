"""Example 10-2. Self-improving agent with circuit breaker.

An agent that reads its own performance log, identifies the top failure mode,
and rewrites its system prompt to address it — with a circuit breaker that
reverts changes if performance degrades.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
import json
from copy import deepcopy


@dataclass
class PerformanceLog:
    """Simulated performance metrics from an agent run."""
    cycle: int
    success_rate: float
    avg_tokens: int
    error_categories: Dict[str, int]


@dataclass
class AgentState:
    """Mutable agent configuration that can self-modify."""
    system_prompt: str
    improvement_count: int = 0
    last_good_prompt: Optional[str] = None
    last_success_rate: float = 0.0


class SelfImprovingAgent:
    """Agent that modifies its own prompt based on performance data."""

    MAX_IMPROVEMENTS = 5
    MIN_IMPROVEMENT_DELTA = 0.01

    def __init__(self, initial_prompt: str):
        self.state = AgentState(
            system_prompt=initial_prompt,
            last_good_prompt=initial_prompt,
        )
        self.history: List[str] = []

    def analyze_and_improve(self, log: PerformanceLog) -> str:
        """Analyze performance log and optionally rewrite prompt."""

        # Circuit breaker: max improvements reached
        if self.state.improvement_count >= self.MAX_IMPROVEMENTS:
            return "HALT: max improvement cycles reached"

        # Circuit breaker: performance degraded
        if (log.cycle > 1 and
                log.success_rate < self.state.last_success_rate - self.MIN_IMPROVEMENT_DELTA):
            self.state.system_prompt = self.state.last_good_prompt
            self.state.improvement_count = 0
            return (f"REVERTED: success rate dropped from "
                    f"{self.state.last_success_rate:.0%} to {log.success_rate:.0%}")

        # Find top failure mode
        if not log.error_categories:
            self.state.last_success_rate = log.success_rate
            return "No errors to address"

        top_error = max(log.error_categories, key=log.error_categories.get)
        top_count = log.error_categories[top_error]

        # Save current as last known good before modifying
        self.state.last_good_prompt = self.state.system_prompt

        # Rewrite prompt to address top failure
        fix_instruction = f"\nIMPORTANT: Address '{top_error}' errors ({top_count} occurrences)."
        self.state.system_prompt += fix_instruction
        self.state.improvement_count += 1
        self.state.last_success_rate = log.success_rate

        self.history.append(
            f"Cycle {log.cycle}: {log.success_rate:.0%} success, "
            f"fixed '{top_error}' (count={top_count})"
        )
        return f"IMPROVED: added fix for '{top_error}'"


# --- Demo ---
if __name__ == "__main__":
    agent = SelfImprovingAgent("You are a code reviewer. Check for bugs and style issues.")

    logs = [
        PerformanceLog(1, 0.72, 1500, {"missed_context": 12, "false_positive": 3}),
        PerformanceLog(2, 0.81, 1800, {"timeout": 5, "false_positive": 2}),
        PerformanceLog(3, 0.65, 3200, {"timeout": 15}),  # Regression!
    ]

    for log in logs:
        result = agent.analyze_and_improve(log)
        print(f"Cycle {log.cycle} ({log.success_rate:.0%} success): {result}")

    print(f"\nTotal improvements applied: {agent.state.improvement_count}")
    print(f"Improvement history: {agent.history}")
    prompt_lines = agent.state.system_prompt.strip().split("\n")
    print(f"Final prompt lines: {len(prompt_lines)}")
