---
name: szh-skill-sync
description: "Maintain a shared Git catalog of locally installed Claude skills and selectively install the skills needed by the current coding-agent session. Use when the user asks to sync, mirror, publish, restore, compare, install, or manage Claude/Codex skills across devices; when starting a new session whose required skills may be missing; or when the user invokes 'szh-skill-sync'."
---

# SZH Skill Sync

Use `~/.claude/skills` as the canonical local skill root for every compatible
coding agent. In this setup Codex's skill directory is linked to that folder,
so do not create or edit a second copy under `~/.codex/skills`.

The shared catalog is `https://github.com/SandyFauzi/SYNESIS.git` under
`claude-skills/`. It contains user-installed skills only; never publish the
provider-managed `.system` directory.

## Session-gated installation rule

Before installing any missing skill for a chat:

1. Infer only the skills that materially help the current task from their name
   and description.
2. Show the exact proposed names and a one-line reason for each.
3. Ask the user for explicit confirmation of that exact set.
4. Install only the names confirmed by the user. Do not install a whole catalog
   by default, and do not treat silence, a previous confirmation, or a request
   to inspect as permission to install.

Use this rule for every coding-agent session that loads this skill. A skill
cannot force runtimes that do not load it, so treat it as a portable operating
policy rather than a global system setting.

## Workflow

1. Inspect the local and remote catalogs without changing either skill folder:

   ```powershell
   python '<skill-dir>\scripts\skill_sync.py' --plan
   ```

   The script clones or fast-forward-pulls its working clone in
   `$CODEX_HOME/state/szh-sync/SYNESIS` (or `%USERPROFILE%\.codex\state\szh-sync\SYNESIS`),
   verifies `origin`, and prints local-only, remote-only, matching, and conflict
   groups.

2. For a new session, propose only the relevant names from `remote-only`, then
   wait for a direct confirmation. After confirmation, install the exact set:

   ```powershell
   python '<skill-dir>\scripts\skill_sync.py' `
     --install skill-a skill-b `
     --confirm skill-a,skill-b
   ```

3. To publish new local skills from a source device, first show the names that
   will be added, then ask the user to confirm the exact set. Publish only
   `local-only` skills:

   ```powershell
   python '<skill-dir>\scripts\skill_sync.py' `
     --publish skill-a skill-b `
     --confirm skill-a,skill-b
   ```

4. If a locally modified skill differs from its catalog copy, stop and present
   it as a conflict. Never overwrite it automatically. Use `--replace-remote`
   only after the user explicitly chooses the local version and confirms its
   exact name.

## Safety rules

- Require `SKILL.md` in every published or installed skill; ignore `.system`,
  hidden folders, `.git`, and `__pycache__`.
- Refuse symlinks, a dirty catalog clone, an unexpected remote, detached HEAD,
  force-pushes, history rewrites, `reset`, `clean`, and broad Git staging.
- Never delete or overwrite an installed local skill. Resolve local conflicts by
  creating a revised skill or by explicit user-directed migration.
- Never put credentials or access tokens in commands. If Git authentication
  fails, report it and stop.
