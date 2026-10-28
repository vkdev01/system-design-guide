<p class="lead">The compressed version of the whole guide: the trade-offs, the mistakes, and a
full worked mock you can use as a rehearsal script.</p>

# Interview practice

| Page | Use it for |
| --- | --- |
| [Trade-off cheat sheet](trade-off-cheatsheet.md) | Last-minute revision; every decision with its price |
| [Common mistakes](common-mistakes.md) | Diagnosing your own bad habits |
| [Mock walkthrough](mock-walkthrough.md) | A complete 45-minute answer, annotated |
| [Question bank](question-bank.md) | Practice prompts grouped by what they test |
| [Glossary](glossary.md) | Terms that come up and get misused |

## The five-sentence summary of everything

1. Put numbers on the problem before choosing anything.
2. Fix reads with caches and replicas, fix writes with queues and sharding, fix queries with
   indexes — in that order of cost.
3. Every dependency needs a timeout, a retry policy, and a fallback.
4. Anything with a side effect needs an idempotency key.
5. Say what you would measure, and what you expect to break first.

If you can say those five sentences and then defend each one, you are most of the way there.
