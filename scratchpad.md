# Scratchpad

## Single-Request Orchestration Status

- [x] Repository structure bootstrapped with book outline, TOC, style guide, and tracker.
- [x] Chapter 2.1 drafted and verified (bootstrap iteration from Copilot-Single).
- [ ] Orchestrator should delegate remaining Part I chapters to sub-agents.
- [ ] After Part I is complete, proceed to Part II chapters.

## Part I: The Pre-Cambrian Explosion

### 1.1 The Great IDE Exodus
- [x] Drafted and verified. Defines all core vocabulary terms (tool-calling, backpressure, composability, feedback loop, checkpoint, agent loop, human-in-the-loop, autonomy gradient).
- [x] Five concept loops: IDE bottleneck, CLI as universal API, composability, autonomy gradient, backpressure and checkpoints.
- [x] Code examples verified (Example 1-1, 1-5).

### 1.2 Claude Code: The "Boris" Persona and Systems Inhabitation
- [ ] Draft via sub-agent with terminal-first workflow examples.

### 1.3 The UX of Autonomy: Streaming, State, and CLI Sovereignty
- [ ] Draft via sub-agent; pair with screenshots or CLI transcripts.

### 2.1 Geoffrey Huntley's "I'm in Danger" Feedback Loops
- [x] Created and verified — use as the template for all future chapter sub-agent prompts.

### 2.2 Recursive Failure: Why Agents Hallucinate in Circles
- [ ] Draft via sub-agent; reuse the 2.1 loop vocabulary to classify retry storms, stale-context errors, and false-positive completion.
- [ ] Include one worked example showing how a bad success metric keeps a loop alive.

### 2.3 The Proverbial Glue: Reliability Engineering for Agentic Loops
- [ ] Draft via sub-agent; cover harness-level controls and observability.

## Next orchestrator actions

1. Select the next chapter to write (recommendation: 2.2 since it follows directly from 2.1).
2. Launch a sub-agent with the chapter-writer prompt template from `RESEARCH_LOOP_PROMPT.md`.
3. After the sub-agent finishes, update this file and `docs/chapter_tracker.md`.
4. Commit with `report_progress`.
5. Repeat for remaining chapters.
