from pathlib import Path

from exactq12.complex_q12 import CQ12
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
