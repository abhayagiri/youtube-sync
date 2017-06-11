#!/bin/bash

FADE_IN_DURATION=1.0
FADE_OUT_DURATION=0.5
FFMPEG_OPTIONS="-hide_banner -loglevel panic"

set -e
cd `dirname "$0"` && cd ..

YOUTUBE_ID="$1"

if [ "$YOUTUBE_ID" = "" ]; then
  echo "Usage: $0 <youtube id>"
  exit 1
fi

if [ "$DYNAMIC_AUDIO_NORMALIZER_BIN" = "" ]; then
  echo "DYNAMIC_AUDIO_NORMALIZER_BIN not defined"
  exit 1
fi

if [ "$DESTINATION_SERVER_PATH" = "" ]; then
  echo "DESTINATION_SERVER_PATH not defined"
  exit 1
fi

set -x

rm -rf tmp
mkdir -p tmp

WORK_DIR=`mktemp -d`

venv/bin/youtube-dl --extract-audio --output "$WORK_DIR/a.%(ext)s" -- "$YOUTUBE_ID"

ffmpeg $FFMPEG_OPTIONS -i tmp/a.* -ac 1 tmp/b.wav

$DYNAMIC_AUDIO_NORMALIZER_BIN \
  --alt-boundary --max-gain 20.0 --gauss-size 51 \
  -i tmp/b.wav -o tmp/c.wav

fade_out_start=`ffprobe -v quiet -show_format_entry duration tmp/c.wav  | grep duration | sed 's/duration=//' | sed 's/$/-1/' | bc -l`

ffmpeg -i tmp/c.wav \
  -af "afade=in:st=0:d=$FADE_IN_DURATION,afade=out:st=$fade_out_start:d=$FADE_OUT_DURATION" \
  -b:a 64k -ac 1 tmp/d.mp3

scp tmp/d.mp3 "$DESTINATION_SERVER_PATH/$YOUTUBE_ID.mp3"

rm -rf $WORK_DIR
