use std::ops::{Add, AddAssign, Div, Neg, Sub};

#[derive(Clone, Copy, Debug, Default, Eq, Hash, PartialEq)]
pub struct IVec2 {
    pub x: i32,
    pub y: i32,
}

impl IVec2 {
    pub const ZERO: Self = Self::splat(0);
    //pub const MIN: Self = Self::splat(i32::MIN);
    //pub const MAX: Self = Self::splat(i32::MAX);

    #[inline]
    #[must_use]
    pub const fn new(x: i32, y: i32) -> Self {
        Self { x, y }
    }

    #[inline]
    #[must_use]
    pub const fn splat(v: i32) -> Self {
        Self { x: v, y: v }
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

    /*
    #[inline]
    #[must_use]
    pub fn min(self, rhs: Self) -> Self {
        Self {
            x: self.x.min(rhs.x),
            y: self.y.min(rhs.y),
        }
    }
    */

    #[inline]
    #[must_use]
    pub fn max(self, rhs: Self) -> Self {
        Self {
            x: self.x.max(rhs.x),
            y: self.y.max(rhs.y),
        }
    }

    #[inline]
    #[must_use]
    pub fn rotate<T>(self, rhs: T) -> Self
    where
        T: Into<Self>,
    {
        let v = rhs.into();
        Self {
            x: self.x * v.x - self.y * v.y,
            y: self.y * v.x + self.x * v.y,
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
    pub const NEIGHBORS_4: [Self; 4] = [Self::East, Self::North, Self::South, Self::West];
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

impl From<&str> for HexOffset {
    #[inline]
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

impl From<HexOffset> for IVec2 {
    #[inline]
    fn from(hex_offset: HexOffset) -> Self {
        match hex_offset {
            HexOffset::North => IVec2 { x: 0, y: 1 },
            HexOffset::NorthEast => IVec2 { x: 1, y: 0 },
            HexOffset::NorthWest => IVec2 { x: -1, y: 1 },
            HexOffset::South => IVec2 { x: 0, y: -1 },
            HexOffset::SouthEast => IVec2 { x: 1, y: -1 },
            HexOffset::SouthWest => IVec2 { x: -1, y: 0 },
        }
    }
}

impl From<Offset> for IVec2 {
    #[inline]
    fn from(offset: Offset) -> Self {
        match offset {
            Offset::East => IVec2 { x: 1, y: 0 },
            Offset::North => IVec2 { x: 0, y: -1 },
            Offset::South => IVec2 { x: 0, y: 1 },
            Offset::West => IVec2 { x: -1, y: 0 },
        }
    }
}

impl Div<IVec2> for IVec2 {
    type Output = Self;

    #[inline]
    fn div(self, rhs: Self) -> Self {
        Self {
            x: self.x.div(rhs.x),
            y: self.y.div(rhs.y),
        }
    }
}

impl Div<i32> for IVec2 {
    type Output = Self;

    #[inline]
    fn div(self, rhs: i32) -> Self {
        Self {
            x: self.x.div(rhs),
            y: self.y.div(rhs),
        }
    }
}

impl Add<IVec2> for IVec2 {
    type Output = Self;

    #[inline]
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
    fn add(self, rhs: Offset) -> Self {
        self + IVec2::from(rhs)
    }
}
impl Sub<IVec2> for IVec2 {
    type Output = Self;

    #[inline]
    fn sub(self, rhs: Self) -> Self {
        Self {
            x: self.x.sub(rhs.x),
            y: self.y.sub(rhs.y),
        }
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
    fn add_assign(&mut self, rhs: Self) {
        self.x.add_assign(rhs.x);
        self.y.add_assign(rhs.y);
    }
}

impl AddAssign<Offset> for IVec2 {
    #[inline]
    fn add_assign(&mut self, rhs: Offset) {
        *self += IVec2::from(rhs)
    }
}

impl Add<HexOffset> for IVec2 {
    type Output = Self;

    #[inline]
    fn add(self, rhs: HexOffset) -> Self {
        self + IVec2::from(rhs)
    }
}
