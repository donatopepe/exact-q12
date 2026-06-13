import json
import subprocess
import sys

import pytest

from exactq12.benchmark import run_benchmark
from exactq12.parser import Instruction, parse_text


def test_parser_handles_comments_and_case() -> None:
    assert parse_text("""
# comment
reset 2
h q0  # inline comment
cnot q0 q1
dump
""") == [
        Instruction("RESET", (2,)),
        Instruction("H", (0,)),
        Instruction("CNOT", (0, 1)),
        Instruction("DUMP"),
    ]


@pytest.mark.parametrize(
    "source, message",
    [
        ("H q0", "used before RESET"),
        ("RESET 0", "at least one qubit"),
        ("RESET 1\nCNOT q0 q0", "must be different"),
        ("RESET 1\nH q2", "out of range"),
    ],
)
def test_invalid_programs_raise(source: str, message: str) -> None:
    from exactq12.gates import execute

    with pytest.raises(ValueError, match=message):
        execute(parse_text(source))


def test_benchmark_returns_json_serializable_result(tmp_path) -> None:
    log_path = tmp_path / "bench.jsonl"
    result = run_benchmark(qubits=2, gates=12, repetitions=2, log_path=str(log_path))
    payload = result.to_dict()
    assert payload["qubits"] == 2
    assert payload["gates"] == 12
    assert payload["repetitions"] == 2
    assert payload["amplitudes"] == 4
    assert payload["average_gate_ns"] >= 0
    assert json.loads(result.to_json()) == payload

    events = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert events[0]["event"] == "benchmark_start"
    assert events[-1]["event"] == "benchmark_end"


def test_cli_run_writes_jsonl_log(tmp_path) -> None:
    circuit = tmp_path / "circuit.q12"
    log_path = tmp_path / "run.jsonl"
    circuit.write_text("RESET 1\nH q0\nDUMP\n", encoding="utf-8")
    completed = subprocess.run(
        [sys.executable, "-m", "exactq12.cli", "run", str(circuit), "--log-jsonl", str(log_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "|0>" in completed.stdout
    events = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert [event["event"] for event in events] == ["run_start", "run_end"]


def test_cli_bench_prints_json() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "exactq12.cli", "bench", "--qubits", "1", "--gates", "3"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)
    assert payload["qubits"] == 1
    assert payload["gates"] == 3
