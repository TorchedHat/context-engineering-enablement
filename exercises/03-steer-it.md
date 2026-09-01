# 03 · Steer it

**Concept:** the summary is written from instructions, and you can add to
them, once or permanently.

Two fixes. Each one is exercise 02 again with a single change.

> **Codex:** `/compact` takes no argument, so Fix A is Claude only. For
> Fix B, see the note under it. The guarantee is exercise 04.

## Setup

Start a fresh session: `claude`. Three pastes rebuild the state from 02.
```
Before we start, three notes, no action needed: the gaudi oven is booked until 3pm, Priya is on call today, and the customer ticket for this is AIPCC-7731.
```
```
!grep -h -E "ERROR|^===" data/logs/*.log
```
```
Which bakes burnt, and how long did each one run before it burnt?
```
Now the same three questions as 02. This is your "before", so keep it on
screen.
```
From what is already in context, no tools:
1. Which burnt bake had the shortest runtime, and how many seconds was it?
2. What error did bake-0035 hit?
3. Who is on call, and what is the ticket number?
```
Expected: bake-0039 at 752s; Gaudi SynapseAI headers not found; Priya,
AIPCC-7731.

## Fix A — this compaction only

Compact, but tell the summarizer what matters:
```
/compact keep every burnt bake number with its runtime and error message, verbatim, and every note the user gave at the start
```
Then the three questions again, word for word:
```
From what is already in context, no tools:
1. Which burnt bake had the shortest runtime, and how many seconds was it?
2. What error did bake-0035 hit?
3. Who is on call, and what is the ticket number?
```
Expected: all three match your "before". Press `ctrl+o` on the `Compacted`
line and look at the summary. The runtimes are in it this time, because you
asked for them. Compare with what the summary in 02 kept.

The text after `/compact` went to this one summary only. The next compaction,
including an automatic one, won't have it.

## Fix B — every compaction

### 1. Add the rule
Open `CLAUDE.md` and add this at the bottom:
```
## Compaction
When compacting, keep every bake number, runtime, and error message that was
discussed, verbatim. Do not summarize them into counts. Keep every note the
user gave.
```
That's the whole change: three lines in a file you own.

> **Codex:** the persistent version is `compact_prompt` in `config.toml`,
> not `AGENTS.md`. With OpenAI models compaction runs server-side and
> ignores it (openai/codex#34428). Try the `AGENTS.md` edit anyway and see.

### 2. Reload the data, plain compact
Right now the summary from Fix A is the only copy of the runtimes, and the
next summary would be written from that. Put the raw lines back first so the
test is fair:
```
!grep -h -E "ERROR|^===" data/logs/*.log
```
```
/compact
```
```
From what is already in context, no tools:
1. Which burnt bake had the shortest runtime, and how many seconds was it?
2. What error did bake-0035 hit?
3. Who is on call, and what is the ticket number?
```

Expected: same as Fix A. You typed nothing after `/compact` this time.
CLAUDE.md is read from disk when the summary is written, so the rule was
there. It's also there when compaction fires on its own.

If the summary ignored the rule, quit, restart `claude`, and redo the setup.
That way the rule is loaded from the start.

Neither fix is a guarantee. They raise the odds. For a guarantee, see 04.
