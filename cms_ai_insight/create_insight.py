import json
from cms_ai_insight.cms_data_helper import fetch_buzzes
from cms_ai_insight.models import BuzzRequest
from dotenv import load_dotenv
import os
import requests
import re


load_dotenv()

# Get environment variables
FIREWORKS_URL = os.getenv('FIREWORKS_URL', 'https://api.fireworks.ai/inference/v1/chat/completions')
FIREWORKS_TOKEN = os.getenv('FIREWORKS_TOKEN', '')

def load_prompt_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def extract_content(markdown_text):
    content_pattern = r"\*\*Content\*\*:\s*\"(.*?)\""
    return re.findall(content_pattern, markdown_text)

def gen_ai_create_insight(buzz_request: BuzzRequest, promt_file):

    buzz_data = fetch_buzzes(
        buzz_request.indexes,
        buzz_request.labels,
        buzz_request.published_from,
        buzz_request.published_to,
        buzz_request.refresh_token,
        buzz_request.token
    )
    # print(buzz_data)
    if buzz_data is None or len(buzz_data) < 5:
        return None, None

    extracted_data = []
    for record in buzz_data:
        source = record.get('_source', {})
        data = {
            'title': source.get('title', None),
            'content': source.get('content', None),
            'url': source.get('url', None),
            'siteName': source.get('siteName', None),
            'siteId': source.get('siteId', None),
            'publishedDate': source.get('publishedDate', None)
        }
        extracted_data.append(data)

    payload = {
        "model": "accounts/fireworks/models/llama-v3p1-405b-instruct",
        "max_tokens": 16384,
        "top_p": 1,
        "top_k": 40,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "temperature": 0.6,
        "messages": [
            {
                "role": "user",
                "content": load_prompt_file(promt_file)
            },
            {
                "role": "user",
                "content": f"Hãy phân tích data sau: {extracted_data}"
            },
            {
                "role": "user",
                "content": f"Hãy trả về định dạng markdown"
            }
        ],
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {FIREWORKS_TOKEN}"
    }
    response = requests.request("POST", FIREWORKS_URL, headers=headers, data=json.dumps(payload))

    result = None
    contents = None
    if response.status_code == 200:
        resp = json.loads(response.text).get('choices')
        if resp[0]['message']['content']:
            result = resp[0]['message']['content']
            contents = extract_content(result)

    return result, contents


