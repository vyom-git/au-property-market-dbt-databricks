-- Synapse serverless SQL views over ADLS Gen2 gold Delta folders.
--
-- These views expose Databricks/dbt gold marts from ADLS Gen2 for SQL and BI consumption.
--
-- Storage account:
-- aupropmarket31963
--
-- Gold container:
-- gold

create schema gold;
go

create or alter view gold.vw_suburb_rankings as
select *
from openrowset(
    bulk 'https://aupropmarket31963.dfs.core.windows.net/gold/agg_suburb_rankings/',
    format = 'delta'
) as rows;
go

create or alter view gold.vw_monthly_suburb_prices as
select *
from openrowset(
    bulk 'https://aupropmarket31963.dfs.core.windows.net/gold/agg_monthly_suburb_prices/',
    format = 'delta'
) as rows;
go

create or alter view gold.vw_property_type_performance as
select *
from openrowset(
    bulk 'https://aupropmarket31963.dfs.core.windows.net/gold/agg_property_type_performance/',
    format = 'delta'
) as rows;
go

create or alter view gold.vw_property_sales as
select *
from openrowset(
    bulk 'https://aupropmarket31963.dfs.core.windows.net/gold/fct_property_sales/',
    format = 'delta'
) as rows;
go