use std::collections::HashMap;

#[derive(Debug, Default)]
struct Program {
    instructions: Vec<Instruction>,
    registers: HashMap<char, i64>,
}

impl Program {
    fn insert(&mut self, key: &Value, value: i64) {
        self.registers.insert(key.reg(), value);
    }

    #[must_use]
    fn resolve(&self, value: &Value) -> i64 {
        match value {
            Value::Number(num) => *num,
            Value::Register(reg) => *self.registers.get(reg).unwrap_or(&0),
        }
    }

    #[must_use]
    fn run(&mut self) -> i64 {
        let mut ip = 0;
        let mut last_played_sound = 0;

        loop {
            match self.instructions[ip as usize] {
                Instruction::Snd(x) => last_played_sound = self.resolve(&x),
                Instruction::Set(x, y) => self.insert(&x, self.resolve(&y)),
                Instruction::Add(x, y) => self.insert(&x, self.resolve(&x) + self.resolve(&y)),
                Instruction::Mul(x, y) => self.insert(&x, self.resolve(&x) * self.resolve(&y)),
                Instruction::Mod(x, y) => self.insert(&x, self.resolve(&x) % self.resolve(&y)),
                Instruction::Rcv(x) => {
                    if self.resolve(&x) != 0 {
                        break last_played_sound;
                    }
                }

                Instruction::Jgz(x, y) => {
                    if self.resolve(&x) > 0 {
                        ip += self.resolve(&y);
                        continue;
                    }
                }
            }
            ip += 1;
        }
    }
}

impl From<&str> for Program {
    #[must_use]
    fn from(raw: &str) -> Self {
        Self {
            instructions: raw.trim().lines().map(Into::into).collect(),
            ..Default::default()
        }
    }
}

#[derive(Clone, Copy, Debug)]
enum Instruction {
    Snd(Value),
    Set(Value, Value),
    Add(Value, Value),
    Mul(Value, Value),
    Mod(Value, Value),
    Rcv(Value),
    Jgz(Value, Value),
}

impl From<&str> for Instruction {
    #[must_use]
    fn from(raw: &str) -> Self {
        let mut it = raw.trim().split_whitespace();
        let op = it.next().unwrap();
        let args = it.map(Into::into).collect::<Vec<_>>();
        match op {
            "snd" => Self::Snd(args[0]),
            "set" => Self::Set(args[0], args[1]),
            "add" => Self::Add(args[0], args[1]),
            "mul" => Self::Mul(args[0], args[1]),
            "mod" => Self::Mod(args[0], args[1]),
            "rcv" => Self::Rcv(args[0]),
            "jgz" => Self::Jgz(args[0], args[1]),
            _ => unreachable!(),
        }
    }
}

#[derive(Clone, Copy, Debug)]
enum Value {
    Number(i64),
    Register(char),
}

impl Value {
    #[must_use]
    fn reg(&self) -> char {
        match self {
            Self::Register(x) => *x,
            _ => panic!(),
        }
    }
}

impl From<&str> for Value {
    #[must_use]
    fn from(raw: &str) -> Self {
        if let Some(num) = raw.parse().ok() {
            Self::Number(num)
        } else {
            Self::Register(raw.chars().next().unwrap())
        }
    }
}

fn p1(input: &str) -> i64 {
    Program::from(input).run()
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
set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2
";
        assert_eq!(p1(input), 4);
    }

    #[test]
    fn p2e1() {
        let input = "
snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d
";
        assert_eq!(p2(input), 4);
    }
}
