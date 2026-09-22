# som-odoo-report-automation

Trial: runs `odoo_quarterly_export.py` on GitHub Actions instead of locally.
Pulls the current quarter's Sales Order and Sales Analysis exports directly
from Odoo's API and uploads them as workflow artifacts.

This is step 1 of the local Odoo report pipeline only. The two build steps
(`build_odoo_report.py`, `build_master_report.py`) are not included yet -
they depend on local reference files (Master Data Customer Odoo.xlsx,
Invoice Lumbung.xlsx, prior quarter reports) that aren't in this repo.

## Setup

1. In this repo's Settings -> Secrets and variables -> Actions, add:
   - `ODOO_URL`
   - `ODOO_DB`
   - `ODOO_USERNAME`
   - `ODOO_PASSWORD`

   (Values are never committed to this repo - see `.env.example` for the
   format if running locally instead.)

2. Run the workflow manually: Actions tab -> "Odoo Quarterly Export" ->
   "Run workflow".

3. Download the `odoo-quarterly-export` artifact from the completed run to
   get the two `.xlsx` files.

## Notes

- Trigger is manual (`workflow_dispatch`) only for now. Add a `schedule:`
  trigger to `.github/workflows/odoo-export.yml` once this has been
  verified to work end-to-end.
- Requires Odoo to be reachable over the public internet from GitHub-hosted
  runners (confirmed OK for this instance).
