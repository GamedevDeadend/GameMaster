import gradio as gr

from core.gm_agent import init_agent, ask_gm_stream

def chat(message, history):
    yield from ask_gm_stream(message)

web_app = gr.ChatInterface(fn=chat, title="⚔️ Veildark Game Master", description="You stand at the edge of a dying world. The Bleed grows. Ask your questions, traveller — if you dare.",
    examples=[
        "Who is Mira Ashveil?",
        "Tell me about the Ashwall",
        "What are the Veilborn?",
        "Who leads the Order of the Ashen Veil?"
    ]
)