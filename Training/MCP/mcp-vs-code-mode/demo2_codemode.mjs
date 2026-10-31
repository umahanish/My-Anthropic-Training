// DEMO 2 - Code Mode (UTCP): Claude gets ONE tool, writes TypeScript, and the
// sandbox calls the same MCP server's tools directly. Intermediate data never
// goes back through the model.
//
//   ANTHROPIC_API_KEY=... node demo2_codemode.mjs
import '@utcp/mcp'; // registers the 'mcp' call template
import { CodeModeUtcpClient } from '@utcp/code-mode';
import Anthropic from '@anthropic-ai/sdk';

const MODEL = 'claude-sonnet-5-5';
const TASK = process.argv[2] ??
  'Check the weather in all our office cities, find the warmest city that is not rainy or stormy, and book me a flight there on 2026-11-20.';

// Hide the UTCP SDK's internal chatter so the demo output stays readable.
const log = console.log;
console.log = (...a) => { if (!/^(\[Mcp|Calling tool|Successfully registered)/.test(String(a[0]))) log(...a); };

const t0 = Date.now();
const stats = { llmCalls: 0, mcpToolCalls: 0, inTokens: 0, outTokens: 0 };

console.log('\n=== DEMO 2: Code Mode ===');
console.log('STEP 1: register the MCP server with Code Mode');
const codemode = await CodeModeUtcpClient.create(process.cwd());
await codemode.registerManual({
  name: 'travel',
  call_template_type: 'mcp',
  config: { mcpServers: { travel: { transport: 'stdio', command: 'uv', args: ['run', '-q', 'travel_server.py'] } } },
});

// Count real MCP calls made from inside the sandbox.
const realCallTool = codemode.callTool.bind(codemode);
codemode.callTool = (name, args) => { stats.mcpToolCalls++; console.log(`  [sandbox -> MCP] ${name}(${JSON.stringify(args)})`); return realCallTool(name, args); };

console.log('STEP 2: turn MCP tools into TypeScript interfaces for the prompt');
const interfaces = await codemode.getAllToolsTypeScriptInterfaces();
const system = `${CodeModeUtcpClient.AGENT_PROMPT_TEMPLATE}

Available tool interfaces:
${interfaces}

Do the whole task in ONE call_tool_chain when you can: fetch, filter, decide and act inside the code, and return only a small summary.
Tool calls return plain values, not promises: never call .then() on them.`;

// The ONLY tool Claude sees.
const tools = [{
  name: 'call_tool_chain',
  description: 'Execute TypeScript code with access to all registered tools. Returns {result, logs}.',
  input_schema: { type: 'object', properties: { code: { type: 'string', description: 'TypeScript function body; use return for the result.' } }, required: ['code'] },
}];

console.log(`STEP 3: give Claude the task + 1 tool (call_tool_chain)\n  user: ${TASK}`);
const claude = new Anthropic();
const messages = [{ role: 'user', content: TASK }];
let resp;
while (true) {
  resp = await claude.messages.create({ model: MODEL, max_tokens: 2048, system, tools, messages });
  stats.llmCalls++; stats.inTokens += resp.usage.input_tokens; stats.outTokens += resp.usage.output_tokens;
  messages.push({ role: 'assistant', content: resp.content });
  if (resp.stop_reason !== 'tool_use') break;
  const results = [];
  for (const block of resp.content.filter((b) => b.type === 'tool_use')) {
    console.log('STEP 4: Claude wrote this code:\n' + block.input.code.replace(/^/gm, '    | '));
    const out = await codemode.callToolChain(block.input.code);
    console.log(`  sandbox result: ${JSON.stringify(out.result)}`);
    if (out.result == null) console.log(`  sandbox logs: ${out.logs.join(' | ').slice(0, 300)}`);
    results.push({ type: 'tool_result', tool_use_id: block.id, content: JSON.stringify(out) });
  }
  messages.push({ role: 'user', content: results });
}

console.log("STEP 5: Claude's final answer");
console.log('  ' + resp.content.filter((b) => b.type === 'text').map((b) => b.text).join('').replaceAll('\n', '\n  '));
console.log(`\nSTATS  LLM calls=${stats.llmCalls}  MCP tool calls=${stats.mcpToolCalls}  input tokens=${stats.inTokens}  output tokens=${stats.outTokens}  time=${((Date.now() - t0) / 1000).toFixed(1)}s`);

await codemode.close();
process.exit(0);
