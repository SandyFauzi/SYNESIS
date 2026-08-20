#!/usr/bin/env python3
"""Safely clone or fast-forward SYNESIS and list one knowledge archive."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

REPO_URL = "https://github.com/SandyFauzi/SYNESIS.git"
REMOTE_ID = "sandyfauzi/synesis"


class ImportError(RuntimeError):
    """A safe import could not be completed."""


def default_codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))


def run(command: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(command, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown command failure"
        raise ImportError(f"Command failed: {' '.join(command[:3])}\n{detail}")
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
        raise ImportError(f"Refusing remote origin {origin!r}; expected {REPO_URL!r}.")


def has_head(repo: Path) -> bool:
    return subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--verify", "HEAD"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def update_repo(repo: Path) -> None:
    if repo.exists():
        if not (repo / ".git").is_dir():
            raise ImportError(f"Refusing non-Git destination: {repo}")
        assert_expected_origin(repo)
        if git(repo, "status", "--porcelain=v1"):
            raise ImportError(f"Refusing dirty repository: {repo}")
        git(repo, "fetch", "origin", "--prune")
        if has_head(repo):
            branch = git(repo, "symbolic-ref", "--quiet", "--short", "HEAD")
            if not branch:
                raise ImportError("Refusing detached HEAD.")
            git(repo, "pull", "--ff-only")
        return
    repo.parent.mkdir(parents=True, exist_ok=True)
    run(["git", "clone", REPO_URL, str(repo)])
    assert_expected_origin(repo)


def session_root(repo: Path) -> Path:
    return repo / "knowladge" / "sessions"


def list_archives(root: Path) -> list[Path]:
    if not root.is_dir():
        return []
    return sorted((entry for entry in root.iterdir() if entry.is_dir()), key=lambda entry: entry.name, reverse=True)


def choose_session(root: Path, session: str | None, latest: bool) -> Path | None:
    archives = list_archives(root)
    if latest:
        return archives[0] if archives else None
    if not session:
        return None
    if Path(session).name != session:
        raise ImportError("Session ID must be a single folder name.")
    chosen = root / session
    if not chosen.is_dir():
        raise ImportError(f"Session archive not found: {session}")
    return chosen


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-dir", type=Path, default=default_codex_home() / "state" / "szh-sync" / "SYNESIS")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--session", help="Select one archived session folder.")
    mode.add_argument("--latest", action="store_true", help="Select the newest archive after update.")
    mode.add_argument("--list", action="store_true", help="List archives after update (default).")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    update_repo(args.repo_dir)
    root = session_root(args.repo_dir)
    selected = choose_session(root, args.session, args.latest)
    if selected:
        print(f"session={selected.name}")
        print(f"handoff={selected / 'handoff.md'}")
        print(f"conversation={selected / 'conversation.md'}")
        print(f"metadata={selected / 'metadata.md'}")
        return 0

    archives = list_archives(root)
    if not archives:
        print("No knowledge archives found under knowladge/sessions.")
        return 0
    for archive in archives:
        print(archive.name)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ImportError as exc:
        print(f"szh-im: {exc}", file=sys.stderr)
        raise SystemExit(1)
