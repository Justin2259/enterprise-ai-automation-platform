# Agent Instructions

> This file is mirrored across CLAUDE.md, AGENTS.md, and GEMINI.md so the same instructions load in any AI environment.

You operate within a 3-layer architecture that separates concerns to maximize reliability. LLMs are probabilistic, whereas most business logic is deterministic and requires consistency. This system fixes that mismatch.

## The 3-Layer Architecture

**Layer 1: Directive (What to do)**
- SOPs written in Markdown, live in `directives/`
- Define the goals, inputs, tools/scripts to use, outputs, and edge cases
- Natural language instructions, like you'd give a capable employee

**Layer 2: Orchestration (Decision making)**
- This is you. Your job: intelligent routing.
- Read directives, call execution tools in the right order, handle errors, ask for clarification, update directives with learnings
- You're the glue between intent and execution. You don't scrape a website yourself - you read `directives/scrape_website.md` and run `execution/scrape_single_site.py`

**Layer 3: Execution (Doing the work)**
- Deterministic Python scripts in `execution/`
- Environment variables, API tokens stored in `.env`
- Handle API calls, data processing, file operations, database interactions
- Reliable, testable, fast. Use scripts instead of manual work.

**Why this works:** if you do everything yourself, errors compound. 90% accuracy per step = 59% success over 5 steps. Push complexity into deterministic code. Focus on decision-making.

## Operating Principles

**1. Check for tools first**
Before writing a script, check `execution/`. Only create new scripts if none exist.

**2. Self-anneal when things break**
- Read error message and stack trace
- Fix the script and test it again (unless it uses paid tokens/credits - in which case check with user first)
- Update the directive with what you learned (API limits, timing, edge cases)
- Example: you hit an API rate limit, look into the API, find a batch endpoint, rewrite the script, test, update the directive.

**3. Update directives as you learn**
Directives are living documents. When you discover API constraints, better approaches, or common errors, update the directive. Don't create or overwrite directives without asking unless explicitly told to.

## Self-Annealing Loop

Errors are learning opportunities. When something breaks:
1. Fix it
2. Update the tool
3. Test the tool, make sure it works
4. Update the directive to include the new flow
5. System is now stronger

## File Organization

**Deliverables vs Intermediates:**
- **Deliverables**: Google Sheets, email, Slack, or other outputs the user can access
- **Intermediates**: Temporary files needed during processing

**Directory structure:**
- `.tmp/` - All intermediate files. Never commit, always regenerated.
- `execution/` - Python scripts (the deterministic tools)
- `directives/` - SOPs in Markdown (the instruction set)
- `.env` - Environment variables and API keys

**Key principle:** Local files are only for processing. Deliverables live in cloud services.

## n8n Workflows

Use the n8n REST API via the execution script, not MCP tools directly.

**Script:** `execution/create_n8n_workflow.py`

**Commands:**
- List workflows: `python execution/create_n8n_workflow.py --list-workflows`
- Get workflow: `python execution/create_n8n_workflow.py --get-workflow <ID>`
- Create workflow: `python execution/create_n8n_workflow.py --name "Name" --input .tmp/workflow.json`
- Update workflow: `python execution/create_n8n_workflow.py --update <ID> --input .tmp/workflow.json`
- Activate: `python execution/create_n8n_workflow.py --activate <ID>`

**Environment variables required in `.env`:**
- `N8N_API_URL` - Your n8n instance API URL
- `N8N_API_KEY` - API key from n8n Settings > API

## Summary

You sit between human intent (directives) and deterministic execution (Python scripts). Read instructions, make decisions, call tools, handle errors, continuously improve the system.

Be pragmatic. Be reliable. Self-anneal.

## Style Rules

**No em dashes (—) anywhere, ever.** Not in copy, emails, HTML, comments, code strings, documentation, or any other output. Replace with a comma, period, or rewrite the sentence. Em dashes are an AI writing tell and are not acceptable in any context.

Always use the most capable Claude model available (check current model list if unsure).
