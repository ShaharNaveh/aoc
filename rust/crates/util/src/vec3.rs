use std::ops::{Add, Div, Mul, Sub};

use crate::num::Num;

#[derive(Clone, Copy, Debug, Default, Eq, Hash, PartialEq)]
pub struct Vec3<T> {
    pub x: T,
    pub y: T,
    pub z: T,
}

impl<T: Num> Vec3<T> {
    pub const ZERO: Self = Self::splat(T::ZERO);

    #[inline]
    #[must_use]
    pub const fn new(x: T, y: T, z: T) -> Self {
        Self { x, y, z }
    }

    #[inline]
    #[must_use]
    pub const fn splat(v: T) -> Self {
        Self { x: v, y: v, z: v }
    }

    #[inline]
    #[must_use]
    pub fn element_sum(self) -> T {
        self.x + self.y + self.z
    }

    #[inline]
    #[must_use]
    pub fn abs(self) -> Self {
        Self {
            x: self.x.abs(),
            y: self.y.abs(),
            z: self.z.abs(),
        }
    }

    #[inline]
    #[must_use]
    pub fn dot(self, rhs: Self) -> T {
        (self.x * rhs.x) + (self.y * rhs.y) + (self.z * rhs.z)
    }

    #[inline]
    #[must_use]
    pub fn length_squared(self) -> T {
        self.dot(self)
    }

    #[inline]
    #[must_use]
    pub fn distance_squared(self, rhs: Self) -> T {
        (self - rhs).length_squared()
    }
}

impl<T: Num> From<&str> for Vec3<T> {
    #[inline]
    fn from(raw: &str) -> Self {
        let buf = raw
            .trim()
            .split(',')
            .filter_map(|s| s.trim().parse().ok())
            .collect::<Vec<_>>();
        Self::new(buf[0], buf[1], buf[2])
    }
}

impl<T: Num> Add<Vec3<T>> for Vec3<T> {
    type Output = Self;

    #[inline]
    fn add(self, rhs: Self) -> Self {
        Self {
            x: self.x.add(rhs.x),
            y: self.y.add(rhs.y),
            z: self.z.add(rhs.z),
        }
    }
}

impl<T: Num> Sub<Vec3<T>> for Vec3<T> {
    type Output = Self;

    #[inline]
    fn sub(self, rhs: Self) -> Self {
        Self {
            x: self.x.sub(rhs.x),
            y: self.y.sub(rhs.y),
            z: self.z.sub(rhs.z),
        }
    }
}

impl<T: Num> Mul<T> for Vec3<T> {
    type Output = Self;

    #[inline]
    fn mul(self, rhs: T) -> Self {
        Self {
            x: self.x.mul(rhs),
            y: self.y.mul(rhs),
            z: self.z.mul(rhs),
        }
    }
}

impl<T: Num> Div<T> for Vec3<T> {
    type Output = Self;

    #[inline]
    fn div(self, rhs: T) -> Self {
        Self {
            x: self.x.div(rhs),
            y: self.y.div(rhs),
            z: self.z.div(rhs),
        }
    }
}
