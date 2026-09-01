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
Before we start, three notes, no action needed: the gaudi oven is booked until 3pm, Priya is on call today, and the customer ticket for this is AIPCC-7731.
```
```
/context
```
`Messages` moved by a few hundred tokens: your note plus the reply. Hold on to
those three facts. They come back in exercise 02.

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
About 1.1k tokens this time. The log is 80 lines, and the answer was two of
them, near the bottom. You paid for all 80, and you'll keep paying for them on
every message from here on.

### 4. The first lever: shape what goes in
Same question, different bake. This time, send it only the two lines that
matter. The `!` prefix runs a shell command and puts its output in the
conversation, and nothing else.
```
!grep -E "ERROR|BURNT" data/logs/bake-0035.log
```
```
why did bake-0035 burn?
```
```
/context
```
Same quality of answer, at about a tenth of the cost. This is the lever you'll
use most: `grep`, `tail`, `head`, `--quiet`, applied before the output enters
the conversation rather than after.

### 5. Forty bakes in one command
Now pull the interesting lines from every log at once. This is the working set
for exercise 02.
```
!grep -h -E "ERROR|^===" data/logs/*.log
```
```
Which bakes burnt, and how long did each one run before it burnt?
```
```
/context
```
Ninety lines, about 1.4k tokens, and it now knows how all 40 bakes ended.
Compare that with step 3: one log in full cost about the same as forty logs
shaped.

### 6. Nothing comes out
```
Forget everything about bake-0017. Remove it from your context.
```
```
/context
```
`Messages` went **up**. It agreed, and the log is still in the request, now
followed by your instruction to forget it. The conversation is
append-only. That's claim 1, and it's why exercise 02 exists: the only thing
that ever makes `Messages` smaller is a summary.

### 7. The safety net, and its limit
```
run the test suite
```
Watch what the agent gets back. The tests print 760 lines, but Claude Code
didn't put them in the conversation. It kept a 2 KB preview and wrote the rest
to a file, because the output was over its limit (30,000 bytes).

That limit is the catch. Anything under it goes in whole: a `pip install` log,
a stack trace, a 300-line test run. Step 4 is how you handle those yourself.

### What you saw

| Step | What went in | `Messages` grew by |
|---|---|---|
| 1 | a sentence | a few hundred tokens |
| 2 | a 20-line file | small |
| 3 | an 80-line log | ~1.1k |
| 4 | two grepped lines | ~0.2k |
| 5 | 90 lines from 40 logs | ~1.4k |
| 6 | "forget it" | up, not down |
| 7 | 760 lines of test output | ~0.7k, the rest went to a file |

Keep this session open. Exercise 02 needs everything that's in it.

> **Codex:** `/status` for the meter. `@file` works. There's no `!` prefix, so
> ask it to run the grep instead. The output lands in context the same way.
