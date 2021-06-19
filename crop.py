import subprocess
import argparse
import pathlib
from functools import cache
from time import perf_counter


parser = argparse.ArgumentParser()
parser.add_argument('video', help='Path to video to crop')
parser.add_argument('-t', '--trim', help='Trim video from arg1 for arg2 duration. Defaults to end if arg2 not provided')
end = parser.add_mutually_exclusive_group()
end.add_argument('-to', help='Trim video to specific time. This is slower than using -d. Mutex with -d')
end.add_argument('-d', '--duration', help='Trim video for this amount from start time. Mutex with -to')
parser.add_argument('-n', '--name', help='Name out cropped video file. Defaults to {filename}_cropped.mp4')
parser.add_argument('-l', '--local', help='Flag for whether to output file in current directory', action='store_true')
args = parser.parse_args()
d = vars(args)

path = pathlib.Path(d['video'])
if not path.is_file():
    raise ValueError('Unable to find that video')

if (d.get('duration') or d.get('to')) and not d.get('trim'):
    d['trim'] = '0'


@cache
def get_output_location(filename):
    """Try to output to folder if exists"""
    if d.get('local'):
        return filename
    subdirs = ('Trimmed', 'Cropped')
    for sd in subdirs:
        subdir = path.with_name(sd)
        if subdir.is_dir():
            return fr'{subdir}\{filename}'
    return filename


def format_time(time):
    if ':' in time:
        return time
    else:
        return f'{time}s'


original_filename = path.name
if name := d.get('name'):
    if '.' not in name:
        name += '.mp4'
    output_filename = name
else:
    output_filename = original_filename[:-4] + '_cropped.mp4'

# https://video.stackexchange.com/questions/4563/how-can-i-crop-a-video-with-ffmpeg
# https://superuser.com/questions/138331/using-ffmpeg-to-cut-up-video
ffmpeg_args = ['ffmpeg']
finish_msg = f'Cropped {original_filename!r} to {get_output_location(output_filename)!r}'
if trim := d.get('trim'):
    finish_msg += f' from {format_time(trim)}'

    if duration := d.get('duration'):
        finish_msg += f' for {format_time(duration)}'
        ffmpeg_args += ['-ss', trim, '-i', d['video'], '-t', duration]

    elif to := d.get('to'):
        finish_msg += f' to {format_time(to)}'
        ffmpeg_args += ['-i', d['video'], '-ss', trim, '-to', to]
        # http://trac.ffmpeg.org/wiki/Seeking
        # need to put '-ss' after '-i' or '-to' does not work as intended
    else:
        ffmpeg_args += ['-ss', trim, '-i', d['video']]

    ffmpeg_args += ['-filter:v', 'crop=in_w-640:in_h', get_output_location(output_filename)]
    # using '-c:a copy' with '-ss' will cause issues such as audio de-sync
else:
    ffmpeg_args += ['-i', d['video'], '-filter:v', 'crop=in_w-640:in_h', '-c:a', 'copy', get_output_location(output_filename)]

print(' '.join(ffmpeg_args))
start = perf_counter()
subprocess.run(ffmpeg_args)
finish = perf_counter()
print(f'{finish_msg} in {finish-start}s')


