fn parse_puzzle(inp: &str) -> Vec<Vec<usize>> {
    inp.trim()
        .lines()
        .map(|row| row.split_whitespace().map(|w| w.parse().unwrap()).collect())
        .collect()
}

fn combinations<T>(nums: T) -> Vec<(usize, usize)>
where
    T: IntoIterator<Item = usize>,
{
    let vec: Vec<_> = nums.into_iter().collect();
    let len = vec.len();
    let mut res = vec![];

    for i in 0..len {
        for j in (i + 1)..len {
            res.push((vec[i], vec[j]));
        }
    }
    res
}

fn find_min_max<T>(nums: T) -> (usize, usize)
where
    T: IntoIterator<Item = usize>,
{
    nums.into_iter()
        .fold((usize::MAX, usize::MIN), |(min, max), x| {
            (min.min(x), max.max(x))
        })
}

fn p1(input: &str) -> usize {
    parse_puzzle(input)
        .into_iter()
        .map(find_min_max)
        .map(|(min, max)| max - min)
        .sum()
}

fn p2(input: &str) -> usize {
    parse_puzzle(input)
        .into_iter()
        .map(|row| {
            let (mut min, mut max) = (usize::MIN, usize::MAX);
            for (a, b) in combinations(row) {
                (min, max) = find_min_max(vec![a, b]);
                if max % min == 0 {
                    break;
                }
            }
            max / min
        })
        .sum()
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
        let inp = "
5 1 9 5
7 5 3
2 4 6 8
        ";
        assert_eq!(p1(inp), 18);
    }

    #[test]
    fn p2e1() {
        let inp = "
5 9 2 8
9 4 7 3
3 8 6 5
        ";
        assert_eq!(p2(inp), 9);
    }
}
