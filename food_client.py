#!/usr/bin/env python
# coding: utf-8

import os
import asyncio
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Setup model 
model = init_chat_model("openai:gpt-4o-mini")

# MCP client
client = MultiServerMCPClient(
    {
        "FoodServices": {
            "command": "python",
            "args": ["./server.py"],
            "transport": "stdio",
        },
    }
)

#
async def setup_graph():
    tools = await client.get_tools()
    llm_with_tools = model.bind_tools(tools)

    ASSISTANT_PROMPT = """
You are a helpful food ordering assistant for a CLI/terminal experience. You can NOT place orders yourself, but you help via these tools:

1) food_search(food_name, restaurant_name)
2) cancel_order(order_id, phone_number)
3) comment_order(order_id, person_name, comment)
4) check_order_status(order_id)

Rules for multi-turn chat in terminal:
- Use conversation memory (previous turns) to resolve short replies. If the user previously indicated an intent (e.g., "check status") and then provides just a number like "87", assume it's the missing order_id and proceed.
- If information is still ambiguous, ask a concise follow-up question. DO NOT repeat questions already answered (e.g., if the user said "any restaurant", don't ask again).
- Never guess required fields; collect them. Do interpret terse follow-ups in context.
- After each tool call, summarize the result briefly and clearly.
- Only say: "Sorry, I can only help with food orders and related services." when the message is truly unrelated. Do NOT say this for numeric-only messages—those are likely IDs.
""".strip()

    def _assistant_node(state: MessagesState):
        output = llm_with_tools.invoke(
            [SystemMessage(content=ASSISTANT_PROMPT)] + state["messages"]
        )
        return {"messages": [output]}

    builder = StateGraph(MessagesState)
    builder.add_node("assistant", _assistant_node)
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", tools_condition)
    builder.add_edge("tools", "assistant")

    memory = MemorySaver()
    return builder.compile(checkpointer=memory)

# Chat loop 
async def main():
    GRAPH = await setup_graph()
    print("Food Assistant Chat (type 'exit' to quit)\n")
    thread_id = "user-1"

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye")
            break

        response = await GRAPH.ainvoke(
            {"messages": user_input},
            config={"configurable": {"thread_id": thread_id}}
        )

        if response and "messages" in response:
            last_msg = response["messages"][-1].content
            print(f"Assistant: {last_msg}\n")

if __name__ == "__main__":
    asyncio.run(main())
