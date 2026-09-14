# 01 · Feel the meter

**Concept:** the conversation only grows, and everything costs its size.

Every step below works the same way: paste one thing, run `/context`, and
watch the `Messages` line. Before each `/context`, take a guess: will it go up
by a little, or a lot? None of the other lines move. Only `Messages` does.

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

### 4. The first lever: ask for less
Step 3 handed over a whole log to answer a question the last two lines could
answer. This time hand over nothing. Say what you need in plain words and let
the agent go get it. Every log ends with one verdict line, so ask for that
line, from all forty logs at once.
```
Find the verdict line at the end of every log in data/logs and tell me which bakes burnt, how long each lasted, and why.
```
```
/context
```
The forty verdict lines are about 1k tokens. Add whatever it did to find
them: it may open a log or two and try a few searches first, so expect a few
k in total. Compare that with step 3. One log in full cost about 1.1k and
answered one question. Forty logs, asked for by the part you need, cost about
the same and answered forty. It now knows how every bake ended and why.

The lever is the wording. "Why did this burn" with a file attached puts the
whole file in. "Find the verdict line" puts in the verdict lines, plus the
cost of looking, and nothing else. Name the part you need instead of handing
over the whole thing. This is the lever you'll use most.

### 5. Nothing comes out
```
Forget everything about bake-0017. Remove it from your context.
```
```
/context
```
`Messages` went **up**. It agreed, and the log is still in the request, now
followed by your instruction to forget it. The only thing that ever makes
`Messages` smaller is a summary, or starting over.

### 6. The safety net, and its limit
```
run the test suite
```
Watch what the agent gets back. The tests print 766 lines, but Claude Code
didn't put them in the conversation. It kept a 2 KB preview and wrote the rest
to a file, because the output was over its limit (30,000 bytes). It may then
choose to read that file back. The safety net only stops the first landing.

That limit is the catch. Anything under it goes in whole: a `pip install` log,
a stack trace, a 300-line test run. Step 4 is how you handle those yourself.

### What you saw

| Step | What went in | `Messages` grew by |
|---|---|---|
| 1 | a sentence | a few hundred tokens |
| 2 | a 20-line file | small |
| 3 | an 82-line log | ~1.1k |
| 4 | 40 verdict lines from 40 logs, because you asked for the lines | ~1k, plus the search |
| 5 | "forget it" | up, not down |
| 6 | 766 lines of test output | a 2 KB preview, the rest went to a file |

> **Codex:** `/status` for the meter. `@file` works. Everything else is the
> same.
