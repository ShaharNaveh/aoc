use std::{
    collections::{HashMap, HashSet},
    ops::Deref,
};

const SEP: &str = "\n\n";

#[inline]
#[must_use]
fn without_last(s: &str) -> &str {
    let mut chars = s.chars();
    chars.next_back();
    chars.as_str()
}

#[inline]
#[must_use]
fn last_word(s: &str) -> &str {
    without_last(s.trim().split_whitespace().last().unwrap())
}

#[derive(Clone, Copy, Debug)]
struct StateCondition {
    write: u8,
    offset: isize,
    nstate: char,
}

impl From<&str> for StateCondition {
    fn from(raw: &str) -> Self {
        let mut it = raw.trim().lines();
        it.next();
        let write = last_word(it.next().unwrap()).parse().unwrap();
        let offset = if last_word(it.next().unwrap()) == "right" {
            1
        } else {
            -1
        };

        let nstate = last_word(it.next().unwrap()).chars().next().unwrap();
        Self {
            write,
            offset,
            nstate,
        }
    }
}

#[derive(Debug)]
struct State([StateCondition; 2]);

impl From<&str> for State {
    fn from(raw: &str) -> Self {
        Self(
            raw.trim()
                .lines()
                .map(|l| l.trim())
                .collect::<Vec<_>>()
                .chunks(4)
                .map(|chunk| chunk.to_vec().join("\n"))
                .map(|s| StateCondition::from(s.as_str()))
                .collect::<Vec<_>>()
                .try_into()
                .unwrap(),
        )
    }
}

impl Deref for State {
    type Target = [StateCondition; 2];

    #[inline]
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

#[derive(Debug)]
struct States(HashMap<char, State>);

impl From<&str> for States {
    fn from(raw: &str) -> Self {
        Self(
            raw.trim()
                .split(SEP)
                .filter_map(|raw_state| raw_state.split_once('\n'))
                .map(|(name, state)| (last_word(name).chars().next().unwrap(), State::from(state)))
                .collect(),
        )
    }
}

#[derive(Debug)]
struct TuringMachineBlueprints {
    begin: char,
    steps: usize,
    states: States,
}

impl From<&str> for TuringMachineBlueprints {
    fn from(raw: &str) -> Self {
        let (raw_metadata, raw_states) = raw.trim().split_once(SEP).unwrap();
        let mut it = raw_metadata.lines();
        let begin = last_word(it.next().unwrap()).chars().next().unwrap();

        let steps = it
            .next()
            .unwrap()
            .split_whitespace()
            .rev()
            .nth(1)
            .unwrap()
            .parse()
            .unwrap();

        Self {
            begin,
            steps,
            states: States::from(raw_states),
        }
    }
}

#[derive(Debug)]
struct TuringMachine {
    tape: HashSet<isize>,
    cursor: isize,
    state: char,
    states: States,
}

impl TuringMachine {
    #[inline]
    #[must_use]
    fn new(state: char, states: States) -> Self {
        Self {
            state,
            states,
            tape: HashSet::new(),
            cursor: 0,
        }
    }
}

impl Iterator for TuringMachine {
    type Item = usize;

    fn next(&mut self) -> Option<Self::Item> {
        let state = self.states.0.get(&self.state).unwrap();
        let curr_val = self.tape.contains(&self.cursor) as u8;
        let state_cond = state[curr_val as usize];
        if state_cond.write == 1 {
            self.tape.insert(self.cursor)
        } else {
            self.tape.remove(&self.cursor)
        };

        self.cursor += state_cond.offset;
        self.state = state_cond.nstate;

        Some(self.tape.len())
    }
}

fn p1(input: &str) -> usize {
    let blueprint = TuringMachineBlueprints::from(input);
    TuringMachine::new(blueprint.begin, blueprint.states)
        .nth(blueprint.steps - 1)
        .unwrap()
}

pub fn solve(input: &str) {
    println!("{}", p1(&input));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1e1() {
        let input = "
Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A.
";

        assert_eq!(p1(input), 3);
    }
}
