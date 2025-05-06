use std::{
    collections::{HashMap, HashSet},
    fmt,
    hash::Hash,
    str::FromStr,
};

#[derive(Debug)]
struct Pipes<T = u16>(HashMap<T, HashSet<T>>)
where
    T: Eq + Hash;

impl<T> Pipes<T>
where
    T: Copy + Eq + Hash,
{
    fn group(&self, pipe: T) -> HashSet<T> {
        let mut group = HashSet::new();
        let mut queue = vec![pipe];
        while let Some(node) = queue.pop() {
            if !group.insert(node) {
                continue;
            }
            queue.extend(self.0.get(&node).unwrap())
        }
        group
    }

    fn group_count(mut self) -> usize {
        let mut count = 0;

        while let Some(pipe) = self.0.keys().next() {
            let group = self.group(*pipe);
            self.0.retain(|&k, _| !group.contains(&k));
            count += 1;
        }

        count
    }
}

impl<T> From<&str> for Pipes<T>
where
    T: Eq + FromStr + Hash,
    <T as FromStr>::Err: fmt::Debug,
{
    fn from(raw: &str) -> Self {
        let map = raw
            .trim()
            .lines()
            .map(|line| {
                let mut it = line.trim().split("<->");
                let pipe = it.next().unwrap().trim().parse().unwrap();
                let connected = it
                    .next()
                    .unwrap()
                    .trim()
                    .split(',')
                    .filter_map(|p| p.trim().parse().ok())
                    .collect();

                (pipe, connected)
            })
            .collect();
        Self(map)
    }
}

fn parse_puzzle(input: &str) -> Pipes {
    input.into()
}

fn p1(input: &str) -> usize {
    parse_puzzle(input).group(0).len()
}

fn p2(input: &str) -> usize {
    parse_puzzle(input).group_count()
}

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "
0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5
";

    #[test]
    fn p1e1() {
        assert_eq!(p1(INPUT), 6);
    }

    #[test]
    fn p2e1() {
        assert_eq!(p2(INPUT), 2);
    }
}
