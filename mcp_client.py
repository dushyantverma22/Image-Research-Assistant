# mcp_client.py
import asyncio
import os
from typing import Annotated

import gradio as gr
from dotenv import load_dotenv
from typing_extensions import TypedDict

from langchain_core.messages import AnyMessage, ToolMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import tools_condition, ToolNode

from langchain_mcp_adapters.client import MultiServerMCPClient


# ------------------------------------------------------------------
# ENV SETUP (LOCAL + PRODUCTION SAFE)
# ------------------------------------------------------------------
import os

# Load .env only if present (for local development)
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass  # In production, env vars will come from GitHub Actions / Docker

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError(
        "❌ OPENAI_API_KEY not found. "
        "Make sure it is set as an environment variable or GitHub Secret."
    )


# ------------------------------------------------------------------
# MCP SERVER CONFIG
# ------------------------------------------------------------------
server_configs = {
    "vision": {
        "command": "python",
        "args": ["visual_analysis_server.py"],
        "transport": "stdio",
    },
    "wikipedia": {
        "command": "python",
        "args": ["research_server.py"],
        "transport": "stdio",
    }
}


# ------------------------------------------------------------------
# STATE DEFINITION
# ------------------------------------------------------------------
class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


# ------------------------------------------------------------------
# MCP RESPONSE PARSER (IMPORTANT)
# ------------------------------------------------------------------
def extract_text_from_mcp_result(result):
    """
    Handles all known MCP response formats and safely extracts text.
    """
    if isinstance(result, list):
        for item in result:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    return item.get("text", "")
                if "text" in item:
                    return item["text"]
    if isinstance(result, dict):
        if "text" in result:
            return result["text"]
        if "content" in result and isinstance(result["content"], str):
            return result["content"]
    return str(result)


# ------------------------------------------------------------------
# CUSTOM TOOL NODE (CRITICAL FIX)
# ------------------------------------------------------------------
class FixedToolNode(ToolNode):
    async def _arun_tool(self, tool_call, state):
        try:
            result = await super()._arun_tool(tool_call, state)
            extracted = extract_text_from_mcp_result(result)

            return ToolMessage(
                content=extracted,
                tool_call_id=tool_call["id"],
                name=tool_call["name"]
            )

        except Exception as e:
            return ToolMessage(
                content=f"Tool execution error: {str(e)}",
                tool_call_id=tool_call["id"],
                name=tool_call["name"]
            )


# ------------------------------------------------------------------
# GRAPH CREATION
# ------------------------------------------------------------------
def create_graph(tools: list):

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=OPENAI_API_KEY,
    )

    llm_with_tools = llm.bind_tools(tools)

    # 🔥 STRICT AGENTIC PROMPT (UNCHANGED)
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an agentic AI system.\n"
            "You MUST follow this workflow strictly:\n"
            "1. If user mentions an image path, call the vision tool to extract the main topic.\n"
            "2. Then call the Wikipedia tool using that topic.\n"
            "3. Return a fact-based explanation using Wikipedia data only.\n"
            "Do NOT skip steps. Do NOT hallucinate. Always use tools."
        ),
        MessagesPlaceholder("messages"),
    ])

    chat_llm = prompt | llm_with_tools

    def chat_node(state: State):
        response = chat_llm.invoke({"messages": state["messages"]})
        return {"messages": [response]}

    tool_node = FixedToolNode(tools)

    builder = StateGraph(State)

    builder.add_node("chat", chat_node)
    builder.add_node("tools", tool_node)

    builder.add_edge(START, "chat")

    builder.add_conditional_edges(
        "chat",
        tools_condition,
        {
            "tools": "tools",
            "__end__": END,
        },
    )

    builder.add_edge("tools", "chat")

    return builder.compile(checkpointer=MemorySaver())


# ------------------------------------------------------------------
# AGENT SETUP (RUNS ONCE)
# ------------------------------------------------------------------
async def setup_agent():
    print("🚀 Initializing MCP Client & Tools...")
    client = MultiServerMCPClient(server_configs)
    tools = await client.get_tools()

    print(f"✅ Loaded {len(tools)} tools:")
    for tool in tools:
        print(f"  - {tool.name}")

    agent = create_graph(tools)
    print("🤖 Agent is READY")
    return agent


agent = asyncio.run(setup_agent())


# ------------------------------------------------------------------
# GRADIO UI
# ------------------------------------------------------------------
with gr.Blocks(theme=gr.themes.Default(primary_hue="blue")) as demo:
    gr.Markdown("# 🧠 Image Research Assistant (MCP + LangGraph)")

    chatbot = gr.Chatbot(height=500)



    with gr.Row():
        image_box = gr.Image(type="filepath", label="Upload Image")
        text_box = gr.Textbox(
            label="Ask a question about the image or research topic",
            placeholder="e.g. Describe this image and explain its historical importance",
            scale=2
        )

    submit_btn = gr.Button("Submit", variant="primary")


    async def get_agent_response(user_text, image_path, chat_history):
        if chat_history is None:
            chat_history = []

        # Build user message
        if image_path:
            full_image_path = os.path.abspath(image_path)
            full_message = f"{user_text}\n\nImage path: {full_image_path}"
            chat_history.append({
                "role": "user",
                "content": f"📷 {image_path}\n{user_text}"
            })
        else:
            full_message = user_text
            chat_history.append({
                "role": "user",
                "content": user_text
            })

        try:
            result = await agent.ainvoke(
                {
                    "messages": [
                        HumanMessage(content=full_message)
                    ]
                },
                config={"configurable": {"thread_id": "gradio-session"}}
            )

            last_message = result["messages"][-1]
            bot_reply = last_message.content if last_message.content else "⚠️ No response generated."

        except Exception as e:
            bot_reply = f"❌ Error: {str(e)}"

        chat_history.append({
            "role": "assistant",
            "content": bot_reply
        })

        return "", chat_history, None



    submit_btn.click(
        get_agent_response,
        inputs=[text_box, image_box, chatbot],
        outputs=[text_box, chatbot, image_box]
    )


#demo.launch(server_name="Localhost", server_port=7860)
demo.launch(server_name="0.0.0.0", server_port=7860)
