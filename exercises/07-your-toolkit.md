# 07 · Your toolkit

**Concept:** everything in the rules block is paid on every turn.

### 1. Measure the rules
```
/context
```
Note the CLAUDE.md and memory lines.

### 2. Generate a CLAUDE.md
```
/init
```
Claude Code reads the repo and writes a CLAUDE.md. Say yes when it asks to
overwrite. Read what it wrote.

### 3. Measure again
```
/context
```
Compare to step 1. Then compare the generated file to the original:
```
git diff CLAUDE.md
```
The original is six lines, four of them non-blank. What did `/init` add that
the agent could not have found by reading the repo? That is the only part worth
keeping.

### 4. Put it back
```
git checkout -- CLAUDE.md
```

### 5. Try the rest
Four more commands, a minute each:
- Open `.claude/settings.json`. This is where Haiku is pinned for these exercises.
- `/autocompact 100k`, then `/context`. The line from exercise 02 moved. The
  command takes `auto` or a token count; `100k` and `100000` both work.
- `/memory` shows what the agent has written about you. Exercise 04 is the long version.
- `/skills` lists packaged instructions. Unlike CLAUDE.md, a skill is only
  loaded when it is invoked. Check the Skills line in `/context` before and
  after using one.

> **Codex:** `/init` writes `AGENTS.md`. Auto-compact is
> `model_auto_compact_token_limit` in `config.toml`.
