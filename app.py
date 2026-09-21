# app.py
# DEMO 2: Real-World AI Integration — LLM + GitHub's official MCP server

import asyncio
import json
import os

import httpx
from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from langchain_openai import ChatOpenAI

load_dotenv()

# --- Config ---
GITHUB_PAT = os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"]
LLM_API_KEY = os.environ["LLM_API_KEY"]
LLM_BASE_URL = os.environ["LLM_BASE_URL"]
LLM_MODEL = os.environ.get("LLM_MODEL", "gpt-5.6-luna")
GITHUB_MCP_URL = "https://api.githubcopilot.com/mcp/"


def _parse_llm_json(raw_text: str) -> dict:
    # Helper: cleans up the LLM's reply and parses it as JSON
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned
        cleaned = cleaned.replace("json", "", 1).strip() if cleaned.lower().startswith("json") else cleaned
    return json.loads(cleaned)


async def run_intelligent_agent():
    # In mcp v2, headers/auth/timeout are set on the httpx client itself,
    # not passed directly into streamable_http_client()
    http_client = httpx.AsyncClient(
        headers={"Authorization": f"Bearer {GITHUB_PAT}"},
        follow_redirects=True,
    )

    async with http_client:
        # Connect to GitHub's remote MCP server
        async with streamable_http_client(url=GITHUB_MCP_URL, http_client=http_client) as (read, write):
            async with ClientSession(read, write) as session:

                # Handshake
                await session.initialize()

                # Tool discovery
                tools_response = await session.list_tools()
                available_tools = tools_response.tools
                print(f"✅ Handshake complete! Server returned {len(available_tools)} tools.")

                # LLM setup
                llm = ChatOpenAI(
                    model=LLM_MODEL,
                    api_key=LLM_API_KEY,
                    base_url=LLM_BASE_URL,
                    temperature=0,
                )

                # User query
                user_query = (
                    "Please check the repository 'langchain-ai/langchain' and tell me "
                    "the title and author of the last raised pull request."
                )
                print(f"\n💬 User query: '{user_query}'")

                # LLM decides which tool to use
                tools_description = "\n".join(f"- {t.name}: {t.description}" for t in available_tools)
                system_prompt = f"""You are an AI assistant with access to these GitHub MCP tools:
{tools_description}

Based on the user's request, pick the single best tool and its arguments.
Respond with ONLY a JSON object, no other text, in this exact shape:
{{"tool": "<tool_name>", "args": {{...}}}}"""

                llm_response = llm.invoke([
                    ("system", system_prompt),
                    ("human", user_query),
                ])
                print(f"\n🎯 LLM's decision: {llm_response.content}")

                decision = _parse_llm_json(llm_response.content)
                tool_name = decision["tool"]
                tool_args = decision["args"]

                # Tool execution
                print(f"\n🚀 Running the '{tool_name}' tool on the server...")
                result = await session.call_tool(tool_name, tool_args)

                # Result
                print("\n📦 Live result from GitHub:\n")
                for block in result.content:
                    if hasattr(block, "text"):
                        print(block.text)


if __name__ == "__main__":
    asyncio.run(run_intelligent_agent())