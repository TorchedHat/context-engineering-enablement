# 03 · Make it survive

**Concept:** anything that has to survive exactly goes in a file. This is
offloading: keep it outside the request, read it back when you need it.

A file isn't in the request until something reads it, so it can't be
summarized away. Works in every tool, including the ones that never show you
a summary.

Continue from exercise 02 in the same session.

### 1. Write it down
```
Write all 30 codes from context to NOTES.md, numbered, one per line.
```
Open the file. It's plain text you can read, edit, and commit. If a line is
wrong, fix it.

### 2. Compact
```
/compact
```
No instructions this time, and no CLAUDE.md rule needed. The summary can
keep whatever it wants. The codes are in the file.

### 3. Read it back
```
Check NOTES.md, then answer: what was code 17, and what is my favorite color?
```
Code 17 comes back exact, every time. Compare with exercise 02.

The color is whatever the summary happened to keep, because nobody wrote it
down. Add it to NOTES.md and it survives too. The file only holds what you put
in it.

### Where to put what
| Lifetime | Put it in | Cost |
|---|---|---|
| Every session in this repo | `CLAUDE.md` / `AGENTS.md` | re-sent every turn, keep it short |
| This task | a file you tell the agent to maintain (`NOTES.md`, `PLAN.md`) | only when read |
| Facts about you | memory files (exercise 04) | loaded at start, same mechanism |

None of these see what compaction dropped. Write it down before the line, not
after.
