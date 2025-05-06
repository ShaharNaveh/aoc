use std::ops::{
    Add,
    //   AddAssign
};

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct IVec2 {
    pub x: i32,
    pub y: i32,
}

impl IVec2 {
    pub const ZERO: Self = Self { x: 0, y: 0 };

    pub fn element_sum(self) -> i32 {
        self.x + self.y
    }

    pub fn abs(self) -> Self {
        Self {
            x: self.x.abs(),
            y: self.y.abs(),
        }
    }

    pub fn hex_manhattan_distance(self) -> u32 {
        ((self.abs().element_sum() + self.element_sum().abs()) / 2) as u32
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

    /*
    pub fn iter() -> impl Iterator<Item = Self> {
        [
            Self::North,
            Self::NorthEast,
            Self::NorthWest,
            Self::South,
            Self::SouthEast,
            Self::SouthWest,
        ]
        .into_iter()
    }
    */
}

impl From<&str> for HexOffset {
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

    fn add(self, rhs: Self) -> Self {
        Self {
            x: self.x.add(rhs.x),
            y: self.y.add(rhs.y),
        }
    }
}

impl Add<HexOffset> for IVec2 {
    type Output = Self;

    fn add(self, rhs: HexOffset) -> Self {
        self + rhs.value()
    }
}

/*
impl AddAssign<IVec2> for IVec2 {
    fn add_assign(&mut self, rhs: Self) {
        self.x.add_assign(rhs.x);
        self.y.add_assign(rhs.y);
    }
}

impl AddAssign<HexOffset> for IVec2 {
    fn add_assign(&mut self, rhs: HexOffset) {
        *self += rhs.value();
    }
}
*/
