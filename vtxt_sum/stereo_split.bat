
ffmpeg -i sample02.m4a -af "pan=stereo|c0=c0"  -y sample02_L.m4a
ffmpeg -i sample02.m4a -af "pan=stereo|c1=c1"  -y sample02_R.m4a
