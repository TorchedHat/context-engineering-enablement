"""Generate the bloat in data/: a wheel catalog and build logs.

Output is committed, so attendees never run this. Deterministic via --seed.
"""
import argparse
import json
import random
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"

PACKAGES = ["torch", "vllm", "triton", "flash-attn", "xformers", "bitsandbytes"]
OVENS = ["cuda", "rocm", "gaudi", "spyre", "cpu"]
PY = ["3.9", "3.10", "3.11", "3.12"]
# Model names are the fun part. Beginners remember "llama-frenchtoast".
MODEL_ADJ = ["frenchtoast", "sourdough", "brioche", "croissant", "bagel", "pretzel",
             "focaccia", "ciabatta", "rye", "pumpernickel", "naan", "pita"]
MODEL_BASE = ["llama", "mistral", "granite", "qwen", "gemma", "phi", "falcon", "olmo"]

STEPS = [
    "Resolving build dependencies",
    "Fetching source tarball",
    "Verifying checksum",
    "Applying accelerator patches",
    "Configuring CMake",
    "Compiling kernels (this is the slow part)",
    "Linking shared objects",
    "Running smoke tests",
    "Auditing wheel with auditwheel",
    "Uploading to wheelhouse",
]
# Failures that make sense for each oven, plus a few that can happen anywhere.
FAILS = {
    "cuda": ["nvcc fatal: unsupported gpu architecture 'compute_120'",
             "smoke test failed: ImportError: libcudart.so.12"],
    "rocm": ["undefined reference to `hipMemcpyAsync'"],
    "gaudi": ["error: Gaudi SynapseAI headers not found"],
    "spyre": ["spyre-runtime: device busy, retry later"],
    "cpu": [],
}
FAILS_ANY = [
    "OOM: kernel compilation exceeded 64GB",
    "auditwheel: wheel is not manylinux_2_28 compatible",
]


def gen_catalog(rng, n):
    wheels = []
    for i in range(n):
        pkg = rng.choice(PACKAGES)
        wheels.append({
            "id": f"whl-{i:05d}",
            "package": pkg,
            "version": f"{rng.randint(1, 4)}.{rng.randint(0, 9)}.{rng.randint(0, 9)}",
            "oven": rng.choice(OVENS),
            "python": rng.choice(PY),
            "consecutive_failures": rng.choices([0, 0, 0, 1, 2, 3, 4], k=1)[0],
            "size_mb": round(rng.uniform(2, 900), 1),
            "baked_at": f"2026-{rng.randint(1, 8):02d}-{rng.randint(1, 28):02d}T{rng.randint(0, 23):02d}:{rng.randint(0, 59):02d}:00Z",
            "served_to": [f"{rng.choice(MODEL_BASE)}-{rng.choice(MODEL_ADJ)}-{rng.choice([7, 8, 13, 34, 70])}b"
                          for _ in range(rng.randint(0, 4))],
            "sha256": "".join(rng.choices("0123456789abcdef", k=64)),
        })
    return {"generated_by": "tools/gen_data.py", "wheels": wheels}


def gen_log(rng, idx):
    pkg = rng.choice(PACKAGES)
    oven = rng.choice(OVENS)
    py = rng.choice(PY)
    fail_at = rng.choice([None, None, None, rng.randint(3, 8)])
    lines = [f"=== bake #{idx:04d} {pkg} oven={oven} python={py} ==="]
    t = 0
    for n, step in enumerate(STEPS, start=1):
        lines.append(f"[{t:05d}s] step {n}/{len(STEPS)}: {step}")
        for _ in range(rng.randint(4, 14)):
            t += rng.randint(1, 40)
            lines.append(f"[{t:05d}s]   {rng.choice(['ok', 'ok', 'ok', 'warn', 'info'])}: "
                         f"{rng.choice(['cache hit', 'cache miss', 'retrying', 'compiled', 'skipped', 'downloaded'])} "
                         f"{rng.choice(['kernel', 'header', 'object', 'artifact', 'layer'])}-{rng.randint(1, 9999)}")
        if fail_at == n:
            lines.append(f"[{t:05d}s] ERROR: {rng.choice(FAILS[oven] + FAILS_ANY)}")
            lines.append(f"=== bake #{idx:04d} BURNT after {t}s ===")
            return "\n".join(lines) + "\n"
    lines.append(f"=== bake #{idx:04d} GOLDEN after {t}s ===")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--logs", type=int, default=40)
    ap.add_argument("--catalog", type=int, default=900)
    ap.add_argument("--seed", type=int, default=2026)
    a = ap.parse_args()
    rng = random.Random(a.seed)
    DATA.mkdir(exist_ok=True)
    (DATA / "logs").mkdir(exist_ok=True)
    (DATA / "catalog.json").write_text(json.dumps(gen_catalog(rng, a.catalog), indent=1))
    for i in range(a.logs):
        (DATA / "logs" / f"bake-{i:04d}.log").write_text(gen_log(rng, i))
    total = sum(p.stat().st_size for p in DATA.rglob("*") if p.is_file())
    print(f"wrote data/: {total/1024:.0f} KB (~{total//4//1000}k tokens at 4 chars/token)")


if __name__ == "__main__":
    main()
