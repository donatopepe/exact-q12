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


def rtl_q12_add(
    x: tuple[int, int, int, int, int],
    y: tuple[int, int, int, int, int],
    subtract: bool = False,
) -> tuple[int, int, int, int, int, bool]:
    a0, b0, c0, d0, e0 = x
    a1, b1, c1, d1, e1 = y
    sign = -1 if subtract else 1
    return (
        a0 + sign * a1,
        b0 + sign * b1,
        c0 + sign * c1,
        d0 + sign * d1,
        e0,
        e0 == e1,
    )


def rtl_q12_add_aligned(
    x: tuple[int, int, int, int, int],
    y: tuple[int, int, int, int, int],
    subtract: bool = False,
    max_shift: int = 4,
) -> tuple[int, int, int, int, int, bool]:
    a0, b0, c0, d0, e0 = x
    a1, b1, c1, d1, e1 = y
    e_out = max(e0, e1)
    diff0 = e_out - e0
    diff1 = e_out - e1
    scale0 = 12**diff0
    scale1 = 12**diff1
    sign = -1 if subtract else 1
    return (
        (a0 * scale0) + sign * (a1 * scale1),
        (b0 * scale0) + sign * (b1 * scale1),
        (c0 * scale0) + sign * (c1 * scale1),
        (d0 * scale0) + sign * (d1 * scale1),
        e_out,
        diff0 <= max_shift and diff1 <= max_shift,
    )


def rtl_q12_scale_sqrt_half(x: tuple[int, int, int, int, int]) -> tuple[int, int, int, int, int]:
    a, b, c, d, e = x
    return 12 * b, 6 * a, 12 * d, 6 * c, e + 1


def rtl_hadamard_pair(left: CQ12, right: CQ12) -> tuple[CQ12, CQ12, bool]:
    real_sum = rtl_q12_add_aligned(
        (left.real.a, left.real.b, left.real.c, left.real.d, left.real.E),
        (right.real.a, right.real.b, right.real.c, right.real.d, right.real.E),
    )
    imag_sum = rtl_q12_add_aligned(
        (left.imag.a, left.imag.b, left.imag.c, left.imag.d, left.imag.E),
        (right.imag.a, right.imag.b, right.imag.c, right.imag.d, right.imag.E),
    )
    real_diff = rtl_q12_add_aligned(
        (left.real.a, left.real.b, left.real.c, left.real.d, left.real.E),
        (right.real.a, right.real.b, right.real.c, right.real.d, right.real.E),
        subtract=True,
    )
    imag_diff = rtl_q12_add_aligned(
        (left.imag.a, left.imag.b, left.imag.c, left.imag.d, left.imag.E),
        (right.imag.a, right.imag.b, right.imag.c, right.imag.d, right.imag.E),
        subtract=True,
    )
    out0 = CQ12(Q12(*rtl_q12_scale_sqrt_half(real_sum[:-1])), Q12(*rtl_q12_scale_sqrt_half(imag_sum[:-1])))
    out1 = CQ12(Q12(*rtl_q12_scale_sqrt_half(real_diff[:-1])), Q12(*rtl_q12_scale_sqrt_half(imag_diff[:-1])))
    return out0, out1, real_sum[-1] and imag_sum[-1] and real_diff[-1] and imag_diff[-1]


def rtl_hadamard_address_pair(num_qubits: int, pair_index: int, target_qubit: int) -> tuple[int, int, bool]:
    if target_qubit < 0 or target_qubit >= num_qubits:
        return 0, 0, False
    target_bit = num_qubits - 1 - target_qubit
    lower_mask = (1 << target_bit) - 1
    addr0 = ((pair_index & ~lower_mask) << 1) | (pair_index & lower_mask)
    return addr0, addr0 | (1 << target_bit), True


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


def test_rtl_q12_add_same_exponent_matches_python_model() -> None:
    left = Q12(3, -2, 4, -5, 2)
    right = Q12(-1, 7, -3, 2, 2)

    add = rtl_q12_add((left.a, left.b, left.c, left.d, left.E), (right.a, right.b, right.c, right.d, right.E))
    sub = rtl_q12_add((left.a, left.b, left.c, left.d, left.E), (right.a, right.b, right.c, right.d, right.E), subtract=True)

    expected_add = left + right
    expected_sub = left - right
    assert add == (expected_add.a, expected_add.b, expected_add.c, expected_add.d, expected_add.E, True)
    assert sub == (expected_sub.a, expected_sub.b, expected_sub.c, expected_sub.d, expected_sub.E, True)


