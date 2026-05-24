#!/usr/bin/env python3
"""
PyEng Transpiler v1.1 – CLI Tool
"PyEng - Hated that? Doesn't make sense? Don't worry PyEng's got your back"

Usage:
    pyeng run <file.pyeng>      # Run a pyeng file
    pyeng convert <file.pyeng>  # Transpile a .pyeng to .py file
    pyeng reverse <file.py>     # Reverse a .py file into .pyeng
    pyeng copyright             # Show copyright status
    pyeng license               # Show PyEng license
    pyeng --help                # The help command for pyeng
"""

import sys
import os
import subprocess
import tempfile

# Import the transpiler function from the sibling module
try:
    from pyeng_transpiler import transpile
except ImportError:
    print("Error: Could not find pyeng_transpiler.py in the current directory.")
    sys.exit(1)

# Import the reverse transpiler
try:
    from pyeng_reverse_transpiler import reverse_transpile
except ImportError:
    print("Error: Could not find pyeng_reverse_transpiler.py in the current directory.")
    sys.exit(1)


def print_help():
    print(__doc__)


def run_file(filepath: str):
    """Transpile a .pyeng file to Python and run it."""
    if not os.path.isfile(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    python_code = transpile(source)

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(python_code)
        tmp_path = tmp.name
    
    print("--------------------------------------")
    print("Created with PyEng (Python but easier)")
    print("--------------------------------------")
    sys.stdout.flush()

    try:
        subprocess.run([sys.executable, tmp_path], check=False)
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def converted_file(filepath: str):
    """Transpile a .pyeng file and save the result as a .py file."""
    if not filepath.endswith(".pyeng"):
        print("Warning: Input file does not have .pyeng extension.")
    outpath = filepath.rsplit(".pyeng", 1)[0] + ".py"

    if not os.path.isfile(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    python_code = transpile(source)

    with open(outpath, "w", encoding="utf-8") as f:
        f.write(python_code)

    print(f"Converted: {outpath}")


def reverse_file(filepath: str):
    """Reverse a .py file back to a .pyeng file."""
    if not filepath.endswith(".py"):
        print("Warning: Input file does not have .py extension.")
    outpath = filepath.rsplit(".py", 1)[0] + ".pyeng"

    if not os.path.isfile(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    pyeng_code = reverse_transpile(source)

    with open(outpath, "w", encoding="utf-8") as f:
        f.write(pyeng_code)

    print(f"Reversed: {outpath}")


def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)

    command = sys.argv[1].lower()

    if command in ("--help", "-h", "help"):
        print_help()
        sys.exit(0)

    if command == "run":
        if len(sys.argv) != 3:
            print("Error: 'run' expects exactly one argument: the .pyeng file.")
            sys.exit(1)
        run_file(sys.argv[2])
    elif command == "convert":
        if len(sys.argv) != 3:
            print("Error: 'convert' expects exactly one argument: the .pyeng file.")
            sys.exit(1)
        converted_file(sys.argv[2])
    elif command == "reverse":
        if len(sys.argv) != 3:
            print("Error: 'reverse' expects exactly one argument: the .py file.")
            sys.exit(1)
        reverse_file(sys.argv[2])
    elif command == "copyright":
        print("COPYRIGHT (C) 2026 NEWPYTHONX STUDIOS.")
        print("All Rights Reserved.")
    elif command == "license":
        print("NewPythonX Studio - Official License")
        print("All rights reserved.")
    else:
        print(f"Unknown command: {command}")
        print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()