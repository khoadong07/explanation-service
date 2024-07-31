import json
import requests
import json
from fastapi import status
from config import FIREWORKS_API_MAX_TOKEN, FIREWORKS_URL, FIREWORKS_TOKEN, FIREWORKS_MODEL, TEMPERATURE

def map_timestamp_to_datetime(data):
    return data


def build_prompt(content):
    content = map_timestamp_to_datetime(content)
    return f"{content}"


def explanation_data(content):
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
                    "content": "Prompt: Phân tích dữ liệu theo ngày, nhóm các mẫu dữ liệu theo ngày dựa trên trường publishedDate được cung cấp. "
                               "Mô tả yêu cầu:\n\nHãy phân tích và nhận định các mẫu dữ liệu theo từng ngày từ tập dữ liệu đã cho. "
                               "Mỗi nhận định cần bao gồm thông tin về ngày xảy ra sự kiện (ngày/tháng/năm), tóm tắt tổng quan về nội dung bình luận trong ngày, "
                               "danh sách các từ khóa ảnh hưởng đến sắc thái của nội dung, và danh sách các chủ thể được nhắc đến nhiều nhất trong ngày. "
                               "Đính kèm link nếu nội dung là tiêu cực"
                },
                {
                    "role": "user",
                    "content": f"Hãy phân tích dữ liệu dưới đây, đảm bảo viết bằng tiếng Việt: {build_prompt(content)}"
                },
                {
                    "role": "user",
                    "content": "Trong kết quả bỏ qua các đường dẫn bài viết tích cực"
                },
                {
                    "role": "user",
                    "content": "Trong kết quả trả về vui lòng sắp xếp ngày theo thứ tự tăng dần và đảm bảo rằng có đầy đủ các ngày đã được input trong data."
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

def explanation_chart(content):
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
                               "dưới,. Trong đó là dữ liệu dùng để phân tích, với mentions được hiểu là số lượng đề "
                               "cập đến topic trong khoảng thời gian với range_old là thời gian trong quá khứ, "
                               "và range_new là thời gian hiện đang filter. Bên cạnh đó dữ liệu chart_values dùng để "
                               "thể hiện những thay đổi về sentiment và lượng mention theo từng ngày. Yêu cầu: Hãy "
                               "viết ra những nhận xét về tương quan dữ liệu giữa thời gian trong quá khứ và hiện "
                               "tại, tương quan giữa sentiment hoặc lượng mentions thông qua các ngày khảo sát."
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
