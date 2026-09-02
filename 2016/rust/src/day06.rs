use std::collections::HashMap;

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[derive(Debug)]
struct Messages(Vec<Vec<char>>);

impl Messages {
    fn counter(&self, idx: usize) -> HashMap<char, usize> {
        let mut counter = HashMap::new();
        for msg in &self.0 {
            *counter.entry(msg[idx]).or_insert(0) += 1;
        }
        counter
    }

    fn most_common_at(&self, idx: usize) -> char {
        self.counter(idx)
            .iter()
            .max_by_key(|&(_, v)| *v)
            .map(|(k, _)| *k)
            .unwrap()
    }

    fn least_common_at(&self, idx: usize) -> char {
        self.counter(idx)
            .iter()
            .min_by_key(|&(_, v)| *v)
            .map(|(k, _)| *k)
            .unwrap()
    }

    fn to_corrected(&self) -> String {
        let len = self.0[0].len();
        let mut buf = String::new();
        for idx in 0..len {
            buf.push(self.most_common_at(idx));
        }
        buf
    }

    fn to_original(&self) -> String {
        let len = self.0[0].len();
        let mut buf = String::new();
        for idx in 0..len {
            buf.push(self.least_common_at(idx));
        }
        buf
    }
}

impl From<&str> for Messages {
    fn from(value: &str) -> Self {
        Self(
            value
                .trim()
                .lines()
                .map(|s| s.trim())
                .filter(|l| !l.is_empty())
                .map(|s| s.chars().collect())
                .collect(),
        )
    }
}

fn p1(input: &str) -> String {
    Messages::from(input).to_corrected()
}

fn p2(input: &str) -> String {
    Messages::from(input).to_original()
}

#[cfg(test)]
mod tests {
    use super::*;

    const MSG: &str = "
eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar
";

    #[test]
    fn p1e1() {
        assert_eq!(p1(MSG), "easter");
    }

    #[test]
    fn p2e1() {
        assert_eq!(p2(MSG), "advent");
    }
}
