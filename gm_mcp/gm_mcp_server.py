from fastmcp import FastMCP
from core.gm_agent import init_agent, ask_gm

mcp = FastMCP(
    name="Veildark Game Master",
    instructions="An MCP server exposing tools to interact with the Veildark Game Master. Use search_lore to find lore, get_character for character info, get_faction for faction info, get_location for location info, and narrate for dramatic scene narration."
)

@mcp.tool()
def search_lore(query: str) -> str:
    """Search the lore vector database for relevant information."""
    return ask_gm(f"Search the lore for information relevant to this query: {query}")

@mcp.tool()
def get_character(name: str) -> str:
    """Get information about a character."""
    return ask_gm(f"Get information about the character: {name}")

@mcp.tool()
def get_faction(name: str) -> str:
    """Get information about a faction."""
    return ask_gm(f"Get information about the faction: {name}")

@mcp.tool()
def get_location(name: str) -> str:
    """Get information about a location."""
    return ask_gm(f"Get information about the location: {name}")

@mcp.tool()
def narrate(description: str) -> str:
    """Narrate a dramatic scene."""
    return ask_gm(f"Narrate the scene: {description}")