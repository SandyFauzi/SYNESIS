---
name: szh-im
description: "Clone or safely fast-forward pull the knowledge archive from SandyFauzi/SYNESIS and load a selected per-session Markdown handoff into the current Codex chat. Use when the user asks to import, restore, pull, clone, continue, or load saved knowledge/context from SYNESIS on another device, including requests such as 'szh-im' or 'import knowledge'."
---

# SZH-IM — Import chat knowledge

Retrieve the local clone of `https://github.com/SandyFauzi/SYNESIS.git`, then
load the relevant archived handoff and conversation into the current chat.

## Safe import workflow

1. Pull the archive with the bundled script:

   ```powershell
   python '<skill-dir>\scripts\import_sessions.py' --list
   ```

   The script clones to `$CODEX_HOME/state/szh-sync/SYNESIS` when necessary. For
   an existing clone, it verifies that `origin` is exactly `SandyFauzi/SYNESIS`,
   refuses a dirty tree, then uses `git fetch` and `git pull --ff-only` only.

2. Select the requested session. If the user has not named one, show the list and
   ask them to choose; use `--latest` only when they explicitly ask for the most
   recent archive.

   ```powershell
   python '<skill-dir>\scripts\import_sessions.py' --session '<session-id>'
   ```

3. Read `handoff.md` first. Read `conversation.md` only as much as needed for the
   user's task; it is a raw visible-message archive and may be long. Tell the user
   which session was loaded and summarize the restored state before acting.

## Boundaries

- An imported archive restores the visible user/assistant conversation and its
  handoff, not hidden system/developer prompts, reasoning, tool results, or live
  credentials.
- Do not push, modify, delete, reset, clean, or rewrite anything in SYNESIS while
  importing.
- If Git authentication, remote verification, or fast-forward pull fails, report
  the failure and stop. Do not substitute another remote or make a new repository.