def test_rtl_q12_add_flags_mismatched_exponents_invalid() -> None:
    assert rtl_q12_add((1, 2, 3, 4, 1), (5, 6, 7, 8, 2))[-1] is False


def test_rtl_q12_add_aligned_matches_python_model_without_reduction() -> None:
    left = Q12(3, -2, 4, -5, 1)
    right = Q12(-1, 7, -3, 2, 3)

    add = rtl_q12_add_aligned((left.a, left.b, left.c, left.d, left.E), (right.a, right.b, right.c, right.d, right.E))
    sub = rtl_q12_add_aligned(
        (left.a, left.b, left.c, left.d, left.E),
        (right.a, right.b, right.c, right.d, right.E),
        subtract=True,
    )

    assert add == (431, -281, 573, -718, 3, True)
    assert sub == (433, -295, 579, -722, 3, True)
    assert Q12(*add[:-1]) == left + right
    assert Q12(*sub[:-1]) == left - right


def test_rtl_q12_add_aligned_flags_large_exponent_gap_invalid() -> None:
    assert rtl_q12_add_aligned((1, 2, 3, 4, 0), (5, 6, 7, 8, 5), max_shift=4)[-1] is False


def test_rtl_complex_add_same_exponent_matches_python_model() -> None:
    left = CQ12(Q12(3, -2, 4, -5, 2), Q12(1, 2, 3, 4, 2))
    right = CQ12(Q12(-1, 7, -3, 2, 2), Q12(5, -6, 7, -8, 2))
    expected = left + right

    real = rtl_q12_add(
        (left.real.a, left.real.b, left.real.c, left.real.d, left.real.E),
        (right.real.a, right.real.b, right.real.c, right.real.d, right.real.E),
    )
    imag = rtl_q12_add(
        (left.imag.a, left.imag.b, left.imag.c, left.imag.d, left.imag.E),
        (right.imag.a, right.imag.b, right.imag.c, right.imag.d, right.imag.E),
    )

    assert real == (expected.real.a, expected.real.b, expected.real.c, expected.real.d, expected.real.E, True)
    assert imag == (expected.imag.a, expected.imag.b, expected.imag.c, expected.imag.d, expected.imag.E, True)


def test_rtl_complex_add_aligned_matches_python_model() -> None:
    left = CQ12(Q12(3, -2, 4, -5, 1), Q12(1, 2, 3, 4, 2))
    right = CQ12(Q12(-1, 7, -3, 2, 3), Q12(5, -6, 7, -8, 1))

    real = rtl_q12_add_aligned(
        (left.real.a, left.real.b, left.real.c, left.real.d, left.real.E),
        (right.real.a, right.real.b, right.real.c, right.real.d, right.real.E),
    )
    imag = rtl_q12_add_aligned(
        (left.imag.a, left.imag.b, left.imag.c, left.imag.d, left.imag.E),
        (right.imag.a, right.imag.b, right.imag.c, right.imag.d, right.imag.E),
    )
    expected = left + right

    assert real == (431, -281, 573, -718, 3, True)
    assert imag == (61, -70, 87, -92, 2, True)
    assert Q12(*real[:-1]) == expected.real
    assert Q12(*imag[:-1]) == expected.imag


def test_rtl_q12_scale_sqrt_half_matches_python_model() -> None:
    cases = [Q12.one(), Q12(3, -2, 4, -5, 2)]
    factor = Q12.sqrt2_half()

    for value in cases:
        scaled = rtl_q12_scale_sqrt_half((value.a, value.b, value.c, value.d, value.E))
        assert Q12(*scaled) == value * factor


def test_rtl_hadamard_pair_matches_python_model() -> None:
    cases = [
        (CQ12.one(), CQ12.zero()),
        (CQ12(Q12(3, -2, 4, -5, 1), Q12(1, 2, 3, 4, 2)), CQ12(Q12(-1, 7, -3, 2, 3), Q12(5, -6, 7, -8, 1))),
    ]
    factor = CQ12(Q12.sqrt2_half(), Q12.zero())

    for left, right in cases:
        out0, out1, valid = rtl_hadamard_pair(left, right)
        assert valid is True
        assert out0 == (left + right) * factor
        assert out1 == (left - right) * factor


