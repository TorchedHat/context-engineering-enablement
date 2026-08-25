# 04 · Make it survive

**Concept:** anything that must survive exactly goes in a file.

Files are not in the request until read, so they cannot be summarized away.
This works in every tool.

### 1. Write it down
```
Write every burnt bake to NOTES.md: bake number, oven, runtime, error. One per line.
```
Open the file. It is text you can read, edit, and commit.

### 2. Compact
```
/compact
```

### 3. Read it back
```
How many seconds did bake-0017 run before it burnt? Check NOTES.md.
```
Compare to exercise 02.

### Where to put what
| Lifetime | Put it in | Cost |
|---|---|---|
| Every session in this repo | `CLAUDE.md` / `AGENTS.md` | re-sent every turn, keep it short |
| This task | a file you tell the agent to maintain (`NOTES.md`, `PLAN.md`) | only when read |
| Facts about you | memory files | injected at start, same mechanism, not a database |

Memory did not see what compaction dropped. Nothing restores that. Write it
down before the line, not after.
