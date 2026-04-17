# Enterprise AI Automation Platform

A production-grade framework for building reliable AI automation systems. The core idea: **LLMs are great at decision-making, terrible at consistency**. This architecture separates the two.

---

## The Problem

When an AI agent tries to do everything itself, errors compound. 90% accuracy per step means 59% success over 5 steps. The fix is to push deterministic work into deterministic code, and let the LLM focus purely on routing and judgment.

---

## Architecture: 3 Layers

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: Directives  (directives/*.md)                     │
│  Natural-language SOPs. What to do, what tools to use,      │
│  what edge cases to handle. Written like instructions to     │
│  a capable employee.                                        │
└────────────────────────┬────────────────────────────────────┘
                         │ read by
┌────────────────────────▼────────────────────────────────────┐
│  Layer 2: Orchestration  (Claude / AI Agent)                │
│  Reads directives, decides which scripts to call and in     │
│  what order, handles errors, asks for clarification,        │
│  updates directives with new learnings.                     │
└────────────────────────┬────────────────────────────────────┘
                         │ calls
┌────────────────────────▼────────────────────────────────────┐
│  Layer 3: Execution  (execution/*.py)                       │
│  Deterministic Python scripts. API calls, data processing,  │
│  file operations, database writes. No judgment. Just work.  │
└─────────────────────────────────────────────────────────────┘
```

**Layer 1 defines intent. Layer 2 makes decisions. Layer 3 does the work.**

---

## How It Works in Practice

Say the task is: *"Pull all support tickets from the last 7 days and summarize the top issues."*

1. The agent reads `directives/weekly_ticket_summary.md`
2. It calls `execution/fetch_tickets.py --days 7`, which returns structured JSON
3. It reads the results, decides which categories matter, drafts the summary
4. It calls `execution/send_email.py` with the finished summary
5. If step 2 fails (rate limit, API change), it reads the error, fixes the script, retries, then updates the directive with what it learned

The AI never touches the API directly. The script never makes judgment calls.

---

## Self-Annealing

When something breaks, the system improves:

1. Script fails with an error
2. Agent reads the stack trace, fixes the script
3. Agent tests the fix
4. Agent updates the directive with the new constraint (rate limit, changed endpoint, etc.)

Each failure makes the system more robust. This is why the directives are living documents, not static SOPs.

---

## File Layout

```
enterprise-ai-automation-platform/
├── directives/              # SOPs - what to do and how
│   ├── example_api_integration.md
│   └── generate_report.md
├── execution/               # Deterministic Python scripts
│   ├── example_api_integration.py
│   └── generate_report.py
├── .env.example             # Required environment variables
└── .gitignore
```

---

## Example: API Integration Directive

See [directives/example_api_integration.md](directives/example_api_integration.md) for a full example of how a directive is structured: inputs, outputs, which script to call, error handling notes.

The matching script is [execution/example_api_integration.py](execution/example_api_integration.py).

---

## Real-World Implementations

This framework is the backbone of two production systems:

- **[genesys-cloud-rag](https://github.com/Justin2259/genesys-cloud-rag)** - Semantic search over a Genesys Cloud contact center org. Plain-English queries against IVR routing, queues, schedules, recording policies, and change history. Built on ChromaDB + ONNX embeddings, deployed as a Docker container on a Linux VPS.

---

## Design Principles

- **Check for existing tools first.** Before writing a new script, check `execution/`. Duplicate tools are a maintenance liability.
- **Execution scripts are dumb by design.** They take inputs and produce outputs. No branching on business logic.
- **Directives are owned by the system, not the session.** Update them as you learn. Don't create ephemeral instructions that disappear after a conversation.
- **Deliverables live in the cloud.** Local files are intermediates. Final outputs go to Google Sheets, Slack, email, or wherever the user can access them.
- **No em dashes.** They are an AI writing tell. Use a comma or rewrite the sentence.

---

## Getting Started

1. Copy `.env.example` to `.env` and fill in your credentials
2. Write a directive in `directives/` describing your automation task
3. Write the execution script in `execution/` that handles the deterministic work
4. Point your AI agent at the directive and let it orchestrate

The framework is model-agnostic. It works with Claude Code, Cursor, any agent that can read files and run shell commands.