def test_rtl_hadamard_address_pair_matches_python_indexing() -> None:
    assert [rtl_hadamard_address_pair(3, pair, 0) for pair in range(4)] == [
        (0, 4, True),
        (1, 5, True),
        (2, 6, True),
        (3, 7, True),
    ]
    assert [rtl_hadamard_address_pair(3, pair, 1) for pair in range(4)] == [
        (0, 2, True),
        (1, 3, True),
        (4, 6, True),
        (5, 7, True),
    ]
    assert [rtl_hadamard_address_pair(3, pair, 2) for pair in range(4)] == [
        (0, 1, True),
        (2, 3, True),
        (4, 5, True),
        (6, 7, True),
    ]
    assert rtl_hadamard_address_pair(3, 0, 3) == (0, 0, False)


def test_rtl_files_contain_expected_modules_and_formulas() -> None:
    q12_mul = (ROOT / "rtl" / "q12_mul.sv").read_text(encoding="utf-8")
    complex_mul = (ROOT / "rtl" / "q12_complex_mul.sv").read_text(encoding="utf-8")
    q12_add = (ROOT / "rtl" / "q12_add.sv").read_text(encoding="utf-8")
    complex_add = (ROOT / "rtl" / "q12_complex_add.sv").read_text(encoding="utf-8")
    q12_add_aligned = (ROOT / "rtl" / "q12_add_aligned.sv").read_text(encoding="utf-8")
    complex_add_aligned = (ROOT / "rtl" / "q12_complex_add_aligned.sv").read_text(encoding="utf-8")
    q12_scale_sqrt_half = (ROOT / "rtl" / "q12_scale_sqrt_half.sv").read_text(encoding="utf-8")
    complex_scale_sqrt_half = (ROOT / "rtl" / "q12_complex_scale_sqrt_half.sv").read_text(encoding="utf-8")
    hadamard_pair = (ROOT / "rtl" / "hadamard_pair.sv").read_text(encoding="utf-8")
    hadamard_pair_packed = (ROOT / "rtl" / "hadamard_pair_packed.sv").read_text(encoding="utf-8")
    hadamard_address_pair = (ROOT / "rtl" / "hadamard_address_pair.sv").read_text(encoding="utf-8")
    hadamard_pair_step = (ROOT / "rtl" / "hadamard_pair_step.sv").read_text(encoding="utf-8")

    assert "module q12_mul" in q12_mul
    assert "A = (a * e) + 2 * (b * f) + 3 * (c * g) + 6 * (d * h);" in q12_mul
    assert "B = (a * f) + (b * e) + 3 * (c * h) + 3 * (d * g);" in q12_mul
    assert "C = (a * g) + (c * e) + 2 * (b * h) + 2 * (d * f);" in q12_mul
    assert "D = (a * h) + (d * e) + (b * g) + (c * f);" in q12_mul

    assert "module q12_complex_mul" in complex_mul
    assert complex_mul.count("q12_mul #(.W(W))") == 4
    assert "out_ar = rr_a - ii_a;" in complex_mul
    assert "out_ai = ri_a + ir_a;" in complex_mul

    assert "module q12_add" in q12_add
    assert "valid = (e0 == e1);" in q12_add
    assert "a_out = a0 - a1;" in q12_add
    assert "a_out = a0 + a1;" in q12_add

    assert "module q12_complex_add" in complex_add
    assert complex_add.count("q12_add #(.W(W), .EW(EW))") == 2
    assert "valid = real_valid && imag_valid;" in complex_add

    assert "module q12_add_aligned" in q12_add_aligned
    assert "parameter int MAX_SHIFT = 4" in q12_add_aligned
    assert "e_out = (e0 >= e1) ? e0 : e1;" in q12_add_aligned
    assert "result = result * 12;" in q12_add_aligned
    assert "a_out = (a0 * scale0) + (a1 * scale1);" in q12_add_aligned

    assert "module q12_complex_add_aligned" in complex_add_aligned
    assert complex_add_aligned.count("q12_add_aligned #(.W(W), .EW(EW), .OUT_W(OUT_W), .MAX_SHIFT(MAX_SHIFT))") == 2
    assert "valid = real_valid && imag_valid;" in complex_add_aligned

    assert "module q12_scale_sqrt_half" in q12_scale_sqrt_half
    assert "a_out = 12 * b_in;" in q12_scale_sqrt_half
    assert "b_out = 6 * a_in;" in q12_scale_sqrt_half
    assert "e_out = e_in + 1'b1;" in q12_scale_sqrt_half

    assert "module q12_complex_scale_sqrt_half" in complex_scale_sqrt_half
    assert complex_scale_sqrt_half.count("q12_scale_sqrt_half #(.W(W), .EW(EW), .OUT_W(OUT_W))") == 2

    assert "module hadamard_pair" in hadamard_pair
    assert hadamard_pair.count("q12_complex_add_aligned #(.W(W), .EW(EW), .OUT_W(ADD_W), .MAX_SHIFT(MAX_SHIFT))") == 2
    assert hadamard_pair.count("q12_complex_scale_sqrt_half #(.W(ADD_W), .EW(EW), .OUT_W(OUT_W))") == 2
    assert "valid = sum_valid && diff_valid;" in hadamard_pair

    assert "module hadamard_pair_packed" in hadamard_pair_packed
    assert "parameter int AMP_W = (8 * COEFF_W) + (2 * EXP_W)" in hadamard_pair_packed
    assert "parameter int OUT_AMP_W = (8 * OUT_COEFF_W) + (2 * EXP_W)" in hadamard_pair_packed
    assert "ar0 = amp_in0[AMP_W-1 -: COEFF_W];" in hadamard_pair_packed
    assert "ei0 = amp_in0[EXP_W-1:0];" in hadamard_pair_packed
    assert "amp_out0 = {ar_out0, br_out0, cr_out0, dr_out0, er_out0, ai_out0, bi_out0, ci_out0, di_out0, ei_out0};" in hadamard_pair_packed
    assert "hadamard_pair #(" in hadamard_pair_packed

    assert "module hadamard_address_pair" in hadamard_address_pair
    assert "target_bit = valid ? (ADDR_W - 1 - target_qubit) : 0;" in hadamard_address_pair
    assert "lower_bits = pair_index & lower_mask;" in hadamard_address_pair
    assert "upper_bits = (pair_index & ~lower_mask) << 1;" in hadamard_address_pair
    assert "addr1 = addr0 | target_mask;" in hadamard_address_pair

    assert "module hadamard_pair_step" in hadamard_pair_step
    assert "hadamard_address_pair #(.ADDR_W(ADDR_W), .QUBIT_W(QUBIT_W))" in hadamard_pair_step
    assert "hadamard_pair_packed #(" in hadamard_pair_step
    assert ".amp_in0(amp_rdata0)" in hadamard_pair_step
    assert ".amp_out0(amp_wdata0)" in hadamard_pair_step
    assert "valid = address_valid && datapath_valid;" in hadamard_pair_step


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
    statevector_pair_mem = (ROOT / "rtl" / "statevector_pair_mem.sv").read_text(encoding="utf-8")

    assert "module program_rom" in program_rom
    assert "parameter string INIT_FILE" in program_rom
    assert "$readmemh(INIT_FILE, rom);" in program_rom
    assert "output logic [23:0]" in program_rom

    assert "module statevector_mem" in statevector_mem
    assert "parameter int AMP_W = (8 * COEFF_W) + (2 * EXP_W)" in statevector_mem
    assert "always_ff @(posedge clk)" in statevector_mem
    assert "mem[addr] <= wdata;" in statevector_mem

    assert "module statevector_pair_mem" in statevector_pair_mem
    assert "output logic [AMP_W-1:0]" in statevector_pair_mem
    assert "mem[addr0] <= wdata0;" in statevector_pair_mem
    assert "mem[addr1] <= wdata1;" in statevector_pair_mem
    assert statevector_pair_mem.index("mem[addr0] <= wdata0;") < statevector_pair_mem.index("mem[addr1] <= wdata1;")
    assert "rdata0 <= mem[addr0];" in statevector_pair_mem
    assert "rdata1 <= mem[addr1];" in statevector_pair_mem


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


