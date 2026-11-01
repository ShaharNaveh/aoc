use std::{
    fmt::Debug,
    hash::Hash,
    ops::{Add, AddAssign, Div, Mul, Neg, Sub, SubAssign},
    str::FromStr,
};

/// Signed integer scalar usable as a vector component.
pub trait Num:
    Copy
    + Debug
    + Default
    + Eq
    + Hash
    + Ord
    + FromStr
    + Add<Output = Self>
    + AddAssign
    + Sub<Output = Self>
    + SubAssign
    + Mul<Output = Self>
    + Div<Output = Self>
    + Neg<Output = Self>
{
    const ZERO: Self;
    const ONE: Self;
    const NEG_ONE: Self;

    #[must_use]
    fn abs(self) -> Self;

    #[must_use]
    fn signum(self) -> Self;
}

macro_rules! impl_num {
    ($($t:ty),* $(,)?) => {
        $(
            impl Num for $t {
                const ZERO: Self = 0;
                const ONE: Self = 1;
                const NEG_ONE: Self = -1;

                #[inline]
                fn abs(self) -> Self {
                    <$t>::abs(self)
                }

                #[inline]
                fn signum(self) -> Self {
                    <$t>::signum(self)
                }
            }
        )*
    };
}

impl_num!(i8, i16, i32, i64, i128, isize);
