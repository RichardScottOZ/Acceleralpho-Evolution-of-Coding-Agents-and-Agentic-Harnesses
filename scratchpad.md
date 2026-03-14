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
- [x] Drafted and verified. Five concept loops: systems inhabitation, Boris persona, git-awareness, psychological shift, permission model.
- [x] Examples 1-6 through 1-10 with realistic terminal transcripts.
- [x] Mermaid diagram showing full interaction loop (inner autonomous + outer human-in-the-loop).
- [x] Callouts: 3 Key ideas, 2 Tips, 1 Warning, 1 Pitfall, 5 Check yourself prompts.

### 1.3 The UX of Autonomy: Streaming, State, and CLI Sovereignty
- [x] Drafted and verified. Five concept loops: streaming trust, layered progress, state management, CLI sovereignty, UX anti-patterns.
- [x] Examples 1-11 through 1-17 with CLI transcripts and code examples.
- [x] Mermaid diagram showing three-layer progress model (token stream → status lines → milestone summaries).
- [x] Callouts: 2 Key ideas, 2 Tips, 2 Warnings, 2 Pitfalls, 5 Check yourself prompts.

### 2.1 Geoffrey Huntley's "I'm in Danger" Feedback Loops
- [x] Created and verified — use as the template for all future chapter sub-agent prompts.

### 2.2 Recursive Failure: Why Agents Hallucinate in Circles
- [x] Drafted via sub-agent. Five failure modes: retry storms, stale context, false-positive completion, context poisoning, metric gaming.
- [x] Examples 2-4 through 2-8. Mermaid diagrams showing failure classification.

### 2.3 The Proverbial Glue: Reliability Engineering for Agentic Loops
- [x] Drafted and verified. Five concept loops: harness as reliability layer, circuit breakers and budget caps, structured observability, checkpoint-and-resume, glue code philosophy.
- [x] Examples 2-9 through 2-13. Mermaid diagrams: harnessed loop architecture, circuit-breaker state machine.
- [x] All four Python code examples verified from ./src.
- [x] Maps all five failure modes from 2.2 to specific harness controls.

## Part II: The Architectural Sovereigns

### 3.1 Steve Yegge's Vision: High-Throughput Agentic Environments
- [x] Drafted and verified. Five concept loops: IDE bottleneck, Gas Town metaphor, bimodal split, high-throughput agent environment anatomy, measuring agent-readiness.
- [x] Examples 3-1 through 3-4. Three mermaid diagrams: IDE event loop bottleneck, Gas Town service architecture, full agent environment anatomy.
- [x] All four Python code examples verified (asyncio-based service simulation, bimodal router, health checker).
- [x] 15 callouts (5 Key idea, 4 Tip, 2 Warning, 4 Pitfall). 6 retrieval-practice exercises.
- [x] Connects back to Section 1.1 (IDE exodus), Section 2.2 (stale context failure mode), and Section 2.3 (harness layer).

## Next orchestrator actions

1. Part I is complete (1.1–2.3). Section 3.1 of Part II is complete.
2. Delegate remaining Part II chapters (3.2, 3.3, 4.1–4.3) to sub-agents.
3. Continue through Parts III–V.
4. After all chapters drafted, run a verification pass on code examples.