def test_rtl_top_wires_rom_sequencer_and_state_memory() -> None:
    top = (ROOT / "rtl" / "exactq12_top.sv").read_text(encoding="utf-8")

    assert "module exactq12_top" in top
    assert "parameter string PROGRAM_INIT_FILE = \"bell.memh\"" in top
    assert "program_rom #(" in top
    assert "exactq12_sequencer #(" in top
    assert "statevector_mem #(" in top
    assert ".addr(pc)" in top
    assert ".instr(instr)" in top
    assert ".state_rdata" not in top
    assert ".rdata(state_rdata)" in top
    assert ".we(1'b0)" in top


def test_rtl_top_notes_document_current_limitations() -> None:
    notes = (ROOT / "rtl" / "README_TOP.md").read_text(encoding="utf-8")

    assert "simulation-oriented integration shell" in notes
    assert "gate execution is not connected" in notes
    assert "not a Tang Nano 20K top-level" in notes


def test_rtl_testbenches_are_self_checking() -> None:
    testbenches = [
        ROOT / "rtl" / "tb" / "q12_mul_tb.sv",
        ROOT / "rtl" / "tb" / "q12_add_tb.sv",
        ROOT / "rtl" / "tb" / "q12_add_aligned_tb.sv",
        ROOT / "rtl" / "tb" / "q12_complex_add_tb.sv",
        ROOT / "rtl" / "tb" / "q12_complex_add_aligned_tb.sv",
        ROOT / "rtl" / "tb" / "q12_scale_sqrt_half_tb.sv",
        ROOT / "rtl" / "tb" / "hadamard_pair_tb.sv",
        ROOT / "rtl" / "tb" / "hadamard_pair_packed_tb.sv",
        ROOT / "rtl" / "tb" / "hadamard_address_pair_tb.sv",
        ROOT / "rtl" / "tb" / "hadamard_pair_step_tb.sv",
        ROOT / "rtl" / "tb" / "statevector_pair_mem_tb.sv",
        ROOT / "rtl" / "tb" / "instruction_decoder_tb.sv",
        ROOT / "rtl" / "tb" / "exactq12_sequencer_tb.sv",
    ]
    for testbench in testbenches:
        text = testbench.read_text(encoding="utf-8")
        assert "$fatal" in text
        assert "$finish" in text
        assert "passed" in text


