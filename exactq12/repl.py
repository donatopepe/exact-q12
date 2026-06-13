from __future__ import annotations

import sys
from typing import TextIO

from exactq12.gates import execute
from exactq12.parser import parse_text


def repl(input_stream: TextIO | None = None, output_stream: TextIO | None = None) -> int:
    input_stream = input_stream or sys.stdin
    output_stream = output_stream or sys.stdout
    program_lines: list[str] = []
    last_output_count = 0
    interactive = input_stream.isatty()

    if interactive:
        print("EXACT-Q12 REPL. Type EXIT or QUIT to leave.", file=output_stream)

    while True:
        if interactive:
            print("q12> ", end="", file=output_stream, flush=True)
        line = input_stream.readline()
        if line == "":
            break

        stripped = line.strip()
        if not stripped:
            continue
        if stripped.upper() in {"EXIT", "QUIT"}:
            break

        program_lines.append(stripped)
        try:
            _, output = execute(parse_text("\n".join(program_lines)))
        except ValueError as exc:
            program_lines.pop()
            print(f"ERROR: {exc}", file=output_stream)
            continue

        for item in output[last_output_count:]:
            print(item, file=output_stream)
        last_output_count = len(output)

    return 0
