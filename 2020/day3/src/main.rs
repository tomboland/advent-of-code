#[macro_use]
extern crate nom;
use std::fs::File;
use std::str;
use std::io::prelude::*;
use std::io::BufReader;
use memmap::MmapOptions;
use std::path::Path;
use nom::{IResult};
use nom::combinator::{eof, not, recognize};
use nom::character::complete::{alpha1, digit1, multispace1, newline, alphanumeric1, anychar};
use nom::bytes::complete::{tag, take_until, take_while, take, is_not};
use nom::error::ErrorKind;
use nom::multi::{count, fold_many0, many_till, many1};
use nom::sequence::{terminated, delimited};
use nom::branch::{alt, permutation};

fn match_one_passport_field<'a> (input: &'a [u8]) -> IResult<&'a [u8], &'a [u8]> {
    is_not(alt((tag("\n\n"), eof)))(&input)
}

fn match_valid_passport_field<'a> (input: &'a str) -> IResult<&'a str, (&'a str, &'a str, &'a str, &'a str, &'a str, &'a str, &'a str)> {
    permutation((
        delimited(tag("byr:"), anychar, multispace1),
        delimited(tag("iyr:"), anychar, multispace1),
        delimited(tag("eyr:"), anychar, multispace1),
        delimited(tag("hgt:"), anychar, multispace1),
        delimited(tag("hcl:"), anychar, multispace1),
        delimited(tag("ecl:"), anychar, multispace1),
        delimited(tag("pid"), anychar, multispace1)
    ))(&input)
}

fn passport_parser (input: &[u8]) -> IResult<&[u8], Vec<&[u8]>> {
    fold_many0(
        match_one_passport_field,
        Vec::new(),
        |mut acc: Vec<_>, item| {
            acc.push(item);
            acc
        }
    )(input)
}

fn main() {
    let path = Path::new("/home/tom/aoc-3/aoc-3-test.txt");
    let file = match File::open(&path) {
        Err(why) => panic!("couldn't open {}: {}", path.display(), why),
        Ok(file) => file,
    };
    let mmap = unsafe { match MmapOptions::new().map(&file) {
        Ok(mmap) => mmap,
        Err(e) => panic!(e)
    }};
    let passports = passport_parser(&mmap).unwrap();
    let result = passports
        .1
        .into_iter()
        .map(|passport| match_valid_passport_field(str::from_utf8(passport).unwrap()))
        //.filter(|passport| passport.is_ok())
        .map(|passport| {println!("{:?}", passport); passport})
        .count();

    //let result = match_valid_passport_field(str::from_utf8(passports.1).unwrap());
    println!("{:?}", result);
}
