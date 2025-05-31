#!/usr/bin/env python3
"""
Debug test to isolate the MCP server time conversion issue
"""

import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime
import pytz

def main():
    load_dotenv()
    
    api_key = os.getenv('ANTHROPIC_API_KEY')
    
    with open('mcp_servers.json', 'r') as f:
        server_url = f.read().strip()
    
    mcp_servers = [{"type": "url", "url": server_url, "name": "time-server"}]
    
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key,
        "anthropic-version": "2023-06-01",
        "anthropic-beta": "mcp-client-2025-04-04"
    }
    
    # Let's test direct timezone queries
    print("=== DEBUGGING MCP TIME SERVER ===")
    
    # Test 1: Get current time in America/Chicago directly
    print("\n1. Direct query for America/Chicago time:")
    payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 500,
        "messages": [{"role": "user", "content": "Get the current time in America/Chicago timezone"}],
        "mcp_servers": mcp_servers
    }
    
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    
    for content_block in result["content"]:
        if content_block["type"] == "mcp_tool_result":
            print(f"MCP Result: {content_block['content']}")
    
    # Test 2: Let's also check what Python thinks the time should be
    print("\n2. Python's calculation of current times:")
    utc_now = datetime.now(pytz.UTC)
    ny_now = utc_now.astimezone(pytz.timezone('America/New_York'))
    chicago_now = utc_now.astimezone(pytz.timezone('America/Chicago'))
    
    print(f"UTC time: {utc_now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"New York time: {ny_now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Chicago time: {chicago_now.strftime('%Y-%m-%d %H:%M:%S')}")
    
    print(f"\nTime difference: NY is {(ny_now.utcoffset().total_seconds() - chicago_now.utcoffset().total_seconds()) / 3600} hours ahead of Chicago")

if __name__ == "__main__":
    main()
