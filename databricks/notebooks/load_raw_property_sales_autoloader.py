# Databricks notebook source
from pyspark.sql.functions import col

S3_PATH = "s3://au-property-market-landing-313589910075-ap-southeast-2-an/raw/nsw_property_sales/"

SCHEMA_LOCATION = (
    "/Volumes/workspace/property_analytics_metadata/"
    "autoloader_metadata/raw_property_sales_schema"
)

CHECKPOINT_LOCATION = (
    "/Volumes/workspace/property_analytics_metadata/"
    "autoloader_metadata/raw_property_sales_checkpoint"
)

TARGET_TABLE = "workspace.property_analytics_bronze.raw_property_sales"

SECRET_SCOPE = "aws-property-ingestion"
AWS_ACCESS_KEY_SECRET = "aws-access-key-id"
AWS_SECRET_KEY_SECRET = "aws-secret-access-key"


access_key = dbutils.secrets.get(
    scope=SECRET_SCOPE,
    key=AWS_ACCESS_KEY_SECRET,
)

secret_key = dbutils.secrets.get(
    scope=SECRET_SCOPE,
    key=AWS_SECRET_KEY_SECRET,
)


column_mapping = {
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
    "_rescued_data": "_rescued_data",
}


df_raw = (
    spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "csv")
    .option("cloudFiles.awsAccessKey", access_key)
    .option("cloudFiles.awsSecretKey", secret_key)
    .option("cloudFiles.schemaLocation", SCHEMA_LOCATION)
    .option("header", "true")
    .option("cloudFiles.inferColumnTypes", "true")
    .option("quote", '"')
    .option("escape", '"')
    .option("multiLine", "true")
    .load(S3_PATH)
)


missing_columns = set(column_mapping.keys()) - set(df_raw.columns)

if missing_columns:
    raise ValueError(f"Missing expected columns in source file: {missing_columns}")


df_clean = df_raw.select(
    [col(raw_name).alias(clean_name) for raw_name, clean_name in column_mapping.items()]
)


query = (
    df_clean.writeStream
    .option("checkpointLocation", CHECKPOINT_LOCATION)
    .trigger(availableNow=True)
    .toTable(TARGET_TABLE)
)

query.awaitTermination()

print(f"Raw property sales loaded into {TARGET_TABLE}.")