from http.server import BaseHTTPRequestHandler
import json
import sys
import os
from pydantic import BaseModel, Field, ValidationError, field_validator
from typing import Optional

# Ensure core is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.tuvi import TuViLogic

class HoroscopeInput(BaseModel):
    name: str = Field(default="Hữu Duyên", max_length=100)
    day: int = Field(..., ge=1, le=31)
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=1900, le=2100)
    hour: int = Field(..., ge=0, le=23)
    gender: int = Field(..., ge=0, le=1) # 1: Nam, 0: Nữ
    viewing_year: int = Field(default_factory=lambda: 2024, ge=1900, le=2100)

    @field_validator('name')
    @classmethod
    def clean_name(cls, v):
        # Allow letters, spaces, and basic punctuation
        allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ àáãạảăắằẳẵặâấầẩẫậèéẹẻẽêếềểễệđìíĩỉịòóõọỏôốồổỗộơớờởỡợùúũụủưứừửữựỳỵỷỹýÀÁÃẠẢĂẮẰẲẴẶÂẤẦẨẪẬÈÉẸẺẼÊẾỀỂỄỆĐÌÍĨỈỊÒÓÕỌỎÔỐỒỔỖỘƠỚỜỞỠỢÙÚŨỤỦƯỨỪỬỮỰỲỴỶỸÝ")
        return "".join([c for c in v if c in allowed or c.isalnum()])

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                 raise ValueError("Empty body")
            
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Pydantic Validation
            validated_data = HoroscopeInput(**data)
            
            # Calculate
            logic = TuViLogic(
                solar_day=validated_data.day,
                solar_month=validated_data.month,
                solar_year=validated_data.year,
                hour=validated_data.hour,
                gender=validated_data.gender,
                name=validated_data.name,
                viewing_year=validated_data.viewing_year
            )
            result = logic.an_sao()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
            
        except ValidationError as e:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Dữ liệu không hợp lệ", "details": e.errors()}).encode('utf-8'))
            
        except ValueError as e:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # In production, hide detailed error from user
            self.wfile.write(json.dumps({"error": "Lỗi server: " + str(e)}).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-Type, Accept")
        self.end_headers()
