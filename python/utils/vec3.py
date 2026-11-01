import dataclasses
from typing import ClassVar, Self

from ._num import div


@dataclasses.dataclass(frozen=True, slots=True, order=True)
class Vec3:
    x: int
    y: int
    z: int

    ZERO: ClassVar["Vec3"]

    @classmethod
    def splat(cls, v: int) -> Self:
        return cls(v, v, v)

    @classmethod
    def from_str(cls, raw: str) -> Self:
        x, y, z = map(int, raw.strip().split(","))
        return cls(x, y, z)

    def element_sum(self) -> int:
        return self.x + self.y + self.z

    def abs(self) -> Self:
        return type(self)(abs(self.x), abs(self.y), abs(self.z))

    def dot(self, rhs: Self) -> int:
        return self.x * rhs.x + self.y * rhs.y + self.z * rhs.z

    def length_squared(self) -> int:
        return self.dot(self)

    def distance_squared(self, rhs: Self) -> int:
        return (self - rhs).length_squared()

    def __add__(self, rhs: Self) -> Self:
        return type(self)(self.x + rhs.x, self.y + rhs.y, self.z + rhs.z)

    def __sub__(self, rhs: Self) -> Self:
        return type(self)(self.x - rhs.x, self.y - rhs.y, self.z - rhs.z)

    def __mul__(self, rhs: int) -> Self:
        return type(self)(self.x * rhs, self.y * rhs, self.z * rhs)

    def __truediv__(self, rhs: int) -> Self:
        return type(self)(div(self.x, rhs), div(self.y, rhs), div(self.z, rhs))

    def __neg__(self) -> Self:
        return type(self)(-self.x, -self.y, -self.z)


Vec3.ZERO = Vec3.splat(0)
