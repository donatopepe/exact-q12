from __future__ import annotations

import json
import platform
from dataclasses import asdict, dataclass
from time import perf_counter_ns

from exactq12.logging_utils import JsonlLogger
from exactq12.statevector import Statevector


@dataclass(frozen=True)
class BenchmarkResult:
    qubits: int
    gates: int
    repetitions: int
    amplitudes: int
    elapsed_ns: int
    average_run_ns: int
    average_gate_ns: int
    max_coefficient_digits: int
    python: str
    platform: str

    def to_dict(self) -> dict[str, int | str]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True)


def _apply_benchmark_gate(state: Statevector, step: int) -> None:
    qubits = state.num_qubits
    target = step % qubits
    opcode = step % 9

    if opcode == 0:
        state.apply_h(target)
    elif opcode == 1:
        state.apply_s(target)
    elif opcode == 2:
        state.apply_t(target)
    elif opcode == 3:
        state.apply_p30(target)
    elif opcode == 4:
        state.apply_p60(target)
    elif opcode == 5:
        state.apply_z(target)
    elif opcode == 6:
        state.apply_x(target)
    elif opcode == 7 and qubits > 1:
        state.apply_cnot(target, (target + 1) % qubits)
    elif qubits > 1:
        state.apply_swap(target, (target + 1) % qubits)
    else:
        state.apply_h(target)


def _max_coefficient_digits(state: Statevector) -> int:
    max_abs = 0
    for amplitude in state.amplitudes:
        for value in (amplitude.real, amplitude.imag):
            max_abs = max(max_abs, abs(value.a), abs(value.b), abs(value.c), abs(value.d))
    return len(str(max_abs))


def run_benchmark(
    qubits: int,
    gates: int,
    repetitions: int = 1,
    log_path: str | None = None,
) -> BenchmarkResult:
    if qubits < 1:
        raise ValueError("qubits must be >= 1")
    if gates < 1:
        raise ValueError("gates must be >= 1")
    if repetitions < 1:
        raise ValueError("repetitions must be >= 1")

    logger = JsonlLogger(log_path)
    logger.write("benchmark_start", qubits=qubits, gates=gates, repetitions=repetitions)

    max_digits = 1
    start = perf_counter_ns()
    for repetition in range(repetitions):
        state = Statevector.reset(qubits)
        logger.write("benchmark_repetition_start", repetition=repetition)
        for step in range(gates):
            _apply_benchmark_gate(state, step)
        max_digits = max(max_digits, _max_coefficient_digits(state))
        logger.write("benchmark_repetition_end", repetition=repetition, max_coefficient_digits=max_digits)
    elapsed_ns = perf_counter_ns() - start

    average_run_ns = elapsed_ns // repetitions
    average_gate_ns = elapsed_ns // (repetitions * gates)
    result = BenchmarkResult(
        qubits=qubits,
        gates=gates,
        repetitions=repetitions,
        amplitudes=2**qubits,
        elapsed_ns=elapsed_ns,
        average_run_ns=average_run_ns,
        average_gate_ns=average_gate_ns,
        max_coefficient_digits=max_digits,
        python=platform.python_version(),
        platform=platform.platform(),
    )
    logger.write("benchmark_end", **result.to_dict())
    return result
