import dataclasses
from typing import Self


@dataclasses.dataclass(frozen=True, slots=True, order=True)
class Vec2:
    x: int
    y: int

    def __iter__(self):
        yield self.x
        yield self.y

    def __add__(self, other: Self) -> Self:
        return type(self)(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self) -> Self:
        return type(self)(self.x - other.x, self.y - other.y)

    def __mul__(self, k: int) -> Self:
        return type(self)(self.x * k, self.y * k)

    __rmul__ = __mul__

    def __floordiv__(self, k: int) -> Self:
        return type(self)(self.x // k, self.y // k)

    def __neg__(self) -> Self:
        return type(self)(-self.x, -self.y)

    def __abs__(self) -> Self:
        return type(self)(abs(self.x), abs(self.y))

    def manhattan(self, other: Self | None = None) -> int:
        d = self - other if other is not None else self
        return abs(d.x) + abs(d.y)

    def neighbors(self, *, diagonals: bool = False) -> list[Self]:
        offsets = DIAGONAL_OFFSETS if diagonals else ORTHOGONAL_OFFSETS
        return [self + offset for offset in offsets]


ORTHOGONAL_OFFSETS = (Vec2(1, 0), Vec2(0, 1), Vec2(-1, 0), Vec2(0, -1))
DIAGONAL_OFFSETS = (
    *ORTHOGONAL_OFFSETS,
    Vec2(1, 1),
    Vec2(-1, 1),
    Vec2(1, -1),
    Vec2(-1, -1),
)


@dataclasses.dataclass(frozen=True, slots=True, order=True)
class Vec3:
    x: int
    y: int
    z: int

    @classmethod
    def from_str(cls, s: str, sep: str = ",") -> Self:
        x, y, z = map(int, s.split(sep))
        return cls(x, y, z)

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __add__(self, other: Self) -> Self:
        return type(self)(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Self) -> Self:
        return type(self)(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, k: int) -> Self:
        return type(self)(self.x * k, self.y * k, self.z * k)

    __rmul__ = __mul__

    def __floordiv__(self, k: int) -> Self:
        return type(self)(self.x // k, self.y // k, self.z // k)

    def __neg__(self) -> Self:
        return type(self)(-self.x, -self.y, -self.z)

    def __abs__(self) -> Self:
        return type(self)(abs(self.x), abs(self.y), abs(self.z))

    def dot(self, other: Self) -> int:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def manhattan(self, other: Self | None = None) -> int:
        d = self - other if other is not None else self
        return abs(d.x) + abs(d.y) + abs(d.z)
