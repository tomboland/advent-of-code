
#[macro_use]
extern crate nom;
use std::fs::File;
use std::io::prelude::*;
use std::io::BufReader;
use std::path::Path;
use nom::IResult;
use nom::sequence::terminated;
use nom::character::complete::{alpha1, digit1, multispace1};
use nom::bytes::complete::tag;
use nom::error::ErrorKind;
use nom::sequence::tuple;
use std::fmt::Debug;

#[derive(Debug)]
struct PasswordPolicy {
    min: usize,
    max: usize,
    enforced_char: String,
    password: String
}

fn parse_password_policy_line<'a> (input: &'a str) -> Option<PasswordPolicy> {
    match tuple::<_, _, (_, ErrorKind), _>((
        terminated(digit1, tag("-")),
        terminated(digit1, multispace1),
        terminated(alpha1, terminated(tag(":"), multispace1)),
        alpha1
    ))(input) {
        Ok((_, (min, max, enforced_char, password))) => Some(PasswordPolicy {
            min: min.parse::<usize>().unwrap(),
            max: max.parse::<usize>().unwrap(),
            enforced_char: enforced_char.into(),
            password: password.to_string()
        }),
        Err(e) => { println!("{:?}", e); None }
    }
}

fn password_meets_policy (pp: PasswordPolicy) -> bool {
    let PasswordPolicy { min, max, enforced_char, password } = pp;
    match password.matches(&enforced_char).count() {
        count if count >= min && count <= max => true,
        _ => false
    }
}

fn main() {
    let path = Path::new("/home/tom/aoc-2/aoc-2.txt");
    let file = match File::open(&path) {
        Err(why) => panic!("couldn't open {}: {}", path.display(), why),
        Ok(file) => file,
    };
    let reader = BufReader::new(file);
    let result = reader
        .lines()
        .map(|line| parse_password_policy_line(&line.unwrap()))
        .map(|pp| password_meets_policy(pp.unwrap()))
        .filter(|x| *x == true)
        .count();
    println!("{:?}", result)
}
