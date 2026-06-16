# Databricks notebook source
# COMMAND ----------
# Export dbt gold mart tables to ADLS Gen2 as Delta folders.
#
# These exported Delta folders can be queried by Synapse serverless SQL.

# COMMAND ----------

storage_account_name = "aupropmarket31963"
storage_account_key = dbutils.secrets.get(
    scope="adls-property-ingestion",
    key="storage-account-key"
)

gold_base_path = f"abfss://gold@{storage_account_name}.dfs.core.windows.net"

# COMMAND ----------

gold_marts = {
    "agg_suburb_rankings": "workspace.property_analytics_marts.agg_suburb_rankings",
    "agg_monthly_suburb_prices": "workspace.property_analytics_marts.agg_monthly_suburb_prices",
    "agg_property_type_performance": "workspace.property_analytics_marts.agg_property_type_performance",
    "fct_property_sales": "workspace.property_analytics_marts.fct_property_sales",
}

# COMMAND ----------

for mart_name, table_name in gold_marts.items():
    output_path = f"{gold_base_path}/{mart_name}/"

    print(f"Exporting {table_name} to {output_path}")

    (
        spark.table(table_name)
        .write
        .format("delta")
        .mode("overwrite")
        .option(
            f"fs.azure.account.key.{storage_account_name}.dfs.core.windows.net",
            storage_account_key
        )
        .save(output_path)
    )

# COMMAND ----------

for mart_name in gold_marts:
    path = f"{gold_base_path}/{mart_name}/"

    row_count = (
        spark.read
        .format("delta")
        .option(
            f"fs.azure.account.key.{storage_account_name}.dfs.core.windows.net",
            storage_account_key
        )
        .load(path)
        .count()
    )

    print(f"{mart_name}: {row_count} rows")