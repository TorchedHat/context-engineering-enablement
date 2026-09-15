#!/usr/bin/env python3
"""Side-screen for the context exercises.

Follows the live Claude Code transcript for this repo and prints one line per
thing that entered the conversation, a running context meter, and the full
compaction summary the moment one is written.

    python3 tools/watch_context.py            # newest session, replay then follow
    python3 tools/watch_context.py --follow   # skip the replay, live only
    python3 tools/watch_context.py --list     # show candidate transcripts and exit
    python3 tools/watch_context.py --file PATH
    python3 tools/watch_context.py --config-dir vertex     # only ~/.claude-vertex

Transcripts live at <config dir>/projects/<cwd with / -> ->/<session>.jsonl.
The config dir is $CLAUDE_CONFIG_DIR if set; this script also scans every
~/.claude* directory and follows whichever transcript for this repo was
written most recently. While running it switches only to sessions started
after it, so another Claude writing in a different config dir can't steal it.
Nothing here is Claude-specific magic: the file is plain JSON lines, one
record per event.

Line legend (left column):
    YOU        something you typed                        (costs its size)
    @FILE      a file you pasted with @                   (costs its size)
    CLAUDE     a reply                                    (costs its size)
    CLAUDE ->  a tool call                                (small)
    TOOL OUT   what the tool returned                     (costs its size)
    /context   the exact numbers from your /context run
    CONTEXT    estimate from the API usage of the last reply
"""
import argparse
import glob
import json
import os
import re
import sys
import time

BAR_WIDTH = 40
STALE_SECONDS = 600

# ---------------------------------------------------------------- colours ---
C = {"you": "\033[36m", "cost": "\033[35m", "claude": "\033[0m", "tool": "\033[2m",
     "meter": "\033[1m", "official": "\033[1;34m", "warn": "\033[1;33m",
     "boundary": "\033[1;30;43m", "summary": "\033[32m", "reset": "\033[0m", "dim": "\033[2m"}


def paint(kind, text):
    if not USE_COLOR:
        return text
    return f"{C[kind]}{text}{C['reset']}"


USE_COLOR = sys.stdout.isatty()

# --------------------------------------------------------------- discovery ---


def slug():
    return os.getcwd().replace("/", "-")


def config_dirs(explicit=None):
    dirs = []
    if explicit:
        explicit = os.path.expanduser(explicit)
        if not os.path.isdir(explicit):                       # "vertex" -> ~/.claude-vertex
            explicit = os.path.expanduser(f"~/.claude-{explicit.lstrip('.').removeprefix('claude-')}")
        return [explicit] if os.path.isdir(explicit) else []
    env = os.environ.get("CLAUDE_CONFIG_DIR")
    if env:
        dirs.append(os.path.expanduser(env))
    dirs += sorted(glob.glob(os.path.expanduser("~/.claude*")))
    seen, out = set(), []
    for d in dirs:
        d = os.path.realpath(d)
        if os.path.isdir(d) and d not in seen:
            seen.add(d)
            out.append(d)
    return out


def candidate_transcripts(explicit=None):
    files = []
    for d in config_dirs(explicit):
        files += glob.glob(os.path.join(d, "projects", slug(), "*.jsonl"))
    return sorted(files, key=os.path.getmtime, reverse=True)


def age(path):
    s = int(time.time() - os.path.getmtime(path))
    return f"{s}s" if s < 120 else f"{s // 60}m"


def describe(path):
    cfg = path.split("/projects/")[0]
    return f"{os.path.basename(path)[:8]}…  in {cfg}  (last write {age(path)} ago)"


# ---------------------------------------------------------------- helpers ---


