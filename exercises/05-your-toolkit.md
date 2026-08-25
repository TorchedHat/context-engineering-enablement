# 05 · Your toolkit

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
The original is six lines. What did `/init` add that the agent could not have
found by reading the repo? That is the only part worth keeping.

### 4. Put it back
```
git checkout -- CLAUDE.md
```

### The rest of the toolkit
- `.claude/settings.json` sets the model and the status line for this repo.
  Open it. That is where Haiku is pinned.
- `/autocompact 100k` moves the line from exercise 02. Try it, then `/context`.
- `/memory` shows what the agent has written about you. It is a file. Open it.
- `/skills` lists packaged instructions. Unlike CLAUDE.md, a skill is only
  loaded when it is invoked. Check the Skills line in `/context` before and
  after using one.

> **Codex:** `/init` writes `AGENTS.md`. Auto-compact is
> `model_auto_compact_token_limit` in `config.toml`.
