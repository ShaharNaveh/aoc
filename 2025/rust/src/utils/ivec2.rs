use std::ops::{Add, Sub};

#[derive(Clone, Copy, Debug, Default, Eq, Hash, PartialEq)]
pub struct IVec2 {
    pub x: isize,
    pub y: isize,
}

impl IVec2 {
    pub const ZERO: Self = Self::splat(0);
    pub const ONE: Self = Self::splat(1);

    pub const X: Self = Self::new(1, 0);
    pub const Y: Self = Self::new(0, 1);
    pub const NEG_X: Self = Self::new(-1, 0);
    pub const NEG_Y: Self = Self::new(0, -1);
    pub const XY: Self = Self::new(1, 1);
    pub const NEG_XY: Self = Self::new(-1, 1);
    pub const X_NEG_Y: Self = Self::new(1, -1);
    pub const NEG_X_NEG_Y: Self = Self::new(-1, -1);

    pub const NEIGHBORS_8: [Self; 8] = [
        Self::X,
        Self::Y,
        Self::NEG_X,
        Self::NEG_Y,
        Self::XY,
        Self::NEG_XY,
        Self::X_NEG_Y,
        Self::NEG_X_NEG_Y,
    ];

    #[must_use]
    pub const fn new(x: isize, y: isize) -> Self {
        Self { x, y }
    }

    #[must_use]
    pub const fn splat(v: isize) -> Self {
        Self { x: v, y: v }
    }

    #[must_use]
    pub fn neighbors_8(self) -> [Self; 8] {
        Self::NEIGHBORS_8.map(|offset| self + offset)
    }

    #[must_use]
    pub const fn element_product(self) -> isize {
        self.x * self.y
    }

    #[must_use]
    pub const fn abs(self) -> Self {
        Self {
            x: self.x.abs(),
            y: self.y.abs(),
        }
    }

    #[must_use]
    pub fn max(self, rhs: Self) -> Self {
        Self {
            x: self.x.max(rhs.x),
            y: self.y.max(rhs.y),
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

impl Sub for IVec2 {
    type Output = Self;

    fn sub(self, rhs: Self) -> Self {
        Self {
            x: self.x.sub(rhs.x),
            y: self.y.sub(rhs.y),
        }
    }
}
