"""Pretend to bake a wheel. Verbose by default: a bake prints one line per minute."""
from .config import OVENS, RECIPES


def bake(package, oven, verbose=True):
    if package not in RECIPES:
        raise ValueError(f"no recipe for {package}")
    if oven not in OVENS:
        raise ValueError(f"unknown oven {oven}")
    minutes = RECIPES[package]
    if verbose:
        for step in range(minutes):
            print(f"[{oven}] baking {package}: minute {step + 1}/{minutes} ... still rising")
    return {"package": package, "oven": oven, "minutes": minutes, "status": "golden"}
