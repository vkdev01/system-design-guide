# Contributing

Thanks for helping. This guide is meant to stay accurate and opinionated rather than
long for its own sake.

## Ways to contribute

- **Fix an error.** Wrong numbers, stale product details, a diagram that does not
  match the prose.
- **Sharpen a trade-off.** If a page says "use a queue" without saying what it costs
  you, that is a bug.
- **Add a case study.** Follow the structure of the existing ones so the section stays
  comparable.
- **Improve a code sample.** Samples should be short enough to read in one sitting and
  covered by a test.

## Page conventions

Every content page follows the same skeleton so readers can skim:

1. An H1 that matches the navigation label.
2. A one-sentence summary in a `<p class="lead">` block.
3. **What it is** — the mechanism, in plain language.
4. **When to reach for it** — the conditions that justify it.
5. **Trade-offs** — at least three, each naming what you lose.
6. **Interview soundbite** — one sentence a candidate could actually say.
7. **Where to go next** — links to related pages.

Diagrams are Mermaid fenced blocks, never images, so they can be edited in a diff.

## Local checks

```bash
pip install -r requirements.txt pytest
mkdocs build --strict      # catches broken internal links and nav entries
pytest -q code/python/tests
```

`--strict` is what CI runs, so a page that is not in `mkdocs.yml` or a link to a
renamed file will fail the build.

## Commits and pull requests

Small, focused commits with an imperative subject line (`Fix replica lag explanation`).
In the pull request, say what you changed and why the previous version was wrong or
unclear. Content changes that contradict another page should update both.
