#!/usr/bin/env python3
"""
PyEng Transpiler v1.1
"PyEng - Hated that? Doesn't make sense? Don't worry PyEng's got your back"

Converts PyEng code into normal Python.
This module provides the `transpile` function.
"""

import sys
import re


def transpile(source: str) -> str:
    """Transpile a PyEng source string to Python."""
    lines = source.splitlines(keepends=True)
    result = []
    in_try = False
    try_indent = 0
    step = 0

    for raw_line in lines:
        stripped = raw_line.lstrip()
        indent = raw_line[: len(raw_line) - len(stripped)]
        indent_len = len(indent)

        # ---- Handle try/except/else blocks ----
        if stripped.startswith("attempt:"):
            result.append(f"{indent}try:\n")
            in_try = True
            try_indent = indent_len
            step = 0
            continue

        if in_try and indent_len == try_indent:
            if stripped == "if it breaks:":
                result.append(f"{indent}except:\n")
                step = 1
                continue
            if stripped == "if it works:" and step == 1:
                result.append(f"{indent}else:\n")
                step = 2
                continue
            if step >= 1:
                in_try = False

        if in_try and indent_len < try_indent and stripped:
            in_try = False

        line = stripped

        # leave empty lines and already‑commented lines as‑is
        if not line or line.startswith("#"):
            result.append(f"{indent}{line}\n")
            continue

        # ------------------------------------------------------------------
        # Structural transformations
        # ------------------------------------------------------------------
        init_handled = False

        # "init me(...):" → "def __init__(self, ...):"
        init_match = re.match(r'^init\s+me\s*\(\s*(.*?)\s*\)\s*:\s*$', line)
        if init_match:
            params = init_match.group(1).strip()
            if params:
                line = f"def __init__(self, {params}):"
            else:
                line = f"def __init__(self):"
            init_handled = True

        # "function X" → "def X"
        if not init_handled and line.startswith("function "):
            line = "def " + line[9:]

        # "loop forever:" → "while True:"
        line = re.sub(r'\bloop forever\b', 'while True', line, flags=re.IGNORECASE)

        # ------------------------------------------------------------------
        # Token replacements (order matters!)
        # ------------------------------------------------------------------

        # "for each X in Y" → "for X in Y"   (must come before single-word replacements)
        line = re.sub(
            r'\bfor each\s+(\w+)\s+in\b',
            r'for \1 in',
            line,
            flags=re.IGNORECASE
        )

        # Multi‑word phrase: "bring in" → "import"
        line = re.sub(r'\bbring in\b', 'import', line, flags=re.IGNORECASE)

        # Multi‑word: "give back" → "return"
        line = re.sub(r'\bgive back\b', 'return', line, flags=re.IGNORECASE)

        # Multi‑word: "throw error" → "raise"
        line = re.sub(r'\bthrow error\b', 'raise', line, flags=re.IGNORECASE)

        # Replace "me" with "self" (but not on init line)
        if not init_handled:
            line = re.sub(r'\bme\b', 'self', line)

        # comment -> #
        line = re.sub(r'\b--\b', '#', line)

        # yes / nah → True / False
        line = re.sub(r'\byes\b', 'True', line, flags=re.IGNORECASE)
        line = re.sub(r'\bnah\b', 'False', line, flags=re.IGNORECASE)

        # else if / elseif → elif
        line = re.sub(r'\belse if\b', 'elif', line, flags=re.IGNORECASE)
        line = re.sub(r'\belseif\b', 'elif', line, flags=re.IGNORECASE)

        # structural keywords
        line = re.sub(r'\bstop loop\b', 'break', line, flags=re.IGNORECASE)
        line = re.sub(r'\bskip\b', 'continue', line, flags=re.IGNORECASE)
        line = re.sub(r'\bdo nothing\b', 'pass', line, flags=re.IGNORECASE)

        # ---- New mappings (v1.1) ----
        # "also" or "either"   → "or"
        line = re.sub(r'\balso\b', 'or', line, flags=re.IGNORECASE)
        line = re.sub(r'\beither\b', 'or', line, flags=re.IGNORECASE)

        # "blueprint" → "class"
        line = re.sub(r'\bblueprint\b', 'class', line, flags=re.IGNORECASE)

        # "use" → "with"   (keyword 'with', be careful with natural language use)
        line = re.sub(r'\buse\b', 'with', line, flags=re.IGNORECASE)

        # "nothing" → "None"
        line = re.sub(r'\bnothing\b', 'None', line, flags=re.IGNORECASE)

        result.append(f"{indent}{line}\n")

    return "".join(result)


if __name__ == "__main__":
    source = sys.stdin.read()
    sys.stdout.write(transpile(source))