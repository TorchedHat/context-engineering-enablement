# 06 · The handoff

**Concept:** a session ends, and everything in the conversation goes with it.
Whatever you'd hate to redo goes in a file first. Exercise 03 did this with
the codes. This time it's your own plan.

Start a fresh session: `claude`.

### 1. Plan something
Use this or your own: a trip, a game night, a garden, a hackathon entry.
```
Help me plan a birthday thing for a coworker who hates surprises. Keep replies short. Ask me one question at a time.
```
It asks one question. Answer with real-sounding details, three or four turns.
Something like:
```
Thursday lunch, 8 people, budget is 120 dollars, she's vegetarian, and she already knows about it.
```
```
The taco place on 5th. No cake, she hates cake, do the cookies from Marco's instead. I'll send the invite, you own the card idea.
```
Stop when it asks you something you haven't decided yet.

### 2. Write the handoff
```
Write everything the next person would need to pick this up to HANDOFF.md: every decision so far, what's still open, and what to do next.
```
Open `HANDOFF.md`. Expect three parts: what's decided, what's still open, what
happens next. If it got a detail wrong, fix it in the file. That's allowed, and
it's the point.

### 3. Lose the session
Quit (`/exit`) and start `claude` again. Don't mention the file yet:
```
Continue where we left off with the birthday plan.
```
It has no idea. It might guess, or it might say it has no context and this is
a fresh session. Either way, the conversation is gone.

### 4. Hand it over
Same session:
```
Read HANDOFF.md and continue where we left off.
```
It reads the file and picks up at the open question. Answer it and finish the
plan. Then have it update the file:
```
Update HANDOFF.md with what we just decided.
```

### Why this matters
Compaction in exercise 02 did to the thirty codes what quitting just did to
your plan, except it happens mid-task and doesn't ask. A file you keep current
is the only thing that survives both. Same trick as `NOTES.md` in exercise 03,
same trick as memory in exercise 04, and it works in every tool.

> **Codex:** identical. Quit, start `codex` again, and the file is still there.
