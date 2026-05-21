# Australian Property Market Analytics Pipeline

A production-style analytics engineering project using NSW public property sales data, AWS S3, Databricks Auto Loader, Delta Lake and dbt.

## Project Goal

This project ingests raw NSW property sales data from cloud storage, loads it into a Databricks bronze Delta table, and transforms it into analytics-ready dbt models for property market analysis.

The project demonstrates a modern data engineering and analytics engineering workflow using:

- AWS S3 as the raw data landing zone
- Databricks Auto Loader for incremental CSV ingestion
- Databricks Delta Lake for bronze storage
- dbt for SQL modelling, testing, documentation and lineage
- GitHub for version control
- Public NSW property sales data as the source dataset

## Dataset

The project uses NSW public property sales data.

Primary source:

- NSW Valuer General Bulk Property Sales Information

Development source:

- Cleaned NSW property sales CSV from nswpropertysalesdata.com

## Architecture

The project follows a lakehouse-style pipeline:

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
dbt mart tables
```

## Pipeline Layers

### Ingestion

Raw NSW property sales data is uploaded to an AWS S3 landing bucket.

A Databricks Auto Loader notebook reads new CSV files from S3 and writes them into a bronze Delta table. The ingestion logic handles quoted CSV fields, schema tracking, checkpointing and source column standardisation.

Notebook:

- `databricks/notebooks/load_raw_property_sales_autoloader.py`

### Bronze

The bronze layer stores the raw property sales data in Delta format with clean technical column names and minimal transformation.

Table:

- `workspace.property_analytics_bronze.raw_property_sales`

### Staging

The dbt staging layer cleans and standardises the bronze table.

It performs:

- data type casting
- timestamp and date parsing
- suburb standardisation
- text cleanup
- purchase price validation
- property purpose grouping

Model:

- `stg_property_sales`

### Intermediate

The intermediate layer prepares records for downstream analytics and adds an `is_analytics_usable` flag.

Model:

- `int_clean_property_sales`

### Marts

The mart layer contains analytics-ready tables for reporting and dashboarding.

Models:

- `fct_property_sales`
- `agg_monthly_suburb_prices`
- `agg_property_type_performance`

## dbt Models

### `stg_property_sales`

Cleans the raw bronze table, converts fields into usable data types and derives basic fields used downstream.

### `int_clean_property_sales`

Creates a cleaner intermediate sales dataset and flags records that have the minimum fields required for analytics.

### `fct_property_sales`

Transaction-level fact table containing analytics-ready property sale records.

### `agg_monthly_suburb_prices`

Monthly suburb-level aggregate table containing:

- sale count
- average purchase price
- median purchase price
- minimum purchase price
- maximum purchase price

### `agg_property_type_performance`

Property purpose-level aggregate table comparing performance across categories such as Residential, Commercial, Vacant Land and Other.

## Data Quality

The project uses dbt tests to validate key fields, including:

- sale counter is present
- purchase price is present
- purchase price is positive
- analytics marts contain required reporting fields

During development, dbt tests surfaced a CSV parsing issue where quoted property names caused shifted columns. The ingestion logic was updated with explicit CSV quote and escape handling before reloading the bronze table.

## dbt Documentation

dbt documentation can be generated locally with:

```bash
dbt docs generate
```

The documentation site can then be served with:

```bash
dbt docs serve
```

This shows model documentation, column descriptions, tests and lineage from source to marts.

## MCP Server

This project includes a local Model Context Protocol (MCP) server for AI-assisted project inspection.

The MCP server is located at:

- `mcp_servers/property_project/server.py`

Current safe tools exposed by the server:

- `inspect_project_structure`
- `list_dbt_models`
- `summarise_pipeline_layers`

The MCP server is intended for local development and does not expose secrets, credentials, dbt profiles, AWS credentials, Databricks tokens or Terraform state files.

Usage instructions are available in:

- `mcp_servers/property_project/README.md`

## CI/CD

This project uses GitHub Actions for basic dbt validation.

Current CI workflow:

- runs on push to `main`
- runs on pull requests to `main`
- installs Python dependencies
- installs dbt packages
- creates a dummy dbt profile
- runs `dbt parse`

The workflow validates dbt project structure, model references, YAML files and Jinja syntax without requiring live Databricks credentials.

## Current Status

Completed:

- GitHub repository setup
- Python virtual environment setup
- dbt Databricks connection
- AWS S3 landing bucket setup
- Databricks secrets for AWS credentials
- Databricks Auto Loader ingestion from S3
- Bronze Delta table creation
- dbt staging model
- dbt intermediate model
- dbt mart models
- dbt tests passing
- Full `dbt build` passing
- Add dbt documentation generation
- GitHub Actions dbt parse CI workflow
- Local MCP server for AI-assisted project inspection

Planned next steps:

- Import existing S3 bucket into Terraform state or use Terraform template in a clean environment
- Add more mart models and dashboard examples
- Add Codex/Cursor workflow documentation