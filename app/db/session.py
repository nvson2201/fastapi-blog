from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import redis
import os

load_dotenv()

SQLALCHEMY_DB_URL = os.getenv("DATABASE_URL")
engine = create_engine(SQLALCHEMY_DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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
