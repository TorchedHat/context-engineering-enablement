# 01 · Feel the meter

**Concept:** the conversation only grows, and everything costs its size.

Every step below works the same way: paste one thing, run `/context`, and
watch the `Messages` line. Before each `/context`, take a guess: will it go up
by a little, or a lot? None of the other lines move. Only `Messages` does.

**Side screen:** Open a second terminal and run `python3 tools/watch_context.py`
from the repo root. Keep it visible. Every step below shows up there as it lands:
one numbered line per thing that entered the conversation with its token cost,
a `/context` bar every time you run `/context`, and at compaction a yellow
banner followed by the summary in green. It follows the most recently written
transcript for this repo across all `~/.claude*` config dirs and prints which
one it picked. If it picked the wrong one, `--list` shows them all and
`--config-dir vertex` (or `--file PATH`) pins it.

Start a fresh session in this repo: `claude`.

### 0. Baseline
```
/context
```
Write down `Messages`. It should be close to zero. Everything else on the
screen is the fixed part. You pay for it on every message, but it isn't what
this exercise is about.

### 1. Chat is cheap
```
Before we start, three notes, no action needed: the gaudi oven is booked until 3pm, the oven team is on call today, and the customer ticket for this is AIPCC-7731.
```
```
/context
```
`Messages` moved by a few hundred tokens: your note plus the reply.

### 2. A file costs its size
```
@bakery/config.py what does this file do?
```
```
/context
```
`@` pastes the whole file into the conversation. This one is 20 lines, so the
jump is small. It stays in the conversation for the rest of the session,
whether or not anyone needs it again.

### 3. A log costs its size too
```
@data/logs/bake-0017.log why did this bake burn?
```
```
/context
```
About 1.1k tokens this time. The log is 82 lines, and the answer was the last
two. You paid for all 82, and you'll keep paying for them on every message
from here on.

### 4. Hand over everything
Step 3 handed over one log. Now watch what happens when you hand over
everything at once.
```
Read every log in data/logs in full, one Read call per file, in order from bake-0000 to bake-0039. Then read data/catalog.json lines 1 to 2000 with the Read tool in one call. No grep, no scripts, no subagents. When you're done, tell me how many bakes burnt.
```
```
/context
```
Watch the side screen. Forty-one Read calls scroll by, each printing one
`TOOL OUT` line with its token cost: about 1.5k per log, then one jump of
about 17k for the catalog chunk. The meter climbs past 100k. `Messages` is
now roughly half the window. Everything it read stays in the conversation for
the rest of the session, whether or not it needs it again. It answered one
question: how many bakes burnt. The answer was one line per log.

### 5. The first lever: ask for less
Repeat the question the cheap way.
```
Find the verdict line at the end of every log in data/logs and tell me which bakes burnt, how long each lasted, and why.
```
```
/context
```
This cost about 1k plus the search. Compare it with step 4: roughly 1k versus
roughly 85k. The lever is the wording. Name the part you need instead of
handing over the whole thing. This is the lever you'll use most.

### 6. Nothing comes out
```
Forget everything about bake-0017. Remove it from your context.
```
```
/context
```
`Messages` went **up**. It agreed, and the log is still in the request, now
followed by your instruction to forget it. The only thing that ever makes
`Messages` smaller is a summary, or starting over.

### 7. The safety net, and its limit
```
run the test suite
```
Watch what the agent gets back. The tests print 766 lines, but Claude Code
didn't put them in the conversation. It kept a 2 KB preview and wrote the rest
to a file, because the output was over its limit (30,000 bytes). It may then
choose to read that file back. The safety net only stops the first landing.

That limit is the catch. Anything under it goes in whole: a `pip install` log,
a stack trace, a 300-line test run. Step 5 is how you handle those yourself.

### What you saw

| Step | What went in | `Messages` grew by |
|---|---|---|
| 1 | a sentence | a few hundred tokens |
| 2 | a 20-line file | small |
| 3 | an 82-line log | ~1.1k |
| 4 | 40 logs in full plus 2,000 catalog lines | ~85k |
| 5 | 40 verdict lines from 40 logs, because you asked for the lines | ~1k, plus the search |
| 6 | "forget it" | up, not down |
| 7 | 766 lines of test output | a 2 KB preview, the rest went to a file |

Don't `/clear`. Exercise 02 works on its own, but it is best continued from this session with the meter this full.

> **Codex:** `/status` for the meter. `@file` works. Everything else is the
> same.
