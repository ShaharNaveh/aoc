pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

/// A valid triangle.
struct Triangle;

impl TryFrom<[usize; 3]> for Triangle {
    type Error = ();

    fn try_from(mut nums: [usize; 3]) -> Result<Self, Self::Error> {
        nums.sort_unstable();
        let [a, b, c] = nums;
        (a + b > c).then_some(Triangle).ok_or(())
    }
}

impl TryFrom<&str> for Triangle {
    type Error = ();

    fn try_from(line: &str) -> Result<Self, Self::Error> {
        let nums: [usize; 3] = line
            .split_whitespace()
            .map(|s| s.parse::<usize>().unwrap())
            .collect::<Vec<_>>()
            .try_into()
            .unwrap();

        nums.try_into()
    }
}

fn p1(input: &str) -> usize {
    input
        .lines()
        .filter_map(|l| Triangle::try_from(l).ok())
        .count()
}

fn p2(input: &str) -> usize {
    const SIZE: usize = 3;

    let rows = input
        .lines()
        .filter(|l| !l.trim().is_empty())
        .map(|l| {
            l.split_whitespace()
                .map(|n| n.parse::<usize>().unwrap())
                .collect::<Vec<_>>()
        })
        .collect::<Vec<_>>();

    let (chunks, []) = rows.as_chunks::<SIZE>() else {
        unreachable!()
    };

    chunks
        .iter()
        .flat_map(|chunk| (0..SIZE).map(move |i| std::array::from_fn(|row| chunk[row][i])))
        .filter_map(|nums| Triangle::try_from(nums).ok())
        .count()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1e1() {
        assert_eq!(p1("5 10 25"), 0);
    }
}
