#!/usr/bin/env python3
"""
"PyEng - Hated that? Doesn't make sense? Don't worry PyEng's got your back"

PyEng Interpreter (BETA)
Runs a .pyeng file by transpiling, executing in-process, then cleaning up.
"""

import sys
import os
import re
import tempfile

# Import the transpiler from the sibling module
try:
    from pyeng_transpiler import transpile
except ImportError:
    print("Error: pyeng_transpiler.py not found. Make sure it's in the same folder.")
    sys.exit(1)


def interpret(filepath: str):
    """Transpile a .pyeng file, print banner, run it, and clean up."""
    if not os.path.isfile(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    # Read the PyEng source
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    # Transpile to Python
    python_code = transpile(source)

    # Write to a temporary .py file (still useful for debugging,
    # but we will exec the code directly from memory)
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(python_code)
        tmp_path = tmp.name

    # Print the banner BEFORE running the script
    print("--------------------------------------")
    print("PyEng Interpretor (BETA)")
    print("--------------------------------------")
    sys.stdout.flush()

    # Execute the Python code directly in this process
    try:
        compiled = compile(python_code, filepath, "exec")
        exec_globals = {
            "__name__": "__main__",
            "__file__": filepath,   # points to the original .pyeng for clarity
        }
        exec(compiled, exec_globals)
    except Exception as e:
        err_type = type(e).__name__
        tip = ("(tip: if you're stuck, try converting your .pyeng file to a "
               ".py file to see what Python thinks you wrote: pyeng convert "
               f"{os.path.basename(filepath)})")

        # NameError – extract the missing name
        if err_type == "NameError":
            name_match = re.search(r"name '(.+?)' is not defined", str(e))
            if name_match:
                name = name_match.group(1)
                msg = (f"I don't know what '{name}' is. "
                       "Did you spell it right or forget to create it?")
            else:
                msg = ("I don't understand this name. "
                       "Did you spell it right or forget to create it?")
        elif err_type == "TypeError":
            msg = ("You used the wrong type of thing. "
                   "Check if you're adding a word to a number or something like that.")
        elif err_type == "SyntaxError":
            msg = ("Your code has a grammar mistake. "
                   "Check your spelling and make sure all your blocks (loops, ifs) "
                   "are set up right.")
        elif err_type == "IndentationError":
            msg = ("Your spaces are uneven. "
                   "Make sure every line inside a block has the same number of spaces at the start.")
        elif err_type == "ZeroDivisionError":
            msg = "You can't divide by zero. That breaks math."
        elif err_type == "FileNotFoundError":
            msg = ("I couldn't find a file you asked for. "
                   "Check the file name and make sure it's there.")
        else:
            msg = f"Your program ran into a problem: {e}"

        # Show the friendly message and tip, then wait before cleanup
        print(f"\n{msg}\n{tip}")
        input("\nPress Enter to close...")
    finally:
        # Delete the temporary .py file after execution
        # (runs even if the script calls sys.exit())
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def main():
    if len(sys.argv) != 2:
        print("CLI Usage: pyeng_interpreter.exe <file.pyeng>")
        sys.exit(1)
    interpret(sys.argv[1])


if __name__ == "__main__":
    main()