use std::collections::HashMap;

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

fn p1(input: &str) -> i32 {
    let mut map = HashMap::new();
    parse_puzzle(input).iter().for_each(|ins| ins.run(&mut map));
    *map.values().max().unwrap_or(&0)
}

fn p2(input: &str) -> i32 {
    let mut map = HashMap::new();
    let mut res = i32::MIN;
    parse_puzzle(input).iter().for_each(|ins| {
        ins.run(&mut map);
        res = res.max(*map.values().max().unwrap_or(&0));
    });
    res
}

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

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
    fn p1e1() {
        assert_eq!(p1(INPUT), 1);
    }

    #[test]
    fn p2e1() {
        assert_eq!(p2(INPUT), 10);
    }
}
