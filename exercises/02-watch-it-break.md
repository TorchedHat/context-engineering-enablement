# 02 · Watch it break

**Concept:** compaction replaces the conversation with a summary. The summary
decides what survives, and it has no idea what you'll ask next.

Continue the session from exercise 01. The test is simple: ask three questions,
compact, ask the same three questions again, and compare.

### 1. Before
```
From what is already in context, no tools:
1. Which burnt bake had the shortest runtime, and how many seconds was it?
2. What error did bake-0035 hit?
3. Who is on call, and what is the ticket number?
```
Expected: bake-0039 at 752s; Gaudi SynapseAI headers not found; Priya,
AIPCC-7731. Leave this answer on screen. You're about to compare against it.

### 2. Measure
```
/context
```
Write down `Messages`. This is everything the agent knows about this session.

### 3. Compact
```
/compact
```
The model just wrote a summary of the whole conversation, and the summary took
its place. Everything above the `Compacted` line is gone from the request.

### 4. Measure again
```
/context
```
`Messages` is a fraction of what it was in step 2. This is the only time that
number goes down.

### 5. Read what survived
Press `ctrl+o` on the `Compacted` line to expand the summary, and read it.
Notice what kind of thing it kept: what you were doing, what was concluded.
Then notice what it condensed. The ninety lines from step 5 of exercise 01 are
now a sentence, if they're there at all.

If `ctrl+o` doesn't show it, ask:
```
Print the compaction summary you were given, verbatim, and nothing else.
```

### 6. After
Paste step 1 again, word for word.
```
From what is already in context, no tools:
1. Which burnt bake had the shortest runtime, and how many seconds was it?
2. What error did bake-0035 hit?
3. Who is on call, and what is the ticket number?
```
Compare with the answer from step 1, line by line.

### What to look for

The three questions were chosen to fail in order.

- **Question 1** needs all eleven burnt runtimes. A summary almost never keeps
  a table. Expect a wrong bake, a wrong number, or "I'd need to re-read the
  logs". A confident wrong number is the common case, and the one that causes
  problems.
- **Question 2** needs one detail from the same output. Sometimes it survives.
- **Question 3** is something *you said*. Summaries keep what the user said far
  more reliably than what a tool printed.

That order is what to take away. The summarizer keeps the story and drops
the data, and its idea of what matters isn't yours.

**If it got all three right:** look at the summary from step 5. The answers are
sitting in it, in words. It didn't remember them, it read them back from the
summary. So ask for something that *isn't* in the summary. The port number
from `config.py` is a good one:
```
From context only: what is DEFAULT_PORT in bakery/config.py?
```
It will offer to read the file. That's the right move, and it costs a read.
Anything that was never written to disk and didn't make the summary has no
such fallback.

**If it reached for a tool** despite "no tools": that's also the lesson. It
can only recover what's on disk, and the on-call note isn't on disk.

### 7. The line
```
/context
```
Look at the autocompact buffer. This time you typed `/compact` yourself. In a
real session it fires when `Messages` reaches that line: in the middle of a
task, without asking, and the summary is written with no idea what you'll need
next. Exercises 03 and 04 are about taking control of that.

> **Codex:** the summary is never shown. Run the same before and after
> questions; the comparison is the only evidence you get.
