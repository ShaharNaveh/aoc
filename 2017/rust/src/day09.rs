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

fn p1(input: &str) -> u32 {
    parse_puzzle(input).0
}

fn p2(input: &str) -> u32 {
    parse_puzzle(input).1
}

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

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
            assert_eq!(p1(input), expected);
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
            assert_eq!(p2(input), expected);
        }
    }
}
