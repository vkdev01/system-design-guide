# System Design Guide

An exhaustive, worked-through guide to designing large systems — written to be read
end to end, or used as a lookup table the night before an interview.

**Read it at [vkdev01.github.io/system-design-guide](https://vkdev01.github.io/system-design-guide/).**

The project started as a twelve-line cheat sheet — *slow reads → add a cache, write
spikes → buffer with a queue, and so on* — and grew into a full curriculum: the theory
underneath those one-liners, the building blocks they name, the trade-offs that decide
between them, and fifteen designs worked through end to end.

## What is inside

| Section | What it covers |
| --- | --- |
| **Start here** | How to use the guide, the shape of a design interview, a six-step answering framework, estimation drills, and a four-week study plan. |
| **Fundamentals** | Scalability, latency versus throughput, availability maths, consistency models, transactions, replication and partitioning, caching theory, networking, storage models, delivery semantics. |
| **Building blocks** | Nineteen components — load balancer, API gateway, CDN, object storage, cache, queue, indexes, replicas, sharding, rate limiter, circuit breaker, retry, idempotency, distributed locks, search, service discovery, observability, sagas, batch and stream. |
| **The 12 patterns** | The original cheat sheet, one page per line: mechanism, when to reach for it, the trade-offs an interviewer will push on, and a sentence to say out loud. |
| **Case studies** | Fifteen designs: URL shortener, rate limiter, ID generator, crawler, news feed, chat, video, file sync, ride hailing, ticket booking, payments, notifications, metrics pipeline, autocomplete, distributed cache. |
| **Interview practice** | Trade-off cheat sheet, the mistakes that sink candidates, a full mock walkthrough, a question bank and a glossary. |
| **Code samples** | Runnable, tested Python for the mechanisms that are easiest to get wrong: backoff, token bucket, circuit breaker, idempotency, consistent hashing, shard routing, LRU. |

## Run it locally

```bash
git clone https://github.com/vkdev01/system-design-guide.git
cd system-design-guide
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve          # http://127.0.0.1:8000
```

Build a static copy with `mkdocs build --strict`; the output lands in `site/`.

The Python samples have their own tests:

```bash
pip install pytest
pytest -q code/python/tests
```

## How the site is built

MkDocs with the Material theme, deployed to GitHub Pages by the workflow in
`.github/workflows/deploy.yml` on every push to `main`. Diagrams are Mermaid, written
inline in the Markdown, so they stay in version control next to the prose that
describes them. A second workflow builds the docs strictly and runs the code tests on
every pull request.

## Contributing

Corrections, sharper diagrams and new case studies are welcome — see
[CONTRIBUTING.md](CONTRIBUTING.md). The one rule that matters: every claim about a
trade-off should say what you give up, not just what you gain.

## Licence

MIT. Use it, fork it, teach from it.
