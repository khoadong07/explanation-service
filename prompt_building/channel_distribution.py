import json
from fastapi import status
import requests
from config import FIREWORKS_API_MAX_TOKEN, FIREWORKS_URL, FIREWORKS_TOKEN, FIREWORKS_MODEL, TEMPERATURE


def build_prompt(content):
    return f"{content}"


def explanation_channel_dist(content):
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
                               "dưới,. Trong đó là dữ liệu dùng để phân tích, với total mentions được hiểu là số "
                               "lượng đề cập đến topic trong khoảng thời gian đang thực hiện filter. Bên cạnh đó dữ "
                               "liệu channel_distribution thể hiện sự phân bổ của số lượng bài viết mention đến topic "
                               "và thống kê số lượng những nhận định về sắc thái của từng kênh như mô tả trong dữ "
                               "liệu. Yêu cầu: Hãy viết ra những nhận xét về tương quan dữ liệu của các channel với "
                               "tổng lượng mentions đang filter,  tương quan giữa tổng lượng sentiment  (có thể tính "
                               "theo tỷ lệ phần trăm trên tổng mentions của từng channel). Cuối cùng hãy thực hiện "
                               "tóm tắt ngắn gọn lại tổng quan về dữ liệu đang phân tích."
                },
                {
                    "role": "user",
                    "content": f"Hãy phân tích dữ liệu dưới đây, đảm bảo viết bằng tiếng Việt: {build_prompt(content)}"
                },
                {
                    "role": "user",
                    "content": "Hãy đảm bảo rằng kết quả nhìn thấy luôn luôn là tiếng Việt"
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