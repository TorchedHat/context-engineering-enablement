# 01 · Feel the meter

**Concept:** the conversation only grows. Everything the agent sees goes in.

After each step, run `/context` and watch which block moved.

### 1. Baseline
```
/context
```
You have typed nothing. The system prompt, tools, and CLAUDE.md are already
there, and they are re-sent on every message. That is the recurring bill.

### 2. A file
```
@bakery/config.py what does this file do?
```
`@` attaches the file to your message. Run `/context`. Which block moved?

### 3. A bigger file
```
@data/catalog.json what is in this file?
```
Same question, different file. Run `/context`. Compare to step 2.

**The cost is the size of what the agent reads, not the size of what you ask.**

### 4. A question that makes it go look
```
why did bake-0017 burn?
```
You attached nothing. The agent went and found the log itself. Run `/context`.

### 5. A noisy command
```
run the test suite
```
Everything the tests print lands in the conversation. Run `/context`.

**Command output counts the same as a file.** Build logs, stack traces, a
verbose install. Same place.

### 6. Try to take it back
```
forget everything you read in catalog.json
```
Run `/context`. Did anything move?

The conversation is append-only. Only compaction makes it smaller, and that
is exercise 02. Keep this session open.

> **Codex:** `/status` in place of `/context`; it shows a total, not the blocks.
