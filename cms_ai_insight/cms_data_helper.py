import requests
from datetime import datetime


def fetch_buzzes(indexes, labels, published_from, published_to, refresh_token, token):
    url = "https://cms-gateway.radaa.net/kompaql"

    payload = {
        "query": """
            query buzzes(
                $input: IndexesInput!
                $filter: FilterBuzzInput
            ) {
                buzzes(input: $input, filter: $filter) {
                    status
                    message
                    total
                    skip
                    limit
                    data {
                        _id
                        _index
                        _source {
                            type
                            publishedDate
                            siteId
                            siteName
                            url
                            title
                            content
                            parentId
                            parentDate
                            commentParentId
                            sentiment {
                                value
                                createdAt
                                createdBy
                                updatedAt
                                updatedBy
                            }
                            labels {
                                value
                                createdAt
                                createdBy
                            }
                            profile {
                                id
                                name
                            }
                        }
                    }
                }
            }
        """,
        "variables": {
            "input": {"indexes": indexes},
            "filter": {
                "publishedFromDate": published_from,
                "publishedToDate": published_to,
                "types": [
                    "FBPAGE_TOPIC", "FBPAGE_COMMENT", "FBGROUP_TOPIC", "FBGROUP_COMMENT",
                    "FBUSER_TOPIC", "FBUSER_COMMENT", "FORUM_TOPIC", "FORUM_COMMENT",
                    "NEWS_TOPIC", "NEWS_COMMENT", "YOUTUBE_TOPIC", "YOUTUBE_COMMENT",
                    "BLOG_TOPIC", "BLOG_COMMENT", "QA_TOPIC", "QA_COMMENT",
                    "SNS_TOPIC", "SNS_COMMENT", "TIKTOK_TOPIC", "TIKTOK_COMMENT",
                    "LINKEDIN_TOPIC", "LINKEDIN_COMMENT", "ECOMMERCE_TOPIC",
                    "ECOMMERCE_COMMENT"
                ],
                "isDeleted": False,
                "sentiments": ["NEGATIVE"],
                "labels": labels,
                "levels": ["NONE", "LEVEL_1", "LEVEL_2", "LEVEL_3"],
                "skip": 0,
                "limit": 300
            }
        }
    }

    headers = {
        'accept': 'application/graphql-response+json, application/json',
        'accept-language': 'vi',
        'content-type': 'application/json',
        'origin': 'https://smcc-2024.radaa.net',
        'referer': 'https://smcc-2024.radaa.net/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'x-refresh-token': f'{refresh_token}',
        'x-token': f'{token}'
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json().get('data')
        if data:
            buzzes = data.get('buzzes')
            if buzzes:
                buzzes_data = buzzes.get('data')
                if buzzes_data:
                    return convert_timestamps(buzzes_data)
    return None


def convert_timestamps(data):
    for item in data:
        # Convert 'publishedDate'
        published_ts = item['_source'].get('publishedDate')
        if published_ts:
            item['_source']['publishedDate'] = datetime.utcfromtimestamp(published_ts / 1000).strftime('%Y-%m-%d %H:%M:%S')

        # Convert 'sentiment.createdAt'
        sentiment_ts = item['_source']['sentiment'].get('createdAt')
        if sentiment_ts:
            item['_source']['sentiment']['createdAt'] = datetime.utcfromtimestamp(sentiment_ts / 1000).strftime('%Y-%m-%d %H:%M:%S')

    return data