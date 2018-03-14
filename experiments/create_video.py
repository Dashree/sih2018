import moviepy.editor as moviepy
clip = moviepy.ImageSequenceClip('image', fps = 1)
clip.write_videofile("video1fps.webm", fps=22,codec='libvpx-vp9')
