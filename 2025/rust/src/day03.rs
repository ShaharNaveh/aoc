use std::ops::Deref;

#[derive(Debug)]
struct Bank(Box<[u8]>);

impl From<&str> for Bank {
    fn from(value: &str) -> Self {
        Self(
            value
                .trim()
                .chars()
                .map(|c| c.to_string().parse::<u8>().unwrap())
                .collect(),
        )
    }
}

impl Deref for Bank {
    type Target = [u8];

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl Bank {
    #[must_use]
    fn joltage(&self, amount: usize) -> usize {
        let end = self.len();

        let mut power = 0;
        let mut idx = 0;
        for i in 1..=amount {
            let buf = &self[idx..(end - amount + i)];

            let (nidx, val) =
                buf.iter().enumerate().fold(
                    (0, 0),
                    |max, (index, &val)| if val > max.1 { (index, val) } else { max },
                );

            idx += nidx + 1;
            power += usize::from(val) * 10usize.pow((amount - i).try_into().unwrap());
        }

        power
    }
}

#[derive(Debug)]
struct Banks(Box<[Bank]>);

impl From<&str> for Banks {
    fn from(value: &str) -> Self {
        Self(value.trim().lines().map(Bank::from).collect())
    }
}

impl Deref for Banks {
    type Target = [Bank];

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

fn p1(input: &str) -> usize {
    Banks::from(input)
        .into_iter()
        .map(|bank| bank.joltage(2))
        .sum()
}

fn p2(input: &str) -> usize {
    Banks::from(input)
        .into_iter()
        .map(|bank| bank.joltage(12))
        .sum()
}

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "
987654321111111
811111111111119
234234234234278
818181911112111
";

    #[test]
    fn p1e1() {
        assert_eq!(p1(INPUT), 357);
    }

    #[test]
    fn p2e1() {
        assert_eq!(p2(INPUT), 3121910778619);
    }

    #[test]
    fn joltage() {
        assert_eq!(Bank::from("987654321111111").joltage(2), 98);
        assert_eq!(Bank::from("811111111111119").joltage(2), 89);
        assert_eq!(Bank::from("234234234234278").joltage(2), 78);
        assert_eq!(Bank::from("818181911112111").joltage(2), 92);

        assert_eq!(Bank::from("987654321111111").joltage(12), 987654321111);
    }
}
