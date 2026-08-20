---
name: szh-ex
description: "Export the visible user and assistant messages from a selected local Codex chat to a tidy Markdown archive under knowladge/sessions in SandyFauzi/SYNESIS, then commit and push it with a guarded Git-only workflow. Use when the user asks to export, save, archive, sync, back up, or push the current/selected Codex chat context to SYNESIS, including requests such as 'szh-ex', 'export knowledge', or 'save this session'."
---

# SZH-EX — Export chat knowledge

Archive a selected Codex session as portable Markdown, then push only that new
session folder to `https://github.com/SandyFauzi/SYNESIS.git`.

## Scope and safety boundary

- Export **visible user and assistant messages** from Codex's local JSONL session
  log. Do not export hidden system/developer instructions, private reasoning,
  tool-call inputs/outputs, credentials, or unrelated session files.
- Create an agent-written `handoff.md` that records the task, decisions, current
  state, important paths, unresolved work, and a next-step prompt. It is a
  concise guide for the next device, not an invented summary.
- The exporter redacts common API keys, tokens, passwords, and secret assignments
  in both Markdown files. Treat this as a guardrail, not a guarantee: review the
  staged diff before committing, especially if the repository is public.
- Use Git only. Never use `git add .`, `git add -A`, force-push, `reset`, `clean`,
  history rewriting, global Git configuration, or an access token in a command.

## Export workflow

1. Locate the session deliberately. Do not assume the most recently modified
   log is the requested chat. List candidates with:

   ```powershell
   $codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE '.codex' }
   python '<skill-dir>\scripts\export_session.py' --list-sessions --sessions-root (Join-Path $codexHome 'sessions')
   ```

   Choose the session matching the user's requested conversation, working
   directory, and time. Ask the user if multiple candidates are plausible.

2. Write a factual `handoff.md` in a temporary location. Use this structure:

   ```markdown
   # Handoff
   ## Goal
   ## Decisions and rationale
   ## Current state
   ## Important files and commands
   ## Open items and risks
   ## Suggested next prompt
   ```

   Include only information supported by the chat or workspace. Do not include
   secrets, authentication material, or hidden instructions.

3. Run the exporter. The default clone location is
   `$CODEX_HOME/state/szh-sync/SYNESIS` (or `%USERPROFILE%\.codex\state\szh-sync\SYNESIS`).
   It clones the repository if absent; otherwise it verifies `origin`, requires a
   clean tree, and updates with `git pull --ff-only`.

   ```powershell
   python '<skill-dir>\scripts\export_session.py' `
     --session '<selected-rollout.jsonl>' `
     --handoff '<temporary-handoff.md>'
   ```

4. Report the created session ID, the number of exported messages, the number of
   redactions, commit SHA, and push result. If Git authentication or a fast-forward
   update fails, report the exact failure and leave the local archive intact; do
   not change Git configuration or use a destructive recovery command.

## Archive layout

```text
knowladge/
  sessions/
    <UTC-timestamp>-<Codex-session-id>/
      conversation.md
      handoff.md
      metadata.md
```

Keep the user-requested spelling `knowladge`. Create a new session directory for
every export; never overwrite or merge an existing archive.
