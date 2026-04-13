from http.server import BaseHTTPRequestHandler
import json
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length)

        data = json.loads(body)
        text = data.get("text", "")

        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=200,
            messages=[{
                "role": "user",
                "content": text
            }]
        )

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps({
            "result": response.content[0].text
        }).encode())
