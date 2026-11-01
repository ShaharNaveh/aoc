use util::{Day, aoc_main};

fn parse_puzzle(input: &str) -> (u32, u32) {
    let mut in_group = 0;
    let mut in_garbage = false;
    let mut score = 0;
    let mut total_garbage = 0;

    let mut it = input.trim().chars();
    while let Some(c) = it.next() {
        if c == '!' {
            it.next();
        } else if in_garbage {
            if c == '>' {
                in_garbage = false;
            } else {
                total_garbage += 1;
            }
        } else if c == '<' {
            in_garbage = true;
        } else if c == '{' {
            in_group += 1;
        } else if c == '}' {
            score += in_group;
            in_group -= 1;
        }
    }

    (score, total_garbage)
}

struct Day09;

impl Day for Day09 {
    type Parsed = (u32, u32);

    fn parse(input: &str) -> Self::Parsed {
        parse_puzzle(input)
    }

    fn part1(input: &Self::Parsed) -> u32 {
        input.0
    }

    fn part2(input: &Self::Parsed) -> u32 {
        input.1
    }
}

aoc_main!(Day09);

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1e1() {
        let tests = [
            ("{}", 1),
            ("{{{}}}", 6),
            ("{{},{}}", 5),
            ("{{{},{},{{}}}}", 16),
            ("{<a>,<a>,<a>,<a>}", 1),
            ("{{<ab>},{<ab>},{<ab>},{<ab>}}", 9),
            ("{{<!!>},{<!!>},{<!!>},{<!!>}}", 9),
            ("{{<a!>},{<a!>},{<a!>},{<ab>}}", 3),
        ];

        for (input, expected) in tests {
            assert_eq!(Day09::part1(&Day09::parse(input)), expected);
        }
    }

    #[test]
    fn p2e1() {
        let tests = [
            ("<>", 0),
            ("<random characters>", 17),
            ("<<<<>", 3),
            ("<{!>}>", 2),
            ("<!!>", 0),
            ("<!!!>>", 0),
            ("<{o\"i!a,<{i<a>", 10),
        ];

        for (input, expected) in tests {
            assert_eq!(Day09::part2(&Day09::parse(input)), expected);
        }
    }
}
