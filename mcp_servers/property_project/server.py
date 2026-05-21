

"""Local MCP server for the Australian Property Market Analytics Pipeline.

This server exposes safe helper tools for AI coding assistants.
It intentionally avoids reading secrets, credentials, dbt profiles, Terraform state,
or raw data files.
"""

from pathlib import Path

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("property-project")

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@mcp.tool()
def inspect_project_structure() -> dict[str, list[str]]:
    """Summarise the main project folders and important files."""
    folders = [
        "models/staging",
        "models/intermediate",
        "models/marts",
        "databricks/notebooks",
        "terraform/aws",
        "docs",
        ".github/workflows",
    ]

    result: dict[str, list[str]] = {}

    for folder in folders:
        folder_path = PROJECT_ROOT / folder
        if folder_path.exists():
            result[folder] = sorted(
                item.name for item in folder_path.iterdir() if item.is_file()
            )
        else:
            result[folder] = []

    return result


@mcp.tool()
def list_dbt_models() -> dict[str, list[str]]:
    """List dbt SQL models by layer."""
    model_layers = {
        "staging": PROJECT_ROOT / "models" / "staging",
        "intermediate": PROJECT_ROOT / "models" / "intermediate",
        "marts": PROJECT_ROOT / "models" / "marts",
    }

    result: dict[str, list[str]] = {}

    for layer, path in model_layers.items():
        if path.exists():
            result[layer] = sorted(file.stem for file in path.glob("*.sql"))
        else:
            result[layer] = []

    return result


@mcp.tool()
def summarise_pipeline_layers() -> str:
    """Return a short summary of the data pipeline layers."""
    return (
        "AWS S3 landing bucket stores raw NSW property sales CSV files. "
        "Databricks Auto Loader ingests those files into a bronze Delta table. "
        "dbt then transforms bronze data through staging, intermediate and mart layers. "
        "The final marts include transaction-level property sales, monthly suburb price aggregates, "
        "and property type performance aggregates."
    )


if __name__ == "__main__":
    mcp.run()