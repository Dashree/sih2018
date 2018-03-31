
#r'C:\\Hackathon_Images\\3DIMG_01SEP2017_0029_L1C_ASIA_MER_IR1.jpg',r'C:\\Hackathon_Images\\3DIMG_01SEP2017_0031_L1C_ASIA_MER_IR1.jpg'
from PIL import Image
from PIL import ImageFilter
from PIL import ImageMorph
from PIL import ImageChops
import csv

# get file name as argumnet

#def morph (arg1, arg2)

def morph(): 

    #check for format - same
    #check for sizes - same
    #if not same - resize

    img1 = Image.open('C:\\Hackathon_Images\\3DIMG_01SEP2017_1600_L1C_ASIA_MER_IR1.jpg')
    
    img1.Info()
    #img1.show()

    img2 = Image.open('C:\\Hackathon_Images\\3DIMG_01SEP2017_1700_L1C_ASIA_MER_IR1.jpg')
    #img2.show()

   # img1.MedianFilter(size=3)

    img3 = img1.filter(ImageFilter.MedianFilter(3))
    img3.save("imgtemp.jpg")
 #   img3.show()

    rangeAlpha = 10
    for i in range(rangeAlpha)
        alpha = i/rangeAlpha
        imgBlend = ImageChops.blend(img1,img2,alpha)
        imgBlend.save("imgtemp.jpg")
        #imgBlend.show()

    img4 = Image.open('C:\\Hackathon_Images\\3DIMG_01SEP2017_1630_L1C_ASIA_MER_IR1.jpg')
    

    imgDiff = ImageChops.difference(img4,imgBlend)
    imgDiff.save("imgtemp.jpg")

    imgDiff.show()

    img1.Info()
       # img4 = img2.filter(ImageFilter.MedianFilter(3))
   # img4.save("imgtemp.jpg")
   # img4.show()

   # img5 = ImageChops.add(img3,img4,2,2)
   # img5.save("imgtemp.jpg")
   # img5.show()

    #img6 = ImageChops.add(img5,img1,2,0)
    #img6.save("imgtemp.jpg")
    #img6.show()
    
    #display(Image1)
  # im = Image.open(path1.jpg)
  # im2 = Image.open(path2.jpg)
   #im.show()
   #im2.show()

#morph(/mnt/C:/Hackathon_Images/3DIMG_01SEP2017_0000_L1C_ASIA_MER_IR1 , /mnt/C:/Hackathon_Images/3DIMG_01SEP2017_0030_L1C_ASIA_MER_IR1)

if __name__ == '__main__':
    morph()
    
#print ('Hello')



    
