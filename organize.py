#!/bin/python3

import argparse
import pathlib
import os
import sys
import taglib

parser = argparse.ArgumentParser(description='''
Organize your music library.

This script will organize your library by scanning the scan-dir for music,
extracting and extracting it's metadata.

The music will then be organized in following matter:

    target-dir/album-artist|artist/album/title
''', formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('--scan-dir', '-s', type=pathlib.Path, default='.',
                    dest='scan_dir', required=True, help='where you want to scan for music.')
parser.add_argument('--target-dir', '-t', type=pathlib.Path, default='.',
                    dest='target_dir', required=True, help='where you want to move your music.')
parser.add_argument('--remove-empty', '-r', action='store_true', dest='remove_empty',
                    help="remove directories that are empty after moving the music files.")
parser.add_argument('--default-artist', dest='default_artist', default="Various Artists",
                    help="default artist name if none was present")
parser.add_argument('--default-album', dest='default_album', default="Unknown Album",
                    help="default album name if none was present")


def delete_empty_dirs(directory):
    files = os.listdir(directory)
    for f in files:
        f = os.path.join(directory, f)
        if os.path.isdir(f):
            print(f)
            delete_empty_dirs(f)

    if not os.listdir(directory):
        print(f"Removing empty dir {directory}")
        os.rmdir(directory)


def scan_dirs(directory):
    files = []

    for f in os.listdir(directory):
        f = os.path.join(directory, f)

        if os.path.isdir(f):
            for f2 in scan_dirs(f):
                files.append(f2)
        elif os.path.isfile(f):
            files.append(f)

    return files


def _extract_key(dir, key):
    if key not in dir:
        return

    value = dir[key]
    if type(value) is list and len(value) > 0:
        return value[0]
    elif type(value) is str:
        return value

    return None


def extract_metadata(file):
    try:
        tags = taglib.File(file).tags
    except OSError:
        return None

    dir = {}
    dir['artist'] = _extract_key(tags, 'ARTIST')
    dir['album_artist'] = _extract_key(tags, 'ALBUMARTIST')
    dir['title'] = _extract_key(tags, 'TITLE')
    dir['album'] = _extract_key(tags, 'ALBUM')

    return dir


def create_directory(target_dir, metadata, args):
    album = metadata['album'] or args.default_album
    artist = metadata['album_artist'] or metadata['artist'] or args.default_artist
    if not (album and artist):
        return

    directory = os.path.join(target_dir, artist, album)
    os.makedirs(directory, exist_ok=True)
    return directory


def move_file(file, target_dir, args):
    metadata = extract_metadata(file)
    if not metadata:
        return

    directory = create_directory(target_dir, metadata, args)
    if not directory:
        return

    title = metadata['title']
    if not title:
        return

    ext = os.path.splitext(file)[1]
    new_file = os.path.join(directory, metadata['title'] + ext)

    if file != new_file:
        print(f"moving '{file}' to '{new_file}")
        os.rename(file, new_file)


if __name__ == "__main__":
    args = parser.parse_args()

    scan_dir = args.scan_dir
    target_dir = args.target_dir
    remove_empty = args.remove_empty

    # Validate args
    if not os.path.exists(scan_dir):
        sys.exit(f"Scan directory '#{scan_dir}' does not exist")

    if not os.path.isdir(scan_dir):
        sys.exit(f"Scan directory '#{scan_dir}' is not a directory")

    os.makedirs(target_dir, exist_ok=True)

    # Move files
    files = scan_dirs(scan_dir)
    for f in files:
        move_file(f, target_dir, args)

    # Delete empty dirs
    if remove_empty:
        delete_empty_dirs(scan_dir)
