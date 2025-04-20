const PUZZLE_FILE: &str = "puzzle.txt";
type Puzzle = Vec<u8>;

fn parse_puzzle(inp: &str) -> Puzzle {
    inp.trim()
        .chars()
        .map(|c| c.to_digit(10).unwrap() as u8)
        .collect()
}

fn solve(vec: &Puzzle, offset: usize) -> usize {
    let len = vec.len();
    vec.into_iter()
        .enumerate()
        .filter(|&(i, x)| *x == vec[(i + offset) % len])
        .map(|(_, &x)| x as usize)
        .sum()
}

fn p1(inp: &str) -> usize {
    solve(&parse_puzzle(inp), 1)
}

fn p2(inp: &str) -> usize {
    let nums = parse_puzzle(inp);
    let offset = nums.len() / 2;
    solve(&nums, offset)
}

fn main() {
    let inp = std::fs::read_to_string(PUZZLE_FILE).unwrap();
    println!("{}", p1(&inp));
    println!("{}", p2(&inp));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1e1() {
        assert_eq!(p1("1122"), 3);
    }

    #[test]
    fn p1e2() {
        assert_eq!(p1("1111"), 4);
    }

    #[test]
    fn p1e3() {
        assert_eq!(p1("1234"), 0);
    }

    #[test]
    fn p1e4() {
        assert_eq!(p1("912129"), 9);
    }

    #[test]
    fn p2e1() {
        assert_eq!(p2("1212"), 6);
    }

    #[test]
    fn p2e2() {
        assert_eq!(p2("1221"), 0);
    }

    #[test]
    fn p2e3() {
        assert_eq!(p2("123425"), 4);
    }

    #[test]
    fn p2e4() {
        assert_eq!(p2("123123"), 12);
    }

    #[test]
    fn p2e5() {
        assert_eq!(p2("12131415"), 4);
    }
}
