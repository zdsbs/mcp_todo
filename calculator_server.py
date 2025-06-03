from mcp.server.fastmcp import FastMCP
from typing import Any
import os
import datetime
import logging
import traceback
import json

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
        last_response = conversation_history[-1]["content"]
        timestamp = datetime.datetime.now().isoformat()

        info = {
            "agent_response": last_response,
            "timestamp": timestamp,
            "model_name": model_name
        }

        # Create a directory for chat history if it doesn't exist
        os.makedirs("chat_history", exist_ok=True)

        # Define the filename for the conversation history
        filename = "chat_history/conversation_history.json"

        # Assign unique IDs to each message in the conversation history
        for index, message in enumerate(conversation_history):
            message["id"] = index + 1  # Unique ID based on index (1-based)

        if os.path.exists(filename):
            with open(filename, 'r') as f:
                existing_data = json.load(f)
        else:
            existing_data = []

        # Extract existing IDs from the existing data
        existing_ids = {msg["id"] for msg in existing_data}

        # Filter out messages with IDs that already exist
        new_messages = [msg for msg in conversation_history if msg["id"] not in existing_ids]

        # Append only new messages to existing data
        existing_data.extend(new_messages)

        with open(filename, 'w') as f:
            json.dump(existing_data, f, indent=4)

        logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
        logging.info(f"[CHAT INFO] Info: {info} | New Messages: {new_messages}")
        return "Conversation history stored"
    except Exception as e:
        logging.error(f"Failed to store conversation history: {e}\n{traceback.format_exc()}")
        return f"Error: {e}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http") 
