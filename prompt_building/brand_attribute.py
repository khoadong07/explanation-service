import json
from fastapi import status
import requests
from config import FIREWORKS_API_MAX_TOKEN, FIREWORKS_URL, FIREWORKS_TOKEN, FIREWORKS_MODEL, TEMPERATURE


def build_prompt(content):
    return f"{content}"


def explanation_brand_attribute(content):
    try:
        url = FIREWORKS_URL

        payload = json.dumps({
            "model": FIREWORKS_MODEL,
            "max_tokens": FIREWORKS_API_MAX_TOKEN,
            "top_p": 1,
            "top_k": 40,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "temperature": TEMPERATURE,
            "messages": [
                {
                    "role": "user",
                    "content": "Prompt: Trong phân tích dữ liệu từ lắng nghe mạng xã hội, tôi có dữ liệu như bên "
                               "dưới. Trong đó là dữ liệu dùng để phân tích với thể hiện trên từng brand attribute "
                               "thì lượng mention đến topic có số lượng như thế nào và phân bổ sắc thái hiện trên "
                               "từng brand attribute đang thể hiện ra sao. Hãy phân tích dữ liệu bên dưới dây cho "
                               "thấy được sự tương quan giữa các brand attribute, đồng thời đưa ra so sánh, "
                               "tóm tắt và kết luận."
                },
                {
                    "role": "user",
                    "content": f"Hãy phân tích dữ liệu dưới đây, đảm bảo viết bằng tiếng Việt: {build_prompt(content)}"
                },
                {
                    "role": "user",
                    "content": "Chuyển tất cả kết quả sang tiếng Việt, yêu cầu viết ngắn gọn xúc tích văn phong chỉnh chu."
                },
                {
                    "role": "user",
                    "content": "Viết lại văn bản trong văn phong của báo cáo chuyên nghiệp, chú ý lỗi chính tả và chuẩn format dưới dạng markdown"
                },
                {
                    "role": "user",
                    "content": "Đảm bảo rằng nhận định được tạo ra từ dữ liệu được cung cấp, không được phép sáng tạo thêm các dữ liệu không có thật."
                }
            ]
        })
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': FIREWORKS_TOKEN
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        result = None
        if response.status_code == status.HTTP_200_OK:
            resp = json.loads(response.text).get('choices')
            if resp[0]['message']['content']:
                result = resp[0]['message']['content']
        print(result)
        return result
    except:
        return None