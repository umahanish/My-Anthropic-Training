# Claude Code & Developer Toolchains — Student Lab Guide
### Module 7: From First Prompt to Production Workflows

New tool, familiar material — every lab below runs against `sample-repo-failing-test` from Module 2 (the off-by-one bug repo) or the `contract-review` Skill from Module 3. You're not learning Claude Code on a toy example; you're pointing it at code you already understand.

**Legend:** 🟢 Core (everyone does this) · 🔵 Stretch (going deeper)

---

## 1. What is Claude Code? Installation & First Prompt

**Basic theory:**
- Claude Code is an agentic coding tool that runs in your terminal (also available in VS Code, JetBrains, desktop, and the web). Unlike a chatbot, it reads your files, runs commands, and makes changes directly — you watch, redirect, or step away.
- This is a **separate install** from everything in Modules 1–6 — not claude.ai, not the Console. One more login to expect.

### 🟢 Lab 1.1 — Install and Log In *(10 min)*
1. Install (pick your OS):
   ```bash
   # macOS, Linux, WSL
   curl -fsSL https://claude.ai/install.sh | bash
   ```
   ```powershell
   # Windows PowerShell
   irm https://claude.ai/install.ps1 | iex
   ```
2. Verify: `claude --version` — should print a version number followed by `(Claude Code)`.
3. `cd` into your `sample-repo-failing-test` folder from Module 2, then run `claude`. Follow the browser login prompt (same account type as Modules 1–3's claude.ai login, Console, or your org's provider).

### 🟢 Lab 1.2 — Your First Real Prompt *(10 min)*
1. Ask: `what does this project do?` — notice Claude reads the files itself; you never point it at anything.
2. Ask: `explain the bug in contract_alerts.py` — see if it independently spots the same off-by-one you fixed by hand back in Module 2.
3. Ask it to actually fix it: `fix the bug in contract_alerts.py`. Watch the proposed change and approve it when prompted — this approval step is the default permission mode, and it's the same "review before it happens" habit from every module so far.

---

## 2. The Explore-Plan-Code-Commit Workflow

**Basic theory:**
- Letting Claude jump straight to coding can solve the wrong problem. The recommended four-phase workflow separates thinking from doing: **Explore** (read-only understanding) → **Plan** (a written approach you can edit) → **Implement** (code against the plan) → **Commit**.
- Skip planning for small, obvious fixes. Use it when scope is unclear, multiple files are involved, or you don't know the codebase well — exactly Lab 1.2's bug, done properly this time.

### 🟢 Lab 2.1 — Run the Full Workflow *(20 min)*
1. **Explore:** press `Shift+Tab` until the status bar shows `⏸ plan mode on`. Ask:
   ```
   Read contract_alerts.py and test_contract_alerts.py and understand
   why one test is failing.
   ```
2. **Plan:** ask for a plan:
   ```
   Propose a fix for the off-by-one bug. What's the exact one-line change,
   and could it affect the other two passing tests?
   ```
3. **Implement:** exit plan mode (`Shift+Tab` again, or approve the plan), then:
   ```
   Implement the fix. Run pytest -v after and show me the output.
   ```
4. **Commit:** `commit with a descriptive message`.

### 🔵 Lab 2.2 (Stretch) — Skip Planning on Purpose *(8 min)*
1. Undo your commit (`git reset --soft HEAD~1`), and ask Claude to fix the same bug again — this time with no plan mode, straight to implementation.
2. Compare: did skipping the plan phase change the quality or your confidence in the result? For a one-line fix like this, was planning actually worth the overhead?

---

## 3. CLAUDE.md, Context Management & Code Review

**Basic theory:**
- CLAUDE.md is a file Claude reads at the start of every session — persistent project context you'd otherwise re-explain each time. Keep it under 200 lines; longer files reduce adherence, not improve it.
- Context fills up fast — every file read and command output counts against it. `/context` shows usage, `/compact` summarizes to free space, `/clear` wipes it entirely between unrelated tasks.

