from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Instruction:
    opcode: str
    args: tuple[int, ...] = ()


def _parse_qubit(token: str) -> int:
    if not token.startswith("q") or not token[1:].isdigit():
        raise ValueError(f"invalid qubit token: {token}")
    return int(token[1:])


def parse_text(source: str) -> list[Instruction]:
    instructions: list[Instruction] = []
    one_qubit = {"X", "Z", "H", "S", "T", "P30", "P60", "MEASURE"}
    two_qubit = {"CNOT", "SWAP"}

    for line_number, raw_line in enumerate(source.splitlines(), start=1):
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue

        parts = line.split()
        opcode = parts[0].upper()
        try:
            if opcode == "RESET":
                if len(parts) != 2 or not parts[1].isdigit():
                    raise ValueError("RESET requires a positive integer")
                instructions.append(Instruction(opcode, (int(parts[1]),)))
            elif opcode in one_qubit:
                if len(parts) != 2:
                    raise ValueError(f"{opcode} requires one qubit")
                instructions.append(Instruction(opcode, (_parse_qubit(parts[1]),)))
            elif opcode in two_qubit:
                if len(parts) != 3:
                    raise ValueError(f"{opcode} requires two qubits")
                instructions.append(Instruction(opcode, (_parse_qubit(parts[1]), _parse_qubit(parts[2]))))
            elif opcode in {"DUMP", "PROB"}:
                if len(parts) != 1:
                    raise ValueError(f"{opcode} takes no arguments")
                instructions.append(Instruction(opcode))
            else:
                raise ValueError(f"unknown opcode: {opcode}")
        except ValueError as exc:
            raise ValueError(f"line {line_number}: {exc}") from exc

    return instructions


def parse_file(path: str | Path) -> list[Instruction]:
    return parse_text(Path(path).read_text())
