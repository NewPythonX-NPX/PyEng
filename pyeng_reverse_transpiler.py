#!/usr/bin/env python3
"""
"PyEng - Hated that? Doesn't make sense? Don't worry PyEng's got your back"

PyEng Reverse Transpiler v1.1
Converts normal Python code back into PyEng (best effort).
Now correctly round‑trips with the main transpiler.
"""

import re


def reverse_transpile(python_source: str) -> str:
    """
    Convert a Python source string to PyEng.
    Every mapping is the exact inverse of the forward transpiler.
    Because PyEng accepts all Python keywords, we leave `else` unchanged
    to avoid breaking if/else statements.
    """
    lines = python_source.splitlines(keepends=True)
    result = []

    for line in lines:
        stripped = line.lstrip()
        indent = line[: len(line) - len(stripped)]

        # Skip empty or comment lines – they stay the same
        if not stripped or stripped.startswith("#"):
            result.append(line)
            continue

        # ------------------------------------------------------------------
        # 1. Multi‑word or structural patterns (longest first)
        # ------------------------------------------------------------------

        # "while True:" → "loop forever:"
        stripped = re.sub(r'\bwhile\s+True\b', 'loop forever', stripped)

        # "for X in" → "for each X in"
        stripped = re.sub(
            r'\bfor\s+(\w+)\s+in\b',
            r'for each \1 in',
            stripped,
            flags=re.IGNORECASE
        )

        # "try:" → "attempt:"
        stripped = re.sub(r'\btry\b', 'attempt', stripped)

        # "except:" → "if it breaks:"
        stripped = re.sub(r'\bexcept\b', 'if it breaks', stripped)

        # "elif" → "else if"
        stripped = re.sub(r'\belif\b', 'else if', stripped)

        # Note: We do NOT convert "else" – that keeps if/else working.
        # The forward transpiler only turns "if it works:" into "else:"
        # inside attempt blocks. Doing nothing is the safest choice.

        # ------------------------------------------------------------------
        # 2. Function / __init__ transformations
        # ------------------------------------------------------------------
        init_match = re.match(r'^\s*def\s+__init__\(\s*self\s*,?\s*(.*?)\s*\)\s*:', stripped)
        if init_match:
            params = init_match.group(1).strip()
            if params:
                stripped = f"init me({params}):"
            else:
                stripped = "init me():"
        else:
            # Normal function: "def" → "function"
            stripped = re.sub(r'\bdef\b', 'function', stripped)

        # ------------------------------------------------------------------
        # 3. Single‑word replacements (order doesn't matter as much,
        #    but keep consistency with forward transpiler)
        # ------------------------------------------------------------------

        # "self" → "me"
        stripped = re.sub(r'\bself\b', 'me', stripped)

        # "return" → "give back"
        stripped = re.sub(r'\breturn\b', 'give back', stripped)

        # "import" → "bring in"
        stripped = re.sub(r'\bimport\b', 'bring in', stripped)

        # "raise" → "throw error"
        stripped = re.sub(r'\braise\b', 'throw error', stripped)

        # "break" → "stop loop"
        stripped = re.sub(r'\bbreak\b', 'stop loop', stripped)

        # "continue" → "skip"
        stripped = re.sub(r'\bcontinue\b', 'skip', stripped)

        # "pass" → "do nothing"
        stripped = re.sub(r'\bpass\b', 'do nothing', stripped)

        # "True" → "yes"
        stripped = re.sub(r'\bTrue\b', 'yes', stripped)

        # "False" → "nah"
        stripped = re.sub(r'\bFalse\b', 'nah', stripped)

        # "or" → "also" (we could also use "either", but pick one)
        stripped = re.sub(r'\bor\b', 'also', stripped)

        # "class" → "blueprint"
        stripped = re.sub(r'\bclass\b', 'blueprint', stripped)

        # "with" → "use"
        stripped = re.sub(r'\bwith\b', 'use', stripped)

        # "None" → "nothing"
        stripped = re.sub(r'\bNone\b', 'nothing', stripped)

        # (no need to convert "#" to "comment" – forward transpiler
        #  treats lines starting with "#" as already commented)

        result.append(indent + stripped + "\n")

    return "".join(result)