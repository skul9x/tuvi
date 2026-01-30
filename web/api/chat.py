from http.server import BaseHTTPRequestHandler
import json
import sys
import os
from pydantic import BaseModel, Field, ValidationError
from typing import Optional, Dict, Any

# Ensure core is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.gemini_client import GeminiClient

class ChatInput(BaseModel):
    data_json: Dict[str, Any] = Field(..., description="Full horoscope result object")
    api_key: Optional[str] = Field(None, description="Optional API key from client")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                 raise ValueError("Empty body")

            post_data = self.rfile.read(content_length)
            payload = json.loads(post_data.decode('utf-8'))
            
            # Validation
            validated_data = ChatInput(**payload)
            data_json = validated_data.data_json
            
            # API Key: Prioritize Headers > Env Var > Payload
            # Vercel env vars are accessed via os.environ
            api_key = os.environ.get("GEMINI_API_KEY")
            
            if not api_key:
                 # Local fallback for dev
                api_key = validated_data.api_key

            client = GeminiClient(api_key=api_key)
            
            # Set headers for SSE
            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Stream response
            stream = client.generate_reading_stream(data_json)
            
            for chunk in stream:
                if chunk:
                    # Format for SSE: "data: <content>\n\n"
                    # JSON encode the chunk to safe strings
                    msg = json.dumps({"text": chunk})
                    self.wfile.write(f"data: {msg}\n\n".encode('utf-8'))
                    self.wfile.flush()
            
            # End stream
            self.wfile.write(b"data: [DONE]\n\n")
            
        except ValidationError as e:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Dữ liệu không hợp lệ", "details": e.errors()}).encode('utf-8'))

        except Exception as e:
            # If headers not sent, send 500. If sent, too late, maybe log?
            print(f"Error: {e}")
            try:
                self.send_response(500)
                self.end_headers()
            except:
                pass # Headers already sent

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
