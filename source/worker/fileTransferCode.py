
import shutil
import os, sys, glob
import time

path = "/mnt/c/Hackathon_Images"
source = os.listdir(path)
destination = "/mnt/c/images"
for files in source:
	if files.endswith(".jpg" or ".jpeg" or ".png"):
		shutil.copy(os.path.join(path, files),destination)
	time.sleep(60)
