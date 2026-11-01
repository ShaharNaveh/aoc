use util::{Day, aoc_main};

fn parse_puzzle(input: &str) -> Vec<isize> {
    input.trim().lines().map(|x| x.parse().unwrap()).collect()
}

fn run(offsets: &mut Vec<isize>, is_p2: bool) -> usize {
    let mut i = 0;
    let mut ip: isize = 0;
    loop {
        if let Some(offset) = offsets.get_mut(ip as usize) {
            ip += *offset;
            if is_p2 && (*offset >= 3) {
                *offset -= 1;
            } else {
                *offset += 1;
            }
        } else {
            break i;
        }
        i += 1;
    }
}

struct Day05;

impl Day for Day05 {
    type Parsed = Vec<isize>;

    fn parse(input: &str) -> Self::Parsed {
        parse_puzzle(input)
    }

    fn part1(input: &Self::Parsed) -> usize {
        run(&mut input.clone(), false)
    }

    fn part2(input: &Self::Parsed) -> usize {
        run(&mut input.clone(), true)
    }
}

aoc_main!(Day05);

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1e1() {
        let input = "

0
3
0
1
-3
";
        assert_eq!(Day05::part1(&Day05::parse(input)), 5);
    }

    #[test]
    fn p2e1() {
        let input = "

0
3
0
1
-3
";
        assert_eq!(Day05::part2(&Day05::parse(input)), 10);
    }
}
