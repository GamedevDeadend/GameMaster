import gradio as gr

from ui.gm_ui import web_app
from core.gm_agent import init_agent

init_agent()
web_app.launch(theme=gr.themes.Mario())