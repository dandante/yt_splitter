#!/usr/bin/env python3

from dataclasses import dataclass, field
import os
import sys
from typing import TextIO

import click
from mutagen.id3 import ID3
from mutagen.id3._frames import TIT2, TALB, TRCK, TPE1
from sh import Command  # pyright: ignore[reportMissingTypeStubs]

# ffmpeg -ss 0 -i input.mp3  -to 142  output.mp3
# ffmpeg -ss 0 -i Motor\ Detectives\ 1\ \[4rj8sRdD04s\].mp3 -to 142 "Home Sweet Home (Tom Legenhausen).mp3"
# time ffmpeg -i Motor\ Detectives\ 1\ \[4rj8sRdD04s\].mp3 -f null -


def get_track_length(track_filename: str) -> float:
    print("Getting track length....")
    ffmpeg = Command("ffmpeg")
    # echo = Command("echo")
    result = ffmpeg("-i", track_filename, "-f", "null", "-", _err_to_out=True)
    if not result:
        raise RuntimeError("Can't calculate track length")
    last_line = result.strip().split("\n")[-1]
    time_str = last_line.split(" ")[1].replace("time=", "")
    return hh_mm_ss_to_s(time_str)


@dataclass
class TrackData:
    name: str
    length: float
    start_time: float
    track_num: str
    path: str = ""
    artist: str = ""


@dataclass
class AlbumData:
    name: str
    total_length: float
    input_file: str
    output_dir: str
    parse: bool
    tracks: list[TrackData] = field(default_factory=list)
    artist: str = ""


def hh_mm_ss_to_s(input: str) -> float:
    segs: list[str] = input.split(":")
    hours = "0"
    if len(segs) == 3:
        hours, minutes, seconds = segs
    else:
        minutes, seconds = segs
    out: int = int(hours) * (60 * 60)
    out += int(minutes) * 60
    return out + float(seconds)


def read_input_data(
    datafile: TextIO,
    total_length: float,
    album_name: str,
    input_file: str,
    output_dir: str,
    parse: bool,
) -> AlbumData:
    lines = datafile.readlines()
    lines = [x.strip() for x in lines]
    album = AlbumData(album_name, total_length, input_file, output_dir, parse)

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
            end_time = hh_mm_ss_to_s(lines[idx + 1].split(" ")[1])
        track_length = end_time - start_time
        track_num = line.split(" ")[0]
        track = TrackData(name, track_length, start_time, track_num)
        if parse:
            track.artist = name.split("(")[-1].replace(")", "")
        album.tracks.append(track)
    return album


def tag_track(track: TrackData, album: AlbumData) -> None:
    print(f"Tagging {track.name}....")
    audio = ID3(track.path)
    audio.add(TIT2(encoding=3, text=track.name))
    audio.add(TALB(encoding=3, text=album.name))
    audio.add(TRCK(encoding=3, text=track.track_num))
    artist = None
    if album.artist:
        artist = album.artist
    if track.artist:
        artist = track.artist
    if artist:
        audio.add(TPE1(encoding=3, text=artist))
    audio.save()


def split_into_tracks(album: AlbumData) -> None:
    ffmpeg = Command("ffmpeg")
    for track in album.tracks:
        outfile = (
            f"{album.output_dir}/{track.track_num}. {track.name.replace('/', '_')}.mp3"
        )
        track.path = outfile
        print(f"Writing {track.name}....")
        ffmpeg(
            "-ss",
            track.start_time,
            "-i",
            album.input_file,
            "-to",
            track.length,
            outfile,
        )
        tag_track(track, album)


@click.command()
@click.argument("inputfile", type=str)
@click.argument("datafile", type=click.File("r"))
@click.option("--name", help="Album Name", required=True)
@click.option("--out", help="output directory", required=True)
@click.option("--artist", help="album artist", required=False)
@click.option("--parse", help="parse track artist from name", is_flag=True)
def cli(inputfile, datafile, name, out, artist, parse):
    if artist and parse:
        print("Pick one of --artist or --parse, but not both.")
        sys.exit(1)
    total_length = get_track_length(inputfile)
    album = read_input_data(datafile, total_length, name, inputfile, out, parse)
    if artist:
        album.artist = artist
    os.makedirs(out, exist_ok=True)
    split_into_tracks(album)


if __name__ == "__main__":
    cli()  # pyright: ignore[reportCallIssue]
