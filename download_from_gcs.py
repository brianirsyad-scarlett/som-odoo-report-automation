#!/usr/bin/env python3
"""Download the reference/prior-quarter files build_odoo_report.py and
build_master_report.py need, into this directory, before running them.
"""
import os

from google.cloud import storage

BUCKET = "bucket_som"

FILES = [
    "sales_parquet/raw/master data/Master Data Customer Odoo.xlsx",
    "sales_parquet/raw/primary/invoice/Invoice Lumbung.xlsx",
    "sales_parquet/raw/primary/odoo/12. 2025 Odoo Report.xlsx",
    "sales_parquet/raw/primary/odoo/13. 2026 Q1 Odoo Report.xlsx",
    "sales_parquet/raw/primary/odoo/14. 2026 Q2 Odoo Report.xlsx",
]


def main():
    client = storage.Client()
    bucket = client.bucket(BUCKET)
    for source in FILES:
        dest = os.path.basename(source)
        blob = bucket.blob(source)
        if not blob.exists():
            raise SystemExit(f"Missing in GCS: gs://{BUCKET}/{source}")
        blob.download_to_filename(dest)
        print(f"Downloaded gs://{BUCKET}/{source} -> {dest}")


if __name__ == "__main__":
    main()
