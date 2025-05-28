# MCP Calculator Server

This project provides a simple MCP (Modular Command Platform) server for calculator operations and chat history management. It is designed to be easily integrated with tools like Cursor and can be extended for more advanced automation and documentation workflows.

## Features

- 🧮 Basic calculator operations (add, subtract, multiply, divide)
- 📝 Chat history management with markdown formatting
- 🔄 Automatic timestamp handling and pretty formatting
- 📊 Support for various data structures (lists, dictionaries, tables)
- 🎨 Beautiful markdown output for chat logs

## System Requirements

- Python 3.8 or newer
- pip (Python package manager)
- macOS, Linux, or Windows (tested on macOS)

## Installation

1. Clone this repository:
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
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

The server will start and listen for incoming requests.

### Available Operations

#### Calculator
```python
# Example calculator operations
calculator("add", 5, 3)      # Returns: 8
calculator("multiply", 4, 2)  # Returns: 8
calculator("divide", 10, 2)   # Returns: 5
```

#### Chat History
```python
# Store simple text
store_chat_info("Hello, world!", "Greeting message")

# Store structured data
info = {
    'summary': 'Example function',
    'code': 'print("Hello")',
    'language': 'python'
}
store_chat_info(info, "Code example")
```

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

### Code Style

- Follow PEP 8 guidelines
- Use type hints where possible
- Include docstrings for all functions and classes
- Keep functions focused and single-purpose

### Testing

(Coming soon)

## TODOs

- [ ] Document how to start the MCP server & integrate with Cursor, including some screen grabs
- [ ] Improve the debugging so we can get better insight into how we're getting called from the LLM
- [ ] Research and experiment with different doc strings

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [FastMCP](link-to-fastmcp)
- Inspired by the need for better LLM integration tools

---