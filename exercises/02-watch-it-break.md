# 02 · Watch it break

**Concept:** compaction keeps the story and drops the specifics.

Carry on from exercise 01. The agent has read a build log, the catalog, and
the test output. It knows things right now that it will not know in five
minutes.

### 1. Ask while it's fresh
```
Which bake numbers burnt with a Gaudi error, and how many seconds did
bake-0017 run before it burnt?
```
It answers from what it already read. Note the numbers.

### 2. Look at the line
```
/context
```
Find the autocompact buffer. When the conversation reaches it, Claude Code
summarizes the conversation and keeps going. It does not ask. You are about
to do the same thing by hand, at a moment of your choosing.

### 3. Compact
```
/compact
```
Run `/context` again. How much smaller is the conversation?

### 4. Look at what is left
```
Show me the first message currently in your context, verbatim.
```
This is the summary. Read it. Find the part about the build logs.

### 5. Ask it back
```
From context only, no re-reading: which bake numbers burnt with a Gaudi
error, and how many seconds did bake-0017 run before it burnt?
```

### What to look for
- **It gets the story, loses the number.** "0017 and 0035 hit the Gaudi error"
  survives because that was a conclusion. The runtime was one line of tool
  output, and tool output is what summaries drop first.
- **It offers to re-read the file.** Fine, and it costs those tokens again.
  Watch the `Read` lines after compaction: Claude Code re-reads a few
  recent files on its own.
- **It gets everything right.** Good model, lucky day. Scroll up to the
  summary and see how thin the line was. You cannot build on it.

Compaction fires at the line whether you are ready or not. You do not pick
when. Exercise 03 is how you pick what.

> **Codex:** same flow, but skip step 4. With OpenAI models the summary is
> encrypted and never shown. Step 5 is the only way to find out what survived.
