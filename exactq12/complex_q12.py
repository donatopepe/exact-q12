from __future__ import annotations

from dataclasses import dataclass

from exactq12.q12 import Q12


@dataclass(frozen=True)
class CQ12:
    real: Q12 = Q12()
    imag: Q12 = Q12()

    @classmethod
    def zero(cls) -> CQ12:
        return cls(Q12.zero(), Q12.zero())

    @classmethod
    def one(cls) -> CQ12:
        return cls(Q12.one(), Q12.zero())

    @classmethod
    def minus_one(cls) -> CQ12:
        return cls(Q12.minus_one(), Q12.zero())

    @classmethod
    def i(cls) -> CQ12:
        return cls(Q12.zero(), Q12.one())

    def __add__(self, other: CQ12) -> CQ12:
        return CQ12(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other: CQ12) -> CQ12:
        return CQ12(self.real - other.real, self.imag - other.imag)

    def __neg__(self) -> CQ12:
        return CQ12(-self.real, -self.imag)

    def __mul__(self, other: CQ12) -> CQ12:
        return CQ12(
            self.real * other.real - self.imag * other.imag,
            self.real * other.imag + self.imag * other.real,
        )

    def conjugate(self) -> CQ12:
        return CQ12(self.real, -self.imag)

    def abs2(self) -> Q12:
        return self.real * self.real + self.imag * self.imag

    def is_zero(self) -> bool:
        return self.real.is_zero() and self.imag.is_zero()

    def __str__(self) -> str:
        if self.imag.is_zero():
            return str(self.real)
        if self.real.is_zero():
            return f"i({self.imag})"
        return f"{self.real} + i({self.imag})"
