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

fn p1(input: &str) -> usize {
    run(&mut parse_puzzle(input), false)
}

fn p2(input: &str) -> usize {
    run(&mut parse_puzzle(input), true)
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
        let input = "

0
3
0
1
-3
";
        assert_eq!(p1(input), 5);
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
        assert_eq!(p2(input), 10);
    }
}
