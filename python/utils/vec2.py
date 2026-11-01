import dataclasses
from typing import ClassVar, Self

from ._num import div, signum


@dataclasses.dataclass(frozen=True, slots=True, order=True)
class Vec2:
    x: int
    y: int

    ZERO: ClassVar["Vec2"]
    ONE: ClassVar["Vec2"]

    X: ClassVar["Vec2"]
    Y: ClassVar["Vec2"]
    NEG_X: ClassVar["Vec2"]
    NEG_Y: ClassVar["Vec2"]
    XY: ClassVar["Vec2"]
    NEG_XY: ClassVar["Vec2"]
    X_NEG_Y: ClassVar["Vec2"]
    NEG_X_NEG_Y: ClassVar["Vec2"]

    NEIGHBORS_4: ClassVar[tuple["Vec2", ...]]
    NEIGHBORS_8: ClassVar[tuple["Vec2", ...]]

    @classmethod
    def splat(cls, v: int) -> Self:
        return cls(v, v)

    def with_y(self, y: int) -> Self:
        return dataclasses.replace(self, y=y)

    def neighbors_4(self) -> tuple[Self, ...]:
        return tuple(self + offset for offset in self.NEIGHBORS_4)

    def neighbors_8(self) -> tuple[Self, ...]:
        return tuple(self + offset for offset in self.NEIGHBORS_8)

    def element_sum(self) -> int:
        return self.x + self.y

    def element_product(self) -> int:
        return self.x * self.y

    def abs(self) -> Self:
        return type(self)(abs(self.x), abs(self.y))

    def signum(self) -> Self:
        return type(self)(signum(self.x), signum(self.y))

    def min(self, rhs: Self) -> Self:
        return type(self)(min(self.x, rhs.x), min(self.y, rhs.y))

    def max(self, rhs: Self) -> Self:
        return type(self)(max(self.x, rhs.x), max(self.y, rhs.y))

    def rotate(self, rhs: Self) -> Self:
        return type(self)(
            self.x * rhs.x - self.y * rhs.y,
            self.y * rhs.x + self.x * rhs.y,
        )

    def __add__(self, rhs: Self) -> Self:
        return type(self)(self.x + rhs.x, self.y + rhs.y)

    def __sub__(self, rhs: Self) -> Self:
        return type(self)(self.x - rhs.x, self.y - rhs.y)

    def __mul__(self, rhs: Self | int) -> Self:
        if isinstance(rhs, Vec2):
            return type(self)(self.x * rhs.x, self.y * rhs.y)
        return type(self)(self.x * rhs, self.y * rhs)

    def __truediv__(self, rhs: Self | int) -> Self:
        if isinstance(rhs, Vec2):
            return type(self)(div(self.x, rhs.x), div(self.y, rhs.y))
        return type(self)(div(self.x, rhs), div(self.y, rhs))

    def __neg__(self) -> Self:
        return type(self)(-self.x, -self.y)


Vec2.ZERO = Vec2.splat(0)
Vec2.ONE = Vec2.splat(1)

Vec2.X = Vec2(1, 0)
Vec2.Y = Vec2(0, 1)
Vec2.NEG_X = Vec2(-1, 0)
Vec2.NEG_Y = Vec2(0, -1)
Vec2.XY = Vec2(1, 1)
Vec2.NEG_XY = Vec2(-1, 1)
Vec2.X_NEG_Y = Vec2(1, -1)
Vec2.NEG_X_NEG_Y = Vec2(-1, -1)

Vec2.NEIGHBORS_4 = (Vec2.X, Vec2.Y, Vec2.NEG_X, Vec2.NEG_Y)
Vec2.NEIGHBORS_8 = (
    *Vec2.NEIGHBORS_4,
    Vec2.XY,
    Vec2.NEG_XY,
    Vec2.X_NEG_Y,
    Vec2.NEG_X_NEG_Y,
)
