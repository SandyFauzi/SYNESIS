#!/usr/bin/env python3
"""Safely archive one visible Codex chat and push it to SYNESIS."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_URL = "https://github.com/SandyFauzi/SYNESIS.git"
REMOTE_ID = "sandyfauzi/synesis"
REDACTIONS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\b(?:sk|rk)_[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b", re.I),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(
        r"(?i)\b(?:api[_ -]?key|access[_ -]?token|auth(?:orization)?|password|secret)\b"
        r"\s*(?:[:=]|is)\s*(?:Bearer\s+)?[^\s`\"']+"
    ),
)


class ExportError(RuntimeError):
    """A safe export could not be completed."""


def default_codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))


def run(command: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(command, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown command failure"
        raise ExportError(f"Command failed: {' '.join(command[:3])}\n{detail}")
    return result.stdout.strip()


def git(repo: Path, *args: str) -> str:
    return run(["git", "-C", str(repo), *args])


def normalize_remote(value: str) -> str:
    value = value.strip().lower().removesuffix(".git")
    value = value.removeprefix("https://github.com/").removeprefix("http://github.com/")
    value = value.removeprefix("git@github.com:").removeprefix("ssh://git@github.com/")
    return value.strip("/")


def assert_expected_origin(repo: Path) -> None:
    origin = git(repo, "remote", "get-url", "origin")
    if normalize_remote(origin) != REMOTE_ID:
        raise ExportError(f"Refusing remote origin {origin!r}; expected {REPO_URL!r}.")


def git_status(repo: Path) -> str:
    return git(repo, "status", "--porcelain=v1")


def has_head(repo: Path) -> bool:
    return subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--verify", "HEAD"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def branch_name(repo: Path) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(repo), "symbolic-ref", "--quiet", "--short", "HEAD"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def prepare_repo(repo: Path) -> tuple[str | None, bool]:
    if repo.exists():
        if not (repo / ".git").is_dir():
            raise ExportError(f"Refusing non-Git destination: {repo}")
        assert_expected_origin(repo)
        if git_status(repo):
            raise ExportError(f"Refusing dirty repository: {repo}")
        git(repo, "fetch", "origin", "--prune")
        if has_head(repo):
            branch = branch_name(repo)
            if not branch:
                raise ExportError("Refusing detached HEAD.")
            git(repo, "pull", "--ff-only")
            return branch, False
        return None, True

    repo.parent.mkdir(parents=True, exist_ok=True)
    run(["git", "clone", REPO_URL, str(repo)])
    assert_expected_origin(repo)
    if has_head(repo):
        branch = branch_name(repo)
        if not branch:
            raise ExportError("Refusing detached HEAD after clone.")
        return branch, False
    return None, True


def redact(text: str) -> tuple[str, int]:
    total = 0
    for pattern in REDACTIONS:
        text, count = pattern.subn("[REDACTED]", text)
        total += count
    return text, total


def message_text(content: Any) -> str:
    if not isinstance(content, list):
        return ""
    parts: list[str] = []
    for part in content:
        if isinstance(part, dict) and part.get("type") in {"input_text", "output_text", "text"}:
            value = part.get("text")
            if isinstance(value, str) and value.strip():
                parts.append(value.rstrip())
    return "\n\n".join(parts)


def extract_messages(session: Path) -> list[tuple[str, str]]:
    messages: list[tuple[str, str]] = []
    try:
        lines = session.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise ExportError(f"Cannot read session file: {exc}") from exc

    for line_number, line in enumerate(lines, start=1):
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ExportError(f"Malformed JSONL at line {line_number}: {exc.msg}") from exc
        if record.get("type") != "response_item":
            continue
        item = record.get("payload", {})
        if item.get("type") != "message" or item.get("role") not in {"user", "assistant"}:
            continue
        text = message_text(item.get("content"))
        if text:
            messages.append((str(item["role"]), text))
    if not messages:
        raise ExportError("No visible user/assistant messages were found in this session.")
    return messages


def session_suffix(session: Path) -> str:
    stem = session.stem
    match = re.search(r"([0-9a-f]{8}-[0-9a-f-]{27,})$", stem, re.I)
    return match.group(1) if match else re.sub(r"[^a-zA-Z0-9-]+", "-", stem).strip("-")[-48:]


def write_archive(repo: Path, session: Path, handoff: Path) -> tuple[Path, int, int]:
    messages = extract_messages(session)
    try:
        handoff_text = handoff.read_text(encoding="utf-8")
    except OSError as exc:
        raise ExportError(f"Cannot read handoff file: {exc}") from exc
    if not handoff_text.strip():
        raise ExportError("Handoff file is empty.")

    archive_id = f"{datetime.now(UTC):%Y%m%dT%H%M%SZ}-{session_suffix(session)}"
    relative_dir = Path("knowladge") / "sessions" / archive_id
    archive_dir = repo / relative_dir
    if archive_dir.exists():
        raise ExportError(f"Archive already exists and will not be overwritten: {relative_dir}")
    archive_dir.mkdir(parents=True)

    redactions = 0
    rendered = ["# Conversation", "", "> Visible user and assistant messages exported from a Codex session.", ""]
    for index, (role, text) in enumerate(messages, start=1):
        text, count = redact(text)
        redactions += count
        rendered.extend((f"## {index:03d} — {role.title()}", "", text, ""))
    handoff_text, count = redact(handoff_text)
    redactions += count

    (archive_dir / "conversation.md").write_text("\n".join(rendered), encoding="utf-8", newline="\n")
    (archive_dir / "handoff.md").write_text(handoff_text.rstrip() + "\n", encoding="utf-8", newline="\n")
    metadata = (
        "# Export Metadata\n\n"
        f"- Exported UTC: `{datetime.now(UTC).isoformat()}`\n"
        f"- Source session: `{session.name}`\n"
        f"- Visible messages: {len(messages)}\n"
        f"- Automatic redactions: {redactions}\n"
        "- Excluded: hidden prompts, reasoning, and tool-call records.\n"
    )
    (archive_dir / "metadata.md").write_text(metadata, encoding="utf-8", newline="\n")
    return relative_dir, len(messages), redactions


def list_sessions(root: Path) -> None:
    if not root.is_dir():
        raise ExportError(f"Sessions directory not found: {root}")
    candidates = sorted(root.rglob("rollout-*.jsonl"), key=lambda item: item.stat().st_mtime, reverse=True)
    for session in candidates:
        session_id = "unknown"
        cwd = "unknown"
        try:
            first = json.loads(session.read_text(encoding="utf-8").splitlines()[0])
            payload = first.get("payload", {})
            session_id = str(payload.get("session_id", session_id))
            cwd = str(payload.get("cwd", cwd))
        except (IndexError, OSError, json.JSONDecodeError):
            pass
        print(f"{session}\n  session_id: {session_id}\n  cwd: {cwd}\n  modified_utc: {datetime.fromtimestamp(session.stat().st_mtime, UTC).isoformat()}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list-sessions", action="store_true", help="List local Codex session candidates and exit.")
    parser.add_argument("--sessions-root", type=Path, default=default_codex_home() / "sessions")
    parser.add_argument("--session", type=Path, help="Selected Codex rollout JSONL file.")
    parser.add_argument("--handoff", type=Path, help="Agent-written Markdown handoff file.")
    parser.add_argument("--repo-dir", type=Path, default=default_codex_home() / "state" / "szh-sync" / "SYNESIS")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.list_sessions:
        list_sessions(args.sessions_root)
        return 0
    if not args.session or not args.handoff:
        raise ExportError("--session and --handoff are required unless --list-sessions is used.")
    if args.session.suffix.lower() != ".jsonl":
        raise ExportError("Selected session must be a .jsonl file.")
    if args.handoff.suffix.lower() != ".md":
        raise ExportError("Handoff must be a .md file.")

    branch, empty_repo = prepare_repo(args.repo_dir)
    relative_dir, message_count, redactions = write_archive(args.repo_dir, args.session, args.handoff)
    git(args.repo_dir, "add", "--", relative_dir.as_posix())
    staged = git(args.repo_dir, "diff", "--cached", "--name-only").splitlines()
    prefix = relative_dir.as_posix() + "/"
    if not staged or any(not path.startswith(prefix) for path in staged):
        raise ExportError("Refusing to commit files outside the new session directory.")
    git(args.repo_dir, "diff", "--cached", "--check")

    if empty_repo:
        branch = "main"
        git(args.repo_dir, "checkout", "-B", branch)
    if not branch:
        raise ExportError("Could not determine the target branch.")
    git(args.repo_dir, "commit", "-m", f"knowladge: export {relative_dir.name}")
    if empty_repo:
        git(args.repo_dir, "push", "-u", "origin", branch)
    else:
        git(args.repo_dir, "push", "origin", f"HEAD:{branch}")
    commit = git(args.repo_dir, "rev-parse", "HEAD")
    print(f"archive={relative_dir.as_posix()}")
    print(f"messages={message_count}")
    print(f"redactions={redactions}")
    print(f"commit={commit}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ExportError as exc:
        print(f"szh-ex: {exc}", file=sys.stderr)
        raise SystemExit(1)
