use crate::utils::IVec2;

fn combinations(n: usize) -> impl Iterator<Item = (usize, usize)> {
    (0..n).flat_map(move |left| ((left + 1)..n).map(move |right| (left, right)))
}

#[derive(Debug)]
struct Tiles {
    red: Vec<IVec2>,
}

impl From<&str> for Tiles {
    fn from(value: &str) -> Self {
        let red = value
            .trim()
            .lines()
            .map(|line| {
                let (x, y) = line.split_once(',').unwrap();
                IVec2::new(x.parse().unwrap(), y.parse().unwrap())
            })
            .collect();

        Self { red }
    }
}

impl Tiles {
    #[must_use]
    fn largest_red(&self) -> usize {
        let len = self.red.len();

        combinations(len).fold(usize::MIN, |max, (idx0, idx1)| {
            let tile0 = self.red[idx0];
            let tile1 = self.red[idx1];

            let dist = ((tile0 - tile1).abs() + IVec2::ONE)
                .element_product()
                .try_into()
                .unwrap();

            if dist > max { dist } else { max }
        })
    }
}

fn p1(input: &str) -> usize {
    Tiles::from(input).largest_red()
}

fn p2(_input: &str) -> usize {
    0
}

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
";

    #[test]
    fn p1e1() {
        assert_eq!(p1(INPUT), 50);
    }

    #[test]
    fn p2e1() {
        assert_eq!(p2(INPUT), 0);
    }
}
