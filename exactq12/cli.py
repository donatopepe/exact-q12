from __future__ import annotations

import argparse
import json
from pathlib import Path

from exactq12.benchmark import run_benchmark
from exactq12.binary import export_binary, export_memh, run_program_image
from exactq12.gates import execute
from exactq12.logging_utils import JsonlLogger
from exactq12.parser import parse_file
from exactq12.repl import repl
from exactq12.rtl_pack import reset_statevector_memh


def run(path: str, log_path: str | None = None) -> int:
    logger = JsonlLogger(log_path)
    logger.write("run_start", path=path)
    _, output = execute(parse_file(path))
    for line in output:
        print(line)
    logger.write("run_end", path=path, output_lines=len(output))
    return 0


def dump(path: str) -> int:
    state, _ = execute(parse_file(path))
    for line in state.dump_lines():
        print(line)
    return 0


def export(path: str, output_path: str, export_format: str) -> int:
    if export_format == "bin":
        byte_count = export_binary(path, output_path)
        print(f"wrote {byte_count} bytes to {output_path}")
        return 0
    if export_format == "memh":
        instruction_count = export_memh(path, output_path)
        print(f"wrote {instruction_count} instructions to {output_path}")
        return 0
    else:
        raise ValueError(f"unsupported export format: {export_format}")


def fpga_run(path: str) -> int:
    _, output = run_program_image(path)
    for line in output:
        print(line)
    return 0


def state_init(qubits: int, output_path: str) -> int:
    if qubits < 1:
        raise ValueError("qubits must be >= 1")
    text = reset_statevector_memh(qubits)
    Path(output_path).write_text(text, encoding="utf-8")
    print(f"wrote {2**qubits} amplitudes to {output_path}")
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

    subparsers.add_parser("repl")

    dump_parser = subparsers.add_parser("dump")
    dump_parser.add_argument("path")

    export_parser = subparsers.add_parser("export")
    export_parser.add_argument("path")
    export_parser.add_argument("--format", choices=["bin", "memh"], required=True)
    export_parser.add_argument("--out", required=True)

    state_init_parser = subparsers.add_parser("state-init")
    state_init_parser.add_argument("--qubits", type=int, required=True)
    state_init_parser.add_argument("--out", required=True)

    fpga_parser = subparsers.add_parser("fpga")
    fpga_subparsers = fpga_parser.add_subparsers(dest="fpga_command", required=True)
    fpga_run_parser = fpga_subparsers.add_parser("run")
    fpga_run_parser.add_argument("path")

    args = parser.parse_args(argv)
    if args.command == "run":
        return run(args.path, args.log_jsonl)
    if args.command == "bench":
        result = run_benchmark(args.qubits, args.gates, args.repetitions, args.log_jsonl)
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
        return 0
    if args.command == "repl":
        return repl()
    if args.command == "dump":
        return dump(args.path)
    if args.command == "export":
        return export(args.path, args.out, args.format)
    if args.command == "state-init":
        return state_init(args.qubits, args.out)
    if args.command == "fpga" and args.fpga_command == "run":
        return fpga_run(args.path)
    parser.error(f"unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
