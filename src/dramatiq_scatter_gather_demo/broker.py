import os

from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware import GroupCallbacks
from dramatiq.rate_limits.backends import RedisBackend as RedisRateLimiterBackend
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend as RedisResultBackend
from redis import Redis

redis = Redis.from_url(
    os.environ.get("VALKEY_URL", "redis://localhost:6379"), socket_timeout=60
)
broker = RedisBroker(client=redis)

# The rate limiter backend is used for completion counters to achieve the gather
rate_limiter_backend = RedisRateLimiterBackend(client=redis)
broker.add_middleware(GroupCallbacks(rate_limiter_backend))

# Middleware order matters: after_ hooks run in reverse middleware order, so
# Results must be added after GroupCallbacks to store the result before the
# callback is enqueued.
result_backend = RedisResultBackend(client=redis)
broker.add_middleware(Results(backend=result_backend))
