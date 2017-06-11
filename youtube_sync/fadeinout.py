import re
import sh

input_wav = '/Users/jagaro/Desktop/b.wav'

def media_duration(path):
    re_duration = re.compile('^ *Duration: (\d+):(\d+):(\d+)(\.\d+),')
    output = sh.ffprobe('-hide_banner', path).stderr.decode('utf-8')
    lines = list(filter(lambda l: re_duration.match(l), output.split('\n')))
    if len(lines) == 1:
        m = re_duration.match(lines[0])
        return (float(m[1])*60*60) + \
            (float(m[2])*60) + \
            (float(m[3])) + float(m[4])
    else:
        raise Exception('Unexpected output from ffprobe: %s' % output)

result = sh.ffmpeg('-i', input_wav,
  '-af', 'silencedetect=noise=-20dB:d=5',
  '-nostats', '-hide_banner', '-f', 'null', '-'
)

output = result.stderr.decode('utf-8')
lines = output.split('\n')
lines = filter(lambda l: re.match(r'^\[sil', l), lines)
lines = map(lambda l: re.sub(r'\[.+\] ', '', l), lines)
lines = map(lambda l: re.sub(r' \| silence_duration.+$', '', l), lines)
pairs = [(a, next(lines, None)) for a in lines]

# assert
for start, end in pairs:
    if not re.match(r'^silence_start: \d+(\.\d+)?$', start) or \
           (end is not None and
            not re.match(r'^silence_end: \d+(\d.\d+)?$', end)):
        raise Exception('Invalid pairs %s' % pairs)

floaty = lambda x: float(re.sub(r'[^0-9]', '', x))
pairs = list(map(lambda p: (floaty(p[0]), floaty(p[1])), pairs))

sh.ffmpeg('-i', input_wav, '-ss', '0', '-t', '84.886', 'b.wav')
sh.ffmpeg('-i', input_wav, '-ss', '90.3009', '-t', '142.329', 'c.wav')


ffmpeg -i "b.wav" -af silencedetect=noise=-30dB:d=5 -nostats -hide_banner -f null - 2>&1 | grep '^\[silence'

[silencedetect @ 0x7faf6ad14f80] silence_start: 83.886
[silencedetect @ 0x7faf6ad14f80] silence_end: 91.3009 | silence_duration: 7.41488


ffmpeg -i clip.mp4 -vf 'fade=in:0:30,fade=out:960:30'
                   -af 'afade=in:st=0:d=1,afade=out:st=32:d=1'
       -c:v libx264 -crf 22 -preset veryfast fadeInOut.mp4
