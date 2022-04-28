import pickle
from app.plugins.redis.redis_session import redis_session
from app.core.config import settings


def get_cache(id: str, suffix: str):  # thêm return type
    if redis_session.exists(id + suffix):
        cache_data = pickle.loads(redis_session.get(id + suffix))
        del cache_data["_sa_instance_state"]
    else:
        cache_data = None

    return cache_data


def set_cache(id: str, suffix: str, data):  # thêm return type, type of data
    try:
        redis_session.setex(
            id + suffix, settings.EXPEIRATION_TIME_CACHE, pickle.dumps(data))
        return data
    except Exception as e:
        print(e)
        return {'msg': 'Bad Request!', 'error': str(e)}


def delete_cache(id: str):  # thêm return type
    redis_session.delete(id)
    return {'msg': 'Deleted!'}
