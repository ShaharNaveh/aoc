use std::collections::HashSet;

const PUZZLE_FILE: &str = "puzzle.txt";

#[derive(Clone, Copy, Debug)]
struct Registers {
    ip: usize,
    registers: [usize; 6],
}

impl Registers {
    fn new() -> Self {
        Self {
            ip: 0,
            registers: [0; 6],
        }
    }

    fn with_ip(mut self, ip: usize) -> Self {
        self.ip = ip;
        self
    }
}

#[derive(Clone, Debug)]
struct Instruction {
    opcode: String,
    a: usize,
    b: usize,
    c: usize,
}

impl Instruction {
    fn execute(&self, registers: &[usize; 6]) -> usize {
        match self.opcode.as_str() {
            "addr" => registers[self.a] + registers[self.b],
            "addi" => registers[self.a] + self.b,
            "mulr" => registers[self.a] * registers[self.b],
            "muli" => registers[self.a] * self.b,
            "banr" => registers[self.a] & registers[self.b],
            "bani" => registers[self.a] & self.b,
            "borr" => registers[self.a] | registers[self.b],
            "bori" => registers[self.a] | self.b,
            "setr" => registers[self.a],
            "seti" => self.a,
            "gtir" => (self.a > registers[self.b]) as usize,
            "gtri" => (registers[self.a] > self.b) as usize,
            "gtrr" => (registers[self.a] > registers[self.b]) as usize,
            "eqir" => (self.a == registers[self.b]) as usize,
            "eqri" => (registers[self.a] == self.b) as usize,
            "eqrr" => (registers[self.a] == registers[self.b]) as usize,
            _ => unreachable!(),
        }
    }
}

impl From<&str> for Instruction {
    fn from(raw: &str) -> Self {
        let mut iter = raw.split_whitespace();
        Self {
            opcode: iter.next().unwrap().into(),
            a: iter.next().unwrap().parse().unwrap(),
            b: iter.next().unwrap().parse().unwrap(),
            c: iter.next().unwrap().parse().unwrap(),
        }
    }
}

fn parse_puzzle(puzzle_file: &str) -> (Registers, Vec<Instruction>) {
    let inp = std::fs::read_to_string(puzzle_file).unwrap();

    let mut registers = Registers::new();
    let mut instructions: Vec<Instruction> = Vec::new();

    for line in inp.lines() {
        if line.starts_with('#') {
            registers = registers.with_ip(line.split_whitespace().nth(1).unwrap().parse().unwrap());
        } else {
            instructions.push(line.into());
        }
    }
    (registers, instructions)
}

fn p1(puzzle_file: &str) -> usize {
    let (mut reg, instructions) = parse_puzzle(puzzle_file);
    let mut ip = 0;
    while ip < instructions.len() {
        reg.registers[reg.ip] = ip;
        let instruction = &instructions[reg.registers[reg.ip]];
        reg.registers[instruction.c] = instruction.execute(&reg.registers);
        ip = reg.registers[reg.ip] + 1;

        if (instruction.opcode == "eqrr") && (instruction.b == 0) {
            break;
        }
    }

    let idx = instructions[0].c;
    reg.registers[idx]
}

fn p2(puzzle_file: &str) -> usize {
    let (mut reg, instructions) = parse_puzzle(puzzle_file);
    let idx = instructions[0].c;
    let mut seen = HashSet::new();
    let mut last = 0;
    let mut ip = 0;
    while ip < instructions.len() {
        reg.registers[reg.ip] = ip;
        let instruction = &instructions[reg.registers[reg.ip]];
        reg.registers[instruction.c] = instruction.execute(&reg.registers);
        ip = reg.registers[reg.ip] + 1;

        if (instruction.opcode == "eqrr") && (instruction.b == 0) {
            let tmp_last = reg.registers[idx];
            if seen.contains(&tmp_last) {
                break;
            }
            last = tmp_last;
            seen.insert(last);
        }
    }
    last
}

fn main() {
    println!("{}", p1(PUZZLE_FILE));
    println!("{}", p2(PUZZLE_FILE));
}
