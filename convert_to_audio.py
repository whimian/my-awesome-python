#!/usr/bin/env python3
import argparse
from pathlib import Path

import moviepy.editor as mp

__author__ = 'yuhao'

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def convert(source_dir, target_dir):
    # print(source_dir)
    # print(target_dir)

    source_dir = Path(source_dir)
    target_dir = Path(target_dir)

    video_files = source_dir.glob("*.mp4")

    audio_files = target_dir.glob("*.mp3")
    names = [a.stem for a in audio_files]

    for file in video_files:
        if file.stem not in names:
            clip = mp.VideoFileClip(str(file))
            clip.audio.write_audiofile(str(target_dir/ (file.stem + ".mp3")))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source_dir', required=True)
    parser.add_argument('-d', '--target_dir', required=True)
    args = parser.parse_args()

    convert(args.source_dir, args.target_dir)
