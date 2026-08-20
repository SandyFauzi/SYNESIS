#!/usr/bin/env python3
"""Safely compare, publish, and selectively install a Claude skill catalog."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_URL = "https://github.com/SandyFauzi/SYNESIS.git"
REMOTE_ID = "sandyfauzi/synesis"
CATALOG_DIR = "claude-skills"
SKILL_NAME = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")
IGNORED_NAMES = {".git", "__pycache__"}


class SyncError(RuntimeError):
    """A safe skill sync could not be completed."""


def default_codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))


def default_claude_skills() -> Path:
    return Path(os.environ.get("CLAUDE_SKILLS_DIR", Path.home() / ".claude" / "skills"))


def run(command: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(command, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown command failure"
        raise SyncError(f"Command failed: {' '.join(command[:3])}\n{detail}")
    return result.stdout.strip()


def git(repo: Path, *args: str) -> str:
    return run(["git", "-C", str(repo), *args])


def normalize_remote(value: str) -> str:
    value = value.strip().lower().removesuffix(".git")
    value = value.removeprefix("https://github.com/").removeprefix("http://github.com/")
    value = value.removeprefix("git@github.com:").removeprefix("ssh://git@github.com/")
    return value.strip("/")


def assert_origin(repo: Path) -> None:
    origin = git(repo, "remote", "get-url", "origin")
    if normalize_remote(origin) != REMOTE_ID:
        raise SyncError(f"Refusing remote origin {origin!r}; expected {REPO_URL!r}.")


def has_head(repo: Path) -> bool:
    return subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--verify", "HEAD"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def current_branch(repo: Path) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(repo), "symbolic-ref", "--quiet", "--short", "HEAD"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def prepare_catalog(repo: Path) -> tuple[str | None, bool]:
    if repo.exists():
        if not (repo / ".git").is_dir():
            raise SyncError(f"Refusing non-Git catalog destination: {repo}")
        assert_origin(repo)
        if git(repo, "status", "--porcelain=v1"):
            raise SyncError(f"Refusing dirty catalog clone: {repo}")
        git(repo, "fetch", "origin", "--prune")
        if has_head(repo):
            branch = current_branch(repo)
            if not branch:
                raise SyncError("Refusing detached HEAD.")
            git(repo, "pull", "--ff-only")
            return branch, False
        return None, True

    repo.parent.mkdir(parents=True, exist_ok=True)
    run(["git", "clone", REPO_URL, str(repo)])
    assert_origin(repo)
    if has_head(repo):
        branch = current_branch(repo)
        if not branch:
            raise SyncError("Refusing detached HEAD after clone.")
        return branch, False
    return None, True


def valid_skill_dir(path: Path) -> bool:
    return path.is_dir() and not path.is_symlink() and bool(SKILL_NAME.fullmatch(path.name)) and (path / "SKILL.md").is_file()


def catalog_skills(root: Path) -> dict[str, Path]:
    if not root.is_dir():
        return {}
    return {entry.name: entry for entry in root.iterdir() if valid_skill_dir(entry)}


def assert_safe_tree(root: Path) -> None:
    if not valid_skill_dir(root):
        raise SyncError(f"Invalid skill directory (a regular SKILL.md folder is required): {root}")
    for item in root.rglob("*"):
        if item.is_symlink():
            raise SyncError(f"Refusing skill containing a symlink: {item}")


def tree_digest(root: Path) -> str:
    assert_safe_tree(root)
    digest = hashlib.sha256()
    for item in sorted(root.rglob("*"), key=lambda value: value.as_posix()):
        if any(part in IGNORED_NAMES for part in item.relative_to(root).parts):
            continue
        if item.is_dir():
            continue
        relative = item.relative_to(root).as_posix().encode("utf-8")
        digest.update(relative + b"\0")
        digest.update(item.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def compare(local: dict[str, Path], remote: dict[str, Path]) -> dict[str, list[str]]:
    result = {"same": [], "local_only": [], "remote_only": [], "different": []}
    for name in sorted(set(local) | set(remote)):
        if name not in remote:
            result["local_only"].append(name)
        elif name not in local:
            result["remote_only"].append(name)
        elif tree_digest(local[name]) == tree_digest(remote[name]):
            result["same"].append(name)
        else:
            result["different"].append(name)
    return result


def print_plan(groups: dict[str, list[str]]) -> None:
    labels = {
        "same": "matching",
        "local_only": "local-only (eligible to publish)",
        "remote_only": "remote-only (eligible to install with confirmation)",
        "different": "conflicts (manual decision required)",
    }
    for key in ("same", "local_only", "remote_only", "different"):
        values = groups[key]
        print(f"{labels[key]}: {', '.join(values) if values else '-'}")


def parse_confirmation(value: str | None, requested: list[str]) -> None:
    if not value:
        raise SyncError("Confirmation is required. Re-run with --confirm containing exactly the requested skill names.")
    confirmed = [name.strip() for name in value.split(",") if name.strip()]
    if sorted(set(confirmed)) != sorted(set(requested)) or len(confirmed) != len(set(confirmed)):
        raise SyncError("--confirm must contain exactly the requested skill names, once each.")


def copy_skill(source: Path, target: Path) -> None:
    assert_safe_tree(source)
    if target.exists():
        raise SyncError(f"Refusing to overwrite existing skill: {target}")
    shutil.copytree(source, target, ignore=shutil.ignore_patterns(".git", "__pycache__"))


def install_skills(remote: dict[str, Path], local_root: Path, requested: list[str], confirmation: str | None) -> None:
    if not requested:
        raise SyncError("Provide at least one skill name to --install.")
    parse_confirmation(confirmation, requested)
    for name in requested:
        if name not in remote:
            raise SyncError(f"Skill is not available in the remote catalog: {name}")
        if (local_root / name).exists():
            raise SyncError(f"Skill is already installed; refusing overwrite: {name}")
    local_root.mkdir(parents=True, exist_ok=True)
    for name in requested:
        copy_skill(remote[name], local_root / name)
        print(f"installed={name}")


def stage_and_push(repo: Path, paths: list[Path], branch: str | None, empty_repo: bool, message: str) -> None:
    for path in paths:
        git(repo, "add", "--", path.as_posix())
    staged = git(repo, "diff", "--cached", "--name-only").splitlines()
    expected = tuple(path.as_posix().rstrip("/") + "/" for path in paths)
    if not staged or any(not item.startswith(expected) for item in staged):
        raise SyncError("Refusing to commit files outside the selected catalog skills.")
    git(repo, "diff", "--cached", "--check")
    if empty_repo:
        branch = "main"
        git(repo, "checkout", "-B", branch)
    if not branch:
        raise SyncError("Could not determine the target branch.")
    git(repo, "commit", "-m", message)
    if empty_repo:
        git(repo, "push", "-u", "origin", branch)
    else:
        git(repo, "push", "origin", f"HEAD:{branch}")
    print(f"commit={git(repo, 'rev-parse', 'HEAD')}")


def publish_new(local: dict[str, Path], remote_root: Path, requested: list[str], confirmation: str | None, repo: Path, branch: str | None, empty_repo: bool) -> None:
    if not requested:
        raise SyncError("Provide at least one skill name to --publish.")
    parse_confirmation(confirmation, requested)
    targets: list[Path] = []
    for name in requested:
        if name not in local:
            raise SyncError(f"Local skill is not available: {name}")
        target = remote_root / name
        if target.exists():
            raise SyncError(f"Remote skill already exists; review it as a conflict: {name}")
        copy_skill(local[name], target)
        targets.append(Path(CATALOG_DIR) / name)
    stage_and_push(repo, targets, branch, empty_repo, f"skills: add {', '.join(requested)}")


def replace_remote(local: dict[str, Path], remote: dict[str, Path], remote_root: Path, requested: list[str], confirmation: str | None, repo: Path, branch: str | None, empty_repo: bool) -> None:
    if not requested:
        raise SyncError("Provide at least one skill name to --replace-remote.")
    parse_confirmation(confirmation, requested)
    for name in requested:
        if name not in local or name not in remote:
            raise SyncError(f"A local and remote version are both required for replacement: {name}")
        if tree_digest(local[name]) == tree_digest(remote[name]):
            raise SyncError(f"Skill is already identical; no replacement needed: {name}")
    targets: list[Path] = []
    for name in requested:
        target = remote_root / name
        git(repo, "rm", "-r", "--", (Path(CATALOG_DIR) / name).as_posix())
        copy_skill(local[name], target)
        targets.append(Path(CATALOG_DIR) / name)
    stage_and_push(repo, targets, branch, empty_repo, f"skills: update {', '.join(requested)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-dir", type=Path, default=default_codex_home() / "state" / "szh-sync" / "SYNESIS")
    parser.add_argument("--claude-skills", type=Path, default=default_claude_skills())
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--plan", action="store_true", help="Compare local skills with the remote catalog (default).")
    mode.add_argument("--install", nargs="+", metavar="SKILL", help="Install selected remote catalog skills.")
    mode.add_argument("--publish", nargs="+", metavar="SKILL", help="Publish selected local-only skills.")
    mode.add_argument("--replace-remote", nargs="+", metavar="SKILL", help="Replace selected conflicting remote skills after confirmation.")
    parser.add_argument("--confirm", help="Comma-separated names exactly matching the selected write operation.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    branch, empty_repo = prepare_catalog(args.repo_dir)
    local = catalog_skills(args.claude_skills)
    remote_root = args.repo_dir / CATALOG_DIR
    remote = catalog_skills(remote_root)
    groups = compare(local, remote)

    if args.install is not None:
        install_skills(remote, args.claude_skills, args.install, args.confirm)
    elif args.publish is not None:
        publish_new(local, remote_root, args.publish, args.confirm, args.repo_dir, branch, empty_repo)
    elif args.replace_remote is not None:
        replace_remote(local, remote, remote_root, args.replace_remote, args.confirm, args.repo_dir, branch, empty_repo)
    else:
        print_plan(groups)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SyncError as exc:
        print(f"szh-skill-sync: {exc}", file=sys.stderr)
        raise SystemExit(1)
