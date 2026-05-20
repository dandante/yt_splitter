# audio splitter

Given an MP3 audio file and a text file in a certain format, split the
MP3 file into pieces and name and tag them according to the text file.

For example, given a source file `source.mp3` and a text file `source.txt`
that looks like this:

```text
01 Introduction (Ralph Bowles)                                        
02 1:38 Cleveland Blues (Jenes Cottrell)                                    
03 6:04 Ring-Ding Song (Jenes Cottrell)                                    
04 9:00 Fisher's Hornpipe (Ira Mullins)                                    
```

The following command will split up the source file into correctly
named/tagged files in the `output` directory:

```bash
./splitter.py  --out output --name "My Album"  --parse  source.mp3 source.txt
```

Sometimes the artist is the same on each track, and not listed in the text file:

```text

01 Bull Run Picnic/Golden Star Hornpipe/Belvedere Hornpipe
02 9:52 John Dye/Cowboy's Dream                                       
03 15:37 John Sharp's Tune/Jump In The Well Pretty Little Miss                      
04 24:28 Old Mose (cut off)                                                 
```

You can split it like this:

```bash
./splitter.py  --out output --name "My Album"  --artist "Joe Blow" source.mp3 source.txt
```

Here's the script's help message:

```text
$ ./splitter.py --help
Usage: splitter.py [OPTIONS] INPUTFILE DATAFILE

Options:
  --name TEXT    Album Name  [required]
  --out TEXT     output directory  [required]
  --artist TEXT  album artist
  --parse        parse track artist from name
  --help         Show this message and exit.
```

## Installation

Make sure `ffmpeg` is installed. On a mac this can be done with the command

```bash
brew install ffmpeg
```

After cloning this repo and changing into its directory, 
it's recommended to install [uv](https://docs.astral.sh/uv/getting-started/installation/).

Then create a virtual environmentL


```bash
uv venv --python 3.14
source .venv/bin/activate
uv pip install -r requirements.txt
```

(In subsequent sessions you only need to run the `source` line.)

You can now run the script:

```bash
./splitter.py --help
```
