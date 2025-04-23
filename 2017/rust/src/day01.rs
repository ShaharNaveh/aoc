pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

fn parse_puzzle(input: &str) -> Vec<u8> {
    input
        .trim()
        .chars()
        .map(|c| c.to_digit(10).unwrap() as u8)
        .collect()
}

fn main<I>(iter: I, offset: usize) -> usize
where
    I: IntoIterator<Item = u8>,
{
    let vec = iter.into_iter().collect::<Vec<_>>();
    let len = vec.len();
    vec.iter()
        .enumerate()
        .filter(|&(i, x)| *x == vec[(i + offset) % len])
        .map(|(_, x)| *x as usize)
        .sum()
}

fn p1(input: &str) -> usize {
    main(parse_puzzle(input), 1)
}

fn p2(input: &str) -> usize {
    let nums = parse_puzzle(input);
    let offset = nums.len() / 2;
    main(nums, offset)
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
