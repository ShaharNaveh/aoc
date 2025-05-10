use std::collections::VecDeque;

#[derive(Clone, Debug, Default)]
struct Program {
    ops: Vec<Opcode>,
    regs: [i64; 26],
    queue: VecDeque<i64>,
    ip: usize,
    sent: usize,
    last_sent: i64,
    first_rcv: i64,
}

impl Program {
    #[must_use]
    #[inline]
    fn with_id(mut self, id: i64) -> Self {
        self.regs[(b'p' - b'a') as usize] = id;
        self
    }

    fn run(&mut self, other: &mut Self, is_first_run: bool) {
        while self.ip < self.ops.len() {
            if self.ops[self.ip].clone().execute(self, other) {
                continue;
            }

            if !is_first_run {
                break;
            }

            other.run(self, false);
            if !self.ops[self.ip].clone().execute(self, other) {
                break;
            }
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
enum Opcode {
    Snd(Value),
    Set(usize, Value),
    Add(usize, Value),
    Mul(usize, Value),
    Mod(usize, Value),
    Rcv(usize),
    Jgz(Value, Value),
}

impl Opcode {
    fn execute(&self, prog: &mut Program, other: &mut Program) -> bool {
        prog.ip += 1;

        match *self {
            Self::Snd(x) => {
                let val = x.resolve(prog);
                prog.last_sent = val;
                other.queue.push_back(val);
                prog.sent += 1;
            }
            Self::Set(x, y) => prog.regs[x] = y.resolve(prog),
            Self::Add(x, y) => prog.regs[x] += y.resolve(prog),
            Self::Mul(x, y) => prog.regs[x] *= y.resolve(prog),
            Self::Mod(x, y) => prog.regs[x] %= y.resolve(prog),
            Self::Rcv(x) => {
                if prog.first_rcv == 0 && prog.regs[x] != 0 {
                    prog.first_rcv = prog.last_sent;
                }

                if let Some(v) = prog.queue.pop_front() {
                    prog.regs[x] = v;
                } else {
                    prog.ip -= 1;
                    return false;
                }
            }
            Self::Jgz(x, y) => {
                if x.resolve(prog) > 0 {
                    prog.ip = (prog.ip as i64 + y.resolve(prog) - 1) as usize;
                }
            }
        }

        true
    }
}

impl From<&str> for Opcode {
    #[must_use]
    fn from(raw: &str) -> Self {
        let mut it = raw.trim().split_whitespace();
        let op = it.next().unwrap();
        let args = it.map(Into::into).collect::<Vec<_>>();
        match op {
            "snd" => Self::Snd(args[0]),
            "set" => Self::Set(args[0].reg(), args[1]),
            "add" => Self::Add(args[0].reg(), args[1]),
            "mul" => Self::Mul(args[0].reg(), args[1]),
            "mod" => Self::Mod(args[0].reg(), args[1]),
            "rcv" => Self::Rcv(args[0].reg()),
            "jgz" => Self::Jgz(args[0], args[1]),
            _ => unreachable!(),
        }
    }
}

#[derive(Clone, Copy, Debug)]
enum Value {
    Const(i64),
    Register(usize),
}

impl Value {
    #[must_use]
    fn resolve(&self, prog: &Program) -> i64 {
        match *self {
            Self::Const(x) => x,
            Self::Register(r) => prog.regs[r],
        }
    }

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
            let reg = (raw.bytes().next().unwrap() - b'a') as usize;
            Self::Register(reg)
        }
    }
}

fn main(input: &str) -> (i64, usize) {
    let mut prog0 = Program::from(input);
    let mut prog1 = prog0.clone().with_id(1);
    prog0.run(&mut prog1, true);
    (prog0.first_rcv, prog1.sent)
}

fn p1(input: &str) -> i64 {
    main(input).0
}

fn p2(input: &str) -> usize {
    main(input).1
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
        assert_eq!(p2(input), 3);
    }
}
