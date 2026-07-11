#!/usr/bin/env python3
"""Show the diff of a change unit as JSON.

Accepts either a single commit or a base/head pair (as produced by
group_commits.py). Modes:

  files  changed paths with status letters (A/M/D/R/C)
  stat   files plus per-file and total insertions/deletions (default)
  patch  stat plus the unified diff text, truncated at --max-patch-chars

Examples:
  show_change.py --repo . --commit abc1234
  show_change.py --repo . --base abc1234 --head def5678 --mode patch
"""
import argparse
import json
import subprocess
import sys

EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"  # git's empty tree object


def run_git(repo, args):
    result = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"git error: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return result.stdout


def name_status(repo, base, head):
    files, by_path = [], {}
    for line in run_git(repo, ["diff", "--name-status", "-M", base, head]).splitlines():
        parts = line.split("\t")
        status = parts[0]
        if status[:1] in ("R", "C") and len(parts) >= 3:
            entry = {"status": status[:1], "old_path": parts[1], "path": parts[2]}
        elif len(parts) >= 2:
            entry = {"status": status, "path": parts[1]}
        else:
            continue
        files.append(entry)
        by_path[entry["path"]] = entry
    return files, by_path


def add_numstat(repo, base, head, by_path):
    total_ins = total_del = 0
    for line in run_git(repo, ["diff", "--numstat", base, head]).splitlines():
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        ins, dels, path = parts[0], parts[1], parts[2]
        if ins == "-" or dels == "-":  # binary file
            continue
        total_ins += int(ins)
        total_del += int(dels)
        if path in by_path:
            by_path[path]["insertions"] = int(ins)
            by_path[path]["deletions"] = int(dels)
    return total_ins, total_del


def main():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--repo", required=True, help="path to the git repository")
    p.add_argument("--commit", help="single commit (diffed against its first parent)")
    p.add_argument("--base", help="base rev of the unit (exclusive)")
    p.add_argument("--head", help="head rev of the unit (inclusive)")
    p.add_argument("--mode", choices=["files", "stat", "patch"], default="stat")
    p.add_argument("--max-patch-chars", type=int, default=40000)
    args = p.parse_args()

    if args.commit:
        head = args.commit
        r = subprocess.run(
            ["git", "-C", args.repo, "rev-parse", "--verify", "--quiet", f"{args.commit}^"],
            capture_output=True,
            text=True,
        )
        base = r.stdout.strip() if r.returncode == 0 else EMPTY_TREE
    elif args.base and args.head:
        base, head = args.base, args.head
    else:
        p.error("provide either --commit or both --base and --head")

    files, by_path = name_status(args.repo, base, head)
    result = {"base": base, "head": head, "files_changed": len(files), "files": files}

    if args.mode in ("stat", "patch"):
        total_ins, total_del = add_numstat(args.repo, base, head, by_path)
        result["total_insertions"] = total_ins
        result["total_deletions"] = total_del

    if args.mode == "patch":
        patch = run_git(args.repo, ["diff", "-M", base, head])
        result["patch_truncated"] = len(patch) > args.max_patch_chars
        result["patch"] = patch[: args.max_patch_chars]

    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
