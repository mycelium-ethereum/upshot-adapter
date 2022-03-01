from dotenv import load_dotenv; load_dotenv()

from utils import *

import aioredis
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from fastapi_cache.backends.redis import RedisBackend

alert(f"{os.getenv('NAME')}: Starting server for Upshot")
app = FastAPI()
logger = setup_custom_logger('root')
setup_file_logger(logger)

@cache()
async def get_cache():
    return 1

@app.on_event("startup")
async def startup():
    redis =  aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

@cache(expire=600)
@app.get("/market_cap")
async def root(collection_name: str):
    try:
        data = upshot.get_collection(collection_name)
        if data != {}: 
            return {'result': 1, 'data': data[0]['marketCap']}
        else:
            return {'result': 0, 'data': None}
    except Exception as e:
        alert(f"{os.getenv('NAME')}: Some bug for {collection_name} in Upshot adapter")
        logger.error(f"Error in server - {e}")
        return {'result': 0, 'data': None}