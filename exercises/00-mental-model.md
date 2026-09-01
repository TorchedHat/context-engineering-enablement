# 00 · The mental model

**Concept:** the agent has no memory. Every time you hit Enter, Claude Code
builds one request from scratch and sends the whole thing to the model.

## The request

```
request =  FIXED PART                     +  THE CONVERSATION
           system prompt                     your messages
           tool definitions                  its replies
           CLAUDE.md, memory, skills         every file it read
           loaded once, when you start       every command's output
           same size every message           grows every message
```

There's no database behind the agent. When it "remembers" the port number
you looked at ten minutes ago, it's because the message where it read that
port is still in the request. When it forgets, that message is gone.

## Three claims

The next two exercises show each of these on screen.

1. **The conversation only grows.** Chat, files, and command output all go in,
   and nothing you say takes anything back out. "Forget that" just adds one
   more message. *(01)*
2. **Everything costs its size.** A 100-line log costs 100 lines, even when the
   answer was on line 98. What you let in is your first lever. *(01)*
3. **When it's full, the conversation gets rewritten.** The model writes a
   summary of everything so far, and the summary takes its place. You don't get
   to choose what the summary keeps, and it fires on its own, mid-task. *(02)*

The rest of the lab is about the levers: what you let in (01), what you tell
the summarizer (03), and what you keep out of the conversation entirely by
putting it in a file (04).

## How to read `/context`

```
  claude-haiku-4-5 · 31k/200k tokens (16%)    ← how full the request is

  System prompt   3.1k   ┐
  System tools   12.4k   │  FIXED PART. Paid on every message.
  MCP tools       5.8k   │  Only changes when you change config
  Memory files    0.6k   │  (CLAUDE.md is in here).
  Skills          1.2k   ┘

  Messages        0.3k   ← THE CONVERSATION. The only line that moves
                            while you work. This is the meter.

  Autocompact buffer 33k ← the line. When the request reaches it,
                            exercise 02 happens on its own.
```

Your numbers will be different. The shape won't be. The status bar at the
bottom of the screen shows the same total as a percentage, so you can watch it
climb without running `/context` every time.

> **Codex:** same model, different names. `/status` instead of `/context`,
> `AGENTS.md` instead of `CLAUDE.md`. Compaction runs server-side and you never
> see the summary, which is exactly why exercise 04 matters there.
