@echo off
cd C:\Users\lsz\Desktop\KeyShield\Video_Assets
ffmpeg -f concat -safe 0 -i final_concat_list_rescaled.txt -c:v libx264 -crf 23 -preset fast -c:a aac -b:a 128k -ar 44100 -ac 1 -r 25 -g 25 final_integrated.mp4 -y
