# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## SECTION 0 — CRITICAL: Project Identity

**This is the first thing done at the start of every session, without exception.**

1. State the project name, local repo path, and GitHub repo URL.
2. Read `PROGRESS.md` and the latest file in `Handover/` from **this repo only**.
3. Confirm to the user: *"We are working on [PROJECT NAME] at [PATH]. Here is where we left off…"*
4. Never carry context, assumptions, or decisions from a different project into this session.
5. If any doubt exists about which project is active, stop and ask the user before proceeding.

There are multiple projects in development simultaneously. Confusion between projects causes irreversible mistakes.

---

## SESSION TRIGGER

When the user types **`22`**, immediately execute Section 0 and Section 1 in full — no other response before doing so.

---

## SECTION 1 — Session Start Protocol

After confirming project identity:

1. **Offer a `git pull`** — ask the user before running it. Never pull silently.
2. Check for `PROGRESS.md` and `Handover/` in the repo root.
   - Both exist → read them, summarise current state to the user, then await instruction.
   - Neither exists → this is a new project → follow **Section 2**.

---

## SECTION 2 — Project Initialisation Protocol

Run this sequence once, in order, for every new project. Do not skip steps.

### Step 1 — Define the project
Discuss with the user until both sides have a shared, written understanding of:
- What the project does and who it is for
- Target platform (web / Android / Linux / Windows / other)
- Key features and explicit non-goals

Write a `PROJECT_BRIEF.md` in the repo root capturing this. Get user sign-off before continuing.

### Step 2 — Agree on tech stack
Discuss the best language, framework, and tooling for this specific project.
Document the decision and the reasoning in `PROJECT_BRIEF.md`.

### Step 3 — Design the architecture
Apply the single-responsibility principle (Section 3) to break the project into named, single-purpose components.
List every component, get user sign-off on the breakdown, before writing any code.

### Step 4 — Create the skeleton
Create the folder and file structure (empty files, no logic yet). Also create:
- `PROGRESS.md` (from template in Section 8)
- `Handover/HANDOVER_YYYY-MM-DD.md` (from template in Section 8)
- `components.json` (from template in Section 3)
- `.env.example`
- `.gitignore` (must include `.env`)
- `.claude/settings.json` (from template in Section 6)
- `.github/workflows/ci.yml` (from template in Section 6)

### Step 5 — Initial GitHub push
Ask the user to approve this sequence before running it:
```
gh repo create [project-name] --public --source=. --remote=origin --push
```
If the GitHub repo already exists:
```
git add -A
git commit -m "chore: initial project structure"
git push -u origin main
```
This sets a clean, clonable baseline on GitHub immediately. Every collaborator can clone from this point.

---

## SECTION 3 — Development Methodology: Single-Responsibility + Orchestration

### The principle
Every function, tool, or feature lives in **its own clearly named file or folder**.
Each component does one thing. Its name describes exactly what that one thing is.
No mixing of concerns. No multi-purpose files.

### The orchestration file
One dedicated orchestration file (e.g. `main.py`, `app.js`, `index.ts`) wires components together.
- Components never import each other directly across domains — they connect only through the orchestration file.
- The orchestration file is updated every time any component changes.
- The orchestration file is always referenced in the handover.

### The component manifest (components.json)
Tracks every component at the root of the repo:
```json
{
  "project": "Project Name",
  "orchestration_file": "main.py",
  "components": [
    {
      "name": "component-name",
      "file": "src/component_name.py",
      "purpose": "One sentence description of what this component does",
      "status": "not-started",
      "connects_to": ["other-component-name"]
    }
  ]
}
```
Update `components.json` whenever a component is added, changed, or completed.

### The build cycle (one component at a time)
1. **Plan** — describe the component in plain language to the user
2. **Discuss** — answer questions, resolve ambiguity before writing any code
3. **Approve** — wait for explicit user "yes"
4. **Build** — write the component in its own dedicated file
5. **Test** — test in isolation before integrating
6. **Integrate** — wire into the orchestration file, update `components.json`
7. **Mark complete** — update `PROGRESS.md`

Never start the next component until the current one is tested, integrated, and marked complete.

---

## SECTION 4 — Change Approval Protocol

Before making ANY change — new code, edit, refactor, config change, dependency, or file rename — present to the user:

| Field | Content |
|---|---|
| **What** | Specific file, function, or config being changed |
| **Why** | Root cause or requirement driving the change |
| **Improvement** | What gets better and how |
| **Loss / Risk** | What could break, regress, or be removed |

Wait for explicit user "yes" before proceeding. No exceptions.

### Risky or architectural changes
For changes that are particularly complex, risky, or fundamental to the project's architecture:

