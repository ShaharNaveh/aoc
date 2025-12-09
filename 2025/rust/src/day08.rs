use std::collections::HashMap;

use crate::utils::IVec3;

#[derive(Clone, Debug)]
pub struct UnionFind {
    parent: Vec<usize>,
    size: Vec<usize>,
    components: usize,
}

impl UnionFind {
    #[must_use]
    fn new(n: usize) -> Self {
        Self {
            parent: (0..n).collect(),
            size: vec![1; n],
            components: n,
        }
    }

    #[must_use]
    pub fn find(&mut self, mut x: usize) -> usize {
        let mut root = x;
        while self.parent[root] != root {
            root = self.parent[root];
        }

        // Compress path
        while self.parent[x] != x {
            let next = self.parent[x];
            self.parent[x] = root;
            x = next;
        }

        root
    }

    fn unite(&mut self, a: usize, b: usize) -> bool {
        let mut ra = self.find(a);
        let mut rb = self.find(b);

        if ra == rb {
            return false;
        }

        if self.size[ra] < self.size[rb] {
            std::mem::swap(&mut ra, &mut rb);
        }

        // Put rb under ra
        self.parent[rb] = ra;
        self.size[ra] += self.size[rb];
        self.components -= 1;
        true
    }
}

#[derive(Clone, Copy, Debug)]
struct Edge {
    idx0: usize,
    idx1: usize,
    distance: usize,
}

impl Edge {
    #[must_use]
    const fn new(idx0: usize, idx1: usize, distance: usize) -> Self {
        Self {
            idx0,
            idx1,
            distance,
        }
    }
}

#[derive(Clone, Debug)]
struct Puzzle {
    jboxes: Vec<IVec3>,
    edges: Vec<Edge>,

    /// Set the amout of connections. If `None`, will do all.
    connections: Option<usize>,
}

impl From<&str> for Puzzle {
    fn from(value: &str) -> Self {
        let jboxes = value.trim().lines().map(IVec3::from).collect::<Vec<_>>();
        let mut edges = vec![];

        let len = jboxes.len();
        for i in 0..(len - 1) {
            for j in (i + 1)..len {
                edges.push(Edge::new(
                    i,
                    j,
                    jboxes[i].distance_squared(jboxes[j]).try_into().unwrap(),
                ))
            }
        }

        edges.sort_unstable_by_key(|edge| edge.distance);
        Self {
            jboxes,
            edges,
            connections: None,
        }
    }
}

impl Puzzle {
    #[must_use]
    fn part1(&self) -> usize {
        let jboxes_len = self.jboxes.len();
        let connections = self.connections.unwrap_or(jboxes_len);
        let mut dsu = UnionFind::new(jboxes_len);

        for i in 0..connections.min(self.edges.len()) {
            let edge = self.edges[i];
            dsu.unite(edge.idx0, edge.idx1);
        }

        let mut comps = HashMap::new();
        for i in 0..jboxes_len {
            let r = dsu.find(i);
            *comps.entry(r).or_insert(0) += 1;
        }

        let mut sizes = comps.values().copied().collect::<Vec<_>>();
        sizes.sort_unstable_by(|a, b| b.cmp(a));
        sizes.iter().take(3).product()
    }

    #[must_use]
    fn part2(&self) -> usize {
        let jboxes_len = self.jboxes.len();
        let mut dsu = UnionFind::new(jboxes_len);
        for (idx0, idx1) in self.edges.iter().map(|edge| (edge.idx0, edge.idx1)) {
            if dsu.unite(idx0, idx1) {
                if dsu.components == 1 {
                    return (self.jboxes[idx0].x * self.jboxes[idx1].x)
                        .try_into()
                        .unwrap();
                }
            }
        }

        unreachable!()
    }

    #[cfg(test)]
    #[must_use]
    fn with_connections(&mut self, connections: Option<usize>) -> Self {
        self.connections = connections;
        self.clone()
    }
}

fn p1(input: &str) -> usize {
    Puzzle::from(input).part1()
}

fn p2(input: &str) -> usize {
    Puzzle::from(input).part2()
}

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
";

    #[test]
    fn p1e1() {
        let puzzle = Puzzle::from(INPUT).with_connections(Some(10));
        assert_eq!(puzzle.part1(), 40);
    }

    #[test]
    fn p2e1() {
        assert_eq!(p2(INPUT), 25272);
    }
}
