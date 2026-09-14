# 00 · The mental model

**Concept:** the agent has no memory. Every time you hit Enter, Claude Code
builds one request from scratch and sends the whole thing to the model.

## The request

```
  ┌─────────────────────────────────────────────────────────┐
  │  THE REQUEST                                            │
  │                                                         │
  │  ┌───────────────────────────────┐                      │
  │  │  FIXED PART                   │  system prompt       │
  │  │  loaded once, when you start  │  tool definitions    │   all of this
  │  │  same size every message      │  CLAUDE.md, memory,  │   is sent
  │  │                               │  skills              │   every single
  │  ├───────────────────────────────┤                      │   time
  │  │  THE CONVERSATION             │  your messages       │
  │  │  grows every message          │  its replies         │
  │  │                               │  every file it read  │
  │  │                               │  every command's     │
  │  │                               │  output              │
  │  └───────────────────────────────┘                      │
  └────────────────────────────┬────────────────────────────┘
                               │
                               ▼
                            MODEL  ──►  reply  ──►  added to the conversation
```

## Key takeaways

1. **The conversation only grows.** Chat, files, and command output all go in,
   and nothing you say takes anything back out. "Forget that" just adds one
   more message.
2. **Everything costs its size.** A 100-line log costs 100 lines, even when the
   answer was on line 98. What you let in is your first lever.
3. **When it's full, the conversation gets rewritten.** The model writes a
   summary of everything so far, and the summary takes its place. You don't get
   to choose what the summary keeps, and it fires on its own, mid-task.

The levers, in order: what you let in, what you tell the summarizer, and what
you keep in a file instead. The last one is called **offloading**, and it works
in every tool.

## Four ways it goes wrong

Four names for what you'll see. Useful at work, when you want to say what
went wrong.

| Name | What it is | Where you'll see it |
|---|---|---|
| **Distraction** | too much history and output. The model rereads all of it every turn, and the one line that mattered is harder to find. | Exercise 01. Seven hundred lines of test output for one line that mattered. |
| **Poisoning** | a wrong fact gets in and stays. Everything after it builds on it. | Exercise 02. After compaction, a confident wrong code. Nothing flags it. |
| **Confusion** | tools and instructions that aren't for this task, crowding the request. Every tool's description is a small prompt, paid every turn. | The System tools and MCP tools lines in `/context`. |
| **Clash** | two things in the request disagree, and the model picks one. | Exercises 02 and 03. The summary remembers one code 17 and `NOTES.md` holds another. Reading the file settles it. |

A bigger window doesn't fix any of these. The levers are about what goes in,
not how much fits.

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