1. Offer to create a feature branch: `git checkout -b feat/[short-description]`
2. Develop and test on that branch only — never on main
3. When stable, present a summary of what changed and offer to merge:
   ```
   git checkout main
   git merge feat/[short-description]
   ```
4. **Always ask the user to approve the merge.** Never auto-merge.
5. After a successful merge, offer to delete the feature branch.

---

## SECTION 5 — Session End Protocol

At the end of every session, or before the context window fills:

1. **Update `PROGRESS.md`** — mark completed items, note blockers, update statuses
2. **Update `components.json`** — reflect any component additions or changes
3. **Update the orchestration file** if any component was added or modified
4. **Create a new `Handover/HANDOVER_YYYY-MM-DD.md`** using the template in Section 8
5. **Offer a git sync** — ask the user to approve before running:
   ```
   git add -A
   git commit -m "[type]: [short description of session work]"
   git push
   ```
6. Confirm to the user: what was completed this session, what is next, and what the next session must read first.

---

## SECTION 6 — Optimisations & Tooling

### Pre-approved commands (.claude/settings.json)
Created at project init. Reduces permission prompts for safe, read-only operations:
```json
{
  "permissions": {
    "allow": [
      "Bash(git status)",
      "Bash(git diff*)",
      "Bash(git log*)",
      "Bash(git branch*)"
    ]
  }
}
```
Add project-specific safe commands as the project grows.

### Commit message format — Conventional Commits
All commits must follow: `type: short description`

| Type | Use for |
|---|---|
| `feat:` | New feature or component |
| `fix:` | Bug fix |
| `docs:` | Documentation or handover updates |
| `refactor:` | Restructuring without behaviour change |
| `test:` | Adding or updating tests |
| `chore:` | Dependencies, CI config, `.gitignore` |
| `style:` | Formatting only, no logic change |

### GitHub Actions CI scaffold (.github/workflows/ci.yml)
Created at project init. Update the test command once the stack is confirmed:
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: echo "Replace with actual test command"
```

### GitHub MCP
The GitHub MCP server is available in Claude Code. Prefer it over the `gh` CLI for:
- Creating and managing repositories
- Opening, reviewing, and merging pull requests
- Managing branches and issues

### Environment variables (.env.example)
Every project must have a `.env.example` at the root listing all required variables with empty values and a comment per entry:
```
# Description of what this variable is used for
VARIABLE_NAME=
```
`.env` is always in `.gitignore` and must never be committed under any circumstances.

---

## SECTION 7 — CLAUDE.md as a Living Document

This file is both a **rigid baseline** and a **dynamic project bible**.

- The rules in Sections 0–6 are permanent. They must never be removed or weakened.
- As the project evolves, add project-specific context directly below a `---` divider at the bottom of this file: confirmed tech stack, architecture decisions, custom field IDs, auth patterns, naming conventions, known constraints, anything a future Claude session needs to know.
- Project-specific additions never contradict the baseline — they only add specificity on top of it.
- If this file was changed during a session, note it in the handover.
- Keep this file scannable — no walls of text, no duplication.

**Every project starts with the same recipe. Every project ends with a CLAUDE.md that is the complete, accurate guide to that specific project.**

---

## SECTION 8 — File Templates

### PROGRESS.md
```markdown
# [Project Name] — Progress Map

**Platform:** [web / Android / Linux / Windows]
**Tech Stack:** [language, framework, key dependencies]
**GitHub:** [repo URL]
**Orchestration File:** [filename]
**Last Updated:** YYYY-MM-DD

---

## Phases

### Phase 1 — [Name]
- [ ] Component: [name] — [one-line purpose]
- [ ] Component: [name] — [one-line purpose]

### Phase 2 — [Name]
- [ ] Component: [name] — [one-line purpose]

---

## Known Issues / Blockers
- None

## Completed Phases
(move completed phases here)
```

### Handover/HANDOVER_YYYY-MM-DD.md
```markdown
# [Project Name] — Handover YYYY-MM-DD

**GitHub:** [repo URL]
**Current Branch:** [branch name]
**Session Date:** YYYY-MM-DD

---

## Quick State (read this first)
- [What the project can do right now — max 5 bullets]
- [Current branch and any open feature branches]
- [Single most important next action]

---

## Completed This Session
- [Component or change] — [file name]

## Orchestration File State
[One paragraph: what is connected, what is stubbed, what is missing]

## Open Decisions / Unresolved Questions
- [Any decision left open for the next session]

## Next Steps (in order)
1. [Exact first action for the next session]
2. [Second action]
3. [Third action]

## Files Modified This Session
- `[file path]` — [what changed]

## Notes for Next Session
[Anything the next Claude instance needs to know that is not obvious from the code]
```

---
<!-- Project-specific context is added below this line as the project evolves -->
