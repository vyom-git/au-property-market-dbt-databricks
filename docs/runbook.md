# Project Runbook

This runbook explains how to run the Australian Property Market Analytics Pipeline from local development through Databricks and dbt.

## 1. Activate local environment

From the project root:

```bash
cd ~/Downloads/au-property-market-dbt-databricks
source .venv/bin/activate
```

## 2. Confirm dbt connection

```bash
dbt debug
```

Expected result:

```text
All checks passed!
```

## 3. Upload raw data to S3

Upload the local NSW property sales CSV to the S3 landing bucket:

```bash
aws s3 cp data/raw/nsw_property_sales.csv s3://au-property-market-landing-313589910075-ap-southeast-2-an/raw/nsw_property_sales/nsw_property_sales.csv
```

Verify the upload:

```bash
aws s3 ls s3://au-property-market-landing-313589910075-ap-southeast-2-an/raw/nsw_property_sales/
```

## 4. Run Databricks ingestion

Run the Databricks Auto Loader notebook:

```text
databricks/notebooks/load_raw_property_sales_autoloader.py
```

This reads raw CSV files from S3 and loads them into:

```text
workspace.property_analytics_bronze.raw_property_sales
```

The notebook uses:

- Databricks Secrets for AWS credentials
- Auto Loader schema tracking
- Auto Loader checkpointing
- CSV quote and escape handling
- controlled column mapping from raw CSV names to clean bronze names

## 5. Validate bronze table

In Databricks SQL Editor, run:

```sql
select *
from workspace.property_analytics_bronze.raw_property_sales
limit 10;
```

To check for malformed purchase prices:

```sql
select *
from workspace.property_analytics_bronze.raw_property_sales
where try_cast(purchase_price as double) is null
  and purchase_price is not null
limit 20;
```

Expected result:

```text
No rows returned
```

## 6. Build dbt models

From the project root, run:

```bash
dbt build
```

This builds and tests the full dbt pipeline:

```text
stg_property_sales
        ↓
int_clean_property_sales
        ↓
fct_property_sales
        ↓
agg_monthly_suburb_prices
agg_property_type_performance
```

## 7. Generate dbt docs

```bash
dbt docs generate
dbt docs serve
```

Open the local docs URL shown in the terminal, usually:

```text
http://localhost:8080
```

Use the docs site to inspect:

- model descriptions
- column descriptions
- dbt tests
- source-to-mart lineage

## Main tables

- `workspace.property_analytics_bronze.raw_property_sales`
- `property_analytics_staging.stg_property_sales`
- `property_analytics_intermediate.int_clean_property_sales`
- `property_analytics_marts.fct_property_sales`
- `property_analytics_marts.agg_monthly_suburb_prices`
- `property_analytics_marts.agg_property_type_performance`

## Common checks

### Run only staging

```bash
dbt run --select stg_property_sales
dbt test --select stg_property_sales
```

### Run only intermediate

```bash
dbt run --select int_clean_property_sales
dbt test --select int_clean_property_sales
```

### Run only marts

```bash
dbt build --select models/marts
```

## Notes

Do not commit local secrets, raw data files, dbt `target/` artifacts or Databricks/AWS credentials.

Secrets should be stored in:

- local environment variables for local dbt development
- Databricks Secrets for Databricks notebook/job execution
