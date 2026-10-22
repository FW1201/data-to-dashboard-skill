---
name: data-to-dashboard-skill
description: Turn a local folder's tabular data into a verified, updating Google Sheets and Apps Script dashboard. Use when a user needs a data dashboard deployed and reconciled with its source files.
---

# Data to Dashboard Skill

Produce a dashboard whose live numbers can be traced to the user's folder. Treat the folder, target Script ID, spreadsheet, deployment, and refresh path as separate identities. Never infer a Script ID from a web-app deployment ID or silently reuse an old spreadsheet.

## 1. Inspect and guide

Run `python3 scripts/scan_environment.py --folder <folder> [--script-id <id-or-editor-url>] [--spreadsheet-id <id-or-url>]`. Read its findings, then inspect the actual data and project instructions. The scan is a local preflight, not proof of remote authorization. It returns user-run installation and access guidance as well as Node/npm, Clasp or another supported Apps Script route, Google login status without printing tokens, data file formats, row counts, headers, and optional Git/gh if publication was requested. Do not install software, log in, or grant scopes solely because the scan recommends it: present the exact missing item, why it is needed, and the supplied next step. Check Google Script API, permission to edit the target project and spreadsheet, and deploy access remotely before mutation.

Give the user a short **ready / missing / action** checklist. Ask only for facts that cannot be established from the folder or accessible services: which source files/tables are authoritative, target Script URL or ID, spreadsheet destination or permission to create one, metric definitions and units when ambiguous, update mechanism, timezone, and intended web-app audience. Explain how to find each missing ID and what decision it controls; never substitute an unrelated ID. Continue independent work while awaiting a required answer. See [intake and dependency guide](references/intake.md).

## 2. Establish a data contract

Inventory the source tables and file provenance. Map IDs, dates, entity/project keys, amounts, statuses, units, and relationships. Calculate local reference counts and at least one independent total or sample for each key metric. Record missing/duplicate/invalid rows and whether absent data means zero, unknown, or incomplete. Use an explicit timezone and date format. Design filters and visuals around the user's actual decision needs; do not hardcode names, categories, or measures from a previous project. Keep source data private and out of reusable skill files or public repositories.

## 3. Build and deploy

Confirm the target Script ID against the editor URL, read and back up existing remote code, and inspect deployments before pushing. Generate or adapt Apps Script server code and HTML plus a sheet data view. Source tables should have stable headers and IDs; aggregation should be testable locally. Make setup idempotent: preserve populated source sheets, own only named generated sheets/triggers, and avoid overwriting unrelated project assets. Data validation failures must surface clearly while preserving the last successful dashboard. Make refresh behavior explicit: sheet edits can use installable triggers; external imports/formulas need an appropriate scheduled check; the web page should read current server data or refresh on a stated interval. Local folder edits do **not** reach Google automatically unless a separate sync/watch job is actually installed and verified.

Run local tests against the source-derived reference values. Push only to the verified Script ID, run initialization with the necessary Google authorization, and deploy/update a web app with the agreed audience. If Google displays an unverified-app warning, hand the browser step to the user after they review the project and requested scopes; never automate a bypass. If scopes, identity, or access are uncertain, report the exact boundary and resolve it before changing remote assets. See [deployment and acceptance](references/deployment.md).

## 4. Verify the live result

Read back remote code/version, source sheet headers and row counts, generated sheet/charts, and installed refresh triggers. Open the **deployed `/exec` URL** as the intended viewer; wait for data, inspect visible cards, charts, filters, errors, and links. Compare visible figures and remote sheet values to local independent reference counts/totals for the same period/filter. For a reversible source edit, record the tab, A1 target, stable row key, original value, and expected delta before writing. Prefer a precise API/range update over free-form UI typing; restore the exact value, force or await the relevant refresh, then reconcile the authoritative source tables again. An API write may not fire an Apps Script edit trigger, so run the scheduled refresh or rebuild when needed. A loaded page or successful push alone is insufficient. If access prevents opening the URL, state what remains unverified and do not call deployment complete.

Only after these checks pass, provide the dashboard URL, spreadsheet URL, tested Script ID, refresh semantics, key reconciliation evidence, and remaining limitations. If public GitHub publication was requested, publish **only the generic skill package** after the live trial passes; check its allowlist for source data, hardcoded IDs, tokens, and personal paths before pushing.
