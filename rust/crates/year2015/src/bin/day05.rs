use util::{Day, aoc_main};

trait Policy {
    fn is_valid(&self, s: &str) -> bool;
}

struct NiceStringValidator<P: Policy> {
    policy: P,
}

impl<P: Policy> NiceStringValidator<P> {
    fn new(policy: P) -> Self {
        Self { policy }
    }

    fn is_valid(&self, s: &str) -> bool {
        self.policy.is_valid(s)
    }
}

struct Part1Policy;

impl Policy for Part1Policy {
    fn is_valid(&self, s: &str) -> bool {
        let chars = s.chars().collect::<Vec<_>>();

        let mut vowels = 0;
        let mut twice_in_row = false;

        for (i, c) in chars.iter().enumerate() {
            vowels += usize::from("aeiou".contains(*c));

            let Some(nc) = chars.get(i + 1) else { break };
            twice_in_row = twice_in_row || c == nc;

            if matches!(format!("{c}{nc}").as_ref(), "ab" | "cd" | "pq" | "xy") {
                return false;
            }
        }

        twice_in_row && (vowels >= 3)
    }
}

struct Part2Policy;

impl Policy for Part2Policy {
    fn is_valid(&self, s: &str) -> bool {
        if !s
            .chars()
            .collect::<Vec<_>>()
            .windows(3)
            .any(|w| w[0] == w[2])
        {
            return false;
        }

        s.char_indices().any(|(i, _)| {
            s.get(i..=i + 1)
                .is_some_and(|pair| s.get(i + 2..).is_some_and(|rest| rest.contains(pair)))
        })
    }
}

struct Day05;

impl Day for Day05 {
    type Parsed = Vec<String>;

    fn parse(input: &str) -> Self::Parsed {
        input.trim().lines().map(Into::into).collect()
    }

    fn part1(input: &Self::Parsed) -> usize {
        let validator = NiceStringValidator::new(Part1Policy);
        input.iter().filter(|s| validator.is_valid(s)).count()
    }

    fn part2(input: &Self::Parsed) -> usize {
        let validator = NiceStringValidator::new(Part2Policy);
        input.iter().filter(|s| validator.is_valid(s)).count()
    }
}

aoc_main!(Day05);

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn part1() {
        let validator = NiceStringValidator::new(Part1Policy);
        for (input, expected) in [
            ("ugknbfddgicrmopn", true),
            ("aaa", true),
            ("jchzalrnumimnmhp", false),
            ("haegwjzuvuyypxyu", false),
            ("dvszwmarrgswjxmb", false),
        ] {
            assert_eq!(validator.is_valid(input), expected, "{input}");
        }
    }

    #[test]
    fn part2() {
        let validator = NiceStringValidator::new(Part2Policy);
        for (input, expected) in [
            ("qjhvhtzxzqqjkmpb", true),
            ("xxyxx", true),
            ("uurcxstgmygtbstg", false),
            ("ieodomkazucvgmuy", false),
        ] {
            assert_eq!(validator.is_valid(input), expected, "{input}");
        }
    }
}