def test_q12_mul_testbench_expected_values_match_model() -> None:
    testbench = (ROOT / "rtl" / "tb" / "q12_mul_tb.sv").read_text(encoding="utf-8")

    first = rtl_q12_mul((1, 2, 3, 4), (5, 6, 7, 8))
    signed = rtl_q12_mul((-3, 0, 2, -1), (4, -5, 0, 6))

    assert first == (284, 172, 102, 60)
    assert signed == (-48, 51, 18, -32)
    assert "A !== 68'sd284" in testbench
    assert "B !== 68'sd172" in testbench
    assert "C !== 68'sd102" in testbench
    assert "D !== 68'sd60" in testbench
    assert "A !== -68'sd48" in testbench
    assert "B !== 68'sd51" in testbench
    assert "C !== 68'sd18" in testbench
    assert "D !== -68'sd32" in testbench


def test_rtl_makefile_runs_optional_iverilog_sims() -> None:
    makefile = (ROOT / "rtl" / "Makefile").read_text(encoding="utf-8")

    assert "IVERILOG ?= iverilog" in makefile
    assert "VVP ?= vvp" in makefile
    assert "q12_mul_tb" in makefile
    assert "q12_add_tb" in makefile
    assert "q12_add_aligned_tb" in makefile
    assert "q12_complex_add_tb" in makefile
    assert "q12_complex_add_aligned_tb" in makefile
    assert "q12_scale_sqrt_half_tb" in makefile
    assert "hadamard_pair_tb" in makefile
    assert "hadamard_pair_packed_tb" in makefile
    assert "hadamard_address_pair_tb" in makefile
    assert "hadamard_pair_step_tb" in makefile
    assert "statevector_pair_mem_tb" in makefile
    assert "instruction_decoder_tb" in makefile
    assert "exactq12_sequencer_tb" in makefile
    assert "-g2012" in makefile


def test_rtl_sim_workflow_runs_iverilog_make_target() -> None:
    workflow = (ROOT / ".github" / "workflows" / "rtl-sim.yml").read_text(encoding="utf-8")

    assert "name: rtl-sim" in workflow
    assert "sudo apt-get install -y iverilog" in workflow
    assert "make -C rtl sim" in workflow
    assert "workflow_dispatch" in workflow
