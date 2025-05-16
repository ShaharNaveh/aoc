use std::ops::{Add, AddAssign, Div, Neg, Sub};

#[derive(Clone, Copy, Debug, Default, Eq, Hash, PartialEq)]
pub struct IVec2 {
    pub x: i32,
    pub y: i32,
}

impl IVec2 {
    pub const ZERO: Self = Self::splat(0);

    pub const X: Self = Self::new(1, 0);
    pub const Y: Self = Self::new(0, 1);
    pub const NEG_X: Self = Self::new(-1, 0);
    pub const NEG_Y: Self = Self::new(0, -1);
    // pub const XY: Self = Self::new(1, 1);
    pub const NEG_XY: Self = Self::new(-1, 1);
    pub const X_NEG_Y: Self = Self::new(1, -1);
    // pub const NEG_X_NEG_Y: Self = Self::new(-1, -1);

    pub const NEIGHBORS_4: [Self; 4] = [Self::X, Self::Y, Self::NEG_X, Self::NEG_Y];

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
        Self::NEIGHBORS_4.map(|offset| *self + offset)
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
    pub fn max(self, rhs: Self) -> Self {
        Self {
            x: self.x.max(rhs.x),
            y: self.y.max(rhs.y),
        }
    }

    #[inline]
    #[must_use]
    pub fn rotate(self, rhs: Self) -> Self {
        Self {
            x: self.x * rhs.x - self.y * rhs.y,
            y: self.y * rhs.x + self.x * rhs.y,
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

impl AddAssign<IVec2> for IVec2 {
    #[inline]
    fn add_assign(&mut self, rhs: Self) {
        self.x.add_assign(rhs.x);
        self.y.add_assign(rhs.y);
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
