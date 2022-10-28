use std::collections::BTreeSet;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let mut expenses_set: BTreeSet<i32> = BTreeSet::new();
    let mut expenses_vec: Vec<i32> = Vec::new();
    if let Ok(lines) = read_lines("./aoc-1.txt") {
        for line in lines {
            if let Ok(unparsed_expense) = line {
                if let Ok(expense) = unparsed_expense.parse::<i32>() {
                    &expenses_vec.push(expense);
                    &expenses_set.insert(expense);
                }
            }
        }
    }

    if let Some((a, b, c)) = find_triple_that_sum_to(2020, &expenses_set, &expenses_vec) {
        println!("{}", a * b * c);
    }
}

fn find_triple_that_sum_to(
    sum: i32,
    item_set: &BTreeSet<i32>,
    item_vec: &Vec<i32>,
) -> Option<(i32, i32, i32)> {
    for (idx, item) in item_vec.iter().enumerate() {
        for jdx in idx + 1..item_vec.len() {
            if item_set.contains(&(sum - item - item_vec[jdx])) {
                //return Some((*item, item_vec[jdx], sum - item - item_vec[jdx]));
                println!("{:?}", (*item * item_vec[jdx] * sum - item - item_vec[jdx]));
            }
        }
    }
    None
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
