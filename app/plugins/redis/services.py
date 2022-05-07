import pickle

from app.plugins.redis.session import redis_session
from app.config import settings


class RedisServices:
    def get_cache(self, id: str, suffix: str):
        if redis_session.exists(id + suffix):
            cache_data = pickle.loads(redis_session.get(id + suffix))
            del cache_data["_sa_instance_state"]
        else:
            cache_data = None

        return cache_data

    def set_cache(self, id: str, suffix: str, data):
        try:
            redis_session.setex(
                id + suffix, settings.EXPEIRATION_TIME_CACHE,
                pickle.dumps(data))
            return data
        except Exception as e:
            print(e)
            return {'msg': 'Bad Request!', 'error': str(e)}

    def delete_cache(self, id: str):
        redis_session.delete(id)
        return {'msg': 'Deleted!'}


redis_services = RedisServices()
