from __future__ import annotations

from dataclasses import dataclass
from math import sqrt


@dataclass(frozen=True)
class Q12:
    """Exact element of Q(sqrt(2), sqrt(3)) with denominator 12**E."""

    a: int = 0
    b: int = 0
    c: int = 0
    d: int = 0
    E: int = 0

    def __post_init__(self) -> None:
        if self.E < 0:
            raise ValueError("Q12 exponent E must be non-negative")

        a, b, c, d, E = self.a, self.b, self.c, self.d, self.E
        if a == b == c == d == 0:
            E = 0
        else:
            while E > 0 and all(x % 12 == 0 for x in (a, b, c, d)):
                a //= 12
                b //= 12
                c //= 12
                d //= 12
                E -= 1

        object.__setattr__(self, "a", a)
        object.__setattr__(self, "b", b)
        object.__setattr__(self, "c", c)
        object.__setattr__(self, "d", d)
        object.__setattr__(self, "E", E)

    @classmethod
    def zero(cls) -> Q12:
        return cls()

    @classmethod
    def one(cls) -> Q12:
        return cls(1, 0, 0, 0, 0)

    @classmethod
    def minus_one(cls) -> Q12:
        return cls(-1, 0, 0, 0, 0)

    @classmethod
    def half(cls) -> Q12:
        return cls(6, 0, 0, 0, 1)

    @classmethod
    def sqrt2_half(cls) -> Q12:
        return cls(0, 6, 0, 0, 1)

    @classmethod
    def sqrt3_half(cls) -> Q12:
        return cls(0, 0, 6, 0, 1)

    def _scaled_to(self, exponent: int) -> tuple[int, int, int, int]:
        scale = 12 ** (exponent - self.E)
        return self.a * scale, self.b * scale, self.c * scale, self.d * scale

    def __add__(self, other: Q12) -> Q12:
        exponent = max(self.E, other.E)
        a1, b1, c1, d1 = self._scaled_to(exponent)
        a2, b2, c2, d2 = other._scaled_to(exponent)
        return Q12(a1 + a2, b1 + b2, c1 + c2, d1 + d2, exponent)

    def __sub__(self, other: Q12) -> Q12:
        return self + (-other)

    def __neg__(self) -> Q12:
        return Q12(-self.a, -self.b, -self.c, -self.d, self.E)

    def __mul__(self, other: Q12) -> Q12:
        a, b, c, d = self.a, self.b, self.c, self.d
        e, f, g, h = other.a, other.b, other.c, other.d
        return Q12(
            a * e + 2 * b * f + 3 * c * g + 6 * d * h,
            a * f + b * e + 3 * c * h + 3 * d * g,
            a * g + c * e + 2 * b * h + 2 * d * f,
            a * h + d * e + b * g + c * f,
            self.E + other.E,
        )

    def is_zero(self) -> bool:
        return self.a == self.b == self.c == self.d == 0

    def to_float(self) -> float:
        return (self.a + self.b * sqrt(2) + self.c * sqrt(3) + self.d * sqrt(6)) / (12**self.E)

    def __str__(self) -> str:
        if self.is_zero():
            return "0"
        numerator = f"({self.a} + {self.b}√2 + {self.c}√3 + {self.d}√6)"
        if self.E == 0:
            return numerator
        return f"{numerator} / 12^{self.E}" if self.E != 1 else f"{numerator} / 12"
