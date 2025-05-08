fn p1(input: &str) -> usize {
    let step = input.trim().parse::<usize>().unwrap();
    let mut buf = vec![0];
    let mut idx = 0;
    for x in 1..=2017 {
        idx = (idx + step) % x + 1;
        buf.insert(idx, x)
    }
    buf[idx + 1]
}

fn p2(input: &str) -> usize {
    let step = input.trim().parse::<usize>().unwrap();
    let mut idx = 0;
    let mut res = 0;
    for x in 1..50_000_000 {
        idx = (idx + step) % x + 1;
        if idx == 1 {
            res = x;
        }
    }
    res
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
        assert_eq!(p1("3"), 638);
    }
}
