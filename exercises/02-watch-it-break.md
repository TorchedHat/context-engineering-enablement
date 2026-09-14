# 02 · Watch it break

**Concept:** compaction replaces the conversation with a summary. The summary
decides what survives, and it has no idea what you'll ask next.

Start a fresh session in this repo: `claude`.

### 1. Say one thing
```
My favorite color is red. No action needed.
```

### 2. Make it produce a lot
```
Generate 30 random 6-digit codes, numbered 1 to 30, one per line, in your reply. No files.
```
Thirty lines nobody could have guessed. Keep them on screen.

### 3. Measure, compact, measure again
```
/context
```
Note the number on the `Messages` line.
```
/compact
```
```
/context
```
Everything above the `Compacted` line is now a summary. `Messages` is a
fraction of what it was. That number only goes down here and in step 8.

### 4. Read what survived
Press `ctrl+o` on the `Compacted` line to expand the summary. If it doesn't
open, ask:
```
Print the compaction summary you were given, verbatim, and nothing else.
```
Your color is in it. The thirty codes are a sentence, if they're there at all.

### 5. Ask for both
```
From what is already in context, no tools: what is my favorite color, and what was code 17?
```
Red comes back. Code 17 comes back wrong, or as a guess, or as "I no longer
have it". Check it against the list from step 2.

### What to look for
- What you said survives. One short fact about you is exactly what a summary keeps.
- What the agent generated does not. Thirty codes become "generated 30 codes".
- A confident wrong code is the common case, and the one that causes problems.

### 6. The fix: tell the summarizer what matters
`/compact` takes instructions. First make the codes again, since the summary is
the only copy now:
```
Generate 30 new random 6-digit codes, numbered 1 to 30, one per line, in your reply. No files.
```
Now compact and say what to keep:
```
/compact keep all 30 codes verbatim, with their numbers
```
Then ask again:
```
From what is already in context, no tools: what was code 17?
```
It matches the list. Press `ctrl+o` on the new `Compacted` line and the codes
are there, because you asked for them.

Those instructions went to this one summary only. The same line in `CLAUDE.md`
reaches every compaction. Neither is a guarantee. The guarantee is exercise 03.

### 7. The line
```
/context
```
Look at the autocompact buffer. Both times you typed `/compact` yourself. In a
real session it fires when `Messages` reaches that line: mid-task, without
asking.

### 8. The other way down
`/compact` keeps a summary. `/clear` keeps nothing. The conversation empties,
`Messages` goes to zero, and only the rules come back: `CLAUDE.md`, memory,
settings. Use it when the task changed. Everything above is then baggage, and
an empty conversation beats a summary of the wrong one.

Don't run it now. Exercise 03 continues from this session and needs the codes.

> **Codex:** `/status` for the meter. The summary is never shown and `/compact`
> takes no argument, so step 6 is Claude only. `/new` is `/clear`. Ask for the
> color and the code before and after; the comparison is the only evidence you
> get.
