#!/usr/bin/env tsx
/**
 * Test script for Anthropic MCP Connector (TypeScript)
 * Tests the MCP connector feature against a remote time server.
 */

import fs from 'fs';
import { config } from 'dotenv';
import Anthropic from '@anthropic-ai/sdk';

// Load environment variables
config();

interface MCPServer {
  type: 'url';
  url: string;
  name: string;
  authorization_token?: string;
}

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

interface TextContent {
  type: 'text';
  text: string;
}

type ContentBlock = TextContent | MCPToolUse | MCPToolResult;

async function main(): Promise<void> {
  // Get API key
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    throw new Error('ANTHROPIC_API_KEY not found in environment variables');
  }

  // Initialize Anthropic client
  const anthropic = new Anthropic({
    apiKey: apiKey,
    defaultHeaders: {
      'anthropic-beta': 'mcp-client-2025-04-04',
    },
  });

  // Read MCP server URL from mcp_servers.json
  const serverUrl = fs.readFileSync('mcp_servers.json', 'utf8').trim();

  console.log(`Testing MCP Connector with server: ${serverUrl}`);
  console.log('='.repeat(60));

  // Configure MCP server
  const mcpServers: MCPServer[] = [
    {
      type: 'url',
      url: serverUrl,
      name: 'time-server',
    },
  ];

  // Test 1: Ask what tools are available
  console.log('\n🔍 Test 1: Discovering available tools');
  console.log('-'.repeat(40));

  try {
    const response1 = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 1000,
      messages: [
        {
          role: 'user',
          content: 'What tools do you have available from the MCP servers?',
        },
      ],
      mcp_servers: mcpServers,
    } as any); // Type assertion needed for beta feature

    const textContent = response1.content.find(
      (block): block is TextContent => block.type === 'text'
    );
    if (textContent) {
      console.log('Response:', textContent.text);
    }
  } catch (error) {
    console.error('Error in Test 1:', error);
    return;
  }

  // Test 2: Get current time
  console.log('\n⏰ Test 2: Getting current time');
  console.log('-'.repeat(40));

  try {
    const response2 = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 1000,
      messages: [
        {
          role: 'user',
          content: 'What is the current time? Use the time server tools.',
        },
      ],
      mcp_servers: mcpServers,
    } as any);

    // Display response content including tool use blocks
    for (const contentBlock of response2.content as ContentBlock[]) {
      if (contentBlock.type === 'text') {
        console.log('Text response:', contentBlock.text);
      } else if (contentBlock.type === 'mcp_tool_use') {
        console.log('🔧 MCP Tool Use:');
        console.log(`  - Tool: ${contentBlock.name}`);
        console.log(`  - Server: ${contentBlock.server_name}`);
        console.log(`  - Input:`, contentBlock.input);
      } else if (contentBlock.type === 'mcp_tool_result') {
        console.log('📊 MCP Tool Result:');
        console.log(`  - Tool Use ID: ${contentBlock.tool_use_id}`);
        console.log(`  - Is Error: ${contentBlock.is_error}`);
        console.log(`  - Content:`, contentBlock.content);
      }
    }
  } catch (error) {
    console.error('Error in Test 2:', error);
    return;
  }

  // Test 3: Convert time between timezones
  console.log('\n🌍 Test 3: Converting time between timezones');
  console.log('-'.repeat(40));

  try {
    const response3 = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 1000,
      messages: [
        {
          role: 'user',
          content:
            'Convert the current time from America/New_York to America/Chicago (Austin, TX timezone) using the time server tools.',
        },
      ],
      mcp_servers: mcpServers,
    } as any);

    // Display response content
    for (const contentBlock of response3.content as ContentBlock[]) {
      if (contentBlock.type === 'text') {
        console.log('Text response:', contentBlock.text);
      } else if (contentBlock.type === 'mcp_tool_use') {
        console.log('🔧 MCP Tool Use:');
        console.log(`  - Tool: ${contentBlock.name}`);
        console.log(`  - Server: ${contentBlock.server_name}`);
        console.log(`  - Input:`, contentBlock.input);
      } else if (contentBlock.type === 'mcp_tool_result') {
        console.log('📊 MCP Tool Result:');
        console.log(`  - Tool Use ID: ${contentBlock.tool_use_id}`);
        console.log(`  - Is Error: ${contentBlock.is_error}`);
        console.log(`  - Content:`, contentBlock.content);
      }
    }
  } catch (error) {
    console.error('Error in Test 3:', error);
    return;
  }

  console.log('\n✅ MCP Connector testing completed!');
}

// Run the main function
main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
