use std::collections::HashMap;

use util::{Day, aoc_main};

#[derive(Debug)]
struct Instruction {
    reg: String,
    op: String,
    val: i32,
    cl: String,
    cmp: String,
    cmp_val: i32,
}

impl Instruction {
    fn run(&self, map: &mut HashMap<String, i32>) {
        let l = *map.entry(self.cl.to_string()).or_insert(0);
        let cmp_val = self.cmp_val;
        let cond = match self.cmp.as_str() {
            "==" => l == cmp_val,
            "!=" => l != cmp_val,
            ">=" => l >= cmp_val,
            "<=" => l <= cmp_val,
            ">" => l > cmp_val,
            "<" => l < cmp_val,
            _ => unreachable!("Unkown cmp: '{}'", self.cmp),
        };

        if !cond {
            return;
        }
        let entry = map.entry(self.reg.to_string()).or_insert(0);
        match self.op.as_str() {
            "inc" => *entry += self.val,
            "dec" => *entry -= self.val,
            _ => unreachable!("Unkown op: '{}'", self.op),
        }
    }
}

impl From<&str> for Instruction {
    fn from(raw: &str) -> Self {
        let mut it = raw.trim().split_whitespace();

        let reg = it.next().unwrap().to_string();
        let op = it.next().unwrap().to_string();
        let val = it.next().unwrap().parse().unwrap();
        it.next();
        let cl = it.next().unwrap().to_string();
        let cmp = it.next().unwrap().to_string();
        let cmp_val = it.next().unwrap().parse().unwrap();

        Self {
            reg,
            op,
            val,
            cl,
            cmp,
            cmp_val,
        }
    }
}

fn parse_puzzle(input: &str) -> Vec<Instruction> {
    input.trim().lines().map(Into::into).collect()
}

struct Day08;

impl Day for Day08 {
    type Parsed = Vec<Instruction>;

    fn parse(input: &str) -> Self::Parsed {
        parse_puzzle(input)
    }

    fn part1(input: &Self::Parsed) -> i32 {
        let mut map = HashMap::new();
        input.iter().for_each(|ins| ins.run(&mut map));
        *map.values().max().unwrap_or(&0)
    }

    fn part2(input: &Self::Parsed) -> i32 {
        let mut map = HashMap::new();
        let mut res = i32::MIN;
        input.iter().for_each(|ins| {
            ins.run(&mut map);
            res = res.max(*map.values().max().unwrap_or(&0));
        });
        res
    }
}

aoc_main!(Day08);

#[cfg(test)]
mod tests {
    use super::*;
    const INPUT: &str = "
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
";

    #[test]
    fn part1() {
        let parsed = Day08::parse(INPUT);
        assert_eq!(Day08::part1(&parsed), 1);
    }

    #[test]
    fn part2() {
        let parsed = Day08::parse(INPUT);
        assert_eq!(Day08::part2(&parsed), 10);
    }
}