### 🟢 Lab 3.1 — Generate and Refine a CLAUDE.md *(12 min)*
1. In the `sample-repo-failing-test` project, run `/init`. Claude analyzes the codebase and writes a starter `CLAUDE.md`.
2. Open it and check: does it mention `pytest -v` as the test command? Add one instruction it wouldn't have discovered on its own, e.g.:
   ```
   # Workflow
   - Always run pytest -v after any change to contract_alerts.py
   ```
3. Run `/context` and confirm your CLAUDE.md appears under **Memory files**.

### 🟢 Lab 3.2 — Context Usage and Code Review *(12 min)*
1. Run `/context` again after a few more prompts — watch the usage grid grow.
2. Make a small edit, then run `/code-review` (or its alias `/review`) to check the current diff for bugs and cleanups before you'd actually commit it — this is Claude reviewing Claude, in a fresh look at just the diff.
3. Run `/compact` and notice project-root CLAUDE.md gets re-read from disk afterward — it survives compaction; nested CLAUDE.md files and path-scoped rules don't reload automatically.

---

## 4. Subagents: Design, Creation & Effective Use

**Basic theory:**
- A subagent runs in its **own context window** with its own tool access and system prompt. Use one when a side task would flood your main conversation with search results or logs you won't reference again.
- Built-in ones exist already: **Explore** (read-only search), **Plan** (research during plan mode), **general-purpose** (multi-step work). You can also define custom ones in `.claude/agents/`.

### 🟢 Lab 4.1 — Create and Use a Custom Subagent *(15 min)*
1. Ask Claude to build one:
   ```
   Create a project-level code-reviewer subagent in .claude/agents/ that
   reviews code for quality, security, and best practices. Make it
   read-only (Read, Grep, Glob, Bash) and use Sonnet.
   ```
2. Open the generated `.claude/agents/code-reviewer.md` — confirm it has `name`, `description`, `tools`, and `model` in the frontmatter.
3. Invoke it explicitly: `Use the code-reviewer subagent to review contract_alerts.py`. Notice the delegation shows as a distinct row in the transcript — that's a separate context window doing the work, not your main conversation.

### 🔵 Lab 4.2 (Stretch) — Parallel Research *(10 min)*
1. Ask: `Use subagents to investigate our test coverage and our error handling patterns in parallel.`
2. Watch two subagents run — each explores independently and reports a summary back, keeping the verbose file-reading out of your main context.

---

## 5. Skills in Claude Code & MCP Server Integration

**Basic theory:**
- A **skill** is a `SKILL.md` file in `.claude/skills/` — domain knowledge or a repeatable workflow Claude loads on demand, not on every session start like CLAUDE.md. This is the exact same mechanism you used in claude.ai back in Module 3.
- MCP servers connect Claude Code to external tools, the same protocol you built a server for in Module 6.

### 🟢 Lab 5.1 — Bring Your Module 3 Skill Into Claude Code *(12 min)*
1. Create the folder: `mkdir -p .claude/skills/contract-review`
2. Copy your `contract-review` Skill's `SKILL.md` content from Module 3 into `.claude/skills/contract-review/SKILL.md`.
3. In Claude Code, type `/` — your skill should appear in the list alongside built-in commands. Try it: `/contract-review` (or ask a contract-review question naturally and see if Claude invokes it on its own).

### 🟢 Lab 5.2 — Connect Your Module 6 MCP Server *(10 min)*
1. With your `contract_server.py` from Module 6 available, connect it:
   ```bash
   claude mcp add contract-server -- python /path/to/contract_server.py
   ```
2. Run `/mcp` to confirm it's connected and see its tools listed.
3. Ask: `What's the renewal status of the Nimbus Cloud Services contract?` — Claude Code should call your MCP tool directly, the same tool you tested manually in the Inspector back in Module 6.

