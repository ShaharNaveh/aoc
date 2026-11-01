use std::ops::{Add, AddAssign, Div, Mul, Neg, Sub, SubAssign};

use crate::num::Num;

#[derive(Clone, Copy, Debug, Default, Eq, Hash, PartialEq)]
pub struct Vec2<T> {
    pub x: T,
    pub y: T,
}

impl<T: Num> Vec2<T> {
    pub const ZERO: Self = Self::splat(T::ZERO);
    pub const ONE: Self = Self::splat(T::ONE);

    pub const X: Self = Self::new(T::ONE, T::ZERO);
    pub const Y: Self = Self::new(T::ZERO, T::ONE);
    pub const NEG_X: Self = Self::new(T::NEG_ONE, T::ZERO);
    pub const NEG_Y: Self = Self::new(T::ZERO, T::NEG_ONE);
    pub const XY: Self = Self::new(T::ONE, T::ONE);
    pub const NEG_XY: Self = Self::new(T::NEG_ONE, T::ONE);
    pub const X_NEG_Y: Self = Self::new(T::ONE, T::NEG_ONE);
    pub const NEG_X_NEG_Y: Self = Self::new(T::NEG_ONE, T::NEG_ONE);

    pub const NEIGHBORS_4: [Self; 4] = [Self::X, Self::Y, Self::NEG_X, Self::NEG_Y];

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

    #[inline]
    #[must_use]
    pub const fn new(x: T, y: T) -> Self {
        Self { x, y }
    }

    #[inline]
    #[must_use]
    pub const fn splat(v: T) -> Self {
        Self { x: v, y: v }
    }

    #[inline]
    #[must_use]
    pub fn with_y(mut self, y: T) -> Self {
        self.y = y;
        self
    }

    #[inline]
    #[must_use]
    pub fn neighbors_4(&self) -> [Self; 4] {
        Self::NEIGHBORS_4.map(|offset| *self + offset)
    }

    #[inline]
    #[must_use]
    pub fn neighbors_8(&self) -> [Self; 8] {
        Self::NEIGHBORS_8.map(|offset| *self + offset)
    }

    #[inline]
    #[must_use]
    pub fn element_sum(self) -> T {
        self.x + self.y
    }

    #[inline]
    #[must_use]
    pub fn element_product(self) -> T {
        self.x * self.y
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
    pub fn signum(self) -> Self {
        Self::new(self.x.signum(), self.y.signum())
    }

    #[inline]
    #[must_use]
    pub fn min(self, rhs: Self) -> Self {
        Self {
            x: self.x.min(rhs.x),
            y: self.y.min(rhs.y),
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

impl<T: Num> Add<Vec2<T>> for Vec2<T> {
    type Output = Self;

    #[inline]
    fn add(self, rhs: Self) -> Self {
        Self {
            x: self.x.add(rhs.x),
            y: self.y.add(rhs.y),
        }
    }
}

impl<T: Num> AddAssign<Vec2<T>> for Vec2<T> {
    #[inline]
    fn add_assign(&mut self, rhs: Self) {
        self.x.add_assign(rhs.x);
        self.y.add_assign(rhs.y);
    }
}

impl<T: Num> Div<Vec2<T>> for Vec2<T> {
    type Output = Self;

    #[inline]
    fn div(self, rhs: Self) -> Self {
        Self {
            x: self.x.div(rhs.x),
            y: self.y.div(rhs.y),
        }
    }
}

impl<T: Num> Div<T> for Vec2<T> {
    type Output = Self;

    #[inline]
    fn div(self, rhs: T) -> Self {
        Self {
            x: self.x.div(rhs),
            y: self.y.div(rhs),
        }
    }
}

impl<T: Num> Mul<Vec2<T>> for Vec2<T> {
    type Output = Self;

    #[inline]
    fn mul(self, rhs: Self) -> Self {
        Self {
            x: self.x.mul(rhs.x),
            y: self.y.mul(rhs.y),
        }
    }
}

impl<T: Num> Mul<T> for Vec2<T> {
    type Output = Self;

    #[inline]
    fn mul(self, rhs: T) -> Self {
        Self {
            x: self.x.mul(rhs),
            y: self.y.mul(rhs),
        }
    }
}

impl<T: Num> Neg for Vec2<T> {
    type Output = Self;

    #[inline]
    fn neg(self) -> Self {
        Self {
            x: self.x.neg(),
            y: self.y.neg(),
        }
    }
}

impl<T: Num> Sub<Vec2<T>> for Vec2<T> {
    type Output = Self;

    #[inline]
    fn sub(self, rhs: Self) -> Self {
        Self {
            x: self.x.sub(rhs.x),
            y: self.y.sub(rhs.y),
        }
    }
}

impl<T: Num> SubAssign<Vec2<T>> for Vec2<T> {
    #[inline]
    fn sub_assign(&mut self, rhs: Self) {
        self.x.sub_assign(rhs.x);
        self.y.sub_assign(rhs.y);
    }
}
