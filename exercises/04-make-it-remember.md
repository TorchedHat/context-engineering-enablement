# 04 · Make it remember

**Concept:** "memory" is a file. The agent writes it when you ask it to
remember something, and reads it once when a session starts. Nothing in it is
magic, and everything in it is yours to open and edit.

Start a fresh session in this repo: `claude`.

If you have run this exercise before, delete the memory folder first (step 2
shows where it is). Otherwise step 1 finds what you saved last time and the
rest plays out differently.

### 1. Tell it three things about yourself
Fill in your own. Keep them harmless and easy to check. In a group, one fact
per person.
```
Three things to remember about me for every future session: I go by Ade, my go-to snack is pretzels, and I'd rather be surfing. Save them to memory now.
```
It writes a file, then says something like "Done, they'll stick around for
future sessions."

### 2. Find the file
Ask now, in this same session. A new session won't know what it just wrote.
```
Which file did you write that to? Print the full path, nothing else.
```
Open that file in your editor. Then open `MEMORY.md` in the same folder. Two
things got written:

- a note with your three facts under a short header
- one line in `MEMORY.md` that points at the note and repeats the facts

Both are plain text. That folder is where every remembered thing lives for this
repo. It looks like:
```
~/.claude/projects/<repo-path-with-dashes>/memory/MEMORY.md
```
The long folder name is the repo's full path with every slash turned into a
dash, so a repo at `/home/sam/context-engineering-enablement` gets
`-home-sam-context-engineering-enablement`. Memory is keyed by that path, so a
second clone of the same repo in a different folder starts with no memory. If
`CLAUDE_CONFIG_DIR` is set, the folder is under that directory instead of
`~/.claude`. Nothing in it lives in the repo, so none of it is committed or
shared; that is the difference from `CLAUDE.md` in exercise 03.

You don't have to create any of this. The agent makes the folder and both
files the first time you ask it to remember something. You can also make them
by hand, and they load the same way.

### 3. New session, ask them back
Quit (`/exit`), then start `claude` again.
```
What do you know about me?
```
It reads the note and recites all three. Run `/context`: the memory is part of
the fixed part, in `Memory files`. It was loaded before you typed anything.

### 4. Forget one
```
Forget the snack.
```
It edits the note and says done. Open both files again. The snack is gone from
the note. Check the line in `MEMORY.md`.

### 5. Did it work?
Quit, start `claude` again, and ask the one thing it just forgot:
```
What's my go-to snack?
```
Usually it still knows. The line in `MEMORY.md` never got updated, and that line
was loaded at start. The agent "forgot" in one file and remembered in the other.

Sometimes it doesn't know, because this time the agent edited both files. Open
them anyway. The lesson is the same either way: two files had to agree, and
nothing checked that they did.

### 6. Fix it yourself
Delete the snack from the `MEMORY.md` line in your editor, or delete the whole
memory folder. Quit, start `claude`, ask again. Now it doesn't know.

That's the takeaway. Asking the agent to remember or forget is a request; the
files are the truth, and you can always open them.

### Talk about it
Memory is per person and per clone; nobody else's agent sees it. What is one
thing you'd want a teammate's agent to know about your work, and where would
you put it so it did?

> **Codex:** there is no automatic memory. Put the three facts in `AGENTS.md`
> under a `## About me` heading by hand, restart, and ask the same questions.
> To forget, delete the line. Same lesson, fewer surprises.
