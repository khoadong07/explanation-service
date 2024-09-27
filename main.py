import json
import logging
import os
from hashlib import md5
from logging.handlers import RotatingFileHandler

import redis
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from cms_ai_insight.create_insight import gen_ai_create_insight
from cms_ai_insight.models import BuzzRequest
from models.brand_attribute import BrandAttributeData
from models.channel_distribution import ChannelDistributionData
from models.sentiment_breakdown import AnalysisResult
from models.trend_line_mentions import InputData
from prompt_building.brand_attribute import explanation_brand_attribute
from prompt_building.channel_distribution import explanation_channel_dist
from prompt_building.sentiment_breakdown import explanation_sentiment_breakdown
from prompt_building.trend_line_mentions import explanation_data, explanation_chart
from config import LOG_PATH, REDIS

logs_dir = LOG_PATH
os.makedirs(logs_dir, exist_ok=True)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_file = os.path.join(logs_dir, "app.log")
handler = RotatingFileHandler(log_file, maxBytes=10000000, backupCount=5)
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)

def get_redis_connection():
    # return redis.StrictRedis(host='0.0.0.0', port=16379, db=0)
    return redis.StrictRedis(host=REDIS, port=6379, db=0)


def hash_body(body: dict) -> str:
    body_json = json.dumps(body, sort_keys=True)
    hashed_key = md5(body_json.encode()).hexdigest()
    return hashed_key


async def get_from_cache_or_compute(key: str, compute_fn):
    redis_conn = get_redis_connection()
    logger.info(redis_conn)
    cached_result = redis_conn.get(key)
    if cached_result:
        logger.info("Got result from cache")
        return json.loads(cached_result.decode('utf-8'))
    else:
        computed_result = await compute_fn()
        if computed_result:
            redis_conn.setex(name=key, time=600, value=json.dumps(computed_result))
        return computed_result


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://0.0.0.0",
    "http://0.0.0.0:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from aiocache import caches, Cache
from aiocache.plugins import HitMissRatioPlugin

caches.set_config({
    'default': {
        'cache': "aiocache.RedisCache",
        'endpoint': REDIS,
        'port': 6379,
        'db': 1,  # Use Redis database 1
        'timeout': 1,  # Timeout for Redis operations
        'serializer': {
            'class': "aiocache.serializers.JsonSerializer"  # To serialize objects as JSON
        },
        'plugins': [
            {'class': HitMissRatioPlugin}  # Optional plugin to track cache hits/misses
        ]
    }
})

def success(message: str, data: any):
    content = {
        "message": message,
        "data": data,
        "result": 1
    }
    return JSONResponse(
        status_code=200,
        content=content
    )


def bad_request(message: str, data: None):
    content = {
        "message": message,
        "data": data,
        "result": -1
    }
    return JSONResponse(
        status_code=400,
        content=content
    )


def retry_run_explanation_data(content):
    retries = 3
    while retries > 0:
        print(f"retry time: {retries}")
        result = explanation_data(content=content)
        if result is not None:
            return result
        retries -= 1
    return False


def retry_run_explanation_chart(content):
    retries = 3
    while retries > 0:
        print(f"retry time: {retries}")
        result = explanation_chart(content=content)
        if result is not None:
            return result
        retries -= 1
    return False


def retry_run_explanation_channel_dist(content):
    retries = 3
    while retries > 0:
        print(f"retry time: {retries}")
        result = explanation_channel_dist(content=content)
        if result is not None:
            return result
        retries -= 1
    return False


def retry_run_explanation_brand_attribute(content):
    retries = 3
    while retries > 0:
        print(f"retry time: {retries}")
        result = explanation_brand_attribute(content=content)
        if result is not None:
            return result
        retries -= 1
    return False


def retry_run_explanation_sentiment_breakdown(content):
    retries = 3
    while retries > 0:
        print(f"retry time: {retries}")
        result = explanation_sentiment_breakdown(content=content)
        if result is not None:
            return result
        retries -= 1
    return False


