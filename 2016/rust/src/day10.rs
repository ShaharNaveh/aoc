use std::{
    collections::{HashMap, HashSet},
    fmt,
    ops::{Deref, DerefMut, Index},
};

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[derive(Copy, Clone, Debug)]
struct LowHigh<T>
where
    T: Copy + fmt::Debug,
{
    low: T,
    high: T,
}

#[derive(Copy, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Microchip(u8);

impl From<u8> for Microchip {
    fn from(value: u8) -> Self {
        Self(value)
    }
}

impl From<Microchip> for usize {
    fn from(value: Microchip) -> Self {
        Self::from(value.0)
    }
}

impl From<&str> for Microchip {
    fn from(mut value: &str) -> Self {
        value = value.trim();
        debug_assert!(value.starts_with("value "));

        Self(value.trim_start_matches("value ").parse().unwrap())
    }
}

type Microchips = LowHigh<Option<Microchip>>;

impl Microchips {
    fn new(a: Microchip, b: Microchip) -> Self {
        let mut this = Self::default();
        this.push(a);
        this.push(b);
        this
    }

    const fn is_ready(&self) -> bool {
        self.low.is_some() && self.high.is_some()
    }

    fn push(&mut self, microchip: Microchip) {
        debug_assert!(!self.is_ready(), "can't push into full slot");
        debug_assert!(self.low.is_none());
        debug_assert_ne!(self.low, Some(microchip));
        debug_assert_ne!(self.high, Some(microchip));

        if let Some(high) = self.high {
            if high > microchip {
                self.low = Some(microchip);
            } else {
                self.low = self.high;
                self.high = Some(microchip);
            }
        } else {
            self.high = Some(microchip);
        }
    }

    fn take_if_ready(&mut self) -> Option<Self> {
        self.is_ready().then(|| Self {
            low: self.low.take(),
            high: self.high.take(),
        })
    }

    const fn is_empty(&self) -> bool {
        self.low.is_none() && self.high.is_none()
    }
}

impl Default for Microchips {
    fn default() -> Self {
        Self {
            low: None,
            high: None,
        }
    }
}

impl PartialEq for Microchips {
    fn eq(&self, other: &Self) -> bool {
        self.low == other.low && self.high == other.high
    }
}

#[derive(Copy, Clone, Debug, Eq, Hash, PartialEq)]
struct BotId(u8);

impl From<&str> for BotId {
    fn from(mut value: &str) -> Self {
        value = value.trim();
        debug_assert!(value.starts_with("bot "));
        Self(value.trim_start_matches("bot ").parse().unwrap())
    }
}

impl From<u8> for BotId {
    fn from(value: u8) -> Self {
        Self(value)
    }
}

impl From<BotId> for u8 {
    fn from(value: BotId) -> Self {
        value.0
    }
}

#[derive(Copy, Clone, Debug)]
enum BotOrOutput {
    Bot(BotId),
    Output(OutputId),
}

impl From<BotId> for BotOrOutput {
    fn from(value: BotId) -> Self {
        Self::Bot(value)
    }
}

impl From<OutputId> for BotOrOutput {
    fn from(value: OutputId) -> Self {
        Self::Output(value)
    }
}

impl From<&str> for BotOrOutput {
    fn from(value: &str) -> Self {
        let (name, raw_id) = value.trim().split_once(' ').unwrap();
        let id = raw_id.parse::<u8>().unwrap();

        match name {
            "bot" => BotId::from(id).into(),
            "output" => OutputId::from(id).into(),
            other => unreachable!("{other}"),
        }
    }
}

type Target = LowHigh<BotOrOutput>;

impl From<&str> for Target {
    fn from(mut value: &str) -> Self {
        value = value.trim();
        debug_assert!(value.starts_with("low to "));

        let (low_chunk, high_chunk) = value.split_once(" and ").unwrap();
        let low = low_chunk.trim_start_matches("low to ").into();
        let high = high_chunk.trim_start_matches("high to ").into();

        Self { low, high }
    }
}

#[derive(Copy, Clone, Debug)]
struct Bot {
    microchips: Microchips,
    target: Target,
}

impl Bot {
    fn new(target: Target) -> Self {
        Self {
            microchips: Microchips::default(),
            target,
        }
    }

    fn take_if_ready(&mut self) -> Option<Microchips> {
        self.microchips.take_if_ready()
    }

    const fn is_empty(&self) -> bool {
        self.microchips.is_empty()
    }
}

#[derive(Debug, Default)]
struct Bots(HashMap<BotId, Bot>);

