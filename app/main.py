from fastapi import FastAPI
from app.sse import create_sse_server
from mcp.server.fastmcp import FastMCP
import httpx
import os
from dotenv import load_dotenv
from app.appconfig import creds
from httpx import BasicAuth

app = FastAPI()
mcp = FastMCP("Weather")
NWS_API_BASE = "https://api.weather.gov"
ADO_API_BASE="https://analytics.dev.azure.com"
USER_AGENT = "weather-app/1.0"

token = os.getenv("ADO_TOKEN")
personal_access_token = creds.ado_pat
credentials = BasicAuth('', creds.ado_pat)

# Mount the Starlette SSE server onto the FastAPI app
app.mount("/", create_sse_server(mcp))

@app.get("/")
def read_root():
    return {"Hello": "World"}


# ADO tool


async def make_ADO_request(url: str) -> dict[str] | None:
    """Make a request to ADO"""
    async with httpx.AsyncClient(auth=BasicAuth('', creds.ado_pat)) as client:
        try:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


@mcp.resource("ADO://{backlogs}")
def backlog_resource(backlogs: str) -> str:
    """Get backlog as a resource"""
    return f"Resource backlogs: {backlogs}"

@mcp.tool()
async def get_backlogs(organization: str, project: str, team: str) -> str:
    """Get backlog from a Azure DevOps project
    
    Args:
        organization: The organization that the project is under
        project: The project where is backlog is held
        team: the team working on the backlog
    """
    ADO_url = f"{ADO_API_BASE}/{organization}/{project}/{team}/_odata/v4.0-preview/WorkItems?$select=WorkItemId,WorkItemType,Title,State&$top=3"
    ADO_data = await make_ADO_request(ADO_url)

    if not ADO_data:
        return "Unable to fetch ADO data for this location."

    return ADO_data

@mcp.prompt()
def ADO_prompt(backlogs: str) -> str:
    """Create an forecast prompt"""
    return f"Please process this message: {backlogs}"