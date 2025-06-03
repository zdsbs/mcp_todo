from mcp.server.fastmcp import FastMCP
from typing import Any
import os
import datetime
import logging
import traceback
import json
import re  # Import the regular expression module

mcp = FastMCP("stuff")

@mcp.tool()
def store_chat_info(model_name: str, conversation_history: list) -> str:
    """
    Stores the assistant's most recent response and chat metadata.
    Also automatically appends the last assistant message to a markdown file.

    Parameters:
    - model_name: Name of the LLM used
    - conversation_history: The full message history

    Automatically infers 'info' from the last assistant message.
    """
    try:
        # Create a directory for chat history if it doesn't exist
        os.makedirs("chat_history", exist_ok=True)

        # Define the filename for the conversation history
        filename = "chat_history/conversation_history.json"

        # Read existing conversation history
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                existing_data = json.load(f)
        else:
            existing_data = []

        # Calculate the next ID based on existing data
        next_id = 1
        if existing_data:
            next_id = max(msg.get("id", 0) for msg in existing_data) + 1

        # Process only the messages we received (should be limited)
        new_messages = []
        for message in conversation_history:
            # Check if this message content is already in existing_data to avoid duplicates
            is_duplicate = False
            for existing_msg in existing_data:
                if (existing_msg.get("role") == message.get("role") and 
                    existing_msg.get("content") == message.get("content")):
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                message_copy = message.copy()  # Create a copy to avoid modifying the original
                message_copy["id"] = next_id
                new_messages.append(message_copy)
                next_id += 1

        # Append only new messages to existing data
        existing_data.extend(new_messages)

        with open(filename, 'w') as f:
            json.dump(existing_data, f, indent=4)

        logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
        logging.info(f"New Messages: {len(new_messages)}")
        
        # Automatically append the last assistant message to the markdown file
        markdown_file = "chat_history/assistant_responses_archive.md"
        
        # Only call append_last_assistant_message if we added new messages
        if new_messages:
            append_last_assistant_message(filename, markdown_file)
            return f"Conversation history stored and last assistant message appended to markdown ({len(new_messages)} new messages)"
        else:
            return "No new messages to store"
    except Exception as e:
        logging.error(f"Failed to store conversation history: {e}\n{traceback.format_exc()}")
        return f"Error: {e}"

def append_last_assistant_message(input_filename: str, output_filename: str) -> None:
    """
    Finds the last assistant message from the conversation history and appends it to a text file.
    Formats the output in a human-readable markdown format.
    Only appends the message if its ID is not already in the markdown file.
    
    Parameters:
    - input_filename: The path to the JSON file containing the conversation history.
    - output_filename: The path to the text file where the last assistant message will be appended.
    """
    try:
        # Ensure the directory for the output file exists
        output_dir = os.path.dirname(output_filename)
        os.makedirs(output_dir, exist_ok=True)
        
        # Read the conversation history from the input file
        with open(input_filename, 'r') as f:
            conversation_history = json.load(f)
        
        # Find the last assistant message
        last_assistant_message = None
        last_user_message = None
        
        # First get the last assistant message
        for message in reversed(conversation_history):
            if message['role'] == 'assistant':
                last_assistant_message = message
                break
        
        if not last_assistant_message:
            print("No assistant messages found in the conversation history.")
            return
            
        # Get the message ID - we'll use this to check if it's already in the file
        message_id = last_assistant_message.get('id', 0)
        
        # Check if this message ID is already in the file
        if os.path.exists(output_filename):
            with open(output_filename, 'r') as f:
                existing_content = f.read()
                
                # Look for a pattern like "<!-- Message ID: X -->" in the file
                id_pattern = f"<!-- Message ID: {message_id} -->"
                if id_pattern in existing_content:
                    print(f"Message with ID {message_id} already exists in the file. Skipping.")
                    return
        
        # Then try to find the user message that preceded it
        if message_id > 1:
            # Find the message that came before this one (likely the user question)
            for message in conversation_history:
                if message['role'] == 'user' and message.get('id', 0) == message_id - 1:
                    last_user_message = message
                    break
        
        # Format the timestamp in a more readable format
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Start building the markdown output
        markdown = f"# Chat Excerpt ({timestamp})\n\n"
        
        # Add a hidden comment with the message ID for future reference
        markdown += f"<!-- Message ID: {message_id} -->\n\n"
        
        # Include the user's question if found
        if last_user_message:
            user_content = last_user_message['content']
            # Check if content has user_query tags
            user_query_match = re.search(r'<user_query>\s*(.*?)\s*</user_query>', user_content, re.DOTALL)
            if user_query_match:
                user_content = user_query_match.group(1).strip()
            
            markdown += f"## Question\n\n{user_content}\n\n"
        
        # Format the assistant's response
        content = last_assistant_message['content']
        
        # Format code blocks properly for markdown
        # Look for code blocks indicated by triple backticks
        content = re.sub(r'```(\w*)\n(.*?)```', r'```\1\n\2\n```', content, flags=re.DOTALL)
        
        markdown += f"## Answer\n\n{content}\n\n"
        markdown += f"---\n\n"
        
        # Append the markdown to the output file
        with open(output_filename, 'a') as out_file:
            out_file.write(markdown)
            
        print(f"Last assistant message (ID: {message_id}) appended to {output_filename} in markdown format")
            
    except FileNotFoundError:
        print(f"Error: The file {input_filename} does not exist.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the file.")
    except Exception as e:
        print(f"An error occurred while appending to the file: {e}")

# Example usage
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
