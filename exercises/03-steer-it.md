# 03 · Steer it

**Concept:** the summary is written from instructions. You can add to them,
once or permanently.

Two fixes. Each one is exercise 02 again with one change.

> **Codex:** `/compact` takes no argument, so Fix A is Claude only. For
> Fix B, see the note under it. The guarantee is exercise 04.

## Fix A — this compaction only

Get the details back into context, then compact with instructions:
```
why did bake-0017 burn, and how long did it run?
```
```
/compact keep every bake number, runtime, and error message we discussed, verbatim
```
```
From context only: how many seconds did bake-0017 run before it burnt?
```
The text after `/compact` was passed to this one summary. The next
compaction, including an automatic one, will not have it.

## Fix B — every compaction

### 1. Add the rule
Open `CLAUDE.md` and add this at the bottom:
```
## Compaction
When compacting, keep every bake number, runtime, and error message that was
discussed, verbatim. Do not summarize them into counts.
```
That is the whole change: two lines of English in a file you own.

> **Codex:** the persistent version is `compact_prompt` in `config.toml`,
> not `AGENTS.md`. With OpenAI models compaction runs server-side and
> ignores it (openai/codex#34428). Try the `AGENTS.md` edit anyway and see.

### 2. Same setup, plain compact
```
why did bake-0035 burn, and how long did it run?
```
```
/compact
```
```
From context only: how many seconds did bake-0035 run before it burnt?
```

You typed nothing extra this time. CLAUDE.md is re-read from disk at
compaction, so the rule was there when the summary was written. It will be
there at 3am too.

Neither fix is a guarantee. They raise the odds. For a guarantee, see 04.
