use std::{
    collections::{HashMap, HashSet},
    ops::Deref,
};

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
struct Cable(usize);

impl From<&str> for Cable {
    fn from(value: &str) -> Self {
        Self(
            value
                .trim()
                .as_bytes()
                .into_iter()
                .enumerate()
                .map(|(i, b)| ((b - b'a') as usize) * 26_usize.pow(i as u32))
                .sum(),
        )
    }
}

#[derive(Debug)]
struct ServerRack(HashMap<Cable, HashSet<Cable>>);

impl Deref for ServerRack {
    type Target = HashMap<Cable, HashSet<Cable>>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl From<&str> for ServerRack {
    fn from(value: &str) -> Self {
        Self(
            value
                .trim()
                .lines()
                .map(|line| {
                    let (cable, outputs) = line.trim().split_once(':').unwrap();
                    (
                        cable.into(),
                        outputs.split_whitespace().map(Into::into).collect(),
                    )
                })
                .collect(),
        )
    }
}

impl ServerRack {
    #[must_use]
    fn walk(&self, start: Cable, end: Cable, cache: &mut HashMap<Cable, usize>) -> usize {
        if start == end {
            return 1;
        }

        if let Some(res) = cache.get(&start) {
            return *res;
        }

        let result = self
            .get(&start)
            .unwrap_or(&HashSet::new())
            .iter()
            .map(|output| self.walk(*output, end, cache))
            .sum();

        cache.insert(start, result);
        result
    }
}

fn p1(input: &str) -> usize {
    ServerRack::from(input).walk("you".into(), "out".into(), &mut HashMap::new())
}

fn p2(input: &str) -> usize {
    let out = Cable::from("out");
    let svr = Cable::from("svr");
    let fft = Cable::from("fft");
    let dac = Cable::from("dac");

    let server_rack = ServerRack::from(input);

    let svr_to_fft = server_rack.walk(svr, fft, &mut HashMap::new());
    let fft_to_dac = server_rack.walk(fft, dac, &mut HashMap::new());
    let dac_to_out = server_rack.walk(dac, out, &mut HashMap::new());
    let svr_to_dac = server_rack.walk(svr, dac, &mut HashMap::new());
    let dac_to_fft = server_rack.walk(dac, fft, &mut HashMap::new());
    let fft_to_out = server_rack.walk(fft, out, &mut HashMap::new());

    (svr_to_fft * fft_to_dac * dac_to_out) + (svr_to_dac * dac_to_fft * fft_to_out)
}

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT1: &str = "
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
";

    const INPUT2: &str = "
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
";

    #[test]
    fn p1e1() {
        assert_eq!(p1(INPUT1), 5);
    }

    #[test]
    fn p2e1() {
        assert_eq!(p2(INPUT2), 2);
    }
}
