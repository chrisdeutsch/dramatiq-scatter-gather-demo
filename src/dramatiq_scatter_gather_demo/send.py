from dramatiq import group

from dramatiq_scatter_gather_demo.actors import flaky, gather, reliable
from dramatiq_scatter_gather_demo.broker import broker, result_backend


def main() -> int:
    g = group([reliable.message(), flaky.message()], broker=broker)
    gather_msg = gather.message([m.asdict() for m in g.children])
    g.add_completion_callback(gather_msg)
    g.run()

    result = gather_msg.get_result(backend=result_backend, block=True, timeout=30_000)
    print(f"Result: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
