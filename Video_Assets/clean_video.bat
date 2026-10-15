@echo off
set FFMPEG_PATH=C:\ffmpeg\bin\ffmpeg.exe
set INPUT_VIDEO=C:\Users\lsz\Desktop\KeyShield\Video_Assets\demo_raw.mp4
set OUTPUT_VIDEO=C:\Users\lsz\Desktop\KeyShield\Video_Assets\demo_cleaned.mp4

%FFMPEG_PATH% -i %INPUT_VIDEO% -vf "crop=1820:1020:50:30,drawbox=x=70:y=30:w=320:h=32:color=black@0.7:t=fill" -c:a copy %OUTPUT_VIDEO% -y

pause