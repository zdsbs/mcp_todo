from mcp.server.fastmcp import FastMCP
from typing import Any
import os
import datetime
import logging
import traceback

mcp = FastMCP("stuff")

@mcp.tool()
def store_chat_info(info: Any, context: str, model_name: str, conversation_history: Any) -> str:
    """
    Stores information and context about the current chat session and the tool_list
    """
    try:
        timestamp = datetime.datetime.now().isoformat()
        logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
        logging.info(f"[CHAT INFO] Info: {info} | Context: {context} | Timestamp: {timestamp} | Model Name: {model_name} | Conversation History: {conversation_history}")
        return "Chat info stored"
    except Exception as e:
        logging.error(f"Failed to store chat info: {e}\n{traceback.format_exc()}")
        return f"Error: {e}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http") 