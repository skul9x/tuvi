import os
import warnings
# Suppress the annoying FutureWarning from google.generativeai
warnings.filterwarnings("ignore", category=FutureWarning)

import google.generativeai as genai
from core.logger import setup_logger

# Get logger
logger, _ = setup_logger()

class GeminiClient:
    def __init__(self, api_key=None, model_name=None):
        # Ưu tiên lấy từ tham số, sau đó đến biến môi trường
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model_name or "models/gemini-2.0-flash"
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
        else:
            self.model = None

    def set_config(self, api_key, model_name):
        """Reconfigure client with new key and model."""
        self.api_key = api_key
        self.model_name = model_name
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
        logger.info(f"Gemini Client reconfigured. Model: {self.model_name}")

    @staticmethod
    def test_connection(api_key):
        """
        Test connection to Gemini API with a minimal request.
        Returns: (Success (bool), Message (str))
        """
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("models/gemini-2.0-flash") # Use lightest model for test
            response = model.generate_content("Hello", generation_config={"max_output_tokens": 5})
            if response and response.text:
                return True, "Kết nối thành công! API Key hợp lệ."
            return False, "Không nhận được phản hồi từ Google."
        except Exception as e:
            error_str = str(e)
            if "403" in error_str or "API_KEY_INVALID" in error_str:
                return False, "API Key không hợp lệ."
            if "429" in error_str:
                return False, "API Key hợp lệ nhưng đang bị giới hạn (Quota Exceeded)."
            return False, f"Lỗi kết nối: {error_str}"

    def generate_reading_stream(self, data_json):
        """
        Gửi data lá số lên Gemini và nhận stream text trả về.
        Có cơ chế thử lại (Retry) nếu gặp lỗi quá tải (429).
        """
        import time
        
        if not self.model:
            yield "Lỗi: Chưa có API Key. Vui lòng nhập API Key."
            return

        # Build prompt
        prompt = self.construct_prompt(data_json)
        logger.debug(f"Prompt constructed ({len(prompt)} chars). Sending to Gemini...")
        
        # Define Fallback Chain in order of priority (Hết nạc vạc đến xương)
        # Nếu model hiện tại là X, tìm X trong list, bắt đầu thử từ X -> ... -> End.
        FALLBACK_MODELS = [
            "models/gemini-2.5-pro", 
            "models/gemini-1.5-pro",
            "models/gemini-2.5-flash",
            "models/gemini-2.0-flash",
            "models/gemini-flash-latest",
            "models/gemini-2.0-flash-lite"
        ]

        # Determine starting index based on current model
        start_index = 0
        if self.model_name in FALLBACK_MODELS:
            start_index = FALLBACK_MODELS.index(self.model_name)
        else:
            # If custom model not in list, try custom first, then fallback to entire list
            FALLBACK_MODELS.insert(0, self.model_name)
            start_index = 0

        # Create execution plan (Current -> ... -> End of list)
        execution_plan = FALLBACK_MODELS[start_index:]
        
        # Max retries per model (just 1 attempt per model in fallback chain to be fast)
        # But we can retry the *same* model once if 429 before switching? 
        # Strategy: Try current model. If 429 -> Switch immediately.
        
        for model_name in execution_plan:
             # Configure client for this model attempt
            try:
                # Re-configure model object (Reuse API key)
                # Note: API Key is tied to Client, Model Name varies.
                current_model_obj = genai.GenerativeModel(model_name)
                
                logger.debug(f"Attempting with model: {model_name}")
                response = current_model_obj.generate_content(prompt, stream=True)
                
                logger.info(f"Gemini API connection established with {model_name}. Streaming response...")
                
                # Yield success message if we switched models
                if model_name != self.model_name:
                     yield f"\n⚠️ Model **{self.model_name}** quá tải. Đã chuyển sang **{model_name}**...\n"
                
                for chunk in response:
                    if chunk.text:
                        yield chunk.text
                logger.info("Gemini stream finished.")
                return # Success - Exit function
                
            except Exception as e:
                error_str = str(e)
                logger.warning(f"Failed with {model_name}: {error_str}")
                
                # Check for 429 / Quota Exceeded
                if "429" in error_str or "Quota exceeded" in error_str or "quota" in error_str.lower():
                    # Move to next model in loop
                    if model_name == execution_plan[-1]: # Last model failed
                        yield f"\n❌ **Tất cả các Model đều quá tải!**\n"
                        yield f"Vui lòng chờ 1-2 phút hoặc kiểm tra lại API Key.\n"
                        return
                    else:
                        # Continue to next iteration
                        continue

                # Other errors (Auth, Network...) -> Fail immediately
                yield f"Lỗi kết nối Gemini ({model_name}): {error_str}"
                return

    def construct_prompt(self, data):
        """
        Tạo prompt đóng vai thầy bói nghiêm túc.
        """
        info = data['info']
        cung = data['cung']
        
        # Build prompt
        prompt = f"""
        Bạn là một chuyên gia TỬ VI ĐẨU SỐ hàng đầu, với kiến thức sâu rộng về Tử Vi Nam Phái và Bắc Phái.
        Phong cách luận giải: NGHIÊM TÚC, CỔ ĐIỂN, SÂU SẮC. Dùng từ ngữ chuyên môn nhưng giải thích dễ hiểu.
        Xưng hô: "Tại hạ" hoặc "Tôi", gọi người xem là "Đương số".

        HÃY LUẬN GIẢI LÁ SỐ SAU ĐÂY:

        1. THÔNG TIN CƠ BẢN:
        - Đương số: {info['name']}
        - Ngày âm: {info['lunar_date']} ({info['can_chi']})
        - Cục: {info['cuc']}
        - Mệnh đóng tại: {info['menh_tai']}
        - Thân đóng tại: {info['than_tai']}

        2. CÁC CUNG VÀ SAO:
        """
        
        for i in range(12):
            c = cung[i]
            prompt += f"- Cung {c['name']} ({c.get('chuc_nang', '')}): {', '.join(c['chinh_tinh'])}\n"

        prompt += """
        
        YÊU CẦU LUẬN GIẢI CHI TIẾT CÁC VẤN ĐỀ SAU (Mỗi phần khoảng 100-150 chữ):
        1. Tổng quan về Mệnh và Thân (Tính cách, tố chất).
        2. Công danh, Sự nghiệp (Cung Quan Lộc).
        3. Tài lộc, tiền bạc (Cung Tài Bạch).
        4. Tình duyên, gia đạo (Cung Phu Thê).
        5. Lời khuyên tổng kết cho năm nay và tương lai.

        Hãy bình giải thật có tâm, dựa trên sự tương tác giữa các sao, thế đứng của các cung. Tuyệt đối không nói chung chung.
        """
        return prompt
