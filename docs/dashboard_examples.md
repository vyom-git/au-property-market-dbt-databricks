# Dashboard Examples

This document describes example dashboard views that can be built from the dbt mart tables in this project.

## Purpose

The dbt marts provide analytics-ready tables for exploring NSW property sales trends by suburb, month and property type.

These examples are not tied to a specific BI tool. They can be implemented in tools such as Databricks SQL dashboards, Power BI, Tableau, Looker Studio or Streamlit.

## Available Mart Tables

### `fct_property_sales`

Transaction-level property sales table.

Useful for:

- detailed sale drilldowns
- filtering by suburb, postcode or property purpose
- validating individual records behind aggregate charts

### `agg_monthly_suburb_prices`

Monthly suburb-level price and sales aggregate.

Useful for:

- suburb price trend analysis
- monthly sales volume comparison
- suburb leaderboard views
- identifying high-value or high-activity suburbs

### `agg_property_type_performance`

Property purpose-level aggregate.

Useful for:

- comparing Residential, Commercial, Vacant Land and Other categories
- understanding which property types have the highest average or median prices
- comparing sales volume by property type

### `agg_suburb_rankings`

Suburb-level ranking table.

Useful for:

- ranking suburbs by median purchase price
- ranking suburbs by average purchase price
- ranking suburbs by total sales volume
- building leaderboard-style dashboard views

## Example Dashboard 1: Suburb Market Trends

Primary table:

- `agg_monthly_suburb_prices`

Suggested visuals:

- line chart of `median_purchase_price` by `contract_month`
- bar chart of `sale_count` by suburb
- table of top suburbs by `avg_purchase_price`
- filter for suburb, postcode and contract month

Questions answered:

- Which suburbs have the strongest price growth?
- Which suburbs have the highest sales volume?
- How do median prices change month by month?

## Example Dashboard 2: Property Type Performance

Primary table:

- `agg_property_type_performance`

Suggested visuals:

- bar chart of `sale_count` by `property_purpose_group`
- bar chart of `median_purchase_price` by `property_purpose_group`
- KPI cards for highest average price and highest sale count

Questions answered:

- Which property type has the highest median sale price?
- Which property type has the most transactions?
- How different are Residential, Commercial and Vacant Land sale prices?

## Example Dashboard 3: Suburb Rankings

Primary table:

- `agg_suburb_rankings`

Suggested visuals:

- leaderboard table sorted by `median_price_rank`
- leaderboard table sorted by `sales_volume_rank`
- bar chart of top suburbs by `median_purchase_price`
- bar chart of top suburbs by `total_sale_count`

Questions answered:

- Which suburbs have the highest median sale prices?
- Which suburbs have the highest sales volume?
- Which suburbs are both expensive and active?

## Example Dashboard 4: Transaction Drilldown

Primary table:

- `fct_property_sales`

Suggested visuals:

- searchable transaction table
- filters for suburb, postcode, property purpose and contract date
- KPI cards for total sales, average price and median price

Questions answered:

- What individual sales sit behind an aggregate trend?
- Which sales are driving a suburb's average price higher?
- What were the largest transactions in a selected period?

## Example Dashboard Metrics

Common metrics across dashboards:

- `sale_count`
- `avg_purchase_price`
- `median_purchase_price`
- `min_purchase_price`
- `max_purchase_price`

## Suggested Next Enhancements

Potential future dashboard improvements:

- add year-over-year price movement
- add suburb ranking by median price
- add postcode-level trend analysis
- add price bands such as under $500k, $500k-$1m and $1m+
- add LGA-level analysis if LGA reference data is introduced
- add dashboard screenshots once a BI layer is built