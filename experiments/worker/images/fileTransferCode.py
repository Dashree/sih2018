
import shutil
import os, sys, glob
import time

path = "/mnt/c/Hackathon/Hackathon_Images"
source = os.listdir(path)
destination = "/mnt/c/sih2018/experiments/worker/images"
for files in source:
	if files.endswith(".jpg" or ".jpeg" or ".png"):
		shutil.copy(os.path.join(path, files),destination)
	time.sleep(60)
