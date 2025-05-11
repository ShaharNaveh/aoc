use std::ops::{Add, AddAssign, Neg};

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct IVec2 {
    pub x: i32,
    pub y: i32,
}

impl IVec2 {
    pub const ZERO: Self = Self { x: 0, y: 0 };

    #[inline]
    #[must_use]
    pub const fn new(x: i32, y: i32) -> Self {
        Self { x, y }
    }

    #[inline]
    #[must_use]
    pub fn neighbors_4(&self) -> [Self; 4] {
        Offset::NEIGHBORS_4.map(|offset| *self + offset)
    }

    #[inline]
    #[must_use]
    pub fn element_sum(self) -> i32 {
        self.x + self.y
    }

    #[inline]
    #[must_use]
    pub fn abs(self) -> Self {
        Self {
            x: self.x.abs(),
            y: self.y.abs(),
        }
    }

    #[inline]
    #[must_use]
    pub fn hex_manhattan_distance(self) -> u32 {
        ((self.abs().element_sum() + self.element_sum().abs()) / 2) as u32
    }
}

#[derive(Clone, Copy, Debug, PartialEq)]
pub enum Offset {
    East,
    North,
    South,
    West,
}

impl Offset {
    pub const NEIGHBORS_4: [Self; 4] = Self::neighbors_4();

    #[inline]
    #[must_use]
    pub const fn value(&self) -> IVec2 {
        match self {
            Self::East => IVec2 { x: 1, y: 0 },
            Self::North => IVec2 { x: 0, y: -1 },
            Self::South => IVec2 { x: 0, y: 1 },
            Self::West => IVec2 { x: -1, y: 0 },
        }
    }

    #[inline]
    #[must_use]
    pub const fn neighbors_4() -> [Self; 4] {
        [Self::East, Self::North, Self::South, Self::West]
    }
}

/// This hex offset is like:
///     2
/// 7       3
///     1
/// 6       4
///     5
///
/// Which is like:
///
/// 72
/// 613
///  54
///
/// The other possible hex offsets layout is:
///   2   3
///
/// 7   1   4
///
///   6   5
///     
/// That can be represented like:
///
/// 23
/// 714
///  65
#[derive(Clone, Copy, Debug)]
pub enum HexOffset {
    North,
    NorthEast,
    NorthWest,
    South,
    SouthEast,
    SouthWest,
}

impl HexOffset {
    #[inline]
    #[must_use]
    pub const fn value(&self) -> IVec2 {
        match self {
            Self::North => IVec2 { x: 0, y: 1 },
            Self::NorthEast => IVec2 { x: 1, y: 0 },
            Self::NorthWest => IVec2 { x: -1, y: 1 },
            Self::South => IVec2 { x: 0, y: -1 },
            Self::SouthEast => IVec2 { x: 1, y: -1 },
            Self::SouthWest => IVec2 { x: -1, y: 0 },
        }
    }
}

impl From<&str> for HexOffset {
    #[inline]
    #[must_use]
    fn from(raw: &str) -> Self {
        match raw {
            "n" => Self::North,
            "ne" => Self::NorthEast,
            "nw" => Self::NorthWest,
            "s" => Self::South,
            "se" => Self::SouthEast,
            "sw" => Self::SouthWest,
            _ => unreachable!(),
        }
    }
}

impl Add<IVec2> for IVec2 {
    type Output = Self;

    #[inline]
    #[must_use]
    fn add(self, rhs: Self) -> Self {
        Self {
            x: self.x.add(rhs.x),
            y: self.y.add(rhs.y),
        }
    }
}

impl Add<Offset> for IVec2 {
    type Output = Self;

    #[inline]
    #[must_use]
    fn add(self, rhs: Offset) -> Self {
        self + rhs.value()
    }
}

impl Neg for IVec2 {
    type Output = Self;
    #[inline]
    fn neg(self) -> Self {
        Self {
            x: self.x.neg(),
            y: self.y.neg(),
        }
    }
}

impl Neg for Offset {
    type Output = Self;
    #[inline]
    fn neg(self) -> Self {
        match self {
            Self::South => Self::North,
            Self::North => Self::South,
            Self::East => Self::West,
            Self::West => Self::East,
        }
    }
}

impl AddAssign<IVec2> for IVec2 {
    #[inline]
    #[must_use]
    fn add_assign(&mut self, rhs: Self) {
        self.x.add_assign(rhs.x);
        self.y.add_assign(rhs.y);
    }
}

impl AddAssign<Offset> for IVec2 {
    #[inline]
    #[must_use]
    fn add_assign(&mut self, rhs: Offset) {
        *self += rhs.value()
    }
}

impl Add<HexOffset> for IVec2 {
    type Output = Self;

    #[inline]
    #[must_use]
    fn add(self, rhs: HexOffset) -> Self {
        self + rhs.value()
    }
}
