use std::ops::Add;

#[derive(Clone, Copy, Debug, Default, Eq, Hash, PartialEq)]
pub struct IVec2 {
    x: i32,
    y: i32,
}

impl IVec2 {
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
    pub const fn new(x: i32, y: i32) -> Self {
        Self { x, y }
    }

    #[must_use]
    pub fn neighbors_8(self) -> [Self; 8] {
        Self::NEIGHBORS_8.map(|offset| self + offset)
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
