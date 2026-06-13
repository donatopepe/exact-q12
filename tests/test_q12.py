from exactq12.q12 import Q12


def test_reduces_denominator_by_12() -> None:
    assert Q12(12, 24, 36, 48, 2) == Q12(1, 2, 3, 4, 1)


def test_add_aligns_denominators() -> None:
    assert Q12.half() + Q12.half() == Q12.one()


def test_multiplication_formula() -> None:
    x = Q12(1, 2, 3, 4, 0)
    y = Q12(5, 6, 7, 8, 0)
    assert x * y == Q12(225, 106, 101, 52, 0)


def test_exact_roots_square_to_expected_rationals() -> None:
    assert Q12.sqrt2_half() * Q12.sqrt2_half() == Q12.half()
    assert Q12.sqrt3_half() * Q12.sqrt3_half() == Q12(9, 0, 0, 0, 1)