impl Deref for Bots {
    type Target = HashMap<BotId, Bot>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for Bots {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

#[derive(Copy, Clone, Debug, Eq, Hash, PartialEq)]
struct OutputId(u8);

impl From<u8> for OutputId {
    fn from(value: u8) -> Self {
        Self(value)
    }
}

#[derive(Debug, Default)]
struct Outputs(HashMap<OutputId, Microchip>);

impl Deref for Outputs {
    type Target = HashMap<OutputId, Microchip>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for Outputs {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

#[derive(Debug)]
struct Factory {
    bots: Bots,
    outputs: Outputs,
}

impl Factory {
    fn responsible<T, U>(&mut self, n0: T, n1: U) -> BotId
    where
        T: Into<Microchip> + Copy,
        U: Into<Microchip> + Copy,
    {
        let microchips = Microchips::new(n0.into(), n1.into());
        let a = n0.into();
        let b = n1.into();

        let mut seen = HashMap::new();
        let bot_ids = self.bot_ids();

        loop {
            for bot_id in &bot_ids {
                let bot = self[bot_id];
                if let Some(microchip) = bot.microchips.low {
                    seen.entry(bot_id)
                        .or_insert_with(HashSet::new)
                        .insert(microchip);
                }

                if let Some(microchip) = bot.microchips.high {
                    seen.entry(bot_id)
                        .or_insert_with(HashSet::new)
                        .insert(microchip);
                }
            }

            if let Some(id) = seen
                .iter()
                .find_map(|(id, saw)| (saw.contains(&a) && saw.contains(&b)).then_some(id))
            {
                return **id;
            };

            if self.is_done() {
                break;
            }

            self.tick();
        }

        panic!("did not find {microchips:?}");
    }

    fn tick(&mut self) {
        let bot_ids = self.bot_ids();
        let mut pending = vec![];

        for bot_id in bot_ids {
            let Some(microchips) = self.bots.get_mut(&bot_id).unwrap().take_if_ready() else {
                continue;
            };

            let target = self[bot_id].target;
            pending.push((target.low, microchips.low.unwrap()));
            pending.push((target.high, microchips.high.unwrap()));
        }

        for (target, value) in pending {
            self.do_action(target, value);
        }
    }

    fn do_action(&mut self, target: BotOrOutput, value: Microchip) {
        match target {
            BotOrOutput::Bot(id) => self.bots.get_mut(&id).unwrap().microchips.push(value),
            BotOrOutput::Output(id) => {
                self.outputs.insert(id, value);
            }
        }
    }

    fn is_done(&self) -> bool {
        self.bots.values().all(|bot| bot.is_empty())
    }

    fn bot_ids(&self) -> Vec<BotId> {
        self.bots.keys().copied().collect()
    }

    fn tick_until_done(&mut self) {
        loop {
            if self.is_done() {
                break;
            }

            self.tick()
        }
    }
}

impl From<&str> for Factory {
    fn from(raw: &str) -> Self {
        let mut bots = Bots::default();
        let mut values = HashMap::new();

        for line in raw.trim().lines() {
            if line.starts_with("bot") {
                let (id_chunk, target_chunk) = line.split_once("gives").unwrap();
                let bot_id = id_chunk.into();
                let target = target_chunk.into();

                bots.insert(bot_id, Bot::new(target));
            } else {
                debug_assert!(line.starts_with("value"));
                let (microchip_chunk, id_chunk) = line.split_once(" goes to ").unwrap();

                let id = id_chunk.into();
                let microchip = microchip_chunk.into();

                values
                    .entry(id)
                    .or_insert(Microchips::default())
                    .push(microchip);
            }
        }

        for (id, microchips) in values {
            bots.get_mut(&id).unwrap().microchips = microchips;
        }

        Self {
            bots,
            outputs: Outputs::default(),
        }
    }
}

impl Index<&BotId> for Factory {
    type Output = Bot;

    fn index(&self, bot_id: &BotId) -> &Self::Output {
        &self.bots[bot_id]
    }
}

impl Index<BotId> for Factory {
    type Output = Bot;

    fn index(&self, bot_id: BotId) -> &Self::Output {
        &self[&bot_id]
    }
}

fn p1(input: &str) -> u8 {
    let mut factory = Factory::from(input);
    factory.responsible(61, 17).into()
}

fn p2(input: &str) -> usize {
    let mut factory = Factory::from(input);
    factory.tick_until_done();
    let outputs = factory.outputs;

    let mut res = 1;
    for id in 0..=2 {
        res *= usize::from(outputs[&id.into()]);
    }

    res
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1e1() {
        let instr = "
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2
"
        .trim();
        let mut factory = Factory::from(instr);
        dbg!(&factory);
        assert_eq!(factory.responsible(5, 2), 3.into());
    }
}
