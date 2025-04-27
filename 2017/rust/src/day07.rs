use std::collections::HashMap;

#[derive(Clone, Debug)]
struct Program {
    name: String,
    weight: u32,
    holds: Vec<String>,
}

#[derive(Debug)]
struct Tower(HashMap<String, Vec<Program>>);

impl Tower {
    fn find_len(&self, name: &str) -> usize {
        let holds = &self.0[name];
        holds.len()
            + holds
                .into_iter()
                .map(|prog| self.find_len(&prog.name))
                .sum::<usize>()
    }
}

impl From<&str> for Tower {
    fn from(raw: &str) -> Self {
        let programs = raw.trim().lines().map(Into::into).collect::<Vec<Program>>();

        Self(
            programs
                .iter()
                .map(|prog| {
                    (prog.name.clone(), {
                        let holds = &prog.holds;
                        programs
                            .iter()
                            .filter(|other| holds.contains(&other.name))
                            .cloned()
                            .collect()
                    })
                })
                .collect(),
        )
    }
}

impl From<&str> for Program {
    fn from(raw: &str) -> Self {
        let parts = raw.trim().split(" -> ").collect::<Vec<_>>();
        let holds = if let Some(names) = parts.get(1) {
            names.trim().split(", ").map(Into::into).collect()
        } else {
            vec![]
        };
        let name_weight = parts[0];
        let (name, raw_weight) = name_weight.split_once(' ').unwrap();
        let weight = {
            let mut chars = raw_weight.chars();
            chars.next();
            chars.next_back();
            chars.as_str().parse().unwrap()
        };

        Program {
            name: name.into(),
            weight,
            holds,
        }
    }
}

fn parse_puzzle(input: &str) -> Tower {
    input.trim().into()
}

fn p1(input: &str) -> String {
    let tower = parse_puzzle(&input);
    tower
        .0
        .clone()
        .into_iter()
        .max_by_key(|(k, _)| tower.find_len(&k))
        .map(|(k, _)| k)
        .unwrap()
}

fn p2(input: &str) -> usize {
    0
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
        let input = "
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
        assert_eq!(p1(input), "tknk".to_string());
    }

    #[test]
    fn p2e1() {
        assert_eq!(0, 0);
    }
}
