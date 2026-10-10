use std::{
    collections::HashSet,
    ops::{Deref, DerefMut, Index, IndexMut},
};

use crate::utils::calculate_hash;

pub fn solve(input: &str) {
    println!("{}", p1(&input));
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
    Cpy { x: Value, y: Register },
    Inc(Register),
    Dec(Register),
    Jnz { x: Value, y: Literal },
    Out(Value),
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
                    y: y.try_into().expect("be a valid literal"),
                }
            }
            "out" => Self::Out(data.into()),
            other => panic!("unknown name: {other}"),
        }
    }
}

#[derive(Debug)]
struct Instructions(Box<[Instruction]>);

impl Deref for Instructions {
    type Target = Box<[Instruction]>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl From<&str> for Instructions {
    fn from(value: &str) -> Self {
        Self(value.trim().lines().map(Into::into).collect())
    }
}

#[derive(Clone, Copy, Debug, Default, Eq, Hash, PartialEq)]
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

#[derive(Debug)]
struct Antenna<'a> {
    ip: usize,
    instructions: &'a Instructions,
    registers: Registers,
}

impl<'anth> Antenna<'anth> {
    fn new<'ins: 'anth>(instructions: &'ins Instructions, registers: Registers) -> Self {
        Self {
            instructions,
            registers,
            ip: 0,
        }
    }
}

impl Iterator for Antenna<'_> {
    type Item = isize;

    fn next(&mut self) -> Option<Self::Item> {
        while let Some(&instruction) = self.instructions.get(self.ip) {
            match instruction {
                Instruction::Cpy { x, y } => self.registers[y] = self.registers.extract_value(x),
                Instruction::Inc(register) => self.registers[register] += 1,
                Instruction::Dec(register) => self.registers[register] -= 1,
                Instruction::Jnz { x, y } => {
                    if self.registers.extract_value(x) != 0 {
                        let nip = isize::try_from(self.ip).unwrap() + *y;
                        self.ip = nip.try_into().unwrap();
                        continue;
                    }
                }
                Instruction::Out(x) => {
                    self.ip += 1;
                    return Some(self.registers.extract_value(x));
                }
            }

            self.ip += 1;
        }

        None
    }
}

fn p1(input: &str) -> isize {
    let instructions = Instructions::from(input);

    for initial_a in 0..=isize::MAX {
        let mut registers = Registers::default();
        registers[Register('a')] = initial_a;

        let mut antenna = Antenna::new(&instructions, registers);

        let mut seen = HashSet::new();

        let mut expect_zero = true;

        while let Some(signal) = antenna.next() {
            if (expect_zero && signal != 0) || (!expect_zero && signal != 1) {
                break;
            }

            expect_zero = !expect_zero;

            if !seen.insert(calculate_hash(&(
                expect_zero,
                antenna.ip,
                &antenna.registers,
            ))) {
                return initial_a;
            }
        }
    }

    panic!("failed to solve");
}
