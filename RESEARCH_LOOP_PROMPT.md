Read book outline from docs/book-outline.md
Read TOC docs/table-of-contents.md
Read ./agents.md for available agents and the sub-agent orchestration model
Read book chapter tracker from docs/chapter_tracker.md
Read scratchpad.md

The goal of this project is to write the book "Acceleralpho: Evolution of coding agents and agentic harnesses". It must be beginner-friendly, but also the absolutely cutting edge of the modern production-grade quality research into coding agents, agentic harnesses, and the evolution of AI-assisted development. Intuition and philosophy must come always first, the explanations must be intuitive and introduce concepts gradually without overload.

## Single-Request Sub-Agent Orchestration

This repo is designed to produce the entire book within **a single GitHub Copilot coding agent session** (1 premium request). The orchestrator agent reads the state files, then delegates chapter writing to sub-agents using the Task tool. Each sub-agent call runs inside the same session and does NOT consume an additional premium request.

### How the loop works

1. **Read state** — the orchestrator reads `scratchpad.md`, `docs/chapter_tracker.md`, and `docs/book-outline.md` to understand what has been done and what remains.
2. **Select work items** — identify ALL planned chapters from the tracker that are not yet drafted.
3. **Delegate to sub-agents** — for each chapter to write, launch a sub-agent (using the Task tool with agent_type "general-purpose" or "task") with a prompt that includes:
   - the chapter topic and section number,
   - the book style guide (`docs/book_style.md`),
   - relevant context from `docs/book-outline.md`,
   - instructions to produce a complete chapter Markdown file.
4. **Collect and commit** — after all sub-agents finish, the orchestrator updates `docs/chapter_tracker.md`, `scratchpad.md`, and `docs/references.md`, then commits all changes.
5. **Repeat** — if there are still unfinished chapters, loop back to step 2 and delegate more sub-agents.

### Why sub-agents?

GitHub Copilot coding agents support spawning sub-agents via the Task tool. These sub-agents:
- run in separate context windows (keeping the orchestrator's context clean),
- execute within the same premium request session,
- can run sequentially to produce multiple chapters without additional cost.

This means the entire book can be written across many sub-agent invocations while only consuming **1 premium request** (1 point for Sonnet, 3 points for Opus).

### Rules for the orchestrator

- Read ALL state files before delegating any work.
- Delegate chapter writing to sub-agents — do NOT write chapters directly in the orchestrator context.
- Each sub-agent should write ONE chapter section and save it to the correct path (e.g., `docs/part1/2.1 I'm in Danger Feedback Loops.md`).
- After each batch of sub-agents completes, update the tracker and scratchpad.
- Use `report_progress` to commit changes after each batch.
- If code needs to be run for verification, it must be done in `./src` directory; it should never be added to commits.
- Follow book style guidance in `docs/book_style.md`.
- Each chapter must build each piece in logical progression (no "we'll come back to it later"), must have a deliverable and verification.
- Explain intuition behind every formula when it is introduced the first time.
- Prefer mermaid diagrams for flowcharts and block diagrams.
- Verify code examples are functional and produce documented output that is aligned with intention.
- Focus only on production-grade 2026 edition.
- Perform necessary research, web search as needed — use available agents to do it.
- Use LaTeX format for formulas when needed.
- Add a short "How to read this chapter" box at the top of each math-heavy chapter.
- Break dense theory into repeated loops: concept -> worked numeric example -> code -> check-yourself prompt; 3-6 concept loops per chapter.
- Use O'Reilly-style Tip / Warning / Sidebar blocks for traps instead of burying them in prose.
- Title key equations and key code blocks.
- Promote retrieval practice at chapter ends.
- Chapters output must be written in the format: `docs/part1/1.1 Your First Rust Program.md`
- Update `scratchpad.md` to add/remove/modify action items after each batch.
- Update `docs/chapter_tracker.md` to track current implementation status.
- Update `docs/references.md` with the list of resources used.
- After all work is done, add added/modified files and commit using `report_progress`.
- Do not add co-authored string to the commit.

### Sub-agent prompt template

When delegating a chapter to a sub-agent, use a prompt like:

```
You are writing chapter section {section_number} "{section_title}" for the book
"Acceleralpho: Evolution of Coding Agents and Agentic Harnesses".

Book style guide:
{paste contents of docs/book_style.md}

Chapter context from outline:
{paste relevant section from docs/book-outline.md}

Write the complete chapter section as a Markdown file. Follow the book style guide
exactly. Include:
1. A "How to read this chapter" callout at the top
2. A "Why this section matters" opener
3. A "Deliverable" section stating what the reader will learn
4. 3-6 concept loops (concept -> worked example -> code -> check-yourself)
5. A mermaid diagram where appropriate
6. O'Reilly-style Tip/Warning/Pitfall callouts
7. A "What we built" summary
8. A verification checklist
9. A "Wrapping up" section with exercises

Save the file to: docs/part{N}/{section_number} {section_title}.md

After writing, verify any code examples by running them.
```

### Pedagogical guidelines

- Orientation before detail. Start each chapter and major section by telling the reader what problem is being solved, why it matters, and what they should retain.
- Segment aggressively. Dense content should be broken into small units, each doing one conceptual job.
- Example before abstraction. Introduce a concrete case, then generalize.
- Keep coupled information physically close. Put the explanation, diagram, code, and verification steps near one another.
- Differentiate the main path from optional depth. The core narrative should be linear and survivable on first read.
- Use signaling ruthlessly. Make importance visible with labels like Key idea, Invariant, Pitfall, Result, Takeaway, and Why this matters.
- Prefer stable recurring structure. Every chapter uses the same high-level rhythm.
- Design for rereading and reference use.
- Make notation cheap to recover.
- End with retrieval, not just recap.
- Let complexity accumulate, not arrive all at once.
- Optimize for confidence, not completeness per page.
