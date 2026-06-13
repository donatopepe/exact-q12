from __future__ import annotations

import argparse

from exactq12.gates import execute
from exactq12.parser import parse_file


def run(path: str) -> int:
    _, output = execute(parse_file(path))
    for line in output:
        print(line)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="exactq12")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("path")

    args = parser.parse_args(argv)
    if args.command == "run":
        return run(args.path)
    parser.error(f"unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
