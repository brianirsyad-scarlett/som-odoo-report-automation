# som-odoo-report-automation

Runs the full local Odoo report pipeline on GitHub Actions instead of
locally: pulls the current quarter's data from Odoo, rebuilds the quarter
report, rebuilds the all-time master report, and uploads everything to GCS.

Mirrors these three local scripts (copies live in this repo, with paths
adapted for GitHub's Linux runners instead of the local D: drive):

1. `odoo_quarterly_export.py` - pulls Sales Order + Sales Analysis from Odoo.
2. `build_odoo_report.py --replace-production` - rebuilds
   `<seq>. <year> Qn Odoo Report.xlsx` using the two files from step 1 plus
   `Master Data Customer Odoo.xlsx` and `Invoice Lumbung.xlsx` (downloaded
   from GCS first - see `download_from_gcs.py`).
3. `build_master_report.py --replace-production` - combines the current
   quarter's report with the 3 prior quarter/year reports (also downloaded
   from GCS) into the all-time `Odoo Report.xlsx`.

The local versions of these scripts and their source files are untouched and
still run as before - this is a parallel path, not a replacement, until it's
proven reliable.

## GCS layout this pipeline reads and writes

- `gs://bucket_som/sales_parquet/raw/primary/odoo/` - the four quarter/year
  Odoo Report files (3 prior ones seeded once, the current quarter's gets
  added/replaced by every run) plus this run's raw Sales Order/Sales
  Analysis exports and the combined `Odoo Report.xlsx`.
- `gs://bucket_som/sales_parquet/raw/master data/Master Data Customer Odoo.xlsx`
- `gs://bucket_som/sales_parquet/raw/primary/invoice/Invoice Lumbung.xlsx`

Note: `build_master_report.py`'s list of files to combine is a hardcoded
`SOURCE_FILES` list (matching the local script's behaviour) - each new
quarter, add a line to that list in this repo, same as the local script
needs updating.

## Setup

1. In this repo's Settings -> Secrets and variables -> Actions, add:
   - `ODOO_URL`
   - `ODOO_DB`
   - `ODOO_USERNAME`
   - `ODOO_PASSWORD`
   - `GCP_SA_KEY` - the full contents of the GCS service-account JSON key
     (the same one the local pipeline uses at
     `Data\Sent Email\sales-som datawarehouse 490008.json`)

   (Values are never committed to this repo - see `.env.example` for the
   format if running locally instead.)

2. Run the workflow manually: Actions tab -> "Odoo Quarterly Export" ->
   "Run workflow".

3. Outputs land in GCS as described above. They're also attached as the
   `odoo-quarterly-export` workflow artifact as a backup/manual-download
   option (30-day retention).

## Notes

- Trigger is manual (`workflow_dispatch`) only for now. Add a `schedule:`
  trigger to `.github/workflows/odoo-export.yml` once this has been
  verified to work reliably over a few runs.
- Requires Odoo to be reachable over the public internet from GitHub-hosted
  runners (confirmed OK for this instance).
