import redis
pool = redis.ConnectionPool(
    host="localhost",
    port="6379",
    password="123456",
)
redis_session = redis.Redis(connection_pool=pool)


if __name__ == "__main__":
    token = {
        "expiredTime": "1506433269",
        "expiration": "2017-09-26T13:41:09Z",
        "credentials": {
            "sessionToken": "sdadffwe2323er4323423",
            "tmpSecretId": "VpxrX0IMC pHXWL0Wr3KQNCqJix1uhMqD",
            "tmpSecretKey": "VpxrX0IMC pHXWL0Wr3KQNCqJix1uhMqD"
        }
    }

    import pickle
    redis_session.setex("user", 100, pickle.dumps(token))
    print(pickle.loads(redis_session.get("user")))
    print(redis_session.exists("2user_id"))
