# ⚔️ Veildark Game Master — AI-Powered RPG Narrator

> *"You stand at the edge of a dying world. The Bleed grows. Ask your questions, traveller — if you dare."*

An MCP-powered AI Game Master that ingests any game world's lore PDF and lets players — or game engines — converse with it in real time. Built on RAG + LangChain + FastAPI + Groq, exposed as both a REST API and an MCP Server callable by any AI client.

---

## 🎮 What It Does

The Veildark Game Master is an AI agent that:

- **Ingests a lore PDF** (game world bible, D&D campaign, custom RPG setting — anything)
- **Retrieves relevant lore** using a two-stage RAG pipeline with CrossEncoder reranking
- **Responds in character** as a dramatic Game Master with full world knowledge
- **Remembers conversation history** — feels like a real session
- **Exposes multiple interfaces** — browser UI, REST API, and MCP server

---

## 🏗️ Architecture

```
Player / Game Engine / AI Client
            ↓
┌─────────────────────────────────┐
│         Interface Layer         │
│  Gradio UI │ FastAPI │ MCP      │
└─────────────┬───────────────────┘
              ↓
┌─────────────────────────────────┐
│         gm_agent.py             │
│  RAG retrieval + LLM chain      │
│  Conversation memory            │
└──────┬──────────────┬───────────┘
       ↓              ↓
┌──────────────┐ ┌────────────────┐
│  gm_rag.py   │ │  gm_llm.py     │
│  ChromaDB    │ │  Groq LLM      │
│  CrossEncoder│ │  llama-3.3-70b │
│  PyMuPDF     │ │                │
└──────────────┘ └────────────────┘
```

### Two-Stage RAG Pipeline

1. **Initial Retrieval** — ChromaDB vector search retrieves top 20 chunks using `all-MiniLM-L6-v2` embeddings
2. **Reranking** — CrossEncoder (`ms-marco-MiniLM-L-6-v2`) scores and reranks to top 5 for higher relevance accuracy

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM | Groq API — `llama-3.3-70b-versatile` |
| Embeddings | HuggingFace — `all-MiniLM-L6-v2` |
| Reranking | CrossEncoder — `ms-marco-MiniLM-L-6-v2` |
| Vector Store | ChromaDB (persistent) |
| PDF Loading | PyMuPDF |
| RAG Framework | LangChain |
| REST API | FastAPI + Uvicorn |
| UI | Gradio |
| MCP Server | FastMCP |
| Inference | Groq API |

---

## 📁 Project Structure

```
GameMaster/
├── core/
│   ├── gm_llm.py          # LLM initialization (Groq)
│   ├── gm_rag.py          # RAG pipeline + reranking
│   └── gm_agent.py        # Brain — orchestrates RAG + LLM + memory
├── api/
│   └── gm_api.py          # FastAPI REST endpoint (/ask, /health)
├── ui/
│   └── gm_ui.py           # Gradio chat interface
├── gm_mcp/
│   └── gm_mcp_server.py   # MCP server with 5 lore tools
├── resources/
│   └── GameLore_Resource.pdf  # Veildark world lore bible
├── main.py                # Entry point — switch between interfaces
└── .gitignore
```

---

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/GamedevDeadend/GameMaster.git
cd GameMaster
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Mac/Linux
```

### 2. Install Dependencies

```bash
pip install langchain langchain-groq langchain-huggingface langchain-community \
            langchain-chroma langchain-text-splitters sentence-transformers \
            pymupdf "fastapi[standard]" uvicorn gradio fastmcp python-dotenv
```

### 3. Configure Environment

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
HF_TOKEN=your_huggingface_token_here
```

Get your free Groq API key at [console.groq.com](https://console.groq.com)

### 4. Run

Open `main.py` and set the `MODE` variable:

```python
MODE = "gradio"      # Browser chat UI
MODE = "fastapi"     # REST API server
MODE = "mcp_local"   # MCP server (stdio, for Claude Desktop)
MODE = "mcp_remote"  # MCP server (HTTP, for production)
```

Then:

```bash
python main.py
```

---

## 🎯 Interfaces

### Gradio UI
```
http://127.0.0.1:7860
```
Chat with the Game Master in your browser. Includes example questions, streaming responses, and dark fantasy theming.

### FastAPI REST
```
http://127.0.0.1:8000/docs   # Swagger UI
```

**POST** `/ask`
```json
{
  "query": "Who is Mira Ashveil?"
}
```

Response streams in real time. Game engines (Unreal, Unity) can call this endpoint over HTTP to integrate the Game Master into gameplay.

**Example Unreal C++ integration:**
```cpp
// Call the Game Master from any game engine via HTTP
FHttpModule::Get().CreateRequest()
    ->SetURL("http://your-server/ask")
    ->SetVerb("POST")
    ->SetContentAsString("{\"query\": \"Describe the Ashwall\"}")
    ->ProcessRequest();
```

### MCP Server (5 Tools)

The Game Master is exposed as an MCP server with specialized lore tools, callable by any MCP-compatible AI client (Claude Desktop, etc.):

| Tool | Description |
|------|-------------|
| `search_lore(query)` | General RAG search across entire lore |
| `get_character(name)` | Fetch character details and backstory |
| `get_faction(name)` | Fetch faction info and allegiances |
| `get_location(name)` | Fetch location details |
| `narrate(situation)` | GM narrates a scene dramatically |

**Claude Desktop config** (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "veildark-gm": {
      "command": "python",
      "args": ["path/to/GameMaster/main.py"],
      "env": {
        "MODE": "mcp_local"
      }
    }
  }
}
```

> The server is designed to be extensible — permission-based elicitation and sampling can be added for multi-agent enterprise workflows.

---

## 🌑 The World — Veildark

The default lore is **Veildark** — a dark fantasy world in the Witcher tradition:

- A dying world torn open by **The Bleed** — a wound in reality through which shadow creatures pour
- **1,200 years of war** against the Veilborn, with humanity retreating behind the Ashwall
- **5 major factions**, **5 key characters**, a full magic system (Veilcraft), and dark legends
- Flickering hope against consuming darkness

> This works with **any game world lore** — just swap the PDF. D&D campaigns, homebrew settings, custom RPG worlds. The Game Master adapts to whatever lore you provide.

---

## 🔧 Bring Your Own Lore

Replace `resources/GameLore_Resource.pdf` with your own lore document, then delete the cached embeddings to rebuild:

```bash
# Delete cached embeddings
rm -rf resources/embeddings/

# Run — it will re-embed your new lore automatically
python main.py
```

---

## 📊 Portfolio Notes

This project demonstrates:

- **Production RAG pipeline** — two-stage retrieval with reranking, not just basic vector search
- **MCP integration** — exposes specialized tools callable by any AI client (cutting-edge 2025/26 skill)
- **Multi-interface architecture** — same core logic powers Gradio UI, FastAPI, and MCP
- **Game engine ready** — FastAPI endpoint designed for HTTP calls from Unreal/Unity
- **Streaming responses** — real-time token streaming across all interfaces
- **Persistent embeddings** — ChromaDB caches embeddings so PDF is only processed once

---

## 🛣️ Roadmap (v2)

- [ ] TTS voice output via ElevenLabs (dramatic GM voice)
- [ ] Game engine integration demo (Unreal HTTP blueprint)
- [ ] Session management for multiple simultaneous players
- [ ] External MCP tools (weather, random events, image generation)
- [ ] Architecture diagram

---

## 📄 License

MIT License — free to use, modify, and build upon.

---

*Built by [GamedevDeadend](https://github.com/GamedevDeadend) — Game Developer turned AI Engineer*
