
import shutil
import os, sys, glob
import time

path = "/mnt/c/Users/Madhura/Desktop/sih2018/experiments/worker/images/"
source = os.listdir(path)
destination = "/mnt/c/Users/Madhura/Desktop/SampleFolder/"
for files in source:
	if files.endswith(".jpg" or ".jpeg" or ".png"):
		shutil.copy(files,destination)
	time.sleep(120)
