import cv2
import numpy as np
import PrintHTML
import Detection
import sys


#def main():
#	imgFile=""
#	outFile=""
#	bootstrap=-1
#
#	try:
#      , args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
#  	except getopt.GetoptError:
#      print 'test.py -i <inputfile> -o <outputfile>'
#      sys.exit(2)




print("..............PROCESSING....................")
orimg = cv2.imread(sys.argv[1], 0)  # Read the image
height, width = orimg.shape[0:2]
img_resized = cv2.resize(orimg, (1300, int(1300*(height/width))))
img = img_resized[:]
print("...............Image Loaded.................")

box_list = list()

print("...............Detecting Images..............")
box_list,page_width = Detection.ImageDetect(img,box_list)
print("Done")

for i in box_list:
	    img[i.y1:i.y2, i.x1:i.x2] = np.ones((i.y2-i.y1, i.x2-i.x1))*255

print("...............Detecting Text..............")
box_list = Detection.TextDetect(img,box_list)
print("Done")


#for i in box_list:
#	print(i.x1,i.y1,i.x2,i.y2,i.tag,i.text,i.size)

box_list.sort(key=lambda x: x.y1)


print("...............Converting into HTML..............")
f = open("HTML.html","w")
PrintHTML.HTML_CSS(box_list,f,page_width)
f.close()

f = open("HTML1.html","w")
PrintHTML.HTML_CSS_BOOTSTRAP(box_list,f,page_width)
f.close()

print("Done")