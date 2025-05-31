#!/usr/bin/env python3
"""
Test script for Anthropic MCP Connector
Tests the MCP connector feature against a remote time server using direct HTTP requests.
"""

import os
import json
import requests
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
    
    # Read MCP server URL from mcp_servers.json
    with open('mcp_servers.json', 'r') as f:
        server_url = f.read().strip()
    
    print(f"Testing MCP Connector with server: {server_url}")
    print("=" * 60)
    
    # Configure MCP server
    mcp_servers = [
        {
            "type": "url",
            "url": server_url,
            "name": "time-server"
        }
    ]
    
    # API endpoint and headers
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key,
        "anthropic-version": "2023-06-01",
        "anthropic-beta": "mcp-client-2025-04-04"
    }
    
    # Test 1: Ask what tools are available
    print("\n🔍 Test 1: Discovering available tools")
    print("-" * 40)
    
    payload1 = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1000,
        "messages": [
            {"role": "user", "content": "What tools do you have available from the MCP servers?"}
        ],
        "mcp_servers": mcp_servers
    }
    
    response1 = requests.post(url, headers=headers, json=payload1)
    
    if response1.status_code == 200:
        result1 = response1.json()
        print("Response:", result1["content"][0]["text"])
    else:
        print(f"Error {response1.status_code}: {response1.text}")
        return
    
    # Test 2: Get current time
    print("\n⏰ Test 2: Getting current time")
    print("-" * 40)
    
    payload2 = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1000,
        "messages": [
            {"role": "user", "content": "What is the current time in Austin, TX? Use the time server tools."}
        ],
        "mcp_servers": mcp_servers
    }
    
    response2 = requests.post(url, headers=headers, json=payload2)
    
    if response2.status_code == 200:
        result2 = response2.json()
        # Display response content including tool use blocks
        for content_block in result2["content"]:
            if content_block["type"] == "text":
                print("Text response:", content_block["text"])
            elif content_block["type"] == "mcp_tool_use":
                print(f"🔧 MCP Tool Use:")
                print(f"  - Tool: {content_block['name']}")
                print(f"  - Server: {content_block['server_name']}")
                print(f"  - Input: {content_block['input']}")
            elif content_block["type"] == "mcp_tool_result":
                print(f"📊 MCP Tool Result:")
                print(f"  - Tool Use ID: {content_block['tool_use_id']}")
                print(f"  - Is Error: {content_block['is_error']}")
                print(f"  - Content: {content_block['content']}")
    else:
        print(f"Error {response2.status_code}: {response2.text}")
        return
    
    # Test 3: Convert time between timezones
    print("\n🌍 Test 3: Converting time between timezones")
    print("-" * 40)
    
    payload3 = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1000,
        "messages": [
            {"role": "user", "content": "Convert the current time from America/New_York to America/Chicago (Austin, TX timezone) using the time server tools."}
        ],
        "mcp_servers": mcp_servers
    }
    
    response3 = requests.post(url, headers=headers, json=payload3)
    
    if response3.status_code == 200:
        result3 = response3.json()
        # Display response content
        for content_block in result3["content"]:
            if content_block["type"] == "text":
                print("Text response:", content_block["text"])
            elif content_block["type"] == "mcp_tool_use":
                print(f"🔧 MCP Tool Use:")
                print(f"  - Tool: {content_block['name']}")
                print(f"  - Server: {content_block['server_name']}")
                print(f"  - Input: {content_block['input']}")
            elif content_block["type"] == "mcp_tool_result":
                print(f"📊 MCP Tool Result:")
                print(f"  - Tool Use ID: {content_block['tool_use_id']}")
                print(f"  - Is Error: {content_block['is_error']}")
                print(f"  - Content: {content_block['content']}")
    else:
        print(f"Error {response3.status_code}: {response3.text}")
        return
    
    print("\n✅ MCP Connector testing completed!")

if __name__ == "__main__":
    main()
