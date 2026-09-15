# 02 · Watch it break

**Concept:** compaction replaces the conversation with a summary. The summary
decides what survives, and it has no idea what you'll ask next.

This works in a fresh session (`claude`) or as a continuation of exercise 01.
Fresh, the numbers are small and the lesson is the same. Continued, the meter
is over 100k and the drop is visible from the back of the room. Either way,
have the side screen running: `python3 tools/watch_context.py` in a second
terminal (see exercise 01).

### 1. Say one thing
```
My favorite color is red. No action needed.
```

### 2. Make it produce a lot
```
Generate 30 random 6-digit codes, numbered 1 to 30, one per line, in your reply. No files.
```
Thirty lines nobody could have guessed. Keep them on screen. Thirty lines cost
about 300 tokens, nothing compared to what's already there; the point is
they're unguessable.

### 3. Show the line, then cross it
First find out where you are.
```
/context
```
Note the total at the top: around `25k / 200k` fresh, `128k / 200k` or so
after exercise 01. Now move the autocompact line to sit about 10k above it:
```
/autocompact 35k
```
Use `140k` after exercise 01, or whatever is 10k above your total. `100k`,
`140000`, `auto` and `off` are all accepted. Run `/context` again and the line
has moved.
In a real session the next big read would cross it and compaction would fire
mid-task without asking. Cross it now.
```
/compact
```
```
/context
```
Watch what happens. `Messages` drops to a few k: from ~25k fresh, from
~100k+ after exercise 01. On the side screen a `COMPACTED: X -> Y tokens`
banner and then the full summary text, printed verbatim. Read the summary on
the side screen out loud: the color is there; the thirty codes are a sentence,
if that. After exercise 01, the ticket number is there too and the forty logs
are a sentence.

### 4. Read what survived
Press `ctrl+o` on the `Compacted` line to expand the summary. If it doesn't
open, ask:
```
Print the compaction summary you were given, verbatim, and nothing else.
```
Your color is in it. The thirty codes are a sentence, if they're there at all.
The side screen already shows the same text from the transcript file, so nothing
here is hidden.

### 5. Ask for what survived
```
From what is already in context, no tools: what is my favorite color, and what was code 17?
```
Red comes back. Code 17 comes back wrong, or as a guess, or as "I no longer
have it". Check it against the list from step 2. After exercise 01, add "what
was the ticket number" to the question: AIPCC-7731 comes back too.

### What to look for
- What you said survives. One short fact about you is exactly what a summary keeps.
- What the agent generated does not. Thirty codes become "generated 30 codes".
- A confident wrong code is the common case, and the one that causes problems.
- What it read does not survive either. After exercise 01, forty logs and 2,000 lines of catalog became one sentence, and it can no longer answer "why did bake-0017 burn" without reading the file again.

### 6. The fix: tell the summarizer what matters
`/compact` takes instructions. First make the codes again, since the summary is
the only copy now:
```
Generate 30 new random 6-digit codes, numbered 1 to 30, one per line, in your reply. No files.
```
Now compact and say what to keep. Be precise: the summarizer reads the whole
conversation, including the request to generate codes, and a vague instruction
lets it invent a fresh list or copy the older one:
```
/compact Copy the 30 numbered codes from the most recent assistant reply into the summary exactly as written, character for character. There are two lists of codes in this conversation; keep only the newest. Do not generate, renumber, or paraphrase codes.
```
Then ask again:
```
From what is already in context, no tools: what was code 17?
```
Check it against the list still on screen. It matches. Press `ctrl+o` on the
new `Compacted` line and the codes are there, because you asked for them. The
side screen shows the same summary, so if the summarizer slipped anyway, it is
visible: a list that does not match the one on screen, or the older set under a
heading like "previous codes".

Those instructions went to this one summary only. The same line in `CLAUDE.md`
reaches every compaction. Neither is a guarantee: in rehearsal on Haiku, `keep
all 30 codes verbatim` produced a summary with a newly invented list on top and
the *first* set copied underneath, and code 17 came back from the wrong set.
The guarantee is exercise 03.

### 7. The line
Put the line back to the default.
```
/autocompact auto
```
```
/context
```
The line is back where it started. You moved it down in step 3 so the audience
could see the meter sitting next to it; the setting lasts only for this session.
Both times you typed `/compact` yourself. In a real session it fires when `Messages`
reaches that line: mid-task, without asking.

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
