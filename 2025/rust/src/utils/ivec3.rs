use core::ops::Sub;

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

    #[must_use]
    pub const fn dot(self, rhs: Self) -> isize {
        (self.x * rhs.x) + (self.y * rhs.y) + (self.z * rhs.z)
    }

    #[must_use]
    pub const fn length_squared(self) -> isize {
        self.dot(self)
    }

    #[must_use]
    pub fn distance_squared(self, rhs: Self) -> isize {
        (self - rhs).length_squared()
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

impl Sub for IVec3 {
    type Output = Self;

    fn sub(self, rhs: Self) -> Self {
        Self {
            x: self.x.sub(rhs.x),
            y: self.y.sub(rhs.y),
            z: self.z.sub(rhs.z),
        }
    }
}
