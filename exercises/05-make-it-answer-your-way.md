# 05 · Make it answer your way

**Concept:** a remembered rule shapes every reply, in every session. It lives
in the same memory folder as exercise 04, and it costs a little on every turn.

Continue from exercise 04, or start `claude`.

### 1. Ask something plain
```
What's a good way to spend a rainy Sunday?
```
Note the shape of the answer: how long it is, whether it uses headers, how it
ends.

### 2. Set your format
Use this one or make your own. Ideas: no emoji ever, answer in Spanish, one
sentence max, always end with a bad pun, always start with a tl;dr. In a
group, each member proposes one and the group picks.
```
From now on, when you answer me: give the one-line answer first, then at most three bullets, and end with one question back to me. Remember this for every session.
```
It writes a file and confirms.

### 3. New session, same question
Quit (`/exit`), start `claude`, and paste step 1 again word for word.
```
What's a good way to spend a rainy Sunday?
```
The answer comes back in your format. If you did exercise 04, it also uses
what it knows about you. Nobody told it to combine them; both were in the
fixed part at start.

### 4. Change it in the file
Open the memory folder from exercise 04 step 2, the one under
`~/.claude/projects/`. There's a new note, and it has a "Why" and a "How to
apply" line the agent wrote on its own. Edit it in your
editor: change three bullets to one, or swap the question at the end for a
joke. Quit, start `claude`, ask the question again. It follows your edit.

You didn't need to ask the agent to change anything. It's a file.

### 5. What it costs
```
/context
```
Look at `Memory files`. Every rule you keep is sent on every message. Short
rules are cheap; a page of them is a tax on everything you do.

### Talk about it
Read the `Memory files` number off `/context`. Does the rule you set earn that
on every turn? What is one rule you'd actually keep for a month?

> **Codex:** put the rule in `AGENTS.md` under `## Answer style`, restart,
> and ask the same question twice.