def approx_tokens(text):
    return max(1, len(text) // 4)


def short(text, n=90):
    text = " ".join(str(text).split())
    return text if len(text) <= n else text[: n - 1] + "…"


def fmt(n):
    return f"{n:,}"


def bar(frac):
    frac = max(0.0, min(frac, 1.0))
    filled = int(frac * BAR_WIDTH)
    return "█" * filled + "·" * (BAR_WIDTH - filled)


def block_text(block):
    if isinstance(block, str):
        return block
    if block.get("type") == "text":
        return block.get("text", "")
    if block.get("type") == "tool_result":
        c = block.get("content", "")
        if isinstance(c, list):
            return "".join(b.get("text", "") for b in c if isinstance(b, dict))
        return str(c)
    return ""


def item(state, kind, tokens, text, colour):
    """One line for one thing that entered the conversation."""
    state["n"] += 1
    state["kinds"][kind] = state["kinds"].get(kind, 0) + 1
    state["est"] += tokens
    line = f"{state['n']:>4}  {kind:<10} +~{fmt(tokens):>6}  {short(text)}"
    print(paint(colour, line))


def k(n):
    return f"{n/1000:.1f}k" if n >= 1000 else str(n)


# ---------------------------------------------------------------- records ---


def handle(rec, state):
    t = rec.get("type")
    sub = rec.get("subtype")
    msg = rec.get("message") or {}
    content = msg.get("content", "")

    if sub == "compact_boundary":
        m = rec.get("compactMetadata", {})
        pre, post = m.get("preTokens", 0), m.get("postTokens", 0)
        kinds = ", ".join(f"{v} {kk}" for kk, v in state["kinds"].items())
        print()
        print(paint("boundary", " " * 78))
        print(paint("boundary", f"  COMPACTED ({m.get('trigger', '?')})   "
                    f"{fmt(pre)} tokens  ->  {fmt(post)} tokens   "
                    f"(dropped {fmt(pre - post)}, {100 * (pre - post) / max(pre, 1):.0f}%)".ljust(78)))
        print(paint("boundary", f"  ▲ the {state['n']} items above ({kinds}) left the request".ljust(78)))
        print(paint("boundary", "  ▼ what replaced them".ljust(78)))
        print(paint("boundary", " " * 78))
        state.update(n=0, kinds={}, est=0, last_total=post)
        return

    if rec.get("isCompactSummary"):
        text = content if isinstance(content, str) else "".join(block_text(b) for b in content)
        print(paint("summary", f"  ┌─ THE SUMMARY  (~{fmt(approx_tokens(text))} tokens, replaces everything above) "
                    .ljust(78, "─")))
        for ln in text.splitlines():
            print(paint("summary", f"  │ {ln}"))
        print(paint("summary", "  └" + "─" * 76))
        print()
        state["n"] = 1
        state["kinds"] = {"summary": 1}
        return

    if t == "attachment":
        a = rec.get("attachment") or {}
        if a.get("type") == "file":
            body = (a.get("content") or {}).get("file", {}).get("content", "")
            if not body:
                body = json.dumps(a.get("content"))
            name = a.get("displayPath") or os.path.basename(a.get("filename", "?"))
            item(state, "@FILE", approx_tokens(body), f"{name}  ({body.count(chr(10)) + 1} lines pasted)", "cost")
        return

    if t == "user":
        if rec.get("isMeta"):
            if isinstance(content, str) and content.startswith("## Context Usage"):
                official(content, state)
            return
        if isinstance(content, str):
            if content.startswith("<local-command") or content.startswith("<command-"):
                return  # slash commands and their local output; not sent to the model
            if content.startswith("/"):
                print(paint("you", f"      YOU ran    {content.strip()}"))
                return
            item(state, "YOU", approx_tokens(content), content, "you")
        else:
            for b in content:
                if not isinstance(b, dict):
                    continue
                if b.get("type") == "tool_result":
                    txt = block_text(b)
                    item(state, "TOOL OUT", approx_tokens(txt), txt, "cost")
                elif b.get("type") == "text":
                    txt = b.get("text", "")
                    if txt.startswith("<local-command") or txt.startswith("<command-"):
                        continue
                    item(state, "YOU", approx_tokens(txt), txt, "you")
        return

    if t == "assistant":
        if isinstance(content, str):
            content = [{"type": "text", "text": content}]
        for b in content:
            if not isinstance(b, dict):
                continue
            if b.get("type") == "text" and b.get("text", "").strip():
                item(state, "CLAUDE", approx_tokens(b["text"]), b["text"], "claude")
            elif b.get("type") == "tool_use":
                inp = b.get("input", {})
                arg = inp.get("file_path") or inp.get("command") or inp.get("pattern") or ""
                print(paint("tool", f"      CLAUDE ->  {b.get('name')}({short(arg, 60)})"))
        u = msg.get("usage") or {}
        total = (u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0)
                 + u.get("cache_creation_input_tokens", 0))
        if total and total != state.get("last_total"):
            state["last_total"] = total
            w = state["window"]
            print(paint("meter", f"      CONTEXT  [{bar(total / w)}] {fmt(total):>8} / {fmt(w)}  "
                        f"({100 * total / w:4.1f}%)  est. from API usage"))


