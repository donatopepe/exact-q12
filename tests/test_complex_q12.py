from exactq12.complex_q12 import CQ12
from exactq12.q12 import Q12


def test_i_squared_is_minus_one() -> None:
    assert CQ12.i() * CQ12.i() == CQ12.minus_one()


def test_abs2_of_t_phase_is_one() -> None:
    phase = CQ12(Q12.sqrt2_half(), Q12.sqrt2_half())
    assert phase.abs2() == Q12.one()


def test_abs2_of_p30_phase_is_one() -> None:
    phase = CQ12(Q12.sqrt3_half(), Q12.half())
    assert phase.abs2() == Q12.one()
