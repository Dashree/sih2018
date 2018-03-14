"""
Height is provided from the terminal and can be 360, 720, 1080.
Width is automatically calculated as per height. Doesn't accept externally provided width
"""
import moviepy.editor as moviepy
import sys
height = sys.argv[1]
clip = moviepy.ImageSequenceClip('images', fps = 1)
clip.resize(height=int(height)).write_videofile("video.webm", fps=22,codec='libvpx-vp9')
