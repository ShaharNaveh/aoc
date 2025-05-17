use std::{
    fmt,
    ops::{Index, IndexMut},
};

#[derive(Clone, Debug, Default)]
struct Program {
    ops: Vec<Opcode>,
    regs: [i64; 8],
    ip: usize,
    mul_invoked: usize,
}

impl Program {
    #[must_use]
    fn run(&mut self) -> Self {
        while self.ip < self.ops.len() {
            self.execute()
        }
        self.clone()
    }

    #[must_use]
    fn execute(&mut self) {
        self.ip += 1;

        match self.ops[self.ip - 1] {
            Opcode::Set(x, y) => self[x] = self.resolve(&y),
            Opcode::Sub(x, y) => self[x] -= self.resolve(&y),
            Opcode::Mul(x, y) => {
                self[x] *= self.resolve(&y);
                self.mul_invoked += 1;
            }

            Opcode::Jnz(x, y) => {
                if self.resolve(&x) != 0 {
                    self.ip = (self.ip as i64 + self.resolve(&y) - 1) as usize;
                }
            }
            Opcode::Halt => self.ip = self.ops.len() + 1,
        }
    }

    #[inline]
    #[must_use]
    fn resolve(&self, val: &Value) -> i64 {
        match *val {
            Value::Const(x) => x,
            Value::Register(r) => self[r],
        }
    }
}

impl From<&str> for Program {
    #[must_use]
    fn from(raw: &str) -> Self {
        Self {
            ops: raw.trim().lines().map(Into::into).collect(),
            ..Default::default()
        }
    }
}

#[derive(Clone, Copy, Debug)]
enum Value {
    Const(i64),
    Register(usize),
}

impl Value {
    #[inline]
    #[must_use]
    fn reg(&self) -> usize {
        match *self {
            Self::Register(r) => r,
            _ => panic!(),
        }
    }
}

impl From<&str> for Value {
    #[must_use]
    fn from(raw: &str) -> Self {
        if let Ok(num) = raw.parse() {
            Self::Const(num)
        } else {
            let reg = (raw.bytes().next().unwrap()) as usize;
            Self::Register(reg)
        }
    }
}

#[derive(Clone, Copy, Debug)]
enum Opcode {
    Set(usize, Value),
    Sub(usize, Value),
    Mul(usize, Value),
    Jnz(Value, Value),
    Halt,
}

impl From<&str> for Opcode {
    #[must_use]
    fn from(raw: &str) -> Self {
        let mut it = raw.trim().split_whitespace();
        let op = it.next().unwrap();

        let args = it.map(Into::into).collect::<Vec<Value>>();
        match op {
            "set" => Self::Set(args[0].reg(), args[1]),
            "sub" => Self::Sub(args[0].reg(), args[1]),
            "mul" => Self::Mul(args[0].reg(), args[1]),
            "jnz" => Self::Jnz(args[0], args[1]),
            _ => unreachable!(),
        }
    }
}

impl<T> Index<T> for Program
where
    u8: TryFrom<T>,
    <u8 as TryFrom<T>>::Error: fmt::Debug,
{
    type Output = i64;

    #[inline]
    fn index(&self, index: T) -> &Self::Output {
        &self.regs[(u8::try_from(index).unwrap() - b'a') as usize]
    }
}

impl<T> IndexMut<T> for Program
where
    u8: TryFrom<T>,
    <u8 as TryFrom<T>>::Error: fmt::Debug,
{
    #[inline]
    fn index_mut(&mut self, index: T) -> &mut Self::Output {
        &mut self.regs[(u8::try_from(index).unwrap() - b'a') as usize]
    }
}

#[inline]
#[must_use]
fn is_prime(n: i64) -> bool {
    (n > 1) && !(2..n).any(|i| n % i == 0)
}

fn p1(input: &str) -> usize {
    Program::from(input).run().mul_invoked
}

fn p2(input: &str) -> usize {
    let prog = {
        let mut p = Program::from(input);
        p.ops[11] = Opcode::Halt;
        p['a'] = 1;
        p.run()
    };

    (prog['b']..=prog['c'])
        .step_by(17)
        .filter(|&n| !is_prime(n))
        .count()
}

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}
