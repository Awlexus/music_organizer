# A small script to organize your music

This is a small script that organizes your music library. After executing this script your music will be restructured like this

```
YourMusic/<album artist or artist>/<album>/<title or filename>.<extension>
```

The album artist will be the prefered directory name in case both album artist and artist exist.


## Prerequisites

## Installation
This script uses [taglib](https://github.com/taglib/taglib) to analyze the contents of your files music.

### Arch linux

```bash
pacman -S taglib
```

## Install the dependencies
This library also depends on [pytaglib](https://github.com/supermihi/pytaglib). Use the following command to install the dependencies necessary.

```bash
pip install -r requirements.txt
```

## Usage
Run `organizer.py --help` to get a overview on how to use this script.

Generally you would use the script like this

```bash
./music_organizer.py -s <scan_dir> -t <target_dir> -r
```

### Options

| Flag(s)                | Description                                                   |
| ---------------------- | ------------------------------------------------------------- |
| `-s`, `--scan-dir`     | The directory where your music is located                     |
| `-t`, `--target-dir`   | The directory where you want to move your music to            |
| `-r`, `--remove-empty` | Remove directories that are empty after executing this script |
| `--default-album`      | Default album name, if the information was not found          |
| `--default-artist`     | Default artsit name, if the information was not found         |

## Todo
As far as I'm concerned, this script works well enough for my needs, might be a nice to have
* [ ] Limit the search depth for music
* [ ] Trying to fetch the metadata for a file, if not available
* [ ] Customize the directory structure
* [ ] Extract metadata from the filename
* [ ] Add easter eggs