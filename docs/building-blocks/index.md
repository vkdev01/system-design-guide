<p class="lead">Nineteen components, each an answer to a specific failure. Learn the
symptom each one fixes and the price it charges, and the design follows.</p>

# Building blocks

| Block | Fixes | The price |
| --- | --- | --- |
| [Load balancer](load-balancer.md) | One machine cannot take the traffic | A new hop, and a new thing that can fail |
| [API gateway](api-gateway.md) | Cross-cutting concerns duplicated in every service | Another network hop, another deploy surface |
| [CDN](cdn.md) | Users are far from the origin | Invalidation, and per-request cost |
| [Object storage](object-storage.md) | Blobs do not belong in a database | Higher latency, no partial updates |
| [Cache](cache.md) | The same expensive answer is computed repeatedly | Staleness, and invalidation logic |
| [Message queue](message-queue.md) | Arrival rate exceeds processing rate | Eventual completion, duplicates, ordering |
| [Indexes](indexes.md) | Queries scan instead of seek | Write amplification, storage |
| [Read replicas](read-replicas.md) | Reads exceed one node | Lag, and failover decisions |
| [Sharding](sharding.md) | Writes or data exceed one node | Cross-shard queries, rebalancing, hot shards |
| [Rate limiter](rate-limiter.md) | One caller can consume the whole system | Rejected requests, shared state |
| [Circuit breaker](circuit-breaker.md) | A dead dependency consumes your resources | A fallback you must design |
| [Retry and backoff](retry.md) | Transient errors become user-visible failures | Amplified load during outages |
| [Idempotency](idempotency.md) | Retries and redeliveries duplicate side effects | A key store, and atomicity |
| [Distributed locks](distributed-locks.md) | Two workers do the same job | Correctness depends on clocks and leases |
| [Search index](search-index.md) | `LIKE '%term%'` is unusable | A derived store that can lag |
| [Service discovery](service-discovery.md) | Instances move and multiply | Another dependency, and staleness |
| [Observability](observability.md) | You find out from users | Cost, cardinality, and effort |
| [Sagas](sagas.md) | Work spans services without a shared transaction | Compensations and visible intermediate states |
| [Batch and stream](batch-and-stream.md) | Per-event processing is too slow or too expensive | Latency, and a second code path |

## How to read a block page

Each page has the same six sections: what it is, how it works, when to reach for it,
trade-offs, failure modes, and an interview soundbite. The **failure modes** section is the
one interviewers probe, so read it even when you are skimming.