---

## 6. Hooks, the SDK & GitHub Integration

**Basic theory:**
- Hooks are shell commands Claude Code runs automatically at lifecycle points — deterministic, unlike CLAUDE.md instructions which are advisory. Use hooks for anything that must happen with zero exceptions.
- The Agent SDK lets you build your own applications on Claude Code's agent loop, in Python or TypeScript.
- GitHub Actions brings Claude Code into CI — responding to `@claude` mentions, running on PRs, or on a schedule.

### 🟢 Lab 6.1 — Block Edits to a Protected File *(15 min)*
1. Save as `.claude/hooks/protect-tests.sh`:
   ```bash
   #!/bin/bash
   INPUT=$(cat)
   FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
   if [[ "$FILE_PATH" == *"test_contract_alerts.py"* ]]; then
     echo "Blocked: don't edit the test file directly, fix the bug in contract_alerts.py instead" >&2
     exit 2
   fi
   exit 0
   ```
2. `chmod +x .claude/hooks/protect-tests.sh`
3. Add to `.claude/settings.json`:
   ```json
   {
     "hooks": {
       "PreToolUse": [
         {
           "matcher": "Edit|Write",
           "hooks": [{ "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-tests.sh" }]
         }
       ]
     }
   }
   ```
4. Ask Claude to edit `test_contract_alerts.py` directly. Confirm it's blocked, with your message shown as the reason — this is enforced, not advisory, unlike a CLAUDE.md instruction saying the same thing.

