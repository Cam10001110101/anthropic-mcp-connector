# Anthropic MCP Connector Test Scripts

Test scripts demonstrating the [Anthropic MCP Connector](https://docs.anthropic.com/en/docs/agents-and-tools/mcp-connector) feature, which enables direct connection to remote MCP servers from the Messages API without a separate MCP client.

## Overview

This repository contains both Python and TypeScript implementations that test the MCP Connector against a remote time server, demonstrating:

- **Tool Discovery**: Listing available MCP tools
- **Tool Execution**: Using MCP tools through the Messages API
- **Multiple Tool Calls**: Executing multiple tools in sequence
- **New Content Types**: Handling `mcp_tool_use` and `mcp_tool_result` blocks

## Features Tested

- ✅ **Direct API Integration**: Connect to MCP servers without implementing an MCP client
- ✅ **Tool Calling Support**: Access MCP tools through the Messages API  
- ✅ **Multiple Servers**: Support for connecting to multiple MCP servers
- ✅ **Beta Feature**: Uses the required `anthropic-beta: mcp-client-2025-04-04` header

## Files

### Test Scripts
- **`test_mcp_connector.py`** - Python implementation using direct HTTP requests
- **`test-mcp-connector.ts`** - TypeScript implementation using the Anthropic SDK

### Configuration
- **`mcp_servers.json`** - MCP server URL configuration
- **`.env`** - Environment variables (API key)
- **`package.json`** - Node.js dependencies for TypeScript version
- **`pyproject.toml`** - Python dependencies

### Debug & Documentation
- **`debug_time_test.py`** - Debug script for isolating server issues
- **`README.md`** - This documentation

## Prerequisites

1. **Anthropic API Key**: Get one from [Anthropic Console](https://console.anthropic.com/)
2. **Python 3.9+** (for Python version)
3. **Node.js 18+** (for TypeScript version)

## Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd anthropic-mcp-connector
```

### 2. Environment Variables
Create a `.env` file:
```bash
ANTHROPIC_API_KEY=your_api_key_here
```

### 3. Python Setup
```bash
# Using uv (recommended)
uv pip install -r pyproject.toml

# Or using pip
pip install anthropic python-dotenv pytz requests
```

### 4. TypeScript Setup
```bash
npm install
```

## Usage

### Python Version
```bash
python test_mcp_connector.py
```

### TypeScript Version
```bash
npm run test
# or
npm run dev  # with watch mode
```

## Sample Output

```
Testing MCP Connector with server: https://mcp-server-http-time.mcpcentral.io
============================================================

🔍 Test 1: Discovering available tools
----------------------------------------
Response: Based on the available tools, I have access to a time server with the following functions:

## Time Server Tools
1. **current_time** - Get the current time
2. **relative_time** - Get relative time from now
3. **days_in_month** - Get days in a specific month
4. **get_timestamp** - Convert date/time to timestamp
5. **convert_time** - Convert time between timezones
6. **get_week_year** - Get week number and ISO week

⏰ Test 2: Getting current time
----------------------------------------
Text response: I'll get the current time for you using the time server.
🔧 MCP Tool Use:
  - Tool: current_time
  - Server: time-server
  - Input: {}
📊 MCP Tool Result:
  - Tool Use ID: mcptoolu_01E52bdMGmqrEqdfeQvXLxLU
  - Is Error: False
  - Content: [{'type': 'text', 'text': 'Current UTC time is 2025-05-31 04:23:31'}]

🌍 Test 3: Converting time between timezones
----------------------------------------
[Multiple tool calls demonstrating timezone conversion...]

✅ MCP Connector testing completed!
```

## MCP Server Configuration

The test scripts connect to a time server that provides various time-related tools:

```json
{
  "type": "url",
  "url": "https://mcp-server-http-time.mcpcentral.io",
  "name": "time-server"
}
```

## Key Technical Implementation

### Python Implementation
- Uses direct HTTP requests to the Messages API
- Includes proper error handling and status code checks
- Demonstrates manual parsing of MCP content blocks

### TypeScript Implementation  
- Uses the official Anthropic SDK with beta headers
- Includes comprehensive TypeScript interfaces for type safety
- Demonstrates modern async/await patterns

### MCP Content Blocks

Both implementations handle the new MCP-specific content types:

```typescript
interface MCPToolUse {
  type: 'mcp_tool_use';
  id: string;
  name: string;
  server_name: string;
  input: Record<string, any>;
}

interface MCPToolResult {
  type: 'mcp_tool_result';
  tool_use_id: string;
  is_error: boolean;
  content: Array<{ type: string; text?: string; [key: string]: any }>;
}
```

## Testing Different Scenarios

You can modify the test scripts to test various scenarios:

1. **Different MCP Servers**: Update `mcp_servers.json` with your server URL
2. **Authentication**: Add `authorization_token` to the server configuration
3. **Multiple Servers**: Add multiple server objects to the `mcp_servers` array
4. **Different Models**: Change the model parameter to test with different Claude versions

## Limitations

- Currently only tool calls are supported (not resources)
- Server must be publicly accessible via HTTP
- Local STDIO servers are not supported
- Not available on Amazon Bedrock or Google Vertex

## Troubleshooting

### Common Issues

1. **"TypeError: Messages.create() got an unexpected keyword argument 'mcp_servers'"**
   - Ensure you're using Anthropic SDK version 0.52.1 or later
   - Verify the beta header is included

2. **Connection Errors**
   - Check that the MCP server URL is accessible
   - Verify the server supports the required transport type

3. **Authentication Errors**
   - Ensure your API key is correctly set in `.env`
   - Check that you have access to the beta feature

## Contributing

Feel free to submit issues or pull requests to improve these test scripts or add support for additional MCP server types.

## License

MIT License - feel free to use and modify as needed.
