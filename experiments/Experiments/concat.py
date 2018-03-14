"""
Takes images from the specified directory and creates a video using vp9 codec
"""

import moviepy.editor as moviepy
from moviepy.editor import VideoFileClip, concatenate_videoclips
clip1 = moviepy.ImageSequenceClip('image', fps = 1)
clip2 = moviepy.ImageSequenceClip('image1', fps = 1)
final_clip = concatenate_videoclips([clip1,clip2])
final_clip.write_videofile("concat.webm", fps=44,codec='libvpx-vp9')
