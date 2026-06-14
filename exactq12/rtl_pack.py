from __future__ import annotations

from exactq12.complex_q12 import CQ12
from exactq12.q12 import Q12
from exactq12.statevector import Statevector


def _pack_signed(value: int, width: int) -> int:
    minimum = -(1 << (width - 1))
    maximum = (1 << (width - 1)) - 1
    if not minimum <= value <= maximum:
        raise ValueError(f"value {value} does not fit in signed {width}-bit field")
    return value & ((1 << width) - 1)


def _unpack_signed(value: int, width: int) -> int:
    sign_bit = 1 << (width - 1)
    mask = (1 << width) - 1
    value &= mask
    return value - (1 << width) if value & sign_bit else value


def pack_q12(value: Q12, coeff_width: int = 32, exp_width: int = 8) -> int:
    if not 0 <= value.E < (1 << exp_width):
        raise ValueError(f"exponent {value.E} does not fit in unsigned {exp_width}-bit field")

    packed = 0
    for coefficient in (value.a, value.b, value.c, value.d):
        packed = (packed << coeff_width) | _pack_signed(coefficient, coeff_width)
    return (packed << exp_width) | value.E


def unpack_q12(payload: int, coeff_width: int = 32, exp_width: int = 8) -> Q12:
    exponent_mask = (1 << exp_width) - 1
    exponent = payload & exponent_mask
    payload >>= exp_width

    coefficients: list[int] = []
    coefficient_mask = (1 << coeff_width) - 1
    for _ in range(4):
        coefficients.append(_unpack_signed(payload & coefficient_mask, coeff_width))
        payload >>= coeff_width
    a, b, c, d = reversed(coefficients)
    return Q12(a, b, c, d, exponent)


def pack_cq12(value: CQ12, coeff_width: int = 32, exp_width: int = 8) -> int:
    q12_width = (4 * coeff_width) + exp_width
    return (pack_q12(value.real, coeff_width, exp_width) << q12_width) | pack_q12(value.imag, coeff_width, exp_width)


def unpack_cq12(payload: int, coeff_width: int = 32, exp_width: int = 8) -> CQ12:
    q12_width = (4 * coeff_width) + exp_width
    q12_mask = (1 << q12_width) - 1
    imag = unpack_q12(payload & q12_mask, coeff_width, exp_width)
    real = unpack_q12(payload >> q12_width, coeff_width, exp_width)
    return CQ12(real, imag)


def cq12_hex(value: CQ12, coeff_width: int = 32, exp_width: int = 8) -> str:
    total_width = 2 * ((4 * coeff_width) + exp_width)
    hex_digits = (total_width + 3) // 4
    return f"{pack_cq12(value, coeff_width, exp_width):0{hex_digits}x}"


def statevector_memh(state: Statevector, coeff_width: int = 32, exp_width: int = 8) -> str:
    return "\n".join(cq12_hex(amplitude, coeff_width, exp_width) for amplitude in state.amplitudes) + "\n"


def reset_statevector_memh(num_qubits: int, coeff_width: int = 32, exp_width: int = 8) -> str:
    return statevector_memh(Statevector.reset(num_qubits), coeff_width, exp_width)
