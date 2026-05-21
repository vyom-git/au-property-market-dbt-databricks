

# AI-Assisted Development Workflow

This project was built using AI-assisted development tools in a controlled, review-driven workflow.

## Tools Used

- ChatGPT for step-by-step project planning, debugging and architecture decisions
- Cursor for editing project files locally
- GitHub for version control and CI validation
- MCP as a local AI-agent extension layer for safe project inspection

## Workflow Principles

AI assistance was used to accelerate development, but changes were reviewed and tested before being committed.

The workflow followed this pattern:

```text
Plan the change
      ↓
Edit files in Cursor
      ↓
Run local checks
      ↓
Run dbt / Terraform / Python validation
      ↓
Review git diff
      ↓
Commit and push
      ↓
Confirm GitHub Actions CI passes
```

## Examples from This Project

### dbt Development

AI assistance helped create and refine dbt models across staging, intermediate and mart layers.

Validation was done using:

```bash
dbt parse
dbt run
dbt test
dbt build
```

### Data Quality Debugging

A dbt test failure revealed that `purchase_price` contained date-like values.

The issue was traced back to CSV parsing in Databricks Auto Loader, where quoted property names caused shifted columns.

The ingestion logic was corrected using explicit CSV parsing options:

```python
.option("quote", '"')
.option("escape", '"')
.option("multiLine", "true")
```

### Infrastructure Documentation

Terraform was added to document the AWS S3 landing bucket setup as infrastructure-as-code.

The existing bucket was created manually during development, so the Terraform code is currently treated as a validated template until the bucket is imported into Terraform state.

### MCP Server

A local MCP server was added to expose safe project inspection tools for AI assistants.

The MCP server does not expose secrets, credentials, dbt profiles, AWS credentials, Databricks tokens or Terraform state files.

## Safety Practices

The project avoids committing:

- AWS credentials
- Databricks tokens
- local dbt profiles
- Terraform state files
- dbt `target/` artifacts
- local Terraform cache files
- raw private data dumps

Secrets are handled through:

- local environment variables for local dbt development
- Databricks Secrets for Databricks notebook execution
- GitHub token permissions for GitHub Actions workflow updates

## Why This Matters

This workflow shows that AI tools were used as engineering assistants, not as a replacement for validation.

Every meaningful change was checked through code review, local validation, dbt tests or GitHub Actions CI before being treated as complete.