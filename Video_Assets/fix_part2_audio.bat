@echo off
cd C:\Users\lsz\Desktop\KeyShield\Video_Assets
ffmpeg -i part2_with_subtitles.mp4 -c:v libx264 -crf 23 -preset fast -c:a aac -b:a 128k -ar 44100 -ac 1 -r 25 -g 25 -force_key_frames "expr:gte(n,n_forced*25)" part2_reencoded_fixed.mp4 -y
