"""Claude API integration for Todo AI Chatbot."""
from typing import Any, Dict, List

from anthropic import Anthropic

from app.config import settings

client = Anthropic(api_key=settings.claude_api_key)


def call_claude_with_tools(
    messages: List[Dict[str, Any]], tools: List[Dict[str, Any]], max_tokens: int = 1024
) -> Dict[str, Any]:
    """Call Claude with tool calling enabled."""
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=max_tokens,
        tools=tools,
        messages=messages,
    )
    return response


def execute_tool_calls(response: Dict[str, Any], executor_func):
    """Execute tool calls and get results for Claude feedback loop."""
    tool_calls = response.tool_calls or []
    tool_results = []
    for tool_call in tool_calls:
        result = executor_func(tool_call)
        tool_results.append(
            {"type": "tool_result", "tool_use_id": tool_call.id, "content": result}
        )
    return tool_results


def get_final_response(
    initial_response: Dict[str, Any], tool_results: List[Dict[str, Any]]
) -> str:
    """Get final Claude response after tool execution."""
    messages = initial_response.messages + tool_results
    final_response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=messages,
    )
    return final_response.content[0].text
