import moviepy.editor as mp
from pathlib import Path

source_dir = Path("C:/Users/yuhao/Desktop/Early Middle Ages/")
target_dir = Path("C:/Users/yuhao/Desktop/Early Middle Ages/converted_audio")

video_files = source_dir.glob("*.mp4")

audio_files = target_dir.glob("*.mp3")
names = [a.stem for a in audio_files]

for file in video_files:
    if file.stem not in names:
        clip = mp.VideoFileClip(str(file))
        clip.audio.write_audiofile(str(target_dir/ (file.stem + ".mp3")))
