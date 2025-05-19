# Health Assist

A simple, human-readable health narrative tracking system using Model Context Protocol (MCP).

## Overview

Health Assist helps users track their personal health story through natural conversation with Claude. It captures health narratives in a simple, file-based system with human-readable naming.

## Architecture

```
Health Assist/
├── health-mcp/         # MCP server for health tracking
│   ├── server.py
│   ├── requirements.txt
│   └── venv/
├── workspace/          # User health data (git-ignored)
│   ├── narratives/    # Human-readable health stories
│   │   └── {user}/
│   │       ├── 2025-01-19-gas-issues.md
│   │       └── 2025-01-20-supplements.md
│   └── structured/    # JSON-formatted health data
│       └── {user}/
│           ├── 2025-01-19-gas-issues.json
│           └── 2025-01-20-supplements.json
└── README.md
```

## Key Features

- **Human-Readable**: Files use simple `date-topic` naming (e.g., `2025-01-19-gas-issues`)
- **Simple Storage**: Each health note is a separate file, no complex databases
- **Dual Format**: Narratives in Markdown, structured data in JSON
- **Natural Conversation**: Talk naturally with Claude about your health
- **Privacy-First**: All data stays local on your machine

## Available Tools

The MCP server provides 5 simple tools:

1. **`save_health_note`** - Save a health observation with a topic
2. **`read_health_notes`** - Read recent health notes (with optional topic filter)
3. **`update_health_note`** - Add structured data to an existing note
4. **`find_health_topics`** - List all health topics you've discussed
5. **`get_health_note`** - Get a specific health note by filename

## Setup

1. Install the MCP server:
   ```bash
   cd health-mcp
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Configure Claude Desktop by editing `~/Library/Application Support/Claude/claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "health-narrative": {
         "command": "/path/to/Health Assist/health-mcp/venv/bin/python",
         "args": ["/path/to/Health Assist/health-mcp/server.py"],
         "env": {
           "HEALTH_ASSIST_WORKSPACE": "/path/to/Health Assist/workspace"
         }
       }
     }
   }
   ```

3. Restart Claude Desktop

## Usage Examples

Simply chat with Claude about your health:

- "I've been having gas issues lately"
- "Started taking magnesium for sleep"
- "What did I say about my cholesterol?"
- "Show me all my supplement notes"

Claude will automatically save your health observations with appropriate topics and dates.

## Privacy Note

All health data is stored locally in the `workspace` directory and is excluded from version control. This is YOUR personal health information - keep it secure and back it up appropriately.

## Philosophy

This project embraces simplicity over complexity. Instead of complex schemas and databases, it uses:
- Simple files with readable names
- Claude's intelligence for searching and filtering
- Minimal structure, maximum flexibility

The goal is to make health tracking as natural as having a conversation.