---
hide:
  - navigation
  - toc
---

<p class="lead">A complete, worked-through guide to system design: the theory, the
building blocks, the twelve heuristics that fix most bottlenecks, fifteen designs
worked end to end, and the practice material to hold it all together.</p>

# System Design Guide

Most system design material is either a list of vocabulary or a pile of interview
transcripts. This guide tries to be the thing in between: the reasoning that connects a
symptom you can observe to a fix you can defend, with the cost of that fix stated up
front.

It began as twelve lines.

> Slow reads → add a cache · Write spikes → buffer with a queue · Too much traffic → add
> a load balancer · Read-heavy DB → add read replicas · Write-heavy DB → shard the data ·
> Slow queries → add indexes · Slow files → object storage + CDN · Temporary failures →
> retry with backoff · Too many requests → rate limiting · One service failing → circuit
> breaker · Duplicate requests → idempotency keys · Can't see what broke → logs, metrics,
> tracing

Those twelve lines are a good diagnostic vocabulary and a terrible education on their
own. Each one hides a question — *when is this the right move, what breaks when I do it,
and what do I give up?* — and the answer to that question is what interviews are
actually testing. So each line became a page, and each page needed the theory and the
component underneath it, and the whole thing needed somewhere to be applied.

## How the guide is organised

<div class="grid cards" markdown>

-   **Start here**

    ---

    The shape of a design interview, a six-step framework for answering one, estimation
    drills and a four-week plan.

    [:octicons-arrow-right-24: Begin](getting-started/index.md)

-   **Fundamentals**

    ---

    Scalability, latency, availability, consistency, transactions, replication, caching,
    networking, storage models, delivery semantics.

    [:octicons-arrow-right-24: Learn the theory](fundamentals/index.md)

-   **Building blocks**

    ---

    Nineteen components, each with the failure modes that matter and the trade-offs
    that decide between them.

    [:octicons-arrow-right-24: Meet the parts](building-blocks/index.md)

-   **The 12 patterns**

    ---

    The original cheat sheet, expanded: mechanism, when to use it, trade-offs, and a
    sentence to say out loud.

    [:octicons-arrow-right-24: Read the patterns](patterns/index.md)

-   **Case studies**

    ---

    Fifteen systems designed from scratch — requirements, estimates, API, data model,
    architecture, bottlenecks, failure story.

    [:octicons-arrow-right-24: Work an example](case-studies/index.md)

-   **Interview practice**

    ---

    Trade-off cheat sheet, common mistakes, a full mock walkthrough, question bank and
    glossary.

    [:octicons-arrow-right-24: Practise](interview/index.md)

</div>

## Three ways to read this

**If you have an interview in a week.** Read [the answering
framework](getting-started/answering-framework.md), then the [trade-off cheat
sheet](interview/trade-off-cheatsheet.md), then two or three case studies out loud with
a timer. Do not try to read the whole guide.

**If you are learning the subject.** Work through Fundamentals, then Building blocks,
then the twelve patterns. Each section assumes the one before it. Do the case studies
last, with the book closed, and compare afterwards.

**If you are here for one answer.** Every page is written so that the first two
sections — *what it is* and *when to reach for it* — stand alone. Search for the symptom
and read the first screen.

## A note on numbers

Every figure in this guide that describes a real system's scale is an assumption, not a
fact, and is labelled as one. The latency table in [estimation
drills](getting-started/estimation.md) is order-of-magnitude, drawn from the widely
circulated "latency numbers every programmer should know". Treat them as enough to
justify a design choice in conversation, not as benchmarks.
