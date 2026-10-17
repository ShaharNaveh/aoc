use std::hash::{DefaultHasher, Hash, Hasher};

pub fn calculate_hash<T: Hash>(t: &T) -> u64 {
    let mut s = DefaultHasher::new();
    t.hash(&mut s);
    s.finish()
}

pub mod ivec2;

pub use ivec2::IVec2;

pub trait Answer {
    /// [`None`] means it's not implemented yet/NA.
    fn try_get(&self) -> Option<String>;
}

macro_rules! impl_answer {
    ($($t:ty),* $(,)?) => {
        $(
            impl Answer for $t {
                fn try_get(&self) -> Option<String> {
                    Some(self.to_string())
                }
            }
        )*
    };
}

impl_answer!(
    u8, u16, u32, u64, u128, usize, i8, i16, i32, i64, i128, isize, f32, f64, String, &str,
);

impl<T: Answer> Answer for Option<T> {
    fn try_get(&self) -> Option<String> {
        self.as_ref().and_then(Answer::try_get)
    }
}

pub trait Day {
    /// Result of parsing, shared by both parts.
    type Parsed;

    fn parse(input: &str) -> Self::Parsed;

    fn part1(input: &Self::Parsed) -> impl Answer;

    fn part2(_input: &Self::Parsed) -> impl Answer {
        None::<&str>
    }
}

pub fn read_input(default_path: &str) -> String {
    let path = std::env::args()
        .nth(1)
        .unwrap_or_else(|| default_path.to_string());
    std::fs::read_to_string(&path).unwrap_or_else(|e| panic!("failed to read {path}: {e}"))
}

pub fn run<D: Day>(input: &str) {
    let parsed = D::parse(input.trim_end());

    if let Some(answer) = D::part1(&parsed).try_get() {
        println!("{answer}");
    }

    if let Some(answer) = D::part2(&parsed).try_get() {
        println!("{answer}");
    }
}

#[macro_export]
macro_rules! aoc_main {
    ($day:ty) => {
        fn main() {
            const DEFAULT_INPUT: &str = concat!(
                env!("CARGO_MANIFEST_DIR"),
                "/../../../inputs/",
                env!("CARGO_PKG_NAME"),
                "/",
                env!("CARGO_BIN_NAME"),
                ".txt",
            );

            let input = $crate::read_input(DEFAULT_INPUT);
            $crate::run::<$day>(&input);
        }
    };
}
