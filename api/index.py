import os
import anthropic
from tools import TOOLS
from tool_runner import run_tool
from workspaces import get_workspace

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)


def run_agent(user_text, workspace_name="default"):

    config = get_workspace(workspace_name)

    messages = [
        {"role": "user", "content": user_text}
    ]

    while True:

        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=800,
            tools=TOOLS,
            messages=messages
        )

        content_blocks = response.content

        for content in content_blocks:

            # 1. RESPUESTA FINAL
            if content.type == "text":
                return content.text

            # 2. TOOL USE
            if content.type == "tool_use":

                tool_name = content.name
                tool_input = content.input

                result = run_tool(tool_name, tool_input, config)

                messages.append({
                    "role": "assistant",
                    "content": response.content
                })

                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": content.id,
                            "content": str(result)
                        }
                    ]
                })
