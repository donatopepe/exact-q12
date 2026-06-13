from exactq12.complex_q12 import CQ12
from exactq12.q12 import Q12
from exactq12.statevector import Statevector


def assert_normalized(state: Statevector) -> None:
    total = Q12.zero()
    for probability in state.probabilities():
        total += probability
    assert total == Q12.one()


def test_x_flips_single_qubit() -> None:
    state = Statevector.reset(1)
    state.apply_x(0)
    assert state.amplitudes == [CQ12.zero(), CQ12.one()]
    assert_normalized(state)


def test_z_negates_one_state() -> None:
    state = Statevector.reset(1)
    state.apply_x(0)
    state.apply_z(0)
    assert state.amplitudes == [CQ12.zero(), CQ12.minus_one()]
    assert_normalized(state)


def test_h_on_zero_creates_exact_superposition() -> None:
    state = Statevector.reset(1)
    state.apply_h(0)
    expected = CQ12(Q12.sqrt2_half(), Q12.zero())
    assert state.amplitudes == [expected, expected]
    assert state.probabilities() == [Q12.half(), Q12.half()]
    assert_normalized(state)


def test_swap_exchanges_qubits() -> None:
    state = Statevector.reset(2)
    state.apply_x(0)
    state.apply_swap(0, 1)
    assert state.amplitudes == [CQ12.zero(), CQ12.one(), CQ12.zero(), CQ12.zero()]
    assert_normalized(state)


def test_supported_gates_preserve_normalization() -> None:
    state = Statevector.reset(3)
    operations = [
        lambda: state.apply_h(0),
        lambda: state.apply_h(1),
        lambda: state.apply_t(0),
        lambda: state.apply_s(1),
        lambda: state.apply_p30(2),
        lambda: state.apply_p60(0),
        lambda: state.apply_cnot(0, 2),
        lambda: state.apply_swap(1, 2),
        lambda: state.apply_z(2),
        lambda: state.apply_x(1),
    ]
    for operation in operations:
        operation()
        assert_normalized(state)
