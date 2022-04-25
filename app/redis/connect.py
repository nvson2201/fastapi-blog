from app.redis.containers import Container

container = Container()
container.config.redis_host.from_env("REDIS_HOST", "localhost:6379")
container.config.redis_password.from_env("REDIS_PASSWORD", "123456")
container.wire(modules=[__name__])