### 🔵 Lab 6.2 (Stretch) — Agent SDK Quickstart *(15 min)*
1. `pip install claude-agent-sdk`, and make sure `ANTHROPIC_API_KEY` is set (same Console key from Module 3 — the SDK doesn't load `.env` files automatically).
2. Save as `sdk_demo.py`, run from inside `sample-repo-failing-test`:
   ```python
   import asyncio
   from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage

   async def main():
       async for message in query(
           prompt="Review contract_alerts.py for bugs that would cause incorrect results. Fix any you find.",
           options=ClaudeAgentOptions(
               allowed_tools=["Read", "Edit", "Glob", "Bash"],
               permission_mode="acceptEdits",
           ),
       ):
           if isinstance(message, AssistantMessage):
               for block in message.content:
                   if hasattr(block, "text"):
                       print(block.text)
                   elif hasattr(block, "name"):
                       print(f"Tool: {block.name}")
           elif isinstance(message, ResultMessage):
               print(f"Done: {message.subtype}")

   asyncio.run(main())
   ```
3. Run it: `python sdk_demo.py`. This is the same agentic loop from the terminal UI, callable from your own code — the `query()` function streams messages as Claude reasons, calls tools, and acts, with `permission_mode="acceptEdits"` auto-approving file changes instead of prompting you like the CLI does.

### 🔵 Lab 6.3 (Stretch) — GitHub Actions Setup *(10 min)*
1. If your sample repo is pushed to GitHub, run `/install-github-app` inside Claude Code and follow the prompts.
2. Open a test PR and comment `@claude summarize this diff` — confirm Claude responds directly on GitHub.

---

## 7. Custom Commands & Advanced Context Control — Project

**Basic theory:**
- Custom commands **are** skills — the same `.claude/skills/` mechanism from Topic 5, with `disable-model-invocation: true` so they only run when you explicitly type `/command-name`, never automatically.
- `$ARGUMENTS` in a skill body captures whatever text follows the command.

### 🔵 Project — Build a `/fix-bug` Command *(25 min)*
1. Create `.claude/skills/fix-bug/SKILL.md`:
   ```markdown
   ---
   name: fix-bug
   description: Fix a specific bug end to end
   disable-model-invocation: true
   ---
   Fix this bug: $ARGUMENTS

   1. Locate the relevant code
   2. Write a failing test that reproduces the bug, if one doesn't exist
   3. Implement the fix
   4. Run the full test suite and confirm everything passes
   5. Commit with a descriptive message
   ```
2. Run it: `/fix-bug the off-by-one error in days_until()`
3. **Advanced context control:** after it finishes, run `/context` — note how much of that multi-step workflow stayed contained in one turn versus how it would look as five separate manual prompts. Then try `/compact Focus on the bug fix, drop the exploration` and check what's preserved.

---

## 8. Rules: Defining Guardrails, Constraints & Enforceable Policies

**Basic theory:**
- `.claude/rules/` splits CLAUDE.md into topic files — each loaded the same way as CLAUDE.md (unconditionally) unless it has `paths` frontmatter, in which case it loads only when Claude touches matching files.
- **Rules and CLAUDE.md are both advisory** — Claude reads and tries to follow them, but nothing stops it from ignoring one. For a *hard* guarantee, you need a hook (Topic 6) or a `permissions.deny` setting, not a rule.

### 🟢 Lab 8.1 — Create a Path-Scoped Rule *(12 min)*
1. Create `.claude/rules/testing.md`:
   ```markdown
   ---
   paths:
     - "test_*.py"
   ---
   # Testing Rules
   - Never weaken an assertion to make a test pass — fix the underlying code instead
   - Every test must have a clear docstring explaining what it verifies
   ```
2. Ask Claude to touch a test file and watch whether it follows the rule. Since this only loads when Claude reads a matching file, confirm with `/context` — it shouldn't appear until you've actually worked with a `test_*.py` file this session.

### 🟢 Lab 8.2 — Advisory vs. Enforced *(10 min)*
1. Add a CLAUDE.md instruction: `Never commit directly to main.`
2. Now add an actually enforced version to `.claude/settings.json`:
   ```json
   {
     "permissions": {
       "deny": ["Bash(git push origin main)"]
     }
   }
   ```
3. Ask Claude to push to main both times you can test it. **Debrief:** which one actually stopped it, and which one just asked nicely? This is the same distinction from Lab 6.1 — write it down, since it's the single most important thing to get right when you're the one deciding what "guardrail" really means for your team.

---

## 9. Spec-to-PR Workflow & Test-Driven Development with Agents — Project

**Basic theory:**
- For anything bigger than a one-line fix: have Claude **interview you** about the feature, write a `SPEC.md`, then start a **fresh session** to implement against it — clean context focused entirely on building, with a written spec to check against instead of a memory of the conversation that produced it.
- TDD with agents: write the failing test first, then implement until it passes — the test *is* the verification loop Claude checks itself against.

### 🔵 Project — Spec, Then TDD, Then PR *(40 min)*
1. **Interview:** in a Claude Code session, describe a small real feature for your sample project, e.g., "add a function that returns all contracts expiring within N days." Ask:
   ```
   I want to build a function that returns all contracts expiring within N
   days. Interview me in detail using the AskUserQuestion tool. Ask about
   edge cases and tradeoffs I might not have considered. Once we've covered
   everything, write a complete spec to SPEC.md.
   ```
2. **Fresh session:** once `SPEC.md` exists, run `/clear` (or exit and restart `claude`) so implementation starts with clean context.
3. **TDD:** ask Claude to work test-first:
   ```
   Read SPEC.md. Write failing tests for the function it describes before
   writing any implementation. Show me the tests, then implement until
   they all pass.
   ```
4. **Adversarial review:** in the same or a fresh subagent context:
   ```
   Use a subagent to review this diff against SPEC.md. Check every
   requirement is implemented and every edge case has a test. Report gaps,
   not style preferences.
   ```
5. **Ship it:** `commit with a descriptive message and open a PR` (if your repo has a GitHub remote configured).

**Debrief:** compare this to how you'd have approached the same feature on Day 1 of this course — typing a single vague prompt into a chat window. Name the specific point in this 5-step flow where that version would most likely have gone wrong.
