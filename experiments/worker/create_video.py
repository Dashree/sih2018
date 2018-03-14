"""
Creating video with a single image
"""
import moviepy.editor as moviepy
import sys
height = sys.argv[1]
clip = moviepy.ImageClip('images/3DIMG_01SEP2017_0030_L1C_ASIA_MER_IR1.jpg', duration=1)
clip.resize(height=int(height)).write_videofile("singleVideo.webm", fps=1,codec='libvpx-vp9')
