<p class="lead">Fifteen systems, each worked through the same eight steps: requirements,
estimates, API, data model, architecture, deep dives, bottlenecks, failure story.</p>

# Case studies

| Design | The interesting constraint |
| --- | --- |
| [URL shortener](url-shortener.md) | Key generation without collisions, and read scale on a tiny record |
| [Rate limiter](rate-limiter-service.md) | Distributed counters, fast enough to be worth having |
| [Unique ID generator](id-generator.md) | Ordered, collision-free IDs across machines with no coordination |
| [Web crawler](web-crawler.md) | Politeness, deduplication, a frontier that never sleeps |
| [News feed](news-feed.md) | Fan-out on write versus read, and the celebrity problem |
| [Chat system](chat.md) | Per-conversation ordering, presence, delivery guarantees |
| [Video platform](video-platform.md) | Storage economics, transcoding pipelines, adaptive streaming |
| [File storage and sync](file-sync.md) | Chunking, conflict resolution, metadata consistency |
| [Ride hailing](ride-hailing.md) | Geospatial matching with a hard freshness requirement |
| [Ticket booking](ticket-booking.md) | No double-selling under a flash crowd |
| [Payments and ledger](payments-ledger.md) | Double-entry correctness, idempotency, reconciliation |
| [Notification system](notifications.md) | Fan-out across channels, dedupe, provider rate limits |
| [Metrics and alerting](metrics-pipeline.md) | High-volume ingestion and cheap aggregation |
| [Search autocomplete](autocomplete.md) | Sub-100 ms prefix lookup on shifting popularity |
| [Distributed cache](distributed-cache.md) | Building the thing you usually just use |

## How to practise with them

Read one, then close the page and redraw it from memory in twenty minutes. The gap between
what you remembered and what was there is your study list.

Each case study ends with a **soundbite** and a **failure story**, because those are the two
parts candidates skip and interviewers weight most heavily.
