#!/usr/bin/env python3
"""scan_claims.py
Lightweight scanner for absolutist/marketing language across a workspace.
Saves a JSON report with per-file matches and summary counts.
"""
import argparse
import json
import re
from pathlib import Path
from collections import defaultdict

DEFAULT_KEYWORDS = [
    "revolutionary",
    "production-ready",
    "breakthrough",
    "dramatic improvement",
    "game-changer",
    "unprecedented",
    "best-in-class",
    "world-class",
    "novel",
    "guaranteed",
    "proven",
    "solved problem",
    "industry-leading",
    "state-of-the-art",
    "cutting-edge",
    "miracle",
    "instant",
    "significant improvement",
    "dramatic",
    "remarkable",
    "superior",
    "outperform",
    "outperforms",
    "eliminates",
    "no need",
    "always",
    "never",
    "100%",
    "zero-risk",
    "fail-proof",
    "safe",
    "scalable to production",
    "ready for deployment",
    "commercial-grade",
    "game changer",
    "break-through"
]

FILE_EXTS = [".md", ".markdown", ".tex", ".rst", ".txt", ".yml", ".yaml", ".json", ".mdown", ".py"]

def compile_patterns(keywords):
    patterns = []
    for kw in keywords:
        # create a case-insensitive regex; match as whole phrase or word
        esc = re.escape(kw)
        pat = re.compile(r"\b" + esc + r"\b", re.IGNORECASE)
        patterns.append((kw, pat))
    return patterns


def scan(root: Path, patterns, exts, skip_dirs=None):
    results = {}
    summary = defaultdict(int)
    files_scanned = 0
    skip_dirs = set(skip_dirs or [".git", "node_modules", "venv", ".venv"])

    for p in root.rglob("*"):
        if any(part in skip_dirs for part in p.parts):
            continue
        if not p.is_file():
            continue
        if p.suffix.lower() not in exts:
            continue
        files_scanned += 1
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        lines = text.splitlines()
        file_matches = []
        for i, line in enumerate(lines, start=1):
            for kw, pat in patterns:
                if pat.search(line):
                    snippet = line.strip()
                    file_matches.append({"keyword": kw, "line": i, "snippet": snippet})
                    summary[kw] += 1
        if file_matches:
            results[str(p)] = file_matches
    return {
        "files_scanned": files_scanned,
        "flagged_files": len(results),
        "keyword_counts": dict(summary),
        "matches": results,
    }


def main():
    ap = argparse.ArgumentParser(description="Scan workspace for flagged marketing/absolutist claims.")
    ap.add_argument("--root", default=".", help="Root path to scan")
    ap.add_argument("--report", default="claims_report.json", help="Path to write JSON report")
    ap.add_argument("--keywords", nargs="*", help="Override keywords (space-separated)")
    ap.add_argument("--extensions", nargs="*", help="File extensions to scan (e.g. .md .tex)")
    ap.add_argument("--fail-on-flag", action="store_true", help="Exit with code 2 if any flags are found")
    args = ap.parse_args()

    root = Path(args.root).expanduser().resolve()
    if args.keywords:
        keywords = args.keywords
    else:
        keywords = DEFAULT_KEYWORDS
    exts = [e.lower() for e in (args.extensions or FILE_EXTS)]

    patterns = compile_patterns(keywords)
    report = scan(root, patterns, exts)

    out_path = Path(args.report)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"Scanned {report['files_scanned']} files; flagged {report['flagged_files']} files")
    if report['flagged_files'] > 0:
        top = sorted(report['keyword_counts'].items(), key=lambda kv: -kv[1])[:10]
        print("Top keywords:")
        for k,c in top:
            print(f"  {k}: {c}")

    if args.fail_on_flag and report['flagged_files']>0:
        print("Flags found; exiting non-zero due to --fail-on-flag")
        raise SystemExit(2)

if __name__ == '__main__':
    main()
