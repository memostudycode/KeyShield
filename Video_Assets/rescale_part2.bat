@echo off
cd C:\Users\lsz\Desktop\KeyShield\Video_Assets
ffmpeg -i part2_reencoded_fixed.mp4 -vf "scale=4000:2250:force_original_aspect_ratio=decrease,pad=4000:2250:(ow-iw)/2:(oh-ih)/2" -c:v libx264 -crf 23 -preset fast -c:a aac -b:a 128k -ar 44100 -ac 1 -r 25 -g 25 part2_rescaled.mp4 -y