@app.post("/api/explanation")
async def process_data(input_data: InputData):
    async def compute_data():
        result_exp_data = retry_run_explanation_data(input_data.data)
        result_exp_chart = retry_run_explanation_chart(input_data.analysis)
        if result_exp_data is False or result_exp_chart is False:
            return None

        result = {
            "exp_data": result_exp_data,
            "exp_chart": result_exp_chart
        }
        return result

    cache_key = hash(input_data.json().encode('utf-8'))

    cached_result = await get_from_cache_or_compute(cache_key, compute_data)

    if cached_result is None:
        return bad_request(
            message="Failed to process data after retries",
            data=None
        )
    return success(
        message="Data processed successfully",
        data=[cached_result.get('exp_data'), cached_result.get('exp_chart')]
    )


@app.post("/api/explanation/channel-distribution")
async def process_data_channel(input_data: ChannelDistributionData):
    async def compute_data():
        result_exp_channel = retry_run_explanation_channel_dist(input_data)
        if result_exp_channel is False:
            return None
        return result_exp_channel

    cache_key = hash(input_data.json().encode('utf-8'))

    cached_result = await get_from_cache_or_compute(cache_key, compute_data)

    if cached_result is None:
        return bad_request(
            message="Failed to process data after retries",
            data=None
        )
    return success(
        message="Data processed successfully",
        data=[cached_result]
    )


@app.post("/api/explanation/brand-attribute")
async def process_data_channel(input_data: BrandAttributeData):
    async def compute_data():
        result_exp_channel = retry_run_explanation_brand_attribute(input_data)
        if result_exp_channel is False:
            return None
        return result_exp_channel

    cache_key = hash(input_data.json().encode('utf-8'))

    cached_result = await get_from_cache_or_compute(cache_key, compute_data)

    if cached_result is None:
        return bad_request(
            message="Failed to process data after retries",
            data=None
        )
    return success(
        message="Data processed successfully",
        data=[cached_result]
    )


@app.post("/api/explanation/sentiment-breakdown")
async def process_data_channel(input_data: AnalysisResult):
    async def compute_data():
        result_exp_channel = retry_run_explanation_sentiment_breakdown(input_data)
        if result_exp_channel is False:
            return None
        return result_exp_channel

    cache_key = hash(input_data.json().encode('utf-8'))

    cached_result = await get_from_cache_or_compute(cache_key, compute_data)

    if cached_result is None:
        return bad_request(
            message="Failed to process data after retries",
            data=None
        )
    return success(
        message="Data processed successfully",
        data=[cached_result]
    )


@app.get("/api/explanation/cache")
async def delete_all_cache():
    redis = get_redis_connection()
    keys_deleted = redis.flushdb()
    redis.close()
    return {"message": f"All keys deleted from cache: {keys_deleted}"}


@app.post("/api/ai-insight")
async def cms_ai_insight(
    buzz_request: BuzzRequest,
    x_refresh_token: str = Header(...),
    x_token: str = Header(...),
):
    if not x_refresh_token or not x_token:
        raise HTTPException(status_code=400, detail="Missing required headers")

    if buzz_request.refresh_token is None:
        buzz_request.refresh_token = x_refresh_token
    if buzz_request.token is None:
        buzz_request.token = x_token

    cache = caches.get('default')
    cached_value = await cache.get(str(buzz_request.indexes))

    if cached_value:
        return success(message="AI insight processed successfully", data=cached_value)

    result, contents = gen_ai_create_insight(buzz_request, promt_file="cms_ai_insight/prompt.txt")
    retries = 0
    while retries < 3 and not contents:
        result, contents = gen_ai_create_insight(buzz_request, promt_file="cms_ai_insight/prompt.txt")
        retries += 1

    if result and contents:
        results = {
            "highlight_content": contents,
            "insight_md": result
        }
        await cache.set(str(buzz_request.indexes), results, ttl=300)
        return success(message="AI insight processed successfully", data=results)
    else:
        results = {
            "highlight_content": None,
            "insight_md": """
        **Không có dữ liệu cảm xúc tiêu cực**

Chúng tôi đã tiến hành phân tích toàn bộ nội dung trong khoảng thời gian bạn yêu cầu và không phát hiện bất kỳ bình luận hoặc ý kiến nào mang cảm xúc tiêu cực. Điều này cho thấy sự hài lòng và phản hồi tích cực từ người dùng đối với sản phẩm/dịch vụ.
        """
        }
        return success(message="AI insight processed successfully", data=results)
    return bad_request(message="Fail", data=None)

@app.get("/api/ai-insight/clear-cache")
async def clear_all_cache():
    cache = caches.get('default')
    await cache.clear()
    return {"status": "all cache cleared"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)