# 00 · The mental model

Read this once. Every exercise points back to it.

**The agent has no memory. Every turn, the harness builds a request from
scratch and sends the whole thing to the model.**

```
request (rebuilt every turn) =
    system prompt              harness, fixed
  + tool definitions           config: MCP servers, plugins
  + CLAUDE.md + memory files   config: loaded from disk at session start
  + conversation history       grows: every message, file read, command output
                                 → model → reply is appended to history
```

Everything in this lab is an operation on that structure:

| You do | What happens to the request |
|---|---|
| read a file, run a command | output is appended to **history** |
| `/context` | prints the size of each block |
| `/compact` | `history = [ summarize(history) ]` — a model call, and lossy |
| `/compact <text>` | `summarize(history, instructions=text)` — **this call only** |
| `/autocompact 100k` | sets the size of history at which `summarize()` runs on its own |
| a rule in `CLAUDE.md` | sits in the **config** block, so it is in every request, including the one that runs `summarize()` — **every compaction, automatic ones too** |
| write a file | nothing, until something reads it |
| use a subagent | a separate request with its own history; only its final reply is appended to yours |

Six things that follow from this. Watch for each one during the lab:

1. **Config is paid every turn.** A 400-line CLAUDE.md costs 400 lines on every message.
2. **Compaction fires on its own.** When history reaches the line, `summarize()` runs mid-task. It does not ask.
3. **"Forget that" does nothing.** History is append-only until compaction.
4. **The compaction summary is just a message.** After `/compact`, it is the first thing in history. You can read it.
5. **Files are not in the request until read.** That is why they are never summarized, and why an agent will re-read disk after compaction loses something.
6. **A subagent's reading never enters your history.** Only its answer does.

| | Claude Code | Codex |
|---|---|---|
| See usage | `/context` (per block) | `/status` (total only) |
| Compaction line | `/autocompact 100k` | `model_auto_compact_token_limit` |
| Compact | `/compact [instructions]` | `/compact` (no argument), summary hidden |
| Standing rules | `CLAUDE.md` | `AGENTS.md` |
