from mcp.server.fastmcp import FastMCP
from typing import Any
import os
import datetime
import logging
import traceback

mcp = FastMCP("stuff")

#TODO: 
# - storing in memory all the chat history
# - - you might have to have an eye forward to printing (what metadata might you want to have in memory?)
# - - - There are a few ways you could do this? 1) timestampts 2) you could mutate the history with a printed flag 3) you could have a history of what's been printed
# - - - There's a data structure here to track what's been printed and what's not
# - printing out the history so that we're not duplicating anything and not missing anything
# - - you'll have to know what's been printed vs in the in memory history
# - make it pretty
# - - CHALLENGE: don't rerun the server all the time to see if you're making it pretty or not? Save off the history RAW so you can recontrsutct the objects. Then iterate on prettness.
# - IN GENERAL KEEP IT CLEAN AND SIMPLE


# today how do we test?
# 1) We make the change
# 2) We retart the server
# 3) we restart the MCP tool
# 4) tytpe in prompt one to get it to give suggestions
# 5) we type in the prompt "store chat info"
# 6) we see the output

# when you test is it pretty? Do you need to go through steps 1-6?
# NO you don't need to do that? You need to write out the objects to disk and then write a new script that will read them in and try to make it pretty

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
