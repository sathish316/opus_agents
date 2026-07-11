#!/usr/bin/env python3
"""Group git commits into change units as JSON, oldest-first.

A change unit is the granularity at which code2spec understands history
and updates specs. Strategies:

  pr      one unit per merged PR (merge commits on the first-parent line);
          direct or squash-merged commits become single-commit units
  window  consecutive commits by the same author within --window-hours
          collapse into one unit (for repos without PR history)
  author  one unit per author across the whole range (attribution lens)

Each unit carries base/head revs so its combined diff can be fetched with
show_change.py. For window units on non-linear history the base..head diff
is an approximation; author units have no meaningful base/head (diff their
commits individually).

Examples:
  group_commits.py --repo . --strategy pr
  group_commits.py --repo . --strategy window --window-hours 24
  group_commits.py --repo . --strategy author --since 2024-01-01
"""
import argparse
import json
import re
import subprocess
import sys
from datetime import datetime

FS = "\x1f"
EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"  # git's empty tree object
PR_NUMBER_RE = re.compile(r"#(\d+)")
MERGE_PR_RE = re.compile(r"^Merge pull request #\d+ from \S+\s*")


def run_git(repo, args):
    result = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"git error: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return result.stdout


def log_commits(repo, rev, extra=None):
    fmt = FS.join(["%H", "%P", "%an", "%ae", "%aI", "%s"])
    out = run_git(
        repo, ["log", rev, f"--pretty=format:{fmt}", "--date-order", "--reverse", *(extra or [])]
    )
    commits = []
    for line in out.splitlines():
        if FS not in line:
            continue
        sha, parents, author, email, date, subject = line.split(FS, 5)
        commits.append(
            {
                "sha": sha,
                "parents": parents.split(),
                "author": author,
                "email": email,
                "date": date,
                "subject": subject,
            }
        )
    return commits


def slugify(text, max_len=40):
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:max_len].rstrip("-") or "change"


def base_of(commit):
    return commit["parents"][0] if commit["parents"] else EMPTY_TREE


def make_unit(index, strategy, title, commits, base, head, pr_number=None):
    return {
        "id": f"unit-{index:04d}-{slugify(title)}",
        "strategy": strategy,
        "title": title,
        "pr_number": pr_number,
        "authors": sorted({c["author"] for c in commits}),
        "start_date": commits[0]["date"],
        "end_date": commits[-1]["date"],
        "commit_count": len(commits),
        "base": base,
        "head": head,
        "commits": [
            {"sha": c["sha"], "subject": c["subject"], "author": c["author"], "date": c["date"]}
            for c in commits
        ],
    }


def group_pr(repo, rev, filters):
    units = []
    for i, c in enumerate(log_commits(repo, rev, ["--first-parent", *filters]), 1):
        m = PR_NUMBER_RE.search(c["subject"])
        pr_number = int(m.group(1)) if m else None
        if len(c["parents"]) > 1:
            members = log_commits(repo, f"{c['parents'][0]}..{c['parents'][1]}") or [c]
            title = MERGE_PR_RE.sub("", c["subject"]).strip() or c["subject"]
            units.append(make_unit(i, "pr", title, members, c["parents"][0], c["sha"], pr_number))
        else:
            units.append(make_unit(i, "pr", c["subject"], [c], base_of(c), c["sha"], pr_number))
    return units


def group_window(repo, rev, filters, window_hours):
    groups = []
    for c in log_commits(repo, rev, ["--no-merges", *filters]):
        ts = datetime.fromisoformat(c["date"])
        if groups:
            last = groups[-1]
            same_author = c["author"] == last["commits"][-1]["author"]
            gap_ok = (ts - last["last_ts"]).total_seconds() <= window_hours * 3600
            if same_author and gap_ok:
                last["commits"].append(c)
                last["last_ts"] = ts
                continue
        groups.append({"commits": [c], "last_ts": ts})
    return [
        make_unit(
            i,
            "window",
            g["commits"][0]["subject"],
            g["commits"],
            base_of(g["commits"][0]),
            g["commits"][-1]["sha"],
        )
        for i, g in enumerate(groups, 1)
    ]


def group_author(repo, rev, filters):
    by_author = {}
    for c in log_commits(repo, rev, ["--no-merges", *filters]):
        by_author.setdefault(c["author"], []).append(c)
    ordered = sorted(by_author.items(), key=lambda kv: kv[1][0]["date"])
    return [
        make_unit(i, "author", f"work by {author}", commits, None, None)
        for i, (author, commits) in enumerate(ordered, 1)
    ]


def main():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--repo", required=True, help="path to the git repository")
    p.add_argument("--strategy", required=True, choices=["pr", "window", "author"])
    p.add_argument("--rev", default="HEAD", help="branch/rev to walk (default: HEAD)")
    p.add_argument("--since", help="only commits after this date")
    p.add_argument("--until", help="only commits before this date")
    p.add_argument("--window-hours", type=float, default=24.0, help="gap for window strategy")
    p.add_argument("--limit", type=int, help="max number of units (from the oldest)")
    args = p.parse_args()

    filters = []
    if args.since:
        filters.append(f"--since={args.since}")
    if args.until:
        filters.append(f"--until={args.until}")

    if args.strategy == "pr":
        units = group_pr(args.repo, args.rev, filters)
    elif args.strategy == "window":
        units = group_window(args.repo, args.rev, filters, args.window_hours)
    else:
        units = group_author(args.repo, args.rev, filters)

    if args.limit:
        units = units[: args.limit]

    json.dump(units, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
