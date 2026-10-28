# About

This guide is a personal curriculum that got out of hand.

It started as a twelve-line cheat sheet of symptoms and fixes, the kind of thing that
circulates on social media because it compresses well. Compression is the problem: those
twelve lines are the *answers* to a design interview, with all the reasoning stripped
out. Knowing that slow reads want a cache does not help you when the interviewer asks
what happens to that cache when a hot key expires, or why you would not simply add
another read replica.

So the twelve lines became the spine, and everything else grew around them.

## What this guide tries to do differently

**State the cost, not just the benefit.** Every pattern page names at least three
trade-offs. A design answer that only lists upsides reads as memorised.

**Keep the numbers honest.** Where a figure is an assumption, it says so. Where a number
is an order of magnitude, it says that too. There is no invented benchmark in here.

**Prefer mechanisms to brand names.** "A durable append-only log with per-partition
ordering" is more useful in an interview than a product name, because it survives the
follow-up question about how it works.

**Write the sentence.** Each pattern and case study ends with a soundbite — the actual
words you would say. Candidates usually know the concept and freeze on the phrasing.

## Scope

In scope: single-datacentre and multi-region web systems, storage and messaging
internals at the level an application engineer needs, reliability patterns, and the
observability needed to run any of it.

Out of scope: hardware, kernel tuning, machine-learning systems, and organisation design.
Occasionally mentioned, never assumed.

## Corrections

If something here is wrong — a stale product detail, a claim that does not hold under
scrutiny, a diagram that contradicts its prose — please open an issue. Corrections with
a source are merged quickly.
