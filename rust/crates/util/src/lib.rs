use std::fmt;

pub trait Day {
    /// Result of parsing, shared by both parts.
    type Parsed;

    fn parse(input: &str) -> Self::Parsed;

    fn part1(input: &Self::Parsed) -> impl fmt::Display;

    /// Optional, the default means that it's not implemented yet.
    fn part2(_input: &Self::Parsed) -> Option<impl fmt::Display> {
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

    println!("{}", D::part1(&parsed));

    if let Some(answer) = D::part2(&parsed) {
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
