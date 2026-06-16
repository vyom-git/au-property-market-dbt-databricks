# Databricks notebook source
# Run dbt build against the Azure Databricks target.

# COMMAND ----------

import os
import subprocess
import textwrap
from pathlib import Path

# COMMAND ----------

repo_path = Path("/Workspace/Users/vyomchauhan@icloud.com/au-property-market-dbt-databricks")
profiles_dir = Path("/tmp/dbt_profiles")
profiles_dir.mkdir(parents=True, exist_ok=True)

# COMMAND ----------

databricks_token = dbutils.secrets.get(
    scope="adls-property-ingestion",
    key="databricks-token"
)

profiles_yml = f"""
au_property_market:
  target: azure_dev
  outputs:
    azure_dev:
      type: databricks
      host: adb-7405605636756373.13.azuredatabricks.net
      http_path: /sql/1.0/warehouses/ad9bf12c8f68726d
      token: "{databricks_token}"
      catalog: adb_au_property_market_dev
      schema: property_analytics
      threads: 4
"""

(profiles_dir / "profiles.yml").write_text(textwrap.dedent(profiles_yml).strip())

# COMMAND ----------

subprocess.run(
    ["python", "-m", "pip", "install", "dbt-databricks"],
    check=True
)

# COMMAND ----------

result = subprocess.run(
    [
        "dbt",
        "build",
        "--target",
        "azure_dev",
        "--profiles-dir",
        str(profiles_dir),
    ],
    cwd=str(repo_path),
    text=True,
    capture_output=True,
)

print(result.stdout)
print(result.stderr)

if result.returncode != 0:
    raise RuntimeError("dbt build failed")

# COMMAND ----------

print("dbt build completed successfully.")
