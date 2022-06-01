import pickle

from app.plugins.redis.session import redis_session
from app.config import settings


class RedisServices:
    def get_cache(self, id: int, prefix: str):
        if redis_session.exists(prefix + str(id)):
            cache_data = pickle.loads(redis_session.get(prefix + str(id)))
            if "_sa_instance_state" in cache_data:
                del cache_data["_sa_instance_state"]
        else:
            cache_data = None

        return cache_data

    def set_cache(self, id: int, prefix: str, data):
        try:
            redis_session.setex(
                prefix + str(id), settings.EXPEIRATION_TIME_CACHE,
                pickle.dumps(data))
            return data
        except Exception as e:
            print(e)
            return {'msg': 'Bad Request!', 'error': str(e)}

    def delete_cache(self, id: str, prefix: str):
        redis_session.delete(prefix + str(id))
        return {'msg': 'Deleted!'}

    def flush_all(self):
        return redis_session.flushall()


redis_services = RedisServices()
