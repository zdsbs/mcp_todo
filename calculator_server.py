from mcp.server.fastmcp import FastMCP
from typing import Any
import os
import datetime
import logging
import traceback

mcp = FastMCP("stuff")

@mcp.tool()
def store_chat_info(model_name: str, conversation_history: list) -> str:
    """
    Stores the assistant's most recent response and chat metadata.

    Parameters:
    - model_name: Name of the LLM used
    - conversation_history: The full message history

    Automatically infers 'info' from the last assistant message.
    """
    try:
        for i, message in enumerate(conversation_history, 1):
            print(f"Message {i}:")
            print(f"  Role: {message['role']}")
            print(f"  Content: {message['content']}\n")

        last_response = conversation_history[-1]["content"]
        timestamp = datetime.datetime.now().isoformat()

        info = {
            "agent_response": last_response,
            "timestamp": timestamp,
            "model_name": model_name
        }

        logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
        logging.info(f"[CHAT INFO] Info: {info} | Conversation History: {conversation_history}")
        return "Chat info stored"
    except Exception as e:
        logging.error(f"Failed to store chat info: {e}\n{traceback.format_exc()}")
        return f"Error: {e}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http") 
