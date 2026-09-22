#!/usr/bin/env python3
"""Upload the freshly exported Odoo xlsx files to GCS."""
import glob
import os

from google.cloud import storage

BUCKET = "bucket_som"
PREFIX = "sales_parquet/raw/primary/odoo/"


def main():
    files = glob.glob("*.xlsx")
    if not files:
        raise SystemExit("No .xlsx files found to upload.")

    client = storage.Client()
    bucket = client.bucket(BUCKET)
    for path in files:
        dest = PREFIX + os.path.basename(path)
        bucket.blob(dest).upload_from_filename(path)
        print(f"Uploaded {path} -> gs://{BUCKET}/{dest}")


if __name__ == "__main__":
    main()
