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
                    "content": "Prompt: Tôi có dữ liệu từ lắng nghe mạng xã hội trong ngành [Tên thương hiệu/ngành] từ ngày [Ngày bắt đầu] đến ngày [Ngày kết thúc]. Dữ liệu bao gồm danh sách các bài đăng và thông tin chi tiết về tần suất nhắc đến và cảm xúc của người dùng. Hãy thực hiện phân tích theo các yêu cầu sau:"
                },
                {
                    "role": "user",
                    "content": "1. Tổng kết số lượt nhắc đến theo từng ngày và phân chia theo các loại cảm xúc (tích cực, trung lập, tiêu cực)."
                },
                {
                    "role": "user",
                    "content": "2. Xác định các bài đăng cụ thể đã tạo ra số lượt nhắc đến cao và cung cấp URL dẫn chứng từ danh sách bài đăng."
                },
                {
                    "role": "user",
                    "content": "3. Đánh giá tác động của các sự kiện chính đối với số lượt nhắc đến, tập trung vào các sự kiện nổi bật như: [Sự kiện A], [Sự kiện B], [Sự kiện C],…"
                },
                {
                    "role": "user",
                    "content": "4. Đánh giá cảm xúc theo từng ngày và phân tích sự thay đổi trong tần suất đề cập trong khoảng thời gian được phân tích."
                },
                {
                    "role": "user",
                    "content": "5. Cung cấp so sánh tổng quan giữa các sự kiện chính và ảnh hưởng của chúng đối với xu hướng nhắc đến thương hiệu/ngành."
                },
                {
                    "role": "user",
                    "content": "Đảm bảo rằng tất cả các nhận định được tạo ra dựa trên dữ liệu được cung cấp, không được phép sáng tạo thêm dữ liệu không có thật. Viết ngắn gọn, xúc tích và theo văn phong chuyên nghiệp, chú ý đúng chính tả và sử dụng định dạng markdown chuẩn."
                },
                {
                    "role": f"Hãy phân tích dữ liệu sau: {content}"
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