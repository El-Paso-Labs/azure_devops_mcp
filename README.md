# Azure DevOps MCP
MCP server for Azure DevOps

## Install requirements.txt

```bash
uv add -r requirements.txt
```

## Run FastAPI server

```bash
uv run uvicorn app.main:app --reload
```

## Configure the server to the client

```bash
{
  "mcpServers": {
    "example-sse": {
      "url": "http://localhost:8000/sse",
      "env": {}
    }
  }
}
```
