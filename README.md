# Australian Property Market Analytics Pipeline

An analytics engineering project using NSW public property sales data, dbt, Databricks, Terraform and GitHub Actions.

## Project Goal

This project models raw Australian property sales records into analytics-ready tables for analysing suburb, LGA and property-type market trends.

The project demonstrates a production-style analytics engineering workflow using:

- dbt for data modelling and testing
- Databricks Delta Lake as the analytics platform
- Terraform for infrastructure-as-code
- GitHub Actions for CI checks
- Public NSW property sales data as the source dataset

## Dataset

The project uses NSW public property sales data.

Primary source:

- NSW Valuer General Bulk Property Sales Information

Development source:

- Cleaned NSW property sales CSV from nswpropertysalesdata.com

## Planned Architecture

Raw CSV data is ingested into a Databricks bronze table, transformed through dbt staging and intermediate models, and published as gold analytics marts.

```text
Raw NSW property sales CSV
        ↓
Databricks Bronze table
        ↓
dbt staging models
        ↓
dbt intermediate models
        ↓
dbt mart models
        ↓
Analytics-ready suburb and property market tables
```

## dbt Model Layers

### Staging

Clean and standardise raw source data.

### Intermediate

Apply business logic, joins, date handling, price validation and location-level transformations.

### Marts

Create final fact, dimension and aggregate tables for analytics.

## Planned Final Models

- `fct_property_sales`
- `dim_suburb`
- `dim_lga`
- `agg_monthly_suburb_prices`
- `agg_lga_market_trends`
- `dashboard_property_market_summary`

## Status

Project in progress.