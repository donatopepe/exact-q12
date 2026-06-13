import pytest

from exactq12.complex_q12 import CQ12
from exactq12.q12 import Q12
from exactq12.rtl_pack import cq12_hex, pack_cq12, pack_q12, unpack_cq12, unpack_q12


def test_pack_q12_roundtrip() -> None:
    values = [
        Q12.zero(),
        Q12.one(),
        Q12(-1, 2, -3, 4, 5),
        Q12.sqrt2_half(),
        Q12.sqrt3_half(),
    ]
    for value in values:
        assert unpack_q12(pack_q12(value)) == value


def test_pack_cq12_roundtrip() -> None:
    value = CQ12(Q12(-1, 2, -3, 4, 5), Q12(6, -7, 8, -9, 2))
    assert unpack_cq12(pack_cq12(value)) == value


def test_pack_q12_uses_twos_complement_order() -> None:
    value = Q12(-1, 2, -3, 4, 5)
    packed = pack_q12(value, coeff_width=8, exp_width=4)
    assert packed == int("ff02fd045", 16)
    assert unpack_q12(packed, coeff_width=8, exp_width=4) == value


def test_cq12_hex_width() -> None:
    value = CQ12(Q12.one(), Q12.zero())
    assert len(cq12_hex(value)) == 68


def test_pack_rejects_out_of_range_fields() -> None:
    with pytest.raises(ValueError, match="signed 8-bit"):
        pack_q12(Q12(128, 0, 0, 0, 0), coeff_width=8, exp_width=4)
    with pytest.raises(ValueError, match="exponent"):
        pack_q12(Q12(1, 0, 0, 0, 16), coeff_width=8, exp_width=4)
