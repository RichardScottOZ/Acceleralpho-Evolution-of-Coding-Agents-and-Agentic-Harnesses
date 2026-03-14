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

### 3.2 Beyond RAG: The Infinite Window and Hyper-Context
- [x] Drafted and verified. Five concept loops: naive RAG failure modes, context economics, Infinite Window architecture, hyper-context strategies, practical context pipeline.
- [x] Examples 3-5 through 3-9. Three mermaid diagrams: RAG pipeline, RAG vs Infinite Window, hyper-context pipeline layers.
- [x] All five Python code examples verified from ./src.
- [x] 17 callouts (8 Key idea, 4 Tip, 2 Warning, 3 Pitfall). 6 exercises (3-7 through 3-12).
- [x] Connects to Section 2.2 (stale context), Section 2.3 (harness layer), Section 3.1 (Gas Town).

### 3.3 Cody and the Evolution of the Context Power Plant
- [x] Drafted and verified. Five concept loops: search-to-engine evolution, triple retrieval, power plant metaphor, engine vs RAG, build your own.
- [x] Examples 3-10 through 3-14. Four mermaid diagrams. Exercises 3-13 through 3-18.

### 4.1 Jordan Hubbard's Threading: LLMs as First-Class OS Citizens
- [x] Drafted. Six concept loops: LLMs as external services, threading metaphor, scheduling/resource management, inter-agent IPC, security/isolation, Loom architecture.
- [x] Examples 4-1 through 4-7. Six mermaid diagrams.

### 4.2 Orchestration vs. Execution: The Loom Framework
- [x] Drafted. Five concept loops: orchestration problem, orchestration vs execution, multi-agent patterns, Loom weave model, failure handling.
- [x] Examples 4-8 through 4-14. Seven mermaid diagrams. 16 callouts. 4 exercises.

## Part III: The Harnesses and the Hyperscalers

### 5.1 Leashing the Beast: Tool-Calling and Sandboxed Execution
- [x] Drafted. Five concept loops: raw model gap, tool-calling protocol, sandboxed execution, full harness pattern, production hardening.
- [x] Examples 5-1 through 5-5. Three mermaid diagrams. 4 exercises.
- [x] Cross-references Sections 2.2, 2.3, and 4.2.

### 5.2 OpenRouter: The Switzerland of the Model Wars
- [x] Drafted. Five concept loops: fragmentation problem, universal gateway, routing strategies, model-switching agent, economics.
- [x] Examples 5-6 through 5-10. Three mermaid diagrams. 4 exercises.
- [x] Cross-references Sections 2.3 and 5.1.

## Next orchestrator actions

1. Part I is complete (1.1–2.3). Part II has 3.1–3.3, 4.1, and 4.2 complete.
2. Delegate remaining Part II chapter (4.3) to sub-agents.
3. Continue through Parts III–V (5.2–6.3, 7.1–8.3, 9.1–10.3).
4. After all chapters drafted, run a verification pass on code examples.
