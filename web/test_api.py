import sys
import os
import io
import json

# Ensure path
sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../core'))

# Import handlers
from api.ansao import handler as AnsaoHandler

class MockServer:
    def __init__(self):
        pass

def test_ansao():
    print("Testing /api/ansao...")
    
    data = {
        "day": 15, "month": 2, "year": 1990,
        "hour": 6, "gender": 1, "name": "Test User"
    }
    body = json.dumps(data).encode('utf-8')
    
    # Instantiate Handler manually
    # BaseHTTPRequestHandler signature: (request, client_address, server)
    # But we can instantiate it and manually set variables to avoid socket logic
    
    class TestHandler(AnsaoHandler):
        def __init__(self, request_body):
            self.rfile = io.BytesIO(request_body)
            self.wfile = io.BytesIO()
            self.headers = {'Content-Length': str(len(request_body))}
            self.client_address = ("0.0.0.0", 80)
            self.requestline = "POST /api/ansao HTTP/1.1"
            self.command = "POST"
            self.path = "/api/ansao"
            self.request_version = "HTTP/1.1" # Fix for AttributeError
            self.close_connection = False # Fix for potential logic
            
        def log_request(self, code='-', size='-'):
            pass # Disable logging for test
            
        def run_test(self):
            self.do_POST()
            return self.wfile.getvalue().decode('utf-8')

    h = TestHandler(body)
    output = h.run_test()
        
    print(f"Response size: {len(output)}")
    if "menh_tai" in output:
        print("✅ Ansao Passed")
    else:
        print("❌ Ansao Failed")
        print(output[:200])

if __name__ == "__main__":
    try:
        test_ansao()
    except Exception as e:
        import traceback
        traceback.print_exc()
