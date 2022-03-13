ffmpeg -i final-mid-com.mp4 -i audio.mp3 -map 0:v -map 1:a -c:v copy gen/mid.mp4
ffmpeg -i final-start.mp4 -filter:v "setpts=PTS/2" gen/start.mp4