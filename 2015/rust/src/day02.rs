use std::ops::Deref;

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[derive(Clone, Copy, Debug)]
struct Present {
    l: usize,
    w: usize,
    h: usize,
}

impl Present {
    fn wrapping_paper(self) -> usize {
        let Self { h, w, l } = self;

        let a = l * w;
        let b = w * h;
        let c = h * l;

        let surface_area = 2 * a + 2 * b + 2 * c;

        let smallest_side = a.min(b).min(c);

        surface_area + smallest_side
    }

    fn ribbon(self) -> usize {
        let Self { h, w, l } = self;

        let mut sides = vec![h, w, l];
        sides.sort_unstable();

        let shortest_dist = sides[0] * 2 + sides[1] * 2;
        let volume = h * w * l;

        shortest_dist + volume
    }
}

impl From<&str> for Present {
    fn from(value: &str) -> Self {
        let [l, w, h] = value
            .trim()
            .split('x')
            .map(|s| s.parse().unwrap())
            .collect::<Vec<_>>()[..]
        else {
            unreachable!()
        };

        Self { l, w, h }
    }
}

#[derive(Debug)]
struct Presents(Box<[Present]>);

impl From<&str> for Presents {
    fn from(value: &str) -> Self {
        Self(value.trim().lines().map(Into::into).collect())
    }
}

impl Deref for Presents {
    type Target = Box<[Present]>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

fn p1(input: &str) -> usize {
    Presents::from(input)
        .iter()
        .map(|p| p.wrapping_paper())
        .sum()
}

fn p2(input: &str) -> usize {
    Presents::from(input).iter().map(|p| p.ribbon()).sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1e1() {
        assert_eq!(p1("2x3x4"), 58);
        assert_eq!(p1("1x1x10"), 43);
    }

    #[test]
    fn p2e1() {
        assert_eq!(p2("2x3x4"), 34);
        assert_eq!(p2("1x1x10"), 14);
    }
}
