# Acceleralpho: Evolution of Coding Agents and Agentic Harnesses

A book about the rapid evolution of AI coding agents—from autocomplete to autonomous systems—written entirely by AI agents using a single-request orchestration loop.

## What is this?

This repository contains the manuscript and tooling for **"Acceleralpho"**, a book that traces the movement from "AI as a chatbox" to "AI as a systems inhabitant." The book covers coding agents like Claude Code, agentic harnesses, the Ralph Wiggum feedback loop, context engines, and the trajectory toward autonomous software development.

## How it works: Single-Request Sub-Agent Orchestration

This repo is designed so that the **entire book can be written within a single GitHub Copilot coding agent session** (1 premium request). Here is the key idea:

1. A **single orchestrator agent** starts and reads the project state files.
2. The orchestrator **delegates chapter writing to sub-agents** via the Task tool.
3. Each sub-agent runs in a separate context window but within the **same session** — no additional premium requests are consumed.
4. The orchestrator loops: delegate → collect → update tracker → commit → delegate more.
5. The result is a complete book manuscript produced by one premium request.

```mermaid
flowchart TD
    A[Orchestrator starts - 1 premium request] --> B[Read state files]
    B --> C[Identify unwritten chapters]
    C --> D[Launch sub-agent for chapter N]
    D --> E[Sub-agent writes chapter and saves file]
    E --> F[Orchestrator updates tracker]
    F --> G{More chapters?}
    G -->|yes| D
    G -->|no| H[Final commit and done]
```

### Cost

| Model | Points | Result |
| --- | --- | --- |
| Sonnet | 1 point | Entire book via sub-agents |
| Opus | 3 points | Entire book via sub-agents |

## Repository structure

```
├── README.md                          # This file
├── RESEARCH_LOOP_PROMPT.md            # Main orchestrator prompt and rules
├── agents.md                          # Sub-agent roles and working agreement
├── scratchpad.md                      # Working state for the current iteration
└── docs/
    ├── book-outline.md                # High-level book outline
    ├── book_style.md                  # Chapter style guide
    ├── chapter_tracker.md             # Per-section status tracker
    ├── references.md                  # Sources used
    ├── table-of-contents.md           # Full table of contents
    └── part1/                         # Part I chapter files
        └── 2.1 I'm in Danger Feedback Loops.md
```

## Getting started

To run the book-writing loop:

1. Open this repository on GitHub.
2. Tag `@copilot` on an issue or PR with: *"Read RESEARCH_LOOP_PROMPT.md and execute the orchestration loop. Write all unwritten chapters by delegating each to a sub-agent."*
3. The agent reads state, delegates chapters to sub-agents, and writes the book — all in one session.

For the full guide — including how to adapt this repo as a template for **your own book** — see **[RUNNING.md](RUNNING.md)**.

## Based on

This project is adapted from [Copilot-Single](https://github.com/RichardScottOZ/Copilot-Single), restructured to use sub-agent delegation so the entire process runs within a single premium request.
