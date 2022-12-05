from enum import Enum, auto
from typing import NewType, Literal, Optional, Tuple, Iterable, cast
import re
from hypothesis import given, strategies as st

Score = NewType("Score", int)
EncodedRPS = Literal["A", "B", "C"]
EncodedWLD = Literal["X", "Y", "Z"]

input_line_re = re.compile('(?P<abc>[ABC]) (?P<xyz>[XYZ])')


@given(st.sampled_from(["A", "B", "C"]), st.sampled_from(["X", "Y", "Z"]))
def test_parse_input_line_parses_correct_data(abc, xyz):
    s = f"{abc} {xyz}\n"
    match parse_input_line(s):
        case RPS(), RPS(): return None
        case None: raise AssertionError()


def test_actual_input_returns_13509():
    with open("input", 'r') as f:
        score = score_from_lines(f)
    assert score == 13509


class RPS(Enum):
    Rock = auto()
    Paper = auto()
    Scissors = auto()


class WLD(Enum):
    Win = auto()
    Lose = auto()
    Draw = auto()


def parse_input_line(line: str) -> Optional[Tuple[RPS, WLD]]:
    m = re.match(input_line_re, line)
    if not m or not m.group('abc') or not m.group('xyz'):
        return None
    abc = cast(EncodedRPS, m.group('abc'))
    xyz = cast(EncodedWLD, m.group('xyz'))
    if abc and xyz:
        return (char_to_rps(abc), char_to_wld(xyz))
    else:
        return None


def char_to_rps(c: EncodedRPS) -> RPS:
    match c:
        case "A" | "X": return RPS.Rock
        case "B" | "Y": return RPS.Paper
        case "C" | "Z": return RPS.Scissors


def char_to_wld(c: EncodedWLD) -> WLD:
    match c:
        case "X": return WLD.Lose
        case "Y": return WLD.Draw
        case "Z": return WLD.Win


def score_for_rps(rps: RPS) -> Score:
    match rps:
        case RPS.Rock: return Score(1)
        case RPS.Paper: return Score(2)
        case RPS.Scissors: return Score(3)


def rps_for_desired_wld(rps: RPS, wld: WLD) -> RPS:
    match rps, wld:
        case _, WLD.Draw: return rps
        case RPS.Rock, WLD.Win: return RPS.Paper
        case RPS.Rock, WLD.Lose: return RPS.Scissors
        case RPS.Paper, WLD.Win: return RPS.Scissors
        case RPS.Paper, WLD.Lose: return RPS.Rock
        case RPS.Scissors, WLD.Win: return RPS.Rock
        case RPS.Scissors, WLD.Lose: return RPS.Paper


def win_lose_draw(them: RPS, me: RPS) -> WLD:
    match (them, me):
        case (RPS.Rock, RPS.Rock): return WLD.Draw
        case (RPS.Rock, RPS.Paper): return WLD.Win
        case (RPS.Rock, RPS.Scissors): return WLD.Lose
        case (RPS.Paper, RPS.Rock): return WLD.Lose
        case (RPS.Paper, RPS.Paper): return WLD.Draw
        case (RPS.Paper, RPS.Scissors): return WLD.Win
        case (RPS.Scissors, RPS.Rock): return WLD.Win
        case (RPS.Scissors, RPS.Paper): return WLD.Lose
        case (RPS.Scissors, RPS.Scissors): return WLD.Draw


def wld_to_score(wld: WLD) -> Score:
    match wld:
        case WLD.Win: return Score(6)
        case WLD.Lose: return Score(0)
        case WLD.Draw: return Score(3)


def score_from_lines(f: Iterable[str]) -> Score:
    totes = Score(0)
    for line in f:
        parsed = parse_input_line(line)
        if not parsed:
            continue
        abc, xyz = parsed
        desired_rps = rps_for_desired_wld(abc, xyz)
        totes = Score(totes + wld_to_score(win_lose_draw(abc, desired_rps)) +
                      score_for_rps(desired_rps))
    return totes


if __name__ == "__main__":
    with open("input", 'r') as f:
        score = score_from_lines(f)

    print(score)