# buzz_request = BuzzRequest(
#     indexes=["595210ee35b7e2410fd3b852"],
# labels = [
#     "-1",
#     "63e695d90ea72a1d3c06f4d6",
#     "63e695d90ea72a1d3c06f4d7",
#     "63e695d90ea72a1d3c06f4d8",
#     "63e695d90ea72a1d3c06f4da",
#     "63e695d90ea72a1d3c06f4dc",
#     "63e695d90ea72a1d3c06f4dd",
#     "63e696550ea72a1d3c06f4de",
#     "63e696550ea72a1d3c06f4df",
#     "63e696550ea72a1d3c06f4e0",
#     "63e696550ea72a1d3c06f4e1",
#     "63e696550ea72a1d3c06f4e2",
#     "63e696550ea72a1d3c06f4e3",
#     "63e696550ea72a1d3c06f4e4",
#     "63e696550ea72a1d3c06f4e5",
#     "63e696550ea72a1d3c06f4e8",
#     "63e696860ea72a1d3c06f4e9",
#     "63e696860ea72a1d3c06f4ea",
#     "63e696860ea72a1d3c06f4eb",
#     "63e696860ea72a1d3c06f4ec",
#     "63e696860ea72a1d3c06f4ed",
#     "63e696860ea72a1d3c06f4ee",
#     "63e696860ea72a1d3c06f4ef",
#     "63e697600ea72a1d3c06f4f2",
#     "63e697600ea72a1d3c06f4f4",
#     "63e697600ea72a1d3c06f4fa",
#     "63e698f10ea72a1d3c06f4fb",
#     "63e6990f0ea72a1d3c06f4fd",
#     "63e699320ea72a1d3c06f4fe",
#     "63e6995c0ea72a1d3c06f500",
#     "63e6995c0ea72a1d3c06f501",
#     "63e6995c0ea72a1d3c06f502",
#     "63e6995c0ea72a1d3c06f503",
#     "63e699f10ea72a1d3c06f508",
#     "63e699f10ea72a1d3c06f50b",
#     "63e69a4a0ea72a1d3c06f510",
#     "63e69a4a0ea72a1d3c06f511",
#     "63e69a6b0ea72a1d3c06f512",
#     "63e69a6b0ea72a1d3c06f513",
#     "63e69a8c0ea72a1d3c06f515",
#     "63e69aaf0ea72a1d3c06f517",
#     "63e69adc0ea72a1d3c06f518",
#     "63e69adc0ea72a1d3c06f51a",
#     "63e69af70ea72a1d3c06f51b",
#     "63e69af70ea72a1d3c06f51c",
#     "63e69b130ea72a1d3c06f51d",
#     "63e69b130ea72a1d3c06f51e",
#     "63e69b2a0ea72a1d3c06f51f",
#     "63e69b780ea72a1d3c06f520",
#     "63e69b780ea72a1d3c06f521",
#     "63e69b970ea72a1d3c06f522",
#     "63f42d87f25ec30eba7b9e70",
#     "66a9ff939433ef563c6d1732",
#     "66b5fec99433ef563c6d1812",
#     "66b5ff419433ef563c6d1813",
#     "66b5ff5c9433ef563c6d1814",
#     "66b5ffb09433ef563c6d1815",
#     "66b603cb9433ef563c6d1816"
# ],
# published_from = "2024-09-16 00:00:00",
# published_to = "2024-09-23 23:59:59",
# refresh_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2M2RhMTJmYzI0ZTI2ODE3MmM1ZWZkMzEiLCJ1c2VybmFtZSI6Im5ndXllbnRoYW5oZGF0IiwicGVybWlzc2lvbnMiOiJbe1wicm9sZXNcIjpbXCJhZG1pblwiXSxcIl9pZFwiOlwiNjNkYTEyZmMyNGUyNjgxNzJjNWVmZDMyXCIsXCJncm91cFwiOlwiY29uc3VsdGluZ1wifSx7XCJyb2xlc1wiOltcImFkbWluXCJdLFwiX2lkXCI6XCI2M2RhMTJmYzI0ZTI2ODE3MmM1ZWZkMzNcIixcImdyb3VwXCI6XCJzbWNjXCJ9XSIsInN0YXR1cyI6ImFjdGl2ZSIsImlhdCI6MTcyNzA2MzE3OCwiZXhwIjoxNzI3MTQ5NTc4fQ.aSC1AssxFidEWjYfXx8Ks0qbpXo9uffx-AImIoMUhf0",
# token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2M2RhMTJmYzI0ZTI2ODE3MmM1ZWZkMzEiLCJ1c2VybmFtZSI6Im5ndXllbnRoYW5oZGF0IiwicGVybWlzc2lvbnMiOiJbe1wicm9sZXNcIjpbXCJhZG1pblwiXSxcIl9pZFwiOlwiNjNkYTEyZmMyNGUyNjgxNzJjNWVmZDMyXCIsXCJncm91cFwiOlwiY29uc3VsdGluZ1wifSx7XCJyb2xlc1wiOltcImFkbWluXCJdLFwiX2lkXCI6XCI2M2RhMTJmYzI0ZTI2ODE3MmM1ZWZkMzNcIixcImdyb3VwXCI6XCJzbWNjXCJ9XSIsInN0YXR1cyI6ImFjdGl2ZSIsImlhdCI6MTcyNzA2MzE3OCwiZXhwIjoxNzI3MDkxOTc4fQ.exRBAIy8GqxMd3n2Kl-e2Yc4qZj-LwISW1S9QPs9Vvw"
# )
#
# gen_ai_create_insight(buzz_request)