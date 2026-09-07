
import gradio as gr
import uvicorn
import argparse

from core.gm_agent import init_agent
from gm_mcp.gm_mcp_server import mcp
from ui.gm_ui import web_app
from api.gm_api import app as fast_app

parser = argparse.ArgumentParser()
parser.add_argument("--mode", choices=["gradio", "fastapi", "mcp_local", "mcp_remote"], default="gradio")
args = parser.parse_args()

MODE = args.mode  # Options: "gradio", "fastapi", "mcp_local", "mcp_remote"

if __name__ == "__main__":
    init_agent()
    
    if MODE == "gradio":
        web_app.launch(server_name="127.0.0.1", server_port=7860, theme=gr.themes.Mario())
    
    elif MODE == "fastapi":
        uvicorn.run(fast_app, host="127.0.0.1", port=8000)
    
    elif MODE == "mcp_local":
        # For Claude Desktop / MCP Inspector testing
        mcp.run(transport="stdio")
    
    elif MODE == "mcp_remote":
        # For HF Spaces / production deployment
        mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
