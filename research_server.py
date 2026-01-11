# wikipedia_server.py
import wikipedia
from mcp.server.fastmcp import FastMCP
from typing import Dict, Any
import logging

mcp = FastMCP("WikipediaSearch")

@mcp.tool()
def fetch_wikipedia_summary(query: str) -> Dict[str, Any]:
    """
    Returns title, summary and url of the best matching Wikipedia page.
    """
    try:
        page = wikipedia.page(query, auto_suggest=True)
        return {
            "title": page.title,
            "summary": page.summary.split("\n")[0],
            "url": page.url
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    logging.getLogger("mcp").setLevel(logging.WARNING)
    mcp.run(transport="stdio")
