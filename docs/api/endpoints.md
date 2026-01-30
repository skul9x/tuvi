# API Documentation

## Horoscope
### POST /api/ansao
- **Description:** Tính toán lá số tử vi dựa trên thông tin đầu vào.
- **Backend:** Python Serverless Function (`api/ansao.py`)
- **Body:**
```json
{
  "name": "Nguyen Van A",
  "day": 15,
  "month": 6,
  "year": 1995,
  "hour": 15,
  "gender": 1, // 1: Male, 0: Female
  "viewing_year": 2026
}
```
- **Response:** Object containing `info`, `cung` (Dictionary of 12 palaces), `stars`.
- **Note:** `cung` is returned as a Dictionary with string keys ("0", "1", ...), representing position index.

## AI Reading
### POST /api/chat
- **Description:** Luận giải lá số tự động bằng Google Gemini AI (Stream Response).
- **Backend:** Python Serverless Function (`api/chat.py`)
- **Body:**
```json
{
  "data_json": { ... }, // Output from /api/ansao
  "style": "Đời thường" // Optional: "Nghiêm túc", "Hài hước", etc.
}
```
- **Response:** Server-Sent Events (SSE) stream.
- **Format:** `data: {"text": "..."}` or `data: [DONE]`

## System
### GET /api/index
- **Description:** Health check endpoints.
- **Response:** `{"status": "alive"}`
