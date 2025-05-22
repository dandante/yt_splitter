#!/usr/bin/env python3

from dataclasses import dataclass
from datetime import date
import sys
from typing import TextIO

import click
from ffmpeg import FFmpeg

# (2 * 60) + 22
# ffmpeg -ss 0 -i input.mp3  -to 142  output.mp3
# ffmpeg -ss 0 -i Motor\ Detectives\ 1\ \[4rj8sRdD04s\].mp3 -to 142 "Home Sweet Home (Tom Legenhausen).mp3"
# time ffmpeg -i Motor\ Detectives\ 1\ \[4rj8sRdD04s\].mp3 -f null -
#

# f = FFmpeg()

@dataclass
class TrackListData():
    pass

@dataclass
class TrackData():
    name: str
    length: int
    start_time: int




def hh_mm_ss_to_s(input: str) -> int:
    hours, minutes, seconds = input.split(":")
    out: int = int(hours) * (60 * 60)
    out += int(minutes) * 60
    out += int(seconds)
    return out


def read_input_data(datafile: TextIO) -> None:
    lines = datafile.readlines()
    lines = [x.strip() for x in lines]
    # print(lines)
    for idx, line in enumerate(lines):
        if idx == 0:
            start_time = 0
        else:
            foo = line.split(" ")[1]
            print(foo);sys.exit(1)

            start_time = hh_mm_ss_to_s(line.split(" ")[1])
        print(idx)
    print("---")
    print(len(lines))

@click.command()
@click.argument("inputfile", type=str)
@click.argument("datafile", type=click.File("r"))
def cli(inputfile, datafile):
    print(inputfile)
    print(datafile)
    read_input_data(datafile)
if __name__ == "__main__":
    # print(hh_mm_ss_to_s("01:01:01"))
    # main()
    cli() # pyright: ignore[reportCallIssue]
