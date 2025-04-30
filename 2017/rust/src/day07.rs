use std::collections::{HashMap, HashSet};

#[derive(Debug)]
struct Tower {
    root: String,
    children: HashMap<String, Vec<String>>,
    weights: HashMap<String, u32>,
}

impl Tower {
    fn walk(&self, root: String) -> (bool, u32) {
        let mut weight = self.weights[&root];
        let mut map: HashMap<u32, Vec<String>> = HashMap::new();

        for child in self.children.get(&root).unwrap_or(&vec![]) {
            let (found, child_weight) = self.walk(child.into());

            if found {
                return (found, child_weight);
            }

            map.entry(child_weight).or_default().push(child.into());
            weight += child_weight;
        }

        if map.len() < 2 {
            return (false, weight);
        }

        let (mut bad_weight, mut bad, mut good) = (0, 0, 0);
        for (&cost, children) in &map {
            if children.len() == 1 {
                bad_weight = self.weights[&children[0]];
                bad = cost;
            } else {
                good = cost;
            }
        }

        (true, bad_weight + good - bad)
    }
}

impl From<&str> for Tower {
    fn from(raw: &str) -> Self {
        let mut all_children = HashSet::new();
        let mut children = HashMap::new();
        let mut weights = HashMap::new();
        for line in raw.trim().lines() {
            let mut it = line.split("->");

            let (name, raw_weight) = it.next().unwrap().trim().split_once(' ').unwrap();
            let weight = {
                let mut chars = raw_weight.chars();
                chars.next();
                chars.next_back();
                chars.as_str().parse().unwrap()
            };
            weights.insert(name.into(), weight);

            let child = it.next().map_or(vec![], |c| {
                c.split(',').map(|x| x.trim().to_owned()).collect()
            });
            all_children.extend(child.clone());
            children.insert(name.into(), child);
        }
        let keys = weights.keys().map(Into::into).collect::<HashSet<String>>();
        let root = keys.difference(&all_children).next().unwrap();
        Self {
            root: root.into(),
            children,
            weights,
        }
    }
}

fn parse_puzzle(input: &str) -> Tower {
    input.into()
}

fn p1(input: &str) -> String {
    parse_puzzle(input).root
}

fn p2(input: &str) -> u32 {
    let tower = parse_puzzle(input);
    tower.walk(tower.root.clone()).1
}

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[cfg(test)]
mod tests {
    use super::*;
    const INPUT: &str = "
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
";

    #[test]
    fn p1e1() {
        assert_eq!(p1(INPUT), "tknk".to_string());
    }

    #[test]
    fn p2e1() {
        assert_eq!(p2(INPUT), 60);
    }
}
