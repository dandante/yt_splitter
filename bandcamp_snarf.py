#!/usr/bin/env python3

"""
Get MY OWN music from bandcamp. I should not have to pay for it.
"""


import os
import sys

import eyed3

def main():
    if len(sys.argv) != 2:
        print("Gimme a dir")
        sys.exit(1)
    dir = sys.argv[1]
    # ls -tr *.mp3 > order.txt
    with open(os.path.join(dir, "order.txt")) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    album = dir.strip("/").split("/")[-1]
    artist = dir.strip("/").split("/")[-2]
    # artist = lines[0].split("-", 1)[0].strip()
    for idx, line in enumerate(lines):
        title = line.split("-", 1)[-1].strip()
        trash = title.split(" ")[-1]
        title = title.replace(trash, "")
        print(f"Processing {title}....")
        filename = os.path.join(dir, line)
        tracknum = idx + 1
        audiofile = eyed3.load(filename)
        if not audiofile.tag:
            audiofile.tag = eyed3.id3.tag.Tag()
        audiofile.tag.artist = artist
        audiofile.tag.album = album
        audiofile.tag.title = title
        audiofile.tag.track_num = tracknum
        audiofile.tag.save()
if __name__ == "__main__":
    main()
