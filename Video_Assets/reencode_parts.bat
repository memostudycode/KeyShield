@echo off
cd C:\Users\lsz\Desktop\KeyShield\Video_Assets

:: Re-encode Part 1 with consistent timestamps
ffmpeg -i part1_with_voiceover.mp4 -c:v libx264 -crf 23 -preset fast -c:a aac -b:a 128k -ar 44100 -r 25 -g 25 -force_key_frames "expr:gte(n,n_forced*25)" part1_reencoded.mp4 -y

:: Re-encode Part 2 with consistent timestamps
ffmpeg -i part2_with_subtitles.mp4 -c:v libx264 -crf 23 -preset fast -c:a aac -b:a 128k -ar 44100 -r 25 -g 25 -force_key_frames "expr:gte(n,n_forced*25)" part2_reencoded.mp4 -y

:: Re-encode Part 3 with consistent timestamps
ffmpeg -i part3_with_voiceover.mp4 -c:v libx264 -crf 23 -preset fast -c:a aac -b:a 128k -ar 44100 -r 25 -g 25 -force_key_frames "expr:gte(n,n_forced*25)" part3_reencoded.mp4 -y
