# MCP Todo Server

A simple MCP (Modular Command Platform) server for chat history management and information tracking. This project is designed to integrate with AI assistants like Claude to provide enhanced functionality.

## Features

- 📝 Chat history management with timestamp and model tracking
- 📦 Stores chat history in both JSON and Markdown formats
- 🗂️ Pretty-formatted, human-readable chat history archive
- 🆔 Message deduplication and unique ID tracking
- 🔄 Tool list tracking for AI operations
- 🎨 Command-line logging of chat operations (with improved logging setup)
- 🚀 Built on FastMCP for easy integration

## System Requirements

- Python 3.8 or newer
- pip (Python package manager)
- macOS, Linux, or Windows (tested on macOS)

## Installation

1. Clone this repository:
   ```bash
   git clone <your-repo-url>
   cd mcp_todo
   ```
2. (Recommended) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Starting the Server

```bash
python calculator_server.py
```

The server will start and listen for incoming requests on the default port.

### Available Operations

#### Store Chat Information
```python
# Store information about the current chat
store_chat_info(model_name, conversation_history)
```

Parameters:
- `model_name`: Name of the LLM used
- `conversation_history`: List of recent messages (each with role, content, etc.)

> **Note:** Only the last few messages are needed for efficient storage and archiving.

## Output Files

- `chat_history/conversation_history.json`: Full conversation history with metadata (role, content, timestamp, model name, unique ID)
- `chat_history/assistant_responses_archive.md`: Chronological archive of assistant responses and user questions in markdown

## Metadata Stored

Each message includes:
- `role`: user or assistant
- `content`: The message text
- `timestamp`: When the message was stored
- `model_name`: Which AI model generated the response
- `id`: Unique message ID

## Example Markdown Output

```
# Chat Excerpt (2025-06-03 15:08:18)

<!-- Message ID: 36 -->

## Question

give advice to make the code prettier

## Answer

Here are some suggestions to make your code prettier and more maintainable:

1. Add type hints consistently throughout the code, especially for function parameters and return values.
2. Extract regex patterns as constants at the module level to improve readability.
...

---
```

## Project Structure

```
.
├── calculator_server.py   # Main server implementation
├── requirements.txt      # Project dependencies
├── chat_history/         # Generated chat history and logs
│   ├── conversation_history.json
│   └── assistant_responses_archive.md
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Development

### Future Enhancements

- Extend the functionality with additional MCP tools
- Add persistent storage for chat history
- Implement user authentication
- Create a web interface for easier interaction

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [FastMCP](https://github.com/mcp-team/fastmcp) framework
- Designed for integration with Claude and other AI assistants

---