def official(text, state):
    """The exact numbers from the presenter's /context run."""
    tot = re.search(r"\*\*Tokens:\*\*\s*([\d.]+)k\s*/\s*([\d.]+)k\s*\((\d+)%\)", text)
    msgs = re.search(r"\|\s*Messages\s*\|\s*([\d.]+k?)\s*\|\s*([\d.]+)%", text)
    if not tot:
        return
    used, win = float(tot.group(1)) * 1000, float(tot.group(2)) * 1000
    state["window"] = int(win)
    mtxt = f"Messages {msgs.group(1)} ({msgs.group(2)}%)" if msgs else "Messages 0"
    print(paint("official", f"      /context [{bar(used / win)}] {fmt(int(used)):>8} / {fmt(int(win))}  "
                f"({tot.group(3):>3}%)  {mtxt}"))


# ----------------------------------------------------------------- follow ---


def follow(path, state, replay, explicit_cfg, known):
    print(paint("dim", f"# following {describe(path)}"))
    print(paint("dim", "# ctrl+c to stop\n"))
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        if not replay:
            f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if line:
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                handle(rec, state)
                sys.stdout.flush()
                continue
            time.sleep(0.5)
            fresh = [c for c in candidate_transcripts(explicit_cfg) if c not in known]
            if fresh:
                known.update(fresh)
                print(paint("warn", f"\n# new session started, switching: {describe(fresh[0])}\n"))
                return fresh[0]


def main():
    global USE_COLOR
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--follow", action="store_true", help="don't replay the file, live only")
    ap.add_argument("--window", type=int, default=200_000, help="model context window for the bar")
    ap.add_argument("--file", help="a specific transcript .jsonl instead of the newest")
    ap.add_argument("--config-dir", help="look only in this Claude config dir")
    ap.add_argument("--list", action="store_true", help="list candidate transcripts and exit")
    ap.add_argument("--no-color", action="store_true")
    args = ap.parse_args()
    if args.no_color:
        USE_COLOR = False

    cands = candidate_transcripts(args.config_dir)
    if args.list:
        for p in cands[:10]:
            print(describe(p))
            print(f"    {p}")
        return
    path = args.file or (cands[0] if cands else None)
    if not path:
        sys.exit(f"no transcripts for {os.getcwd()} in {', '.join(config_dirs(args.config_dir))}.\n"
                 f"Start `claude` in this repo first, or pass --file.")
    if not args.file and len(cands) > 1:
        print(paint("dim", "# transcripts for this repo, newest first (picked the first; "
                    "use --config-dir NAME or --file PATH to pick another):"))
        for pth in cands[:4]:
            print(paint("dim", f"#   {describe(pth)}"))
    if not args.file and time.time() - os.path.getmtime(path) > STALE_SECONDS:
        print(paint("warn", f"# newest transcript was last written {age(path)} ago. If that is not your demo "
                    f"session, start `claude` in this repo now; this screen switches to it automatically."))
    state = {"window": args.window, "last_total": None, "n": 0, "kinds": {}, "est": 0}
    replay = not args.follow
    known = set(cands) | {path}
    try:
        while True:
            nxt = follow(path, state, replay, args.config_dir, known)
            path, replay = nxt, True
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
