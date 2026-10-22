# Intake and dependency guidance

The local scanner reports observations, not a deployment authorization. Resolve each missing item with a concrete action:

| Item | Why needed | Guidance |
| --- | --- | --- |
| Project folder and authoritative files | Prevent accidental use of examples, backups, or append-only tests | Ask which files are production sources; identify formats, headers, counts, and update cadence. |
| Apps Script ID | Determines the code being changed | Use the ID between `/projects/` and `/edit` in the Apps Script editor URL. A value beginning `AKfy...` is generally a deployment ID, so request the editor URL. |
| Spreadsheet | Determines editable source and generated output | Ask for the Sheets URL or create a new sheet if the task permits it; verify edit permission. Never infer the sheet from an unrelated prior project. |
| Metric contract | Prevent misleading aggregation | Ask what counts, units, date window, status filters, missing-data semantics, and denominator each KPI uses when source labels are ambiguous. |
| Update path | Determines what “dynamic” means | Sheet edits: installable edit/change triggers. API imports or formula recalculation: scheduled content check. Folder edits: separate sync/watch process or explicit re-import, with conflict policy. State actual latency and failures. |
| Timezone and audience | Determines dates and deployment permissions | Use a confirmed timezone; select web-app execution identity and viewer scope deliberately. |
| Google access | Enables push, initialization, deployment, and viewing | Check Clasp login and Script API access without displaying credentials; run the project and complete Google OAuth only for required scopes. Verify the viewer can open `/exec`. |

Scan formats intentionally. CSV and JSON can be inspected with Python standard library; XLSX/ODS/PDF need a suitable parser or conversion. Do not silently skip an authoritative format. Node/npm and Clasp are needed for the Clasp route; supported connectors/UI can replace Clasp. Git and GitHub authentication matter only if repository publication was requested. Report install/login steps appropriate to the current OS when absent rather than assuming the user has them.

Before remote changes, preserve a local backup of the current Script and check whether a deployment already exists. Identify whether source sheets are populated; never reseed over user data. Keep credentials, `.clasprc.json`, local datasets, rendered private screenshots, and case-specific IDs out of any public skill repo.
