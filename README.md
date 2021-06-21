# UltraWideCrop

Crops videos from 2560x1080 -> 1920x1080. Basically removes blackbars on the sides. I use this to make my VALORANT clips viewable on 16:9 monitors without blackbars on all sides.

Note: This requires [`ffmpeg`](https://www.ffmpeg.org/) to be installed and in PATH

This takes 1 positional command-line argument which is the file path to the video to crop.

Optional command-line args:
- `-t --trim` to specify a start time to trim clip from
- `-e --end --to` to specify end time to trim clip from. (`--end` and `--duration` are mutually exclusive)
- `-d --duration` to specify the total duration of the clip to trim. (`--end` and `--duration` are mutually exclusive)
- `-n --name` to specify the output filename. Defaults to {filename}_cropped.mp4
- `-l --local` to specify whether the output should be in the current directory
- `-m --mute` to specify whether the output should be muted
