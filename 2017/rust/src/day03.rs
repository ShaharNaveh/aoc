use std::collections::HashMap;

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

fn parse_puzzle(input: &str) -> isize {
    input.trim().parse().unwrap()
}

fn find_next_val(x: isize, y: isize) -> (isize, isize) {
    if (x == 0) && (y == 0) {
        return (1, 0);
    } else if (y > -x) && (x > y) {
        return (x, y + 1);
    } else if (y > -x) && (y >= x) {
        return (x - 1, y);
    } else if (y <= -x) && (x < y) {
        return (x, y - 1);
    } else if (y <= -x) && (x >= y) {
        return (x + 1, y);
    }
    unreachable!();
}

fn p1(input: &str) -> isize {
    let data = parse_puzzle(input);
    let circle = (f32::sqrt(data as f32).ceil() / 2.0f32) as isize;
    let circle_zero = (circle * 2 - 1).pow(2);
    let centers = vec![1, 3, 5, 7]
        .iter()
        .map(|x| circle_zero + x * circle)
        .collect::<Vec<isize>>();
    circle + centers.into_iter().map(|x| (data - x).abs()).min().unwrap()
}

fn p2(input: &str) -> isize {
    let data = parse_puzzle(input);
    let (mut x, mut y) = (0, 0);
    let mut vals = HashMap::from([((x, y), 1)]);
    let offsets = (-1..=1)
        .flat_map(|i| (-1..=1).map(move |j| (i, j)))
        .collect::<Vec<(isize, isize)>>();
    while vals[&(x, y)] <= data {
        (x, y) = find_next_val(x, y);
        vals.insert(
            (x, y),
            offsets
                .iter()
                .filter_map(|(i, j)| vals.get(&(x + i, y + j)))
                .sum(),
        );
    }

    vals[&(x, y)]
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1e1() {
        assert_eq!(p1("1"), 0);
    }

    #[test]
    fn p1e2() {
        assert_eq!(p1("12"), 3);
    }

    #[test]
    fn p1e3() {
        assert_eq!(p1("23"), 2);
    }

    #[test]
    fn p1e4() {
        assert_eq!(p1("1024"), 31);
    }
}
