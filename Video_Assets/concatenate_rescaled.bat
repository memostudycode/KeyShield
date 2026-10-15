@echo off
cd C:\Users\lsz\Desktop\KeyShield\Video_Assets
ffmpeg -f concat -safe 0 -i final_concat_list_rescaled.txt -c copy final_integrated.mp4 -y
