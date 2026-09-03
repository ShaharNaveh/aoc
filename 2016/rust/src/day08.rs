use core::{
    fmt,
    ops::{Deref, DerefMut},
};

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[derive(Clone, Copy, Debug)]
enum Instr {
    Rect { x: usize, y: usize },
    RotateColumn { x: usize, by: usize },
    RotateRow { y: usize, by: usize },
}

impl From<&str> for Instr {
    fn from(value: &str) -> Self {
        let (name, rest) = value.trim().split_once(' ').unwrap();

        if name == "rect" {
            let (x, y) = rest.split_once('x').unwrap();
            return Self::Rect {
                x: x.parse().unwrap(),
                y: y.parse().unwrap(),
            };
        }

        debug_assert_eq!(name, "rotate");

        let (axis, rest) = rest.split_once(' ').unwrap();

        let (axis_idx, by) = {
            let tup = rest.split_once("by").unwrap();

            (
                tup.0
                    .split_once('=')
                    .map(|(_, v)| v.trim().parse().unwrap())
                    .unwrap(),
                tup.1.trim().parse().unwrap(),
            )
        };

        match axis {
            "row" => Self::RotateRow { y: axis_idx, by },
            "column" => Self::RotateColumn { x: axis_idx, by },
            other => unreachable!("got: {other}"),
        }
    }
}

#[derive(Debug)]
struct Instrs(Vec<Instr>);

impl From<&str> for Instrs {
    fn from(value: &str) -> Self {
        Self(value.trim().lines().map(Into::into).collect())
    }
}

impl Deref for Instrs {
    type Target = Vec<Instr>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

#[derive(Clone, Copy, Debug)]
struct Screen<const WIDE: usize, const TALL: usize>([[bool; WIDE]; TALL]);

impl<const WIDE: usize, const TALL: usize> Screen<WIDE, TALL> {
    const fn new() -> Self {
        Self([[false; WIDE]; TALL])
    }

    fn do_instrs(&mut self, instrs: Instrs) {
        for &instr in instrs.iter() {
            self.do_instr(instr);
        }
    }

    fn do_instr(&mut self, instr: Instr) {
        match instr {
            Instr::Rect { x, y } => self.do_rect(x, y),
            Instr::RotateColumn { x, by } => self.do_rotate_column(x, by),
            Instr::RotateRow { y, by } => self.do_rotate_row(y, by),
        }
    }

    fn do_rect(&mut self, x: usize, y: usize) {
        for idx in 0..y {
            self[idx][0..x].fill(true);
        }
    }

    fn do_rotate_column(&mut self, x: usize, by: usize) {
        let mut column: [bool; TALL] = std::array::from_fn(|row| self[row][x]);
        column.rotate_right(by % TALL);

        for row in 0..TALL {
            self[row][x] = column[row];
        }
    }

    fn do_rotate_row(&mut self, y: usize, by: usize) {
        self[y].rotate_right(by % WIDE);
    }

    fn lit_count(&self) -> usize {
        self.into_iter().flatten().filter(|&b| b).count()
    }
}

impl<const WIDE: usize, const TALL: usize> fmt::Display for Screen<WIDE, TALL> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        for (i, row) in self.iter().enumerate() {
            if i > 0 {
                writeln!(f)?;
            }

            for &cell in row {
                write!(f, "{}", if cell { '#' } else { '.' })?;
            }
        }

        Ok(())
    }
}

impl<const WIDE: usize, const TALL: usize> Deref for Screen<WIDE, TALL> {
    type Target = [[bool; WIDE]; TALL];

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl<const WIDE: usize, const TALL: usize> DerefMut for Screen<WIDE, TALL> {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

fn p1(input: &str) -> usize {
    let mut screen = Screen::<50, 6>::new();

    let instrs = Instrs::from(input);
    screen.do_instrs(instrs);
    screen.lit_count()
}

fn p2(input: &str) -> String {
    let mut screen = Screen::<50, 6>::new();

    let instrs = Instrs::from(input);
    screen.do_instrs(instrs);
    screen.to_string().replace('.', " ")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1e1() {
        let mut screen = Screen::<7, 3>::new();
        assert_eq!(screen.lit_count(), 0);

        screen.do_instr("rect 3x2".into());
        assert_eq!(
            screen.to_string(),
            "
###....
###....
.......
"
            .trim()
        );

        screen.do_instr("rotate column x=1 by 1".into());
        assert_eq!(
            screen.to_string(),
            "
#.#....
###....
.#.....
"
            .trim()
        );

        screen.do_instr("rotate row y=0 by 4".into());
        assert_eq!(
            screen.to_string(),
            "
....#.#
###....
.#.....
"
            .trim()
        );

        screen.do_instr("rotate column x=1 by 1".into());
        assert_eq!(
            screen.to_string(),
            "
.#..#.#
#.#....
.#.....
"
            .trim()
        );
    }
}
