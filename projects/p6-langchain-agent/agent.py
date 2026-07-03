# agent.py
# Agentic AI — ReAct agent with tool calling
# Built by: Mohammed Haroon Khan
# Stack: LangGraph · Groq · LLaMA 3.3

import os
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent  # noqa
from duckduckgo_search import DDGS

API_KEY = os.environ.get(" ")

# ── LLM ──────────────────────────────────────
llm = ChatGroq(
    api_key=API_KEY,
    model="llama-3.3-70b-versatile"
)

# ── TOOLS ─────────────────────────────────────
@tool
def calculate(expression: str) -> str:
    """Evaluate a math expression. Input must be a valid Python math expression like '15 * 8500 / 100'"""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"

@tool
def web_search(query: str) -> str:
    """Search the web for current information about any topic."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            if not results:
                return "No results found."
            return "\n\n".join([
                f"{r['title']}: {r['body']}"
                for r in results
            ])
    except Exception as e:
        return f"Search error: {e}"

tools = [calculate, web_search]

# ── AGENT ─────────────────────────────────────
# LangGraph's create_react_agent — modern replacement for AgentExecutor
agent = create_react_agent(
    model=llm,
    tools=tools
)

# ── RUN ───────────────────────────────────────
def run_agent(query: str):
    print(f"\n{'='*50}")
    print(f"Query: {query}")
    print('='*50)

    result = agent.invoke({
        "messages": [HumanMessage(content=query)]
    })

    # Get the last message — that's the final answer
    final = result["messages"][-1].content
    print(f"\nFinal Answer: {final}")
    return final

if __name__ == "__main__":
    run_agent("What is 15% of 8500?")
    run_agent("What is the capital of Karnataka and what is it famous for?")