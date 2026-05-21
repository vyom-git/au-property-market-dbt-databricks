# Property Project MCP Server

This folder will contain a local Model Context Protocol (MCP) server for the Australian Property Market Analytics Pipeline.

## Goal

The MCP server will let AI tools inspect and operate on this project in a controlled way.


It is intended for local development only.

## Local Usage

Install project dependencies from the project root:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

Run the MCP server locally:

```bash
python mcp_servers/property_project/server.py
```

The server is intended to be connected to an MCP-compatible AI tool such as Cursor or another local AI coding assistant.

Current safe tools exposed by the server:

- `inspect_project_structure`
- `list_dbt_models`
- `summarise_pipeline_layers`

## Planned Tools

The current version exposes safe helper tools such as:

- `list_dbt_models` — list dbt models in the project
- `inspect_project_structure` — summarise the main project folders
- `summarise_pipeline_layers` — describe the S3, Databricks and dbt pipeline layers

## Why MCP is useful here

MCP adds an AI-agent tooling layer beside the data pipeline.

The data pipeline is:

```text
AWS S3
  ↓
Databricks Auto Loader
  ↓
Bronze Delta table
  ↓
dbt staging/intermediate/marts
```

The MCP layer will help AI coding tools understand and interact with the project safely.

## Safety Rules

The MCP server should not expose secrets or credentials.

It should not read:

- `.env` files
- `~/.dbt/profiles.yml`
- AWS credentials
- Databricks tokens
- Terraform state files

It should only operate on safe project files and safe commands.
