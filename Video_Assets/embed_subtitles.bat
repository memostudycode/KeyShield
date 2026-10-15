@echo off
cd C:\Users\lsz\Desktop\KeyShield\Video_Assets
ffmpeg -i demo_cleaned.mp4 -vf "subtitles=part2_subtitles.srt" -c:a copy part2_with_subtitles.mp4 -y
