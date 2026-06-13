from exactq12.complex_q12 import CQ12
from exactq12.gates import execute
from exactq12.parser import parse_text
from exactq12.q12 import Q12


def run_program(source: str):
    state, _ = execute(parse_text(source))
    return state.amplitudes


def phase_program(gate: str, count: int):
    return "\n".join(["RESET 1", "X q0", *([f"{gate} q0"] * count), "DUMP"])


def test_hadamard_twice_returns_zero_state() -> None:
    amplitudes = run_program("""
RESET 1
H q0
H q0
DUMP
""")
    assert amplitudes == [CQ12.one(), CQ12.zero()]


def test_t_eight_times_is_identity() -> None:
    assert run_program(phase_program("T", 8)) == [CQ12.zero(), CQ12.one()]


def test_s_four_times_is_identity() -> None:
    assert run_program(phase_program("S", 4)) == [CQ12.zero(), CQ12.one()]


def test_p30_twelve_times_is_identity() -> None:
    assert run_program(phase_program("P30", 12)) == [CQ12.zero(), CQ12.one()]


def test_p60_six_times_is_identity() -> None:
    assert run_program(phase_program("P60", 6)) == [CQ12.zero(), CQ12.one()]


def test_bell_state() -> None:
    amplitudes = run_program("""
RESET 2
H q0
CNOT q0 q1
DUMP
""")
    bell = CQ12(Q12.sqrt2_half(), Q12.zero())
    assert amplitudes == [bell, CQ12.zero(), CQ12.zero(), bell]


def test_parser_and_dump_output() -> None:
    _, output = execute(parse_text("""
RESET 1
H q0
DUMP
PROB
"""))
    assert output[0].startswith("|0> = ")
    assert output[2].startswith("P(|0>) = ")
