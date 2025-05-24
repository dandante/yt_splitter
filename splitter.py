#!/usr/bin/env python3

from dataclasses import dataclass, field
import os
from typing import TextIO
from typing_extensions import List

import click
from sh import Command

# ffmpeg -ss 0 -i input.mp3  -to 142  output.mp3
# ffmpeg -ss 0 -i Motor\ Detectives\ 1\ \[4rj8sRdD04s\].mp3 -to 142 "Home Sweet Home (Tom Legenhausen).mp3"
# time ffmpeg -i Motor\ Detectives\ 1\ \[4rj8sRdD04s\].mp3 -f null -

def get_track_length(track_filename: str) -> float:
    ffmpeg = Command("ffmpeg")
    # echo = Command("echo")
    result = ffmpeg("-i", track_filename, "-f", "null", "-", _err_to_out=True)
    if not result:
        raise RuntimeError("Can't calculate track length")
    last_line = result.strip().split("\n")[-1]
    time_str = last_line.split(" ")[1].replace("time=", "")
    return hh_mm_ss_to_s(time_str)

@dataclass
class TrackData():
    name: str
    length: float
    start_time: float


@dataclass
class AlbumData():
    name: str
    total_length: float
    input_file: str
    output_dir: str
    tracks: list[TrackData] = field(default_factory=list)


def hh_mm_ss_to_s(input: str) -> float:
    segs: List[str] = input.split(":")
    hours = "0"
    if len(segs) == 3:
        hours, minutes, seconds = segs
    else:
       minutes, seconds = segs
    out: int = int(hours) * (60 * 60)
    out += int(minutes) * 60
    return out +  float(seconds)


def read_input_data(datafile: TextIO, total_length: float, album_name: str, input_file: str, output_dir: str) -> AlbumData:
    lines = datafile.readlines()
    lines = [x.strip() for x in lines]
    album = AlbumData(album_name, total_length, input_file, output_dir)

    for idx, line in enumerate(lines):
        if idx == 0:
            start_time = 0
            name = line.split(" ", 1)[1]
        else:
            start_time = hh_mm_ss_to_s(line.split(" ")[1])
            name = line.split(" ", 2)[-1]
        if idx == len(lines) - 1:
            end_time = total_length
        else:
            end_time = hh_mm_ss_to_s(lines[idx+1].split(" ")[1])
        track_length = end_time - start_time
        track = TrackData(name, track_length, start_time)
        album.tracks.append(track)
    return album

def split_into_tracks(album: AlbumData) -> None:
    ffmpeg = Command("ffmpeg")
    for track in album.tracks:
        outfile = f"{album.output_dir}/{track.name.replace('/', '_')}.mp3"
        print(f"Writing {track.name}....")
        ffmpeg("-ss", track.start_time, "-i", album.input_file, "-to", track.length, outfile)

@click.command()
@click.argument("inputfile", type=str)
@click.argument("datafile", type=click.File("r"))
@click.option('--name', help="Album Name", required=True)
@click.option("--out", help="output directory", required=True)
def cli(inputfile, datafile, name, out):
    total_length = get_track_length(inputfile)
    album = read_input_data(datafile, total_length, name, inputfile, out)
    os.makedirs(out, exist_ok=True)
    split_into_tracks(album)

if __name__ == "__main__":
    cli() # pyright: ignore[reportCallIssue]
