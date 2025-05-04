use std::{env, fs};

mod day01;
mod day02;
mod day03;
mod day04;
mod day05;
mod day06;
mod day07;
mod day08;

fn main() {
    let day = env::args().nth(1).unwrap_or("01".to_string());
    let input =
        fs::read_to_string(format!("input/day{}.txt", day)).expect("Failed to read input file");

    match day.as_str() {
        "01" => day01::solve(&input),
        "02" => day02::solve(&input),
        "03" => day03::solve(&input),
        "04" => day04::solve(&input),
        "05" => day05::solve(&input),
        "06" => day06::solve(&input),
        "07" => day07::solve(&input),
        "08" => day08::solve(&input),
        _ => eprintln!("Day {day} not found"),
    }
}
