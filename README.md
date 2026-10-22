# Folder to Apps Script Dashboard

A Codex skill for turning a local folder's tabular data into a Google Sheets and Apps Script dashboard with a live, reconciled deployment URL.

The workflow scans local dependencies and data, guides missing inputs, builds a data contract, deploys with explicit refresh behavior, and verifies the `/exec` page against the folder. It does not contain a user's datasets, credentials, or project IDs.

Install by copying this directory to `~/.codex/skills/folder-to-apps-script-dashboard`. Invoke it as `$folder-to-apps-script-dashboard` with a project folder and the target Apps Script editor URL. The skill can also be selected automatically for a matching dashboard task.

Run the local preflight:

```bash
python3 scripts/scan_environment.py --folder /path/to/project --script-id 'https://script.google.com/.../projects/SCRIPT_ID/edit' --spreadsheet-id 'https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit'
```

The scanner uses Python's standard library. It reports file hashes, CSV/TSV/JSON structure, installed tools, and next actions without displaying credentials. It also returns install and authorization handoff steps, including when a user must personally complete Google's unverified-app warning. Remote authorization, deployment access, and live data agreement still require the skill's verification steps.

Licensed under MIT.
