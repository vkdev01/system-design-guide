<p class="lead">The ten ideas everything else is built from. Read these before the
building blocks — the blocks only make sense as answers to the questions posed here.</p>

# Fundamentals

Each page in this section answers a question that recurs in every design:

| Question | Page |
| --- | --- |
| How does a system grow without being rewritten? | [Scalability](scalability.md) |
| Why is the system slow when it is not busy? | [Latency and throughput](latency-and-throughput.md) |
| How many nines can I afford, and what does each one cost? | [Availability and reliability](availability.md) |
| What does a user actually see while replicas catch up? | [Consistency models](consistency.md) |
| When do I need a transaction, and when is it in the way? | [ACID, BASE and transactions](transactions.md) |
| How do I split data without splitting it wrongly? | [Replication and partitioning](replication-and-partitioning.md) |
| What belongs in a cache, and what must never be? | [Caching theory](caching.md) |
| Which of the 0.5 ms and 150 ms numbers apply here? | [Networking](networking.md) |
| Which database, actually? | [Data storage models](storage-models.md) |
| What does "exactly once" really mean? | [Delivery semantics](delivery-semantics.md) |

## The thread running through them

All ten pages are about the same tension: you cannot have perfect consistency, perfect
availability, low latency and cheap operation at the same time. Every building block in
the next section is a device for trading one of those for another. Knowing which trade a
component makes is what lets you pick it deliberately instead of by reputation.
