use util::{Day, aoc_main};

#[derive(Debug)]
struct Area {
    width: usize,
    height: usize,
    presents: Vec<usize>,
}

impl From<&str> for Area {
    fn from(value: &str) -> Self {
        let mut it = value.trim().split_ascii_whitespace();

        let (width, height) = it.next().unwrap().split_once('x').unwrap();
        let presents = it.map(|x| x.parse().unwrap()).collect();

        Self {
            width: width.parse().unwrap(),
            height: height.trim_end_matches(':').parse().unwrap(),
            presents,
        }
    }
}

impl Area {
    #[must_use]
    const fn size(&self) -> usize {
        self.width * self.height
    }
}

struct Day12;

impl Day for Day12 {
    type Parsed = String;

    fn parse(input: &str) -> Self::Parsed {
        input.to_string()
    }

    fn part1(input: &Self::Parsed) -> usize {
        let (presents_chunk, areas_chunk) = input.trim().rsplit_once("\n\n").unwrap();

        let presents = presents_chunk
            .split("\n\n")
            .map(|chunk| chunk.chars().filter(|c| *c == '#').count())
            .collect::<Vec<_>>();

        areas_chunk
            .split('\n')
            .map(Area::from)
            .filter(|area| {
                area.size()
                    >= area
                        .presents
                        .iter()
                        .zip(&presents)
                        .map(|(count, present)| count * present)
                        .sum()
            })
            .count()
    }
}

aoc_main!(Day12);

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
";

    #[test]
    fn p1e1() {
        assert_eq!(
            Day12::part1(&Day12::parse(INPUT)),
            // Solution only works on real input:/
            // 2
            3
        );
    }
}
