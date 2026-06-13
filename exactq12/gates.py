from __future__ import annotations

from exactq12.parser import Instruction
from exactq12.statevector import Statevector


def execute(instructions: list[Instruction]) -> tuple[Statevector, list[str]]:
    state: Statevector | None = None
    output: list[str] = []

    for instruction in instructions:
        opcode = instruction.opcode
        args = instruction.args

        if opcode == "RESET":
            state = Statevector.reset(args[0])
            continue

        if state is None:
            raise ValueError(f"{opcode} used before RESET")

        if opcode == "X":
            state.apply_x(args[0])
        elif opcode == "Z":
            state.apply_z(args[0])
        elif opcode == "H":
            state.apply_h(args[0])
        elif opcode == "S":
            state.apply_s(args[0])
        elif opcode == "T":
            state.apply_t(args[0])
        elif opcode == "P30":
            state.apply_p30(args[0])
        elif opcode == "P60":
            state.apply_p60(args[0])
        elif opcode == "CNOT":
            state.apply_cnot(args[0], args[1])
        elif opcode == "SWAP":
            state.apply_swap(args[0], args[1])
        elif opcode == "DUMP":
            output.extend(state.dump_lines())
        elif opcode == "PROB":
            output.extend(state.probability_lines())
        elif opcode == "MEASURE":
            output.append(f"MEASURE q{args[0]} = {state.measure(args[0])}")
        else:
            raise ValueError(f"unknown opcode: {opcode}")

    if state is None:
        raise ValueError("program must contain RESET")
    return state, output
