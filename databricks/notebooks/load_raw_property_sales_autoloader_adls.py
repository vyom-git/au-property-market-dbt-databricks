# Databricks notebook source
# Load NSW property sales CSV files from ADLS Gen2 using Databricks Auto Loader.
#
# Source:
# abfss://raw@aupropmarket31963.dfs.core.windows.net/nsw_property_sales/
#
# Target:
# workspace.property_analytics_bronze.raw_property_sales_adls

# COMMAND ----------

storage_account_name = "aupropmarket31963"
storage_account_key = dbutils.secrets.get(
    scope="adls-property-ingestion",
    key="storage-account-key"
)

# COMMAND ----------

source_path = (
    f"abfss://raw@{storage_account_name}.dfs.core.windows.net/"
    "nsw_property_sales/"
)

schema_location = (
    "/Volumes/workspace/property_analytics_metadata/autoloader_metadata/"
    "adls/schema/nsw_property_sales/"
)

checkpoint_location = (
    "/Volumes/workspace/property_analytics_metadata/autoloader_metadata/"
    "adls/checkpoints/nsw_property_sales/"
)

target_table = "workspace.property_analytics_bronze.raw_property_sales_adls"

# COMMAND ----------

raw_column_mapping = {
    "Property ID": "property_id",
    "Sale counter": "sale_counter",
    "Download date / time": "download_date_time",
    "Property name": "property_name",
    "Property unit number": "property_unit_number",
    "Property house number": "property_house_number",
    "Property street name": "property_street_name",
    "Property locality": "property_locality",
    "Property post code": "property_post_code",
    "Area": "area",
    "Area type": "area_type",
    "Contract date": "contract_date",
    "Settlement date": "settlement_date",
    "Purchase price": "purchase_price",
    "Zoning": "zoning",
    "Nature of property": "nature_of_property",
    "Primary purpose": "primary_purpose",
    "Strata lot number": "strata_lot_number",
    "Dealing number": "dealing_number",
    "Property legal description": "property_legal_description",
}

# COMMAND ----------

df = (
    spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "csv")
    .option("cloudFiles.schemaLocation", schema_location)
    .option(
        f"fs.azure.account.key.{storage_account_name}.dfs.core.windows.net",
        storage_account_key
    )
    .option("header", "true")
    .option("inferSchema", "false")
    .option("quote", '"')
    .option("escape", '"')
    .option("multiLine", "true")
    .load(source_path)
)

for source_column, target_column in raw_column_mapping.items():
    if source_column in df.columns:
        df = df.withColumnRenamed(source_column, target_column)

# COMMAND ----------

query = (
    df.writeStream
    .format("delta")
    .option("checkpointLocation", checkpoint_location)
    .option("mergeSchema", "true")
    .trigger(availableNow=True)
    .toTable(target_table)
)

query.awaitTermination()

# COMMAND ----------

display(
    spark.sql(f"""
        select count(*) as row_count
        from {target_table}
    """)
)

# COMMAND ----------

display(
    spark.sql(f"""
        select *
        from {target_table}
        limit 5
    """)
)

# COMMAND ----------

display(
    spark.sql(f"""
        describe table {target_table}
    """)
)

# COMMAND ----------

