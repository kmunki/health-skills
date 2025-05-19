# Health Assist

A personal health narrative tracking system using Model Context Protocol (MCP).

## Overview

Health Assist helps users track their personal health story through natural conversation. Unlike official health records, this captures the user's own narrative - the way they experience and remember their health journey.

## Architecture

```
health-assist/
├── file-ops-mcp/       # MCP server for file operations
├── health-assist/      # Main project directory
│   └── workspace/      # User health data (git-ignored)
│       ├── narratives/    # Human-readable health stories
│       ├── structured/    # JSON-formatted health events
│       └── conversations/ # Chat logs with AI
└── README.md
```

## Key Features

- Natural conversation interface through Claude
- Dual storage: narrative (human-readable) and structured (JSON)
- Local-first: all data stays on your machine
- Privacy-focused: no cloud storage or external APIs

## Setup

1. Install the MCP server:
   ```bash
   cd file-ops-mcp
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install "mcp[cli]"
   ```

2. Configure Claude Desktop (update paths as needed):
   ```json
   {
     "mcpServers": {
       "file-ops": {
         "command": "/path/to/file-ops-mcp/venv/bin/python",
         "args": ["/path/to/file-ops-mcp/server.py"],
         "env": {
           "HEALTH_ASSIST_WORKSPACE": "/path/to/health-assist/workspace"
         }
       }
     }
   }
   ```

3. Restart Claude Desktop

## Privacy Note

All health data is stored locally in the `workspace` directory and is excluded from version control. This is YOUR personal health information - keep it secure and back it up appropriately.

## Development

This project uses MCP (Model Context Protocol) to enable Claude to manage health narratives through file operations while maintaining user privacy and data ownership.