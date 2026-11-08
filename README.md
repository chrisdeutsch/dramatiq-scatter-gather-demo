# `dramatiq-scatter-gather-demo`

A minimal distributed scatter-gather with [dramatiq](https://dramatiq.io): two actors, `reliable`
and `flaky`, run as a `group`, and a `gather` actor is enqueued as the group's completion
callback. It reads their results from the result backend and sums them.

Each actor has its own queue and its own worker container, to show that the steps can
run on different machines. Valkey is the broker, the result backend and the backend
for the group barrier.

## Run

Needs Docker and [uv](https://docs.astral.sh/uv/). The workers and Valkey run in
containers; the sender runs on your machine and reaches Valkey on `127.0.0.1:6379`.

```sh
docker compose up -d --build
uv run send             # prints "Result: 3"
docker compose logs -f  # watch the workers
docker compose down     # stop everything
```
