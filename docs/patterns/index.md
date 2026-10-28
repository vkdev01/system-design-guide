<p class="lead">Twelve symptoms and the fix each one points to. The diagnostic
vocabulary for the last ten minutes of any design interview.</p>

# The twelve patterns

| # | Symptom | Fix | Layer |
| --- | --- | --- | --- |
| 01 | [Slow reads](slow-reads-cache.md) | Add a cache | Read path |
| 02 | [Write spikes](write-spikes-queue.md) | Buffer with a queue | Ingest |
| 03 | [Too much traffic](traffic-load-balancer.md) | Add a load balancer | Edge |
| 04 | [Read-heavy database](read-heavy-replicas.md) | Add read replicas | Storage |
| 05 | [Write-heavy database](write-heavy-shard.md) | Shard the data | Storage |
| 06 | [Slow queries](slow-queries-indexes.md) | Add indexes | Storage |
| 07 | [Slow file loads](slow-files-object-storage-cdn.md) | Object storage + CDN | Media |
| 08 | [Temporary failures](temporary-failures-retry.md) | Retry with backoff | Resilience |
| 09 | [Too many requests](too-many-requests-rate-limit.md) | Rate limiting | Edge |
| 10 | [One service failing](one-service-failing-breaker.md) | Circuit breaker | Resilience |
| 11 | [Duplicate requests](duplicate-requests-idempotency.md) | Idempotency keys | Resilience |
| 12 | [Can't see what broke](cannot-see-what-broke-telemetry.md) | Logs, metrics, tracing | Observability |

## How to use the list

It is a checklist, not a script. In the last ten minutes of an interview, walk it in this
order and say one sentence per line that applies:

1. Are reads slow? (01, 04, 06)
2. Are writes spiking? (02, 05)
3. Is the entry point overloaded? (03, 09)
4. Are files slow? (07)
5. What happens when a dependency fails? (08, 10, 11)
6. How would you know? (12)

The order matters. It goes from cheapest and most reversible (indexes, caches) to most
expensive and permanent (sharding), which is also the order a careful engineer would actually
work in.

!!! tip "The single most common mistake"
    Reaching for a distributed-systems pattern when the answer is a missing index. A
    candidate who says "before anything else I'd check `EXPLAIN` — this might be a missing
    composite index" has demonstrated more judgement than one who immediately shards.

## The one-line version

> Slow reads, cache. Write spikes, queue. Too much traffic, load balance. Read-heavy,
> replicate. Write-heavy, shard. Slow queries, index. Slow files, object storage and a CDN.
> Temporary failures, retry with backoff. Too many requests, rate limit. One service failing,
> break the circuit. Duplicate requests, idempotency keys. Can't see what broke, logs, metrics
> and tracing.

Then read [choosing between overlapping fixes](choosing-between-fixes.md), which is where the
marks are actually won.
