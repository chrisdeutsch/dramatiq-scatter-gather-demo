from random import random
from typing import Any

import dramatiq

from dramatiq_scatter_gather_demo.broker import broker, result_backend

logger = dramatiq.get_logger(__name__)


@dramatiq.actor(store_results=True, queue_name="reliable_queue", broker=broker)
def reliable() -> int:
    logger.info("reliable")
    return 1


@dramatiq.actor(
    store_results=True,
    queue_name="flaky_queue",
    broker=broker,
    min_backoff=500,
    max_backoff=2_000,
)
def flaky() -> int:
    logger.info("flaky")
    if random() < 0.8:
        raise ValueError("boom")

    return 2


@dramatiq.actor(store_results=True, queue_name="gather_queue", broker=broker)
def gather(messages: list[dict[str, Any]]) -> int:
    results = [
        dramatiq.Message(**msg).get_result(backend=result_backend) for msg in messages
    ]
    logger.info("gather: %s", results)
    return sum(results)
