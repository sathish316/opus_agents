#!/usr/bin/env python3
"""List git commits as JSON, oldest-first by default.

Part of the code2spec skill: deterministic git traversal for
reverse-engineering OpenSpec specs from a repository's history.

Examples:
  list_commits.py --repo /path/to/repo
  list_commits.py --repo . --order newest-first --limit 20
  list_commits.py --repo . --no-merges --since 2024-01-01 --author alice
"""
import argparse
import json
import subprocess
import sys

RS = "\x1e"  # record separator between commits
FS = "\x1f"  # field separator within a commit


def run_git(repo, args):
    result = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"git error: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return result.stdout


def parse_files(block):
    files = []
    for line in block.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        status = parts[0]
        if status[:1] in ("R", "C") and len(parts) >= 3:
            files.append({"status": status[:1], "old_path": parts[1], "path": parts[2]})
        elif len(parts) >= 2:
            files.append({"status": status, "path": parts[1]})
    return files


def main():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--repo", required=True, help="path to the git repository")
    p.add_argument("--rev", default="HEAD", help="branch/rev to walk (default: HEAD)")
    p.add_argument("--order", choices=["oldest-first", "newest-first"], default="oldest-first")
    p.add_argument("--author", help="filter by author name/email pattern")
    p.add_argument("--since", help="only commits after this date (e.g. 2024-01-01)")
    p.add_argument("--until", help="only commits before this date")
    p.add_argument("--limit", type=int, help="max number of commits")
    p.add_argument("--no-merges", action="store_true", help="skip merge commits")
    p.add_argument("--path", help="only commits touching this path")
    p.add_argument("--no-files", action="store_true", help="omit per-commit file lists (faster)")
    args = p.parse_args()

    fmt = RS + FS.join(["%H", "%h", "%P", "%an", "%ae", "%aI", "%s", "%b"]) + FS
    git_args = ["log", args.rev, f"--pretty=format:{fmt}", "--date-order"]
    if not args.no_files:
        git_args.append("--name-status")
    if args.order == "oldest-first":
        git_args.append("--reverse")
    elif args.limit:
        # only safe to let git truncate when taking the newest commits;
        # for oldest-first the limit is applied after parsing instead
        git_args.append(f"--max-count={args.limit}")
    if args.author:
        git_args.append(f"--author={args.author}")
    if args.since:
        git_args.append(f"--since={args.since}")
    if args.until:
        git_args.append(f"--until={args.until}")
    if args.no_merges:
        git_args.append("--no-merges")
    if args.path:
        git_args.extend(["--", args.path])

    commits = []
    for record in run_git(args.repo, git_args).split(RS):
        if not record.strip():
            continue
        fields = record.split(FS)
        if len(fields) < 9:
            continue
        sha, short, parents, author, email, date, subject, body, files_block = fields[:9]
        commit = {
            "sha": sha,
            "short_sha": short,
            "parents": parents.split(),
            "is_merge": len(parents.split()) > 1,
            "author": author,
            "email": email,
            "date": date,
            "subject": subject,
            "body": body.strip(),
        }
        if not args.no_files:
            commit["files"] = parse_files(files_block)
        commits.append(commit)

    if args.limit:
        commits = commits[: args.limit]

    json.dump(commits, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
