# 04 · Make it survive

**Concept:** anything that has to survive exactly goes in a file.

A file isn't in the request until something reads it, so it can't be
summarized away. This works in every tool, including the ones that never show
you a summary.

Continue from 03, or redo its setup block in a fresh session.

### 1. Write it down
```
From what is in context, write every burnt bake to NOTES.md: bake number, package, oven, runtime, error. One per line.
```
Open the file. It's plain text you can read, edit, and commit. If a line is
wrong, fix it.

### 2. Compact
```
/compact
```
No instructions this time, and no CLAUDE.md rule needed. The summary can
keep whatever it wants. The data is in the file.

### 3. Read it back
```
Check NOTES.md, then answer:
1. Which burnt bake had the shortest runtime, and how many seconds was it?
2. What error did bake-0035 hit?
3. Who is on call, and what is the ticket number?
```
Questions 1 and 2 come back exact, every time. Compare with exercise 02.

Question 3 is whatever the summary happened to keep, because nobody wrote it
down. Add it to NOTES.md and it survives too. The file only holds what you put
in it.

### Where to put what
| Lifetime | Put it in | Cost |
|---|---|---|
| Every session in this repo | `CLAUDE.md` / `AGENTS.md` | re-sent every turn, keep it short |
| This task | a file you tell the agent to maintain (`NOTES.md`, `PLAN.md`) | only when read |
| Facts about you | memory files | injected at start, same mechanism, not a database |

Memory never saw what compaction dropped, and nothing brings it back. Write it
down before the line, not after.
