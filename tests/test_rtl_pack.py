import pytest

from exactq12.complex_q12 import CQ12
from exactq12.q12 import Q12
from exactq12.rtl_pack import (
    cq12_hex,
    pack_cq12,
    pack_q12,
    parse_cq12_hex,
    parse_statevector_memh,
    reset_statevector_memh,
    statevector_memh,
    unpack_cq12,
    unpack_q12,
)
from exactq12.statevector import Statevector


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


def test_statevector_memh_reset_layout() -> None:
    text = reset_statevector_memh(2)
    lines = text.splitlines()
    assert len(lines) == 4
    assert lines[0] == cq12_hex(CQ12.one())
    assert lines[1:] == [cq12_hex(CQ12.zero()), cq12_hex(CQ12.zero()), cq12_hex(CQ12.zero())]


def test_statevector_memh_uses_current_amplitudes() -> None:
    state = Statevector.reset(1)
    state.apply_h(0)
    assert statevector_memh(state).splitlines() == [cq12_hex(state.amplitudes[0]), cq12_hex(state.amplitudes[1])]


def test_parse_cq12_hex_roundtrip() -> None:
    value = CQ12(Q12.sqrt2_half(), Q12.sqrt3_half())
    assert parse_cq12_hex(cq12_hex(value)) == value


def test_parse_statevector_memh_roundtrip() -> None:
    state = Statevector.reset(2)
    state.apply_h(0)
    parsed = parse_statevector_memh(statevector_memh(state))
    assert parsed.num_qubits == 2
    assert parsed.amplitudes == state.amplitudes


def test_parse_statevector_memh_rejects_bad_shape() -> None:
    with pytest.raises(ValueError, match="empty"):
        parse_statevector_memh("")
    with pytest.raises(ValueError, match="power of two"):
        parse_statevector_memh("0\n0\n0\n")
    with pytest.raises(ValueError, match="hex digits"):
        parse_statevector_memh("0\n")
