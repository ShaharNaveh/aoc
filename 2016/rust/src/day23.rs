use std::ops::{Deref, DerefMut, Index, IndexMut};

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[derive(Clone, Copy, Debug)]
struct Literal(isize);

impl Deref for Literal {
    type Target = isize;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl TryFrom<&str> for Literal {
    type Error = ();

    fn try_from(value: &str) -> Result<Self, Self::Error> {
        Ok(value.parse().map_err(|_| ()).map(Self)?)
    }
}

#[derive(Clone, Copy, Debug)]
struct Register(char);

impl From<Register> for usize {
    fn from(value: Register) -> Self {
        (value.0 as u8 - b'a') as usize
    }
}

impl From<&str> for Register {
    fn from(value: &str) -> Self {
        debug_assert_eq!(value.len(), 1);
        Self(value.chars().next().unwrap())
    }
}

#[derive(Clone, Copy, Debug)]
enum Value {
    Literal(Literal),
    Register(Register),
}

impl From<Literal> for Value {
    fn from(value: Literal) -> Self {
        Self::Literal(value)
    }
}

impl From<Register> for Value {
    fn from(value: Register) -> Self {
        Self::Register(value)
    }
}

impl From<&str> for Value {
    fn from(value: &str) -> Self {
        Literal::try_from(value).map_or_else(|()| Register::from(value).into(), Into::into)
    }
}

#[derive(Clone, Copy, Debug)]
enum Instruction {
    Cpy { x: Value, y: Value },
    Inc(Value),
    Dec(Value),
    Jnz { x: Value, y: Value },
    Tgl(Register),
}

impl From<&str> for Instruction {
    fn from(value: &str) -> Self {
        let (name, data) = value.trim().split_once(' ').unwrap();

        match name {
            "cpy" => {
                let (x, y) = data.split_once(' ').unwrap();
                Self::Cpy {
                    x: x.into(),
                    y: y.into(),
                }
            }
            "inc" => Self::Inc(data.into()),
            "dec" => Self::Dec(data.into()),
            "jnz" => {
                let (x, y) = data.split_once(' ').unwrap();
                Self::Jnz {
                    x: x.into(),
                    y: y.into(),
                }
            }
            "tgl" => Self::Tgl(data.into()),
            other => panic!("unknown name: {other}"),
        }
    }
}

#[derive(Debug)]
struct Instructions(Box<[Instruction]>);

impl Instructions {
    fn solve(&mut self, mut registers: Registers) -> isize {
        let mut ip = 0;

        while let Some(&instruction) = self.get(ip) {
            match instruction {
                Instruction::Cpy { x, y } => {
                    let Value::Register(y) = y else {
                        ip += 1;
                        continue;
                    };

                    registers[y] = registers.extract_value(x);
                }
                Instruction::Inc(register) => {
                    let Value::Register(register) = register else {
                        ip += 1;
                        continue;
                    };
                    registers[register] += 1;
                }
                Instruction::Dec(register) => {
                    let Value::Register(register) = register else {
                        ip += 1;
                        continue;
                    };
                    registers[register] -= 1;
                }
                Instruction::Jnz { x, y } => {
                    if registers.extract_value(x) != 0 {
                        let nip = isize::try_from(ip).unwrap() + registers.extract_value(y);
                        ip = nip.try_into().unwrap();
                        continue;
                    }
                }
                Instruction::Tgl(x) => {
                    let Ok(target) = usize::try_from(isize::try_from(ip).unwrap() + registers[x])
                    else {
                        ip += 1;
                        continue;
                    };

                    let Some(instr) = self.get_mut(target) else {
                        ip += 1;
                        continue;
                    };

                    *instr = match instr {
                        Instruction::Inc(x) => Instruction::Dec(*x),
                        Instruction::Dec(x) => Instruction::Inc(*x),
                        Instruction::Tgl(x) => Instruction::Inc((*x).into()),
                        Instruction::Jnz { x, y } => Instruction::Cpy { x: *x, y: *y },
                        Instruction::Cpy { x, y } => Instruction::Jnz { x: *x, y: *y },
                    }
                }
            }

            ip += 1;
        }

        registers[Register('a')]
    }
}

impl Deref for Instructions {
    type Target = Box<[Instruction]>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for Instructions {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

impl From<&str> for Instructions {
    fn from(value: &str) -> Self {
        Self(value.trim().lines().map(Into::into).collect())
    }
}

#[derive(Clone, Copy, Debug, Default)]
struct Registers([isize; 4]);

impl Registers {
    fn extract_value(&self, value: Value) -> isize {
        match value {
            Value::Literal(v) => *v,
            Value::Register(register) => self[register],
        }
    }
}

impl Deref for Registers {
    type Target = [isize; 4];

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for Registers {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

impl Index<Register> for Registers {
    type Output = isize;

    fn index(&self, register: Register) -> &Self::Output {
        &self.0[usize::from(register)]
    }
}

impl Index<&Register> for Registers {
    type Output = isize;

    fn index(&self, register: &Register) -> &Self::Output {
        &self[*register]
    }
}

impl IndexMut<Register> for Registers {
    fn index_mut(&mut self, register: Register) -> &mut Self::Output {
        &mut self.0[usize::from(register)]
    }
}

impl IndexMut<&Register> for Registers {
    fn index_mut(&mut self, register: &Register) -> &mut Self::Output {
        &mut self[*register]
    }
}

fn p1(input: &str) -> isize {
    let mut registers = Registers::default();
    registers[Register('a')] = 7;
    Instructions::from(input).solve(registers)
}

fn p2(input: &str) -> isize {
    let mut registers = Registers::default();
    registers[Register('a')] = 12;
    Instructions::from(input).solve(registers)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1e1() {
        assert_eq!(
            p1("
cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a
"
            .trim()),
            3
        );
    }
}
