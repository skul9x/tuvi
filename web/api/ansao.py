from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Ensure core is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.tuvi import TuViLogic

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            
            # Extract data
            solar_day = data.get('day')
            solar_month = data.get('month')
            solar_year = data.get('year')
            hour = data.get('hour')
            gender = data.get('gender')
            name = data.get('name', 'Hữu Duyên')
            viewing_year = data.get('viewing_year')
            
            # Calculate
            logic = TuViLogic(
                solar_day=solar_day,
                solar_month=solar_month,
                solar_year=solar_year,
                hour=hour,
                gender=gender,
                name=name,
                viewing_year=viewing_year
            )
            result = logic.an_sao()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-Type, Accept")
        self.end_headers()
