from __future__ import annotations

from pathlib import Path

from exactq12.gates import execute
from exactq12.parser import Instruction, parse_file
from exactq12.statevector import Statevector


OPCODES: dict[str, int] = {
    "RESET": 0x00,
    "X": 0x01,
    "Z": 0x02,
    "H": 0x03,
    "S": 0x04,
    "T": 0x05,
    "P30": 0x06,
    "P60": 0x07,
    "CNOT": 0x08,
    "SWAP": 0x09,
    "DUMP": 0x0A,
    "PROB": 0x0B,
    "MEASURE": 0x0C,
}
OPCODE_NAMES = {value: key for key, value in OPCODES.items()}


def encode_instruction(instruction: Instruction) -> bytes:
    if instruction.opcode not in OPCODES:
        raise ValueError(f"unknown opcode: {instruction.opcode}")
    args = instruction.args
    if len(args) > 2:
        raise ValueError(f"too many arguments for {instruction.opcode}")
    arg0 = args[0] if len(args) >= 1 else 0
    arg1 = args[1] if len(args) >= 2 else 0
    if not 0 <= arg0 <= 255 or not 0 <= arg1 <= 255:
        raise ValueError("binary instruction arguments must fit in one byte")
    return bytes((OPCODES[instruction.opcode], arg0, arg1))


def encode_instructions(instructions: list[Instruction]) -> bytes:
    return b"".join(encode_instruction(instruction) for instruction in instructions)


def encode_memh(instructions: list[Instruction]) -> str:
    payload = encode_instructions(instructions)
    return "\n".join(payload[offset : offset + 3].hex() for offset in range(0, len(payload), 3)) + "\n"


def decode_memh(text: str) -> list[Instruction]:
    payload = bytearray()
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue
        if len(line) != 6:
            raise ValueError(f"line {line_number}: memh instruction must be 6 hex digits")
        try:
            payload.extend(bytes.fromhex(line))
        except ValueError as exc:
            raise ValueError(f"line {line_number}: invalid hex instruction") from exc
    return decode_instructions(bytes(payload))


def decode_instructions(payload: bytes) -> list[Instruction]:
    if len(payload) % 3 != 0:
        raise ValueError("binary payload length must be a multiple of 3")

    instructions: list[Instruction] = []
    no_arg = {"DUMP", "PROB"}
    one_arg = {"RESET", "X", "Z", "H", "S", "T", "P30", "P60", "MEASURE"}
    two_arg = {"CNOT", "SWAP"}

    for offset in range(0, len(payload), 3):
        opcode_byte, arg0, arg1 = payload[offset : offset + 3]
        if opcode_byte not in OPCODE_NAMES:
            raise ValueError(f"unknown binary opcode: 0x{opcode_byte:02x}")
        opcode = OPCODE_NAMES[opcode_byte]
        if opcode in no_arg:
            instructions.append(Instruction(opcode))
        elif opcode in one_arg:
            instructions.append(Instruction(opcode, (arg0,)))
        elif opcode in two_arg:
            instructions.append(Instruction(opcode, (arg0, arg1)))
        else:
            raise ValueError(f"unsupported binary opcode: {opcode}")
    return instructions


def export_binary(source_path: str | Path, output_path: str | Path) -> int:
    instructions = parse_file(source_path)
    payload = encode_instructions(instructions)
    Path(output_path).write_bytes(payload)
    return len(payload)


def export_memh(source_path: str | Path, output_path: str | Path) -> int:
    instructions = parse_file(source_path)
    text = encode_memh(instructions)
    Path(output_path).write_text(text, encoding="utf-8")
    return len(instructions)


def run_binary(path: str | Path) -> tuple[Statevector, list[str]]:
    return execute(decode_instructions(Path(path).read_bytes()))


def run_memh(path: str | Path) -> tuple[Statevector, list[str]]:
    return execute(decode_memh(Path(path).read_text(encoding="utf-8")))


def run_program_image(path: str | Path) -> tuple[Statevector, list[str]]:
    path = Path(path)
    if path.suffix.lower() == ".memh":
        return run_memh(path)
    return run_binary(path)
