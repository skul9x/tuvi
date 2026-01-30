from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Ensure core is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.gemini_client import GeminiClient

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            payload = json.loads(post_data.decode('utf-8'))
            data_json = payload.get('data_json')
            
            # API Key: Prioritize Headers > Env Var
            # Vercel env vars are accessed via os.environ
            api_key = os.environ.get("GEMINI_API_KEY")
            
            if not api_key:
                 # Local fallback for dev
                api_key = payload.get('api_key') 

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
            
        except Exception as e:
            # If headers not sent, send 500. If sent, too late, maybe log?
            # On Vercel, logs are visible.
            print(f"Error: {e}") 

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
