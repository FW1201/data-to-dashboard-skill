# Data to Dashboard Skill

`data-to-dashboard-skill` turns tabular files in a local folder into a Google Sheets and Google Apps Script dashboard. It starts with a dependency and data scan, guides any missing installation or access step, then verifies the published `/exec` dashboard against the original folder.

It is designed for projects that need a traceable path from CSV, TSV, JSON, XLSX, XLS, or ODS source data to a live dashboard. The reusable package contains no user datasets, credentials, screenshots, spreadsheet IDs, Script IDs, or deployment URLs.

## What the skill does

1. Scans the folder for source files, hashes, headers, and row counts.
2. Checks the local route: Python, Node.js, npm, Clasp, Git, and GitHub CLI when publication is requested.
3. Produces a **ready / missing / action** guide, with commands or official download pages only for missing items.
4. Builds an explicit data contract before designing measures, filters, sheets, and visuals.
5. Safely syncs to the confirmed Apps Script project, initializes sheets and refresh triggers, and deploys a web app.
6. Opens the final `/exec` URL and reconciles visible dashboard values, remote source sheets, and local reference data.
7. Performs a reversible update test, restores the original data, and verifies that all source tables still match the local folder.

## Prerequisites

The skill itself needs Python 3. It uses only the Python standard library for its preflight scan.

For the Clasp workflow, install these tools on the computer that holds the data folder:

