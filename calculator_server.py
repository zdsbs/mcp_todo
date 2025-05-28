from mcp.server.fastmcp import FastMCP
from typing import Any
import os
import datetime

mcp = FastMCP("Calculator")

chat_history = []

@mcp.tool()
def calculator(operation: str, num1: float, num2: float) -> float:
    """A tool to perform basic arithmetic operations: add, subtract, multiply, divide."""
    if operation == "add":
        return num1 + num2
    elif operation == "subtract":
        return num1 - num2
    elif operation == "multiply":
        return num1 * num2
    elif operation == "divide":
        if num2 == 0:
            raise ValueError("Cannot divide by zero")
        return num1 / num2
    else:
        raise ValueError("Invalid operation")

@mcp.tool()
def store_chat_info(info: Any, context: str) -> str:
    """
    Stores information and context about the current chat session.

    Appends the provided info and context, along with a timestamp, to the in-memory chat history and writes the updated history to a markdown file.

    Args:
        info (Any): Information to store. Can be a string, list, or dictionary.
            - For code snippets, use a dict with keys: 'summary', 'code', and optionally 'language'.
            - For summary tables, use either a markdown string or a list of dicts/lists.
        context (str): Description of the context or purpose of the info.

    Returns:
        str: Confirmation message with the total number of stored items.

    Side Effects:
        - Appends to the global chat_history list.
        - Updates (appends to) the 'chat_history.md' file.

    Example:
        info = {
            'summary': 'Example Python function.',
            'code': 'def hello():\n    print("Hello, world!")',
            'language': 'python'
        }
        context = 'Demonstrating code snippet storage.'
        store_chat_info(info, context)
        
    Example:
        info = [
            {'heading': 'Short Title', 'content': 'Detailed explanation or suggestion'},
            {'heading': 'Short Title', 'content': 'Detailed explanation or suggestion'}
        ]
        context = 'Description of the context or purpose of the info.'
        store_chat_info(info, context)

    Example:
        info = [
            {'suggestion': 'Short Title', 'current': 'description of the current functionality', 'suggestion': 'Detailed explanation or suggestion'},
            {'suggestion': 'Short Title', 'current': 'description of the current functionality', 'suggestion': 'Detailed explanation or suggestion'}
        ]
        context = 'Description of the context or purpose of the info.'
        store_chat_info(info, context)
    """
    timestamp = datetime.datetime.now().isoformat()
    entry = {"info": info, "context": context, "timestamp": timestamp}
    print(f"[CHAT INFO] Info: {repr(info)} | Context: {context} | Timestamp: {timestamp}")
    chat_history.append(entry)
    write_chat_history_markdown(entry)  # Always update the markdown file
    return f"Info and context stored. Total items: {len(chat_history)}"

# Helper function to write markdown tables from a list of dicts
def write_markdown_table_from_dicts(table: list) -> str:
    if not table:
        return ""
    headers = table[0].keys()
    lines = ["| " + " | ".join(headers) + " |"]
    lines.append("|" + "|".join(["-" * (len(h) + 2) for h in headers]) + "|")
    for row in table:
        lines.append("| " + " | ".join(str(row[h]) for h in headers) + " |")
    return "\n".join(lines)

def format_timestamp(iso_timestamp: str) -> str:
    """Format an ISO timestamp string into a pretty, human-readable string."""
    try:
        dt = datetime.datetime.fromisoformat(iso_timestamp)
        return dt.strftime('%A, %B %d, %Y, %H:%M:%S')
    except Exception:
        return iso_timestamp

def get_info_type(info: Any) -> str:
    """Determine the type of the info object for formatting purposes."""
    if isinstance(info, list):
        if info and isinstance(info[0], dict):
            return "list_of_dicts"
        else:
            return "list"
    elif isinstance(info, dict):
        return "dict"
    elif isinstance(info, str):
        return "str"
    else:
        return "unknown"

def format_chat_history_entry(entry: dict, entry_number: int) -> str:
    """Format a single chat history entry as a markdown string."""
    lines = [f"## Entry {entry_number}\n"]
    if "timestamp" in entry:
        pretty_time = format_timestamp(entry['timestamp'])
        lines.append(f"**Timestamp:** {pretty_time}\n\n")
    lines.append(f"**Context:** {entry['context']}\n\n")
    lines.append("**Info:**\n\n")
    info_type = get_info_type(entry["info"])
    if info_type == "list_of_dicts":
        table_md = write_markdown_table_from_dicts(entry["info"])
        lines.append(table_md + "\n\n")
    elif info_type == "list":
        for item in entry["info"]:
            if isinstance(item, dict):
                for k, v in item.items():
                    lines.append(f"- **{k.capitalize()}**: {v}\n")
                lines.append("\n")
            else:
                lines.append(f"- {item}\n")
        lines.append("\n")
    elif info_type == "dict":
        for k, v in entry["info"].items():
            lines.append(f"- **{k.capitalize()}**: {v}\n")
        lines.append("\n")
    elif info_type == "str":
        lines.append(f"{entry['info']}\n\n")
    else:
        lines.append(f"[Unrecognized info type: {type(entry['info']).__name__}]\n\n")
    return "".join(lines)

def write_chat_history_markdown(entry: dict, filename: str = "chat_history.md") -> str:
    """Append a single chat history entry to a markdown file, nicely formatted."""
    print(f"entry: {entry}")
    file_exists = os.path.exists(filename)
    with open(filename, "a") as f:
        if not file_exists:
            f.write("# Chat History\n\n")
        entry_md = format_chat_history_entry(entry, 1)
        f.write(entry_md)
    return f"Entry appended to {filename}"

@mcp.prompt("joke")
async def joke(text: str) -> list[dict]:
    """Tells a joke."""
    print(f"[SUMMARY] {text}")
    return [
        {"role": "system", "content": "You are a helpful assistant skilled at telling jokes."},
        {"role": "user", "content": f"Please tell a joke about the following text:\n\n{text}"}
    ]

if __name__ == "__main__":
    mcp.run(transport="streamable-http") 