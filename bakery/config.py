"""Bakery settings."""

# Where the bakery API listens.
DEFAULT_PORT = 8080

# The accelerator "ovens" we can bake wheels on.
OVENS = ["cuda", "rocm", "gaudi", "spyre", "cpu"]

# Packages we know how to bake, and how long a bake usually takes (minutes).
RECIPES = {
    "torch": 42,
    "vllm": 27,
    "triton": 18,
    "flash-attn": 35,
    "xformers": 21,
    "bitsandbytes": 9,
}

# Wheels that burn (fail) this many times in a row get pulled from the menu.
BURNT_THRESHOLD = 3
