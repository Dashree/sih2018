"""
Height and width is provided from the terminal.
"""
import moviepy.editor as moviepy
import sys
height = sys.argv[2]
width = sys.argv[1]
clip = moviepy.ImageSequenceClip('images', fps = 1)
clip.resize(newsize=(int(width),int(height)).write_videofile("video.webm", fps=22,codec='libvpx-vp9')
