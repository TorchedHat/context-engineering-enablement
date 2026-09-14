# Context Engineering Enablement

> Every model has a context window, but capacity isn't quality.

Hands-on exercises for working with a coding agent without letting its context
get away from you. The repo is a small toy Python project, a wheel bakery,
with a noisy test suite and forty build logs: enough to feel the meter. You'll
watch the agent's context fill, watch it break, and learn the levers that
control it.

> Written for Claude Code. Codex CLI notes are inline where commands differ.

## Setup

```bash
git clone https://github.com/TorchedHat/context-engineering-enablement.git
cd context-engineering-enablement
claude
```
Type `hello` and get a reply. That's it. Nothing to install.

## Exercises

Seven exercises in managing context and memory inside a coding session, and
three standalone follow-ons. Start at [exercises/](exercises/README.md).

## Repository layout

```
.
├── README.md                 this file
├── CLAUDE.md                 standing rules for Claude Code, loaded at session start
├── AGENTS.md                 the same rules, for Codex
├── pyproject.toml            project metadata
├── .claude/
│   ├── settings.json         model pin and status line for these exercises
│   └── statusline.sh         status bar: model, context used, session cost
├── bakery/                   the toy app
│   ├── config.py             oven and wheel configuration
│   └── oven.py               the bake loop
├── tests/
│   └── test_oven.py          test suite; prints enough output to matter
├── data/
│   ├── catalog.json          wheel catalog
│   └── logs/                 40 pre-generated build logs, bake-0000 to bake-0039
├── tools/
│   └── gen_data.py           regenerates data/
└── exercises/                one file per exercise, plus an index
```
