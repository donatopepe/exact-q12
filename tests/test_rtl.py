from pathlib import Path
import re

from exactq12.binary import OPCODES, encode_instructions
from exactq12.complex_q12 import CQ12
from exactq12.parser import parse_text
from exactq12.q12 import Q12


ROOT = Path(__file__).resolve().parents[1]


def rtl_q12_mul(x: tuple[int, int, int, int], y: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    a, b, c, d = x
    e, f, g, h = y
    return (
        a * e + 2 * b * f + 3 * c * g + 6 * d * h,
        a * f + b * e + 3 * c * h + 3 * d * g,
        a * g + c * e + 2 * b * h + 2 * d * f,
        a * h + d * e + b * g + c * f,
    )


def test_rtl_q12_mul_formula_matches_python_model() -> None:
    cases = [
        ((1, 2, 3, 4), (5, 6, 7, 8)),
        ((-3, 0, 2, -1), (4, -5, 0, 6)),
        ((0, 6, 0, 0), (0, 6, 0, 0)),
        ((6, 0, 0, 0), (0, 0, 6, 0)),
    ]

    for x, y in cases:
        expected = Q12(*x, 0) * Q12(*y, 0)
        assert rtl_q12_mul(x, y) == (expected.a, expected.b, expected.c, expected.d)


def test_rtl_complex_mul_formula_matches_python_model() -> None:
    left = CQ12(Q12(1, 2, 3, 4, 0), Q12(-1, 0, 2, 1, 0))
    right = CQ12(Q12(5, -1, 0, 2, 0), Q12(0, 3, -2, 1, 0))
    expected = left * right

    rr = rtl_q12_mul((1, 2, 3, 4), (5, -1, 0, 2))
    ii = rtl_q12_mul((-1, 0, 2, 1), (0, 3, -2, 1))
    ri = rtl_q12_mul((1, 2, 3, 4), (0, 3, -2, 1))
    ir = rtl_q12_mul((-1, 0, 2, 1), (5, -1, 0, 2))

    real = tuple(a - b for a, b in zip(rr, ii))
    imag = tuple(a + b for a, b in zip(ri, ir))
    assert real == (expected.real.a, expected.real.b, expected.real.c, expected.real.d)
    assert imag == (expected.imag.a, expected.imag.b, expected.imag.c, expected.imag.d)


def test_rtl_files_contain_expected_modules_and_formulas() -> None:
    q12_mul = (ROOT / "rtl" / "q12_mul.sv").read_text(encoding="utf-8")
    complex_mul = (ROOT / "rtl" / "q12_complex_mul.sv").read_text(encoding="utf-8")

    assert "module q12_mul" in q12_mul
    assert "A = (a * e) + 2 * (b * f) + 3 * (c * g) + 6 * (d * h);" in q12_mul
    assert "B = (a * f) + (b * e) + 3 * (c * h) + 3 * (d * g);" in q12_mul
    assert "C = (a * g) + (c * e) + 2 * (b * h) + 2 * (d * f);" in q12_mul
    assert "D = (a * h) + (d * e) + (b * g) + (c * f);" in q12_mul

    assert "module q12_complex_mul" in complex_mul
    assert complex_mul.count("q12_mul #(.W(W))") == 4
    assert "out_ar = rr_a - ii_a;" in complex_mul
    assert "out_ai = ri_a + ir_a;" in complex_mul


def test_rtl_opcode_package_matches_python_binary_encoder() -> None:
    package = (ROOT / "rtl" / "exactq12_pkg.sv").read_text(encoding="utf-8")
    matches = re.findall(r"localparam logic \[7:0\] OP_(\w+)\s+=\s+8'h([0-9a-fA-F]{2});", package)
    rtl_opcodes = {name: int(value, 16) for name, value in matches}
    assert rtl_opcodes == OPCODES


def test_rtl_instruction_decoder_uses_export_byte_order() -> None:
    decoder = (ROOT / "rtl" / "instruction_decoder.sv").read_text(encoding="utf-8")
    assert "opcode = instr[23:16];" in decoder
    assert "arg0 = instr[15:8];" in decoder
    assert "arg1 = instr[7:0];" in decoder
    assert "OP_CNOT" in decoder
    assert "OP_SWAP" in decoder
    assert "valid = 1'b0;" in decoder


def rtl_den_reduce_once(a: int, b: int, c: int, d: int, E: int) -> tuple[int, int, int, int, int, bool]:
    if (a, b, c, d) == (0, 0, 0, 0):
        return 0, 0, 0, 0, 0, E != 0
    if E != 0 and all(value % 12 == 0 for value in (a, b, c, d)):
        return a // 12, b // 12, c // 12, d // 12, E - 1, True
    return a, b, c, d, E, False


def test_rtl_den_reduce_one_step_matches_q12_normalization() -> None:
    cases = [
        (12, 24, 36, 48, 3),
        (-24, 0, 12, -36, 2),
        (1, 12, 24, 36, 2),
        (0, 0, 0, 0, 5),
    ]

    for case in cases:
        a, b, c, d, E, _ = rtl_den_reduce_once(*case)
        assert Q12(*case) == Q12(a, b, c, d, E)


def test_rtl_den_reduce_file_contains_expected_logic() -> None:
    reducer = (ROOT / "rtl" / "q12_den_reduce.sv").read_text(encoding="utf-8")
    assert "module q12_den_reduce" in reducer
    assert "all_divisible_by_12" in reducer
    assert "a_out = a_in / 12;" in reducer
    assert "e_out = e_in - 1'b1;" in reducer
    assert "all_zero" in reducer


def test_rtl_bell_memh_matches_python_binary_export() -> None:
    instructions = parse_text("""
RESET 2
H q0
CNOT q0 q1
DUMP
PROB
""")
    payload = encode_instructions(instructions)
    expected_lines = [payload[index : index + 3].hex() for index in range(0, len(payload), 3)]
    memh_lines = (ROOT / "rtl" / "bell.memh").read_text(encoding="utf-8").splitlines()
    assert memh_lines == expected_lines


def test_rtl_program_rom_and_statevector_memory_interfaces() -> None:
    program_rom = (ROOT / "rtl" / "program_rom.sv").read_text(encoding="utf-8")
    statevector_mem = (ROOT / "rtl" / "statevector_mem.sv").read_text(encoding="utf-8")

    assert "module program_rom" in program_rom
    assert "parameter string INIT_FILE" in program_rom
    assert "$readmemh(INIT_FILE, rom);" in program_rom
    assert "output logic [23:0]" in program_rom

    assert "module statevector_mem" in statevector_mem
    assert "parameter int AMP_W = (8 * COEFF_W) + (2 * EXP_W)" in statevector_mem
    assert "always_ff @(posedge clk)" in statevector_mem
    assert "mem[addr] <= wdata;" in statevector_mem


def test_rtl_sequencer_decodes_and_halts_on_dump_or_invalid() -> None:
    sequencer = (ROOT / "rtl" / "exactq12_sequencer.sv").read_text(encoding="utf-8")

    assert "module exactq12_sequencer" in sequencer
    assert "instruction_decoder decoder" in sequencer
    assert "ST_IDLE" in sequencer
    assert "ST_FETCH" in sequencer
    assert "ST_DECODE" in sequencer
    assert "ST_HALT" in sequencer
    assert "if (!decoder_valid)" in sequencer
    assert "opcode == OP_DUMP" in sequencer
    assert "pc <= pc + 1'b1;" in sequencer
