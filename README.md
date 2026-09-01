# Context Engineering Enablement

> Every model has a context window, but capacity isn't quality.

Hands-on lab. The repo is a toy AIPCC-style service, **The Wheel Bakery**,
which bakes Python wheels for AI packages on accelerator "ovens", plus enough
build logs and catalog data to feed an agent. You'll watch its context
fill, watch it break, and learn the levers that control it.

Written for **Claude Code**. Codex CLI notes are inline where commands differ.

## Before the session

```bash
git clone https://github.com/TorchedHat/context-engineering-enablement.git
cd context-engineering-enablement
claude
```
Type `hello` and get a reply. That's it. Nothing to install.

## How it works

```
  Every time you hit Enter, the agent gets one package with everything it knows.
  It remembers nothing between packages.

  ┌─────────────────────────────────────────────────────────┐
  │  THE PACKAGE                                            │
  │                                                         │
  │  ┌───────────────────────────────┐                      │
  │  │  RULES                        │  CLAUDE.md, memory,  │
  │  │  loaded once when you start   │  tools, MCP servers  │   all of this
  │  ├───────────────────────────────┤                      │   is sent
  │  │  THE CONVERSATION             │  what you said       │   every single
  │  │                               │  what it said        │   time
  │  │  your messages                │  every file it read  │
  │  │  its replies                  │  every command's     │
  │  │  files it read                │  output              │
  │  │  command output               │                      │
  │  │  keeps growing                │                      │
  │  └───────────────────────────────┘                      │
  └────────────────────────────┬────────────────────────────┘
                               │
                               ▼
                            MODEL  ──►  reply  ──►  added to the conversation
```

**The conversation only grows.** Files, output, and chat all go in. Nothing comes out on its own.

## Your levers

| Command | What it does | Use it when |
|---|---|---|
| `/context` | shows what's in the package and how big each part is | anything feels slow, expensive, or forgetful. Look first. |
| `!grep ERROR build.log` | runs a command and puts only its output in the package | before a big log or output goes in. Shape it first. |
| `/compact` | replaces the conversation with a summary. Details get lost. | mid task, running out of room, still need the history |
| `/compact keep the bake numbers and runtimes` | same, but you say what to keep. Works once. | you know exactly what must survive |
| `/autocompact 100k` | sets the line where compaction fires on its own | you want it sooner, or later |
| a line in `CLAUDE.md` that says *when compacting, keep …* | every compaction keeps it, including the automatic ones | the same things always matter in this repo |
| *write that to NOTES.md* | puts it in a file. Files never get summarized. | anything you can't afford to lose. Ports, IDs, decisions, checklists. |
| `/clear` | empties the conversation. Rules stay. | the task changed. A fresh package beats a summarized one. |
| `/memory` | shows the notes the agent wrote about you. Loaded at start, it's a file. | it "remembers" something and you want to know where from |
| *use a subagent to read …* | reads in its own package. You only get the answer. | big reading jobs. Logs, investigations, lots of files. |

**Compaction fires at the line whether you're ready or not. You don't pick when. You pick what's in it.**

**If losing it means redoing work, put it in a file.**

**Everything in RULES is sent every message. Keep it short.**

**Anything under 30 KB of output goes in whole. Shape it before it goes in.**

> Codex users: `/status` instead of `/context`. `AGENTS.md` instead of `CLAUDE.md`. `/compact` takes no instructions and the summary is never shown. The file rule works everywhere.

## Exercises

Do them in order. Every step is something to paste, with the expected result
under it. Each exercise says whether to continue the session or start a new one.

| Exercise | Concept |
|---|---|
| [00 · The mental model](exercises/00-mental-model.md) | one request per Enter, and three claims to prove |
| [01 · Feel the meter](exercises/01-feel-the-meter.md) | everything costs its size, nothing comes out, shape what goes in |
| [02 · Watch it break](exercises/02-watch-it-break.md) | same three questions before and after `/compact` |
| [03 · Steer it](exercises/03-steer-it.md) | `/compact` instructions: this call vs. every call |
| [04 · Make it survive](exercises/04-make-it-survive.md) | what must survive exactly goes in a file |
| [05 · Your toolkit](exercises/05-your-toolkit.md) | `/init`, settings, `/autocompact`, memory |

## Extra credit

| Exercise | Concept |
|---|---|
| [06 · Delegate](exercises/06-delegate.md) | subagents filter context |
| [07 · Your repo](exercises/07-your-repo.md) | one thing to prune tomorrow |
| [transcripts/](transcripts/) | three broken sessions. Name the lever. |

## Lost? Reset.

Quit the agent, then in a terminal:
```
git checkout -- CLAUDE.md AGENTS.md && rm -f NOTES.md && claude
```
Rejoin at the current step.

## Layout

```
bakery/        the toy app
tests/         test suite
data/          pre-generated build logs and wheel catalog
exercises/     the lab, one file per exercise
transcripts/   broken sessions for the diagnosis round
tools/         gen_data.py, how data/ was generated
CLAUDE.md      standing rules. Exercise 03 adds to it
AGENTS.md      same, for Codex
```
