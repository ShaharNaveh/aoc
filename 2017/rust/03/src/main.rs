use std::collections::HashMap;
const PUZZLE_FILE: &str = "puzzle.txt";

fn parse_puzzle(inp: &str) -> isize {
    inp.trim().parse().unwrap()
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

fn p1(inp: &str) -> isize {
    let data = parse_puzzle(inp);
    let circle = (f32::sqrt(data as f32).ceil() / 2.0f32) as isize;
    let circle_zero = (circle * 2 - 1).pow(2);
    let centers = vec![1, 3, 5, 7]
        .iter()
        .map(|x| circle_zero + x * circle)
        .collect::<Vec<isize>>();
    circle + centers.into_iter().map(|x| (data - x).abs()).min().unwrap()
}

fn p2(inp: &str) -> isize {
    let data = parse_puzzle(inp);
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
        let inp = "1";
        assert_eq!(p1(inp), 0);
    }

    #[test]
    fn p1e2() {
        let inp = "12";
        assert_eq!(p1(inp), 3);
    }
    #[test]
    fn p1e3() {
        let inp = "23";
        assert_eq!(p1(inp), 2);
    }

    #[test]
    fn p1e4() {
        let inp = "1024";
        assert_eq!(p1(inp), 31);
    }
}
