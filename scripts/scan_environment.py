#!/usr/bin/env python3
"""Local, credential-safe preflight for a folder-to-Apps-Script dashboard."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

SKIP = {".git", "node_modules", ".tooling", "remote-backup", "evidence", "skill-release", "__pycache__"}
TABULAR = {".csv", ".tsv", ".json", ".xlsx", ".xls", ".ods"}
CONFIG_NAMES = {"appsscript.json", "package.json", "package-lock.json", "tsconfig.json", ".clasp.json"}


def version(command):
    if not command:
        return None
    try:
        result = subprocess.run([str(command), "--version"], capture_output=True, text=True, timeout=5)
        return (result.stdout or result.stderr).strip().splitlines()[0][:100] if result.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired, IndexError):
        return None


def auth_status():
    gh = shutil.which("gh")
    if not gh:
        return None
    try:
        return subprocess.run([gh, "auth", "status"], capture_output=True, timeout=8).returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def script_id(value):
    if not value:
        return None
    match = re.search(r"/projects/([^/]+)/edit", value)
    token = match.group(1) if match else value.strip()
    return token if re.fullmatch(r"[A-Za-z0-9_-]{20,}", token) and not token.startswith("AKfy") else None


def sheet_id(value):
    if not value:
        return None
    match = re.search(r"/spreadsheets/d/([^/]+)", value)
    token = match.group(1) if match else value.strip()
    return token if re.fullmatch(r"[A-Za-z0-9_-]{20,}", token) else None


def inspect_file(path, root):
    info = {"path": str(path.relative_to(root)), "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    try:
        if path.suffix.lower() in (".csv", ".tsv"):
            with path.open(encoding="utf-8-sig", newline="") as handle:
                reader = csv.reader(handle, delimiter="\t" if path.suffix.lower() == ".tsv" else ",")
                info["headers"] = next(reader, [])
                info["data_rows"] = sum(any(cell.strip() for cell in row) for row in reader)
        elif path.suffix.lower() == ".json":
            with path.open(encoding="utf-8-sig") as handle:
                data = json.load(handle)
            info["json_type"] = type(data).__name__
            if isinstance(data, list):
                info["data_rows"] = len(data)
                info["headers"] = list(data[0]) if data and isinstance(data[0], dict) else []
            elif isinstance(data, dict):
                info["top_level_keys"] = list(data)[:30]
        else:
            info["needs_parser"] = True
    except (UnicodeError, csv.Error, ValueError, OSError) as exc:
        info["error"] = type(exc).__name__ + ": " + str(exc)[:160]
    return info


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--folder", required=True)
    parser.add_argument("--script-id", default="")
    parser.add_argument("--spreadsheet-id", default="")
    parser.add_argument("--publish-github", action="store_true")
    args = parser.parse_args()
    root = Path(args.folder).expanduser().resolve()
    if not root.is_dir():
        parser.error("folder does not exist")
    local_clasp = root / ".tooling/node_modules/.bin/clasp"
    clasp = shutil.which("clasp") or (str(local_clasp) if local_clasp.exists() else None)
    paths = sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in TABULAR
                   and p.name not in CONFIG_NAMES
                   and not any(part in SKIP or part.startswith(".") for part in p.relative_to(root).parts[:-1]))
    files = [inspect_file(p, root) for p in paths]
    sid, shid = script_id(args.script_id), sheet_id(args.spreadsheet_id)
    checks = {
        "python": version(shutil.which("python3")), "node": version(shutil.which("node")),
        "npm": version(shutil.which("npm")), "clasp": version(clasp),
        "git": version(shutil.which("git")), "gh": version(shutil.which("gh")),
        "gh_authenticated": auth_status() if args.publish_github else None,
        "clasp_credentials_present": (Path.home() / ".clasprc.json").is_file(),
        "script_id": sid, "spreadsheet_id": shid,
    }
    missing = []
    if not files:
        missing.append("No supported tabular files found; identify source files or add an appropriate parser.")
    if not sid:
        missing.append("Provide the Apps Script editor URL or its Script ID (not an AKfy deployment ID).")
    if not shid:
        missing.append("Provide a Google Sheets URL/ID or authorize creation of a new destination spreadsheet.")
    if not clasp:
        missing.append("Install Clasp with npm, or use a supported Apps Script connector/UI route.")
    if clasp and (not checks["node"] or not checks["npm"]):
        missing.append("Install Node.js and npm to run Clasp, or use a supported connector/UI route.")
    if clasp and not checks["clasp_credentials_present"]:
        missing.append("Run clasp login for the intended Google account; do not copy credentials into the project.")
    if args.publish_github and not checks["gh"]:
        missing.append("Install GitHub CLI or use an authenticated GitHub connector before publication.")
    elif args.publish_github and checks["gh_authenticated"] is False:
        missing.append("GitHub CLI is installed but not authenticated; run gh auth login or use an authenticated GitHub connector.")
    if any(f.get("needs_parser") for f in files):
        missing.append("Install a parser or convert each XLS/XLSX/ODS source before using its values.")
    output = {"folder": str(root), "checks": checks, "files": files, "missing_or_next_actions": missing,
              "remote_checks_still_required": ["Google account and Script API access", "target Script edit permission",
                                               "spreadsheet edit permission", "deployment viewer access", "OAuth scope grant"]}
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
