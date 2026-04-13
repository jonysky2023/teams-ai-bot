import json
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def handler(request):
    try:
        body = request.get_json()
        text = body.get("text", "")

        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=200,
            messages=[{
                "role": "user",
                "content": text
            }]
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "result": response.content[0].text
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }
