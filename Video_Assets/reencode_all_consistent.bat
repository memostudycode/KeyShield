@echo off
cd C:\Users\lsz\Desktop\KeyShield\Video_Assets

:: Re-encode Part 1 to 25 fps, mono audio, 44100 Hz
ffmpeg -i part1_with_voiceover.mp4 -c:v libx264 -crf 23 -preset fast -r 25 -g 25 -c:a aac -b:a 128k -ar 44100 -ac 1 part1_final.mp4 -y

:: Re-encode Part 3 to 25 fps, mono audio, 44100 Hz
ffmpeg -i part3_with_voiceover.mp4 -c:v libx264 -crf 23 -preset fast -r 25 -g 25 -c:a aac -b:a 128k -ar 44100 -ac 1 part3_final.mp4 -y

:: Part 2 is already fixed (part2_reencoded_fixed.mp4)
