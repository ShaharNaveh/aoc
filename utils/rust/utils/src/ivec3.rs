use std::ops::{Add, Div, Mul};

#[derive(Clone, Copy, Debug, Default, Eq, Hash, PartialEq)]
pub struct IVec3 {
    pub x: isize,
    pub y: isize,
    pub z: isize,
}

impl IVec3 {
    #[must_use]
    pub const fn new(x: isize, y: isize, z: isize) -> Self {
        Self { x, y, z }
    }

    #[inline]
    #[must_use]
    pub fn element_sum(self) -> isize {
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
}

impl From<&str> for IVec3 {
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

impl Add<IVec3> for IVec3 {
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

impl Mul<isize> for IVec3 {
    type Output = Self;

    #[inline]
    fn mul(self, rhs: isize) -> Self {
        Self {
            x: self.x.mul(rhs),
            y: self.y.mul(rhs),
            z: self.z.mul(rhs),
        }
    }
}

impl Div<isize> for IVec3 {
    type Output = Self;

    #[inline]
    fn div(self, rhs: isize) -> Self {
        Self {
            x: self.x.div(rhs),
            y: self.y.div(rhs),
            z: self.z.div(rhs),
        }
    }
}
