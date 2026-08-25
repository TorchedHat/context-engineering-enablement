# 06 · Delegate

**Concept:** a subagent filters context. It reads in its own bucket and hands
you only the answer.

Reading all of `data/` would fill most of your conversation. Do the same work
without paying for it in your session.

### 1. Note the number
```
/context
```

### 2. Delegate the reading
```
Use a subagent to read every file under data/ and report which packages burn
most, on which ovens, and why. Give me only the report.
```

### 3. Check the number
```
/context
```
Compare to step 1, and to what a single log cost in exercise 01. The
subagent had its own request and its own history. Yours got one message: the
report.

### The honest part
- You still paid for those tokens. You bought a lean history, not free work.
- You waited for it. Delegation costs latency.
- Whatever the subagent left out of the report, you never see. Ask for what
  you need in the report, not after.

**Use this for research** — "investigate X", "read all the logs", "find every
caller" — anything that would fill your bucket with things you only need the
conclusion of.

> **Codex:** `/subagents`, or ask for one in the prompt as above.
