

# Project Summary

## Short Pitch

Built an end-to-end Australian property market analytics pipeline using AWS S3, Databricks Auto Loader, Delta Lake and dbt.

The project ingests NSW property sales CSV data from S3, loads it into a Databricks bronze Delta table, and transforms it through dbt staging, intermediate and mart layers for suburb and property-type market analysis.

## Architecture

```text
NSW property sales CSV
        ↓
AWS S3 landing bucket
        ↓
Databricks Auto Loader
        ↓
Bronze Delta table
        ↓
dbt staging model
        ↓
dbt intermediate model
        ↓
dbt marts
```

## Tools Used

- AWS S3 for raw data landing storage
- Databricks Auto Loader for incremental CSV ingestion
- Databricks Delta Lake for bronze table storage
- Databricks Secrets for AWS credential handling
- dbt for SQL modelling, testing, documentation and lineage
- GitHub for version control
- GitHub Actions for CI validation
- Terraform for infrastructure-as-code templates
- Cursor and ChatGPT for AI-assisted development
- MCP for local AI-agent project inspection

## Key Models

### `stg_property_sales`

Cleans and standardises the bronze property sales table.

Key work:

- casts dates and timestamps
- casts purchase price and numeric fields
- standardises suburb names
- cleans text fields
- derives property purpose groups
- flags invalid purchase prices

### `int_clean_property_sales`

Creates a cleaner intermediate sales dataset and adds an `is_analytics_usable` flag for downstream marts.

### `fct_property_sales`

Analytics-ready transaction-level fact table containing usable property sale records.

### `agg_monthly_suburb_prices`

Monthly suburb-level aggregate table containing sale count, average price, median price, minimum price and maximum price.

### `agg_property_type_performance`

Property purpose-level aggregate table comparing sales performance across categories such as Residential, Commercial, Vacant Land and Other.

## Data Quality Work

The project uses dbt tests to validate key fields such as sale counter, purchase price and required mart fields.

During development, dbt tests exposed a CSV parsing issue where quoted property names caused shifted columns and invalid purchase prices. The issue was traced to the ingestion layer and fixed in Databricks Auto Loader by adding explicit CSV parsing options for quote, escape and multiline handling.

This showed the correct engineering approach: fix data issues at the ingestion layer instead of masking them in downstream dbt models.

## CI/CD

GitHub Actions runs a dbt parse workflow on push and pull request events.

The CI workflow validates:

- dbt project structure
- model references
- YAML files
- Jinja syntax
- source and model configuration

## Terraform

Terraform templates were added for the AWS S3 landing bucket, including:

- bucket definition
- public access blocking
- server-side encryption
- lifecycle rule for temporary files

The bucket was originally created manually during development, so the Terraform code is currently a validated template. A production next step would be importing the existing bucket into Terraform state.

## MCP

A local MCP server was added for AI-assisted project inspection.

Current tools:

- `inspect_project_structure`
- `list_dbt_models`
- `summarise_pipeline_layers`

The MCP server is local-only and avoids exposing secrets, credentials, dbt profiles, Terraform state or raw data dumps.

## Interview Talking Points

- Built an end-to-end lakehouse analytics pipeline from S3 ingestion to dbt marts.
- Used Databricks Auto Loader to incrementally ingest CSV files from AWS S3 into a bronze Delta table.
- Used dbt to create staging, intermediate and mart layers with tests and documentation.
- Debugged a real CSV parsing issue surfaced by dbt tests and fixed it at the ingestion layer.
- Added GitHub Actions CI to automatically validate dbt project parsing on push and pull requests.
- Added Terraform templates to document the S3 landing bucket infrastructure.
- Added a local MCP server to demonstrate AI-agent tooling around the project.

## Resume Bullet Version

Built an end-to-end property market analytics pipeline using AWS S3, Databricks Auto Loader, Delta Lake and dbt; ingested NSW property sales data into a bronze Delta table, transformed it through staging/intermediate/mart layers, added dbt tests and docs, implemented GitHub Actions CI, and documented infrastructure using Terraform templates.