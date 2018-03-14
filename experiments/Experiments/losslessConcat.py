"""
Lossless concatination of videos with the passed resolution from terminal
"""
import subprocess, sys

resolution = sys.argv[1]
command = ['ffmpeg',
           '-c:v', 'libvpx-vp9',
           '-i', 'test.webm',
           '-c:v', 'libvpx-vp9',
           '-i', 'test1.webm',
           '-filter_complex', '[0:v:0] [1:v:0] concat=n=2:v=1:a=0[outv]',
           '-codec', 'libvpx-vp9',
           '-lossless', '1',
           '-map', '[outv]', '-s', resolution,'4.webm']
subprocess.run(command)
