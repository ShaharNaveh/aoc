use std::{env, fs};

mod utils;

mod day01;
mod day02;
mod day03;
mod day04;
mod day05;
mod day06;
mod day07;
/*
mod day08;
mod day09;
mod day10;
mod day11;
mod day12;
*/

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
        /*
        "08" => day08::solve(&input),
        "09" => day09::solve(&input),
        "10" => day10::solve(&input),
        "11" => day11::solve(&input),
        "12" => day12::solve(&input),
        */
        _ => eprintln!("Day {day} not found"),
    }
}
