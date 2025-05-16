use crate::utils::IVec2;
use std::collections::HashMap;

struct TubeNetwork(HashMap<IVec2, char>);

impl TubeNetwork {
    #[must_use]
    #[inline]
    fn start_pos(&self) -> IVec2 {
        *self.0.keys().find(|k| k.y == 0).unwrap()
    }

    #[must_use]
    fn walk(&self) -> (String, usize) {
        let mut pos = self.start_pos();
        let mut offset = IVec2::Y;
        let mut buf = vec![];
        let mut steps = 0;

        while let Some(&tile) = self.0.get(&pos) {
            steps += 1;

            if tile.is_uppercase() {
                buf.push(tile);
            } else if tile == '+' {
                offset = IVec2::NEIGHBORS_4
                    .into_iter()
                    .filter(|&noffset| noffset != -offset)
                    .find(|&noffset| self.0.contains_key(&(pos + noffset)))
                    .unwrap();
            }

            pos += offset;
        }

        (buf.into_iter().collect(), steps)
    }
}

impl From<&str> for TubeNetwork {
    #[must_use]
    fn from(raw: &str) -> Self {
        let mut grid = HashMap::new();
        for (y, line) in raw
            .trim_end()
            .lines()
            .filter(|line| !line.is_empty())
            .enumerate()
        {
            for (x, tile) in line.chars().enumerate() {
                if tile.is_whitespace() {
                    continue;
                }
                grid.insert(IVec2::new(x as i32, y as i32), tile);
            }
        }

        Self(grid)
    }
}

fn p1(input: &str) -> String {
    TubeNetwork::from(input).walk().0
}

fn p2(input: &str) -> usize {
    TubeNetwork::from(input).walk().1
}

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "
     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ 
";

    #[test]
    fn p1e1() {
        assert_eq!(p1(INPUT), "ABCDEF");
    }

    #[test]
    fn p2e1() {
        assert_eq!(p2(INPUT), 38);
    }
}
