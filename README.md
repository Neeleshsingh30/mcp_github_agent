# 🤖 MCP + LLM Agent Demo

### *A real LLM reads a live tool registry and decides what to run — on its own*

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![MCP SDK](https://img.shields.io/badge/MCP%20SDK-v2-orange)
![LangChain](https://img.shields.io/badge/LangChain-OpenAI--compatible-1C3C3C)
![GitHub MCP](https://img.shields.io/badge/GitHub-Official%20MCP%20Server-181717?logo=github&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🎯 What This Demonstrates

This is **Demo 2** of a two-part MCP teaching series. Where Demo 1 showed the raw plumbing manually, this demo shows the *complete real-world picture*:

- Connects to **GitHub's official, pre-built remote MCP server** — no server code written by us at all
- Automatically fetches its full tool registry (`tools/list`)
- Hands that registry + a plain-English question to an **LLM**
- The LLM decides — entirely on its own — which tool fits and what arguments to use
- That decision is executed for real (`tools/call`), and a **live** result comes back from GitHub

> Nothing is hardcoded about which tool runs. The model reads the menu and orders for itself.

---

## 🧩 How It's Different From Demo 1

| | Demo 1 (Manual) | Demo 2 (This one) |
|---|---|---|
| Server | Custom-built by us | Pre-built, official (GitHub) |
| Who picks the tool | You, manually, in Inspector | The LLM, automatically |
| Transport | stdio (local process) | Streamable HTTP (remote URL) |
| Goal | Show the mechanics | Show the full intelligent flow |

---

## 📋 Prerequisites

- **Python 3.10+** — [download here](https://www.python.org/downloads/)
- A **GitHub Personal Access Token** — free, from *Settings → Developer settings → Personal access tokens*
- An LLM API key + base URL for your OpenAI-compatible gateway

---

## 🚀 Setup — Step by Step

```bash
# 1. Create and enter the project folder
mkdir mcp_llm_demo
cd mcp_llm_demo

# 2. Create and activate a virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

> ⚠️ **Windows PowerShell error?**
> If activation fails with `running scripts is disabled on this system`, run this once:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### 🔑 Configure your keys

Copy `.env.example` → `.env` and fill in your real values:

```
GITHUB_PERSONAL_ACCESS_TOKEN=your_github_pat_here
LLM_API_KEY=your_llm_api_key_here
LLM_BASE_URL=https://your-llm-gateway.example/v1
LLM_MODEL=your-model-name
```

> 🔒 `.env` holds real secrets — never commit it or push it to GitHub.

---

## ▶️ Running the Demo

```bash
python app.py
```

**What you'll see, step by step:**

```
✅ Handshake complete! Server returned N tools.
💬 User query: 'Please check the repository "..." and tell me...'
🎯 LLM's decision: {"tool": "...", "args": {...}}
🚀 Running the '...' tool on the server...
📦 Live result from GitHub:
    <real PR title and author here>
```

### Want to check your own repo?
Edit the `user_query` in `app.py`:
```python
user_query = "Please check the repository 'your-username/your-repo' and tell me ..."
```
Works for private repos too — just make sure your PAT has the `repo` scope, not only `public_repo`.

---

## 📁 Project Structure

```
mcp_llm_demo/
├── app.py              # LLM + MCP client — connects, discovers, decides, executes
├── requirements.txt    # mcp, langchain-openai, python-dotenv
├── .env.example        # Copy to .env and fill in real keys
└── README.md
```

---

## 🩹 Known Gotchas

- **`ImportError: cannot import name 'streamablehttp_client'`** → you're on **MCP SDK v2**, where it was renamed to `streamable_http_client` with a new signature (headers now set via `httpx.AsyncClient`). This project's `app.py` already uses the v2-correct API.
- **Flaky 500 errors from GitHub's MCP endpoint** → happens occasionally on their end; re-run, or test once before a live class demo.

---

## 💡 The Big Takeaway

Once a tool registry exists (from *any* MCP server — custom or pre-built), a model can act on it dynamically. Demo 1 proved the plumbing works; this demo proves an LLM can use that plumbing intelligently, without a developer hardcoding which tool answers which question.
