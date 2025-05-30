# MCP Todo Server

A simple MCP (Modular Command Platform) server for chat history management and information tracking. This project is designed to integrate with AI assistants like Claude to provide enhanced functionality.

## Features

- 📝 Chat history management with timestamp tracking
- 🔄 Tool list tracking for AI operations
- 🎨 Command-line logging of chat operations
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
store_chat_info(info, context, tool_list)
```

Parameters:
- `info`: Any data that needs to be stored (text, dictionaries, lists, etc.)
- `context`: String describing the context of the stored information
- `tool_list`: List of tools available for the current operation

## Project Structure

```
.
├── calculator_server.py   # Main server implementation
├── requirements.txt      # Project dependencies
├── chat_history.md      # Generated chat history
├── .gitignore          # Git ignore rules
└── README.md           # This file
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