from fastmcp import FastMCP
from core.gm_agent import ask_gm

mcp = FastMCP(
    name="Veildark Game Master",
    instructions="An MCP server exposing tools to interact with the Veildark Game Master. Use search_lore to find lore, get_character for character info, get_faction for faction info, get_location for location info, and narrate for dramatic scene narration."
)

@mcp.tool()
def search_lore(query: str) -> str:
    """Search the lore vector database for relevant information."""
    return ask_gm(
        f"Search the lore and provide a comprehensive answer to this query: {query}. "
        f"Include any relevant context, history, or connections to other elements of the world."
    )

@mcp.tool()
def get_character(name: str) -> str:
    """Get detailed information about a specific character."""
    return ask_gm(
        f"Focus specifically on the character '{name}'. "
        f"Describe their background, role in the world, motivations, abilities, and any key relationships or allegiances. "
        f"If this character is not in the lore, say so clearly."
    )

@mcp.tool()
def get_faction(name: str) -> str:
    """Get detailed information about a specific faction."""
    return ask_gm(
        f"Focus specifically on the faction '{name}'. "
        f"Describe their goals, leadership, history, territory, and relationships with other factions. "
        f"If this faction is not in the lore, say so clearly."
    )

@mcp.tool()
def get_location(name: str) -> str:
    """Get detailed information about a specific location."""
    return ask_gm(
        f"Focus specifically on the location '{name}'. "
        f"Describe its geography, significance, history, current state, and any key events or figures associated with it. "
        f"If this location is not in the lore, say so clearly."
    )

@mcp.tool()
def narrate(situation: str) -> str:
    """Narrate a dramatic in-world scene as the Game Master."""
    return ask_gm(
        f"Narrate the following situation dramatically as the Game Master, in second person: {situation}. "
        f"Be atmospheric, vivid, and immersive. Draw on the world's tone — dark, weighty, but not without hope. "
        f"End with an open moment that invites the player to act."
    )