| Tool | Used for | How the skill handles it |
| --- | --- | --- |
| Node.js LTS and npm | Running Clasp | Detects absence and directs the user to [nodejs.org](https://nodejs.org/) or an approved package manager. |
| `@google/clasp` | Reading and pushing Apps Script files | Detects absence and offers `npm install --global @google/clasp`. |
| Google account access | Editing the supplied Apps Script project and spreadsheet | Guides the user through `clasp login` and project-specific OAuth consent. |
| Git and GitHub CLI | Optional public skill publication | Checked only when publication is requested; an authenticated GitHub connector is also supported. |

Google Apps Script editor access, spreadsheet edit access, and deployment access cannot be proven by a local scan. The skill checks them remotely before it changes code or data.

## Install

### Option A: Clone from GitHub

Clone the repository directly into the Codex skills folder:

```bash
git clone https://github.com/FW1201/data-to-dashboard-skill.git \
  ~/.codex/skills/data-to-dashboard-skill
```

If the repository is still available under an earlier URL, GitHub's redirect is safe to follow; use the canonical URL shown above for new installations.

### Option B: Install from a downloaded folder

Copy the complete folder, including `SKILL.md`, `scripts/`, `references/`, and `agents/`, into:

```text
~/.codex/skills/data-to-dashboard-skill/
```

The finished layout must look like this:

```text
~/.codex/skills/data-to-dashboard-skill/
├── SKILL.md
├── README.md
├── agents/openai.yaml
├── references/
└── scripts/scan_environment.py
```

### Validate the installation

Run the bundled validator available with Codex:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  ~/.codex/skills/data-to-dashboard-skill
```

Expected result:

```text
Skill is valid!
```

Restart or refresh the Codex skills list if the new name does not appear immediately. Invoke it with `$data-to-dashboard-skill`, or let Codex select it for a matching data-to-dashboard request.

## First-run guide

Start with the source folder and, when known, the Apps Script editor and Sheets URLs:

```bash
python3 ~/.codex/skills/data-to-dashboard-skill/scripts/scan_environment.py \
  --folder /path/to/project \
  --script-id 'https://script.google.com/u/0/home/projects/SCRIPT_ID/edit' \
  --spreadsheet-id 'https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit'
```

Add `--publish-github` only when you plan to publish the generic skill package. It checks GitHub tooling without exposing credentials.

The result is JSON. Read these sections in order:

| Output field | Meaning | What to do |
| --- | --- | --- |
| `files` | Detected tabular files, hashes, headers, and row counts | Identify which files are authoritative and which are samples, archives, or test data. |
| `missing_or_next_actions` | Required missing information or tooling | Resolve each item before deploying. Do not substitute a deployment ID for a Script ID. |
| `installation_and_access_guidance` | User-run installation, login, and consent actions | Complete only the relevant action, then rerun the scan or remote check. |
| `remote_checks_still_required` | Access checks that cannot happen locally | Confirm them in the selected Google account before push, initialization, or deployment. |

## Installation and access guide

The scanner gives context-specific steps. This is the expected sequence when the Clasp route is selected:

1. **Node.js/npm missing:** install current Node.js LTS from [nodejs.org](https://nodejs.org/) or the organization's approved package manager. Rerun the scanner.
2. **Clasp missing:** run `npm install --global @google/clasp`. Rerun the scanner and confirm it reports a version.
3. **Clasp credentials missing:** run `clasp login`. Choose the Google account that can edit the target Apps Script project and target spreadsheet. Do not copy `.clasprc.json` into the project folder or repository.
4. **Apps Script or Sheet ID missing:** provide the Apps Script editor URL (the ID is between `/projects/` and `/edit`) and the Google Sheets URL (the ID is after `/d/`). An `AKfy...` value is a web-app deployment ID, not a Script ID.
5. **Google consent required:** review the exact requested scopes. The usual operations are reading/writing the selected spreadsheet, running setup, installing named refresh triggers, and serving the web app.
6. **Google unverified-app warning:** the user must personally inspect the project name, account, and scopes in the browser, then complete Google's warning and Allow steps. The skill does not bypass this browser security step.
7. **GitHub publishing requested:** install GitHub CLI from [cli.github.com](https://cli.github.com/) and run `gh auth login`, or use an authenticated GitHub connector. Publish only generic skill files after the live dashboard trial has passed.

After every setup step, rerun the relevant scan or remote read. A command having been entered is not enough; the tool, intended account, and selected remote asset must be verifiably accessible.

## Dashboard workflow

The implementation workflow has four gates:

1. **Understand the data.** Confirm authoritative source files; map unique IDs, date fields, categories/projects, measures, statuses, units, missing-value semantics, timezone, and update cadence. Derive local reference totals before touching Google assets.
2. **Build safely.** Confirm the target Script ID from the editor URL; back up remote code; preserve populated source sheets; keep generated sheets and named triggers idempotent; then implement aggregation, spreadsheet view, dashboard, and the agreed refresh path.
3. **Deploy deliberately.** Run setup after consent, inspect the execution log, create or update a web-app deployment with the intended audience, and use the deployed `/exec` URL as the acceptance target. A `/dev` URL is not the deliverable.
4. **Verify end-to-end.** Compare local reference values, remote sheet values, generated charts, and visible page values for default and alternate filters. Make a controlled temporary source change, observe its exact effect, restore it, refresh or rebuild as needed, then compare all authoritative source tables to the original local data again.

Local folder edits do not automatically appear in Google. The skill makes the selected refresh mechanism explicit: sheet edits can trigger an update; external imports and formula changes need scheduled content checks; local-file synchronization needs a separately designed sync/watch job.

## Safe update-test protocol

Before any live test edit, record all of the following:

- source sheet tab and exact A1 range;
- a stable row key proving which record is being changed;
- original and temporary values;
- expected change in the dashboard metric; and
- exact restoration value.

Prefer a precise range or connector update over free-form spreadsheet UI typing. UI focus can change after a tab switch, which risks overwriting an unrelated cell. Some API updates do not invoke Apps Script `onEdit`; use the scheduled refresh or a rebuild function before deciding that the web dashboard failed to update. Finish every test by restoring the original value and reconciling remote source tables against local data.

## Output you should receive

After a successful run, the skill provides:

- the deployed `/exec` dashboard URL;
- the source spreadsheet URL and verified Apps Script ID;
- refresh interval and trigger behavior;
- local-to-remote reconciliation counts and key totals;
- the results of the reversible update-and-restore test; and
- any remaining limitation, such as restricted viewer access or an unverified external import path.

## Privacy and publication

Keep user datasets, credentials, `.clasprc.json`, screenshots, logs, personal paths, Sheet IDs, Script IDs, and deployment IDs out of public repositories. When publication is requested, publish only the generic skill files: `SKILL.md`, `README.md`, `agents/`, `references/`, scripts, and an appropriate license.

Licensed under MIT.
