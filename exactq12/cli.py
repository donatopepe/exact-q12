from __future__ import annotations

import argparse
import json

from exactq12.benchmark import run_benchmark
from exactq12.gates import execute
from exactq12.logging_utils import JsonlLogger
from exactq12.parser import parse_file


def run(path: str, log_path: str | None = None) -> int:
    logger = JsonlLogger(log_path)
    logger.write("run_start", path=path)
    _, output = execute(parse_file(path))
    for line in output:
        print(line)
    logger.write("run_end", path=path, output_lines=len(output))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="exactq12")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("path")
    run_parser.add_argument("--log-jsonl", dest="log_jsonl")

    bench_parser = subparsers.add_parser("bench")
    bench_parser.add_argument("--qubits", type=int, required=True)
    bench_parser.add_argument("--gates", type=int, required=True)
    bench_parser.add_argument("--repetitions", type=int, default=1)
    bench_parser.add_argument("--log-jsonl", dest="log_jsonl")

    args = parser.parse_args(argv)
    if args.command == "run":
        return run(args.path, args.log_jsonl)
    if args.command == "bench":
        result = run_benchmark(args.qubits, args.gates, args.repetitions, args.log_jsonl)
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
        return 0
    parser.error(f"unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
