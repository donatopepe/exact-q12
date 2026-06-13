from __future__ import annotations

from dataclasses import dataclass
from random import Random

from exactq12.complex_q12 import CQ12
from exactq12.q12 import Q12


@dataclass
class Statevector:
    num_qubits: int
    amplitudes: list[CQ12]

    @classmethod
    def reset(cls, num_qubits: int) -> Statevector:
        if num_qubits < 1:
            raise ValueError("RESET requires at least one qubit")
        amplitudes = [CQ12.zero() for _ in range(2**num_qubits)]
        amplitudes[0] = CQ12.one()
        return cls(num_qubits, amplitudes)

    def _mask(self, qubit: int) -> int:
        if qubit < 0 or qubit >= self.num_qubits:
            raise ValueError(f"q{qubit} is out of range for {self.num_qubits} qubits")
        return 1 << (self.num_qubits - 1 - qubit)

    def apply_x(self, qubit: int) -> None:
        mask = self._mask(qubit)
        for index in range(len(self.amplitudes)):
            if index & mask == 0:
                other = index | mask
                self.amplitudes[index], self.amplitudes[other] = self.amplitudes[other], self.amplitudes[index]

    def apply_z(self, qubit: int) -> None:
        self.apply_phase(qubit, CQ12.minus_one())

    def apply_h(self, qubit: int) -> None:
        mask = self._mask(qubit)
        factor = CQ12(Q12.sqrt2_half(), Q12.zero())
        for index in range(len(self.amplitudes)):
            if index & mask == 0:
                other = index | mask
                in0 = self.amplitudes[index]
                in1 = self.amplitudes[other]
                self.amplitudes[index] = factor * (in0 + in1)
                self.amplitudes[other] = factor * (in0 - in1)

    def apply_phase(self, qubit: int, phase: CQ12) -> None:
        mask = self._mask(qubit)
        for index, amplitude in enumerate(self.amplitudes):
            if index & mask:
                self.amplitudes[index] = amplitude * phase

    def apply_s(self, qubit: int) -> None:
        self.apply_phase(qubit, CQ12.i())

    def apply_t(self, qubit: int) -> None:
        phase = CQ12(Q12.sqrt2_half(), Q12.sqrt2_half())
        self.apply_phase(qubit, phase)

    def apply_p30(self, qubit: int) -> None:
        phase = CQ12(Q12.sqrt3_half(), Q12.half())
        self.apply_phase(qubit, phase)

    def apply_p60(self, qubit: int) -> None:
        phase = CQ12(Q12.half(), Q12.sqrt3_half())
        self.apply_phase(qubit, phase)

    def apply_cnot(self, control: int, target: int) -> None:
        if control == target:
            raise ValueError("CNOT control and target must be different")
        control_mask = self._mask(control)
        target_mask = self._mask(target)
        for index in range(len(self.amplitudes)):
            if index & control_mask and index & target_mask == 0:
                other = index | target_mask
                self.amplitudes[index], self.amplitudes[other] = self.amplitudes[other], self.amplitudes[index]

    def apply_swap(self, q0: int, q1: int) -> None:
        if q0 == q1:
            return
        mask0 = self._mask(q0)
        mask1 = self._mask(q1)
        for index in range(len(self.amplitudes)):
            bit0 = bool(index & mask0)
            bit1 = bool(index & mask1)
            if bit0 != bit1 and not bit0:
                other = index ^ mask0 ^ mask1
                self.amplitudes[index], self.amplitudes[other] = self.amplitudes[other], self.amplitudes[index]

    def probabilities(self) -> list[Q12]:
        return [amplitude.abs2() for amplitude in self.amplitudes]

    def measure(self, qubit: int, rng: Random | None = None) -> int:
        rng = rng or Random()
        mask = self._mask(qubit)
        prob_one = sum(prob.to_float() for index, prob in enumerate(self.probabilities()) if index & mask)
        return 1 if rng.random() < prob_one else 0

    def basis_label(self, index: int) -> str:
        return format(index, f"0{self.num_qubits}b")

    def dump_lines(self) -> list[str]:
        return [f"|{self.basis_label(index)}> = {amp}" for index, amp in enumerate(self.amplitudes)]

    def probability_lines(self) -> list[str]:
        return [f"P(|{self.basis_label(index)}>) = {prob}" for index, prob in enumerate(self.probabilities())]
