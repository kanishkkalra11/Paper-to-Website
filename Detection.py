import cv2
import pytesseract
import re
import box
import math
import numpy as np

def ImageDetect(pimg, box_list):
	img = pimg[:]
	(thresh, img_bin) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # Thresholding the image
	img_bin = 255-img_bin  # Invert the Image_bin
	#cv2.imwrite("Image_bin.jpg",img_bin)

	# Defining a kernel length
	kernel_length = np.array(img).shape[1]//40

	# A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
	verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))

	# A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
	hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))

	# A kernel of (3 X 3) ones.
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

	# Morphological operation to detect verticle lines from an image
	img_temp1 = cv2.erode(img_bin, verticle_kernel, iterations=3)
	verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=3)
	#cv2.imwrite("verticle_lines.jpg",verticle_lines_img)

	# Morphological operation to detect horizontal lines from an image
	img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=3)
	horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)
	#cv2.imwrite("horizontal_lines.jpg",horizontal_lines_img)

	# Weighting parameters, this will decide the quantity of an image to be added to make a new image.
	alpha = 0.5
	beta = 1.0 - alpha

	# This function helps to add two image with specific weight parameter to get a third image as summation of two image.
	img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
	img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
	(thresh, img_final_bin) = cv2.threshold(img_final_bin, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

	# For Debugging
	# Enable this line to see verticle and horizontal lines in the image which is used to find boxes
	#cv2.imwrite("img_final_bin.jpg",img_final_bin)

	contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	# Sort all the contours by top to bottom.
	#(contours, boundingBoxes) = sort_contours(contours, method="top-to-bottom")

	_, _, page_width, _ = cv2.boundingRect(contours[0])

	for c in range (1,len(contours),2):
	    # Returns the location and width,height for every contour
	    x, y, w, h = cv2.boundingRect(contours[c])
	    if(w>20 and h>20):
	        box_Object = box.box(x, y, x + w, y + h, "Image", None, -1)
	        box_list.append(box_Object)

	return (box_list,page_width)



def TextDetect(pimg,box_list):
	img = pimg[:]
	#TEXT_DETECT
	edges = cv2.Canny(img,50,150,apertureSize = 3)

	kernel = np.ones((2,2),np.uint8)
	dilate=cv2.dilate(edges,kernel,iterations = 20)


	contours, hierarchy = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


	pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
	for i in contours:
	    x,y,w,h = cv2.boundingRect(i)
	    #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
	    l = pytesseract.image_to_string(img[y-1:y+h+1,x-1:x+w+1])#, output_type=pytesseract.Output.DICT)
	    #text = findText(l)
	    #cv2.imshow("image",img[y-1:y+h+1,x-1:x+w+1])
	    #cv2.waitKey()
	    boxObject = box.box(x, y, x+w, y+h, "text", l, -1)
	    box_list.append(boxObject)


	for i in box_list:
	    if(i.tag=="text"):
	        l2 = re.split("\n",i.text)
	        i.size = (i.y2-i.y1)/len(l2)
	        x=""
	        for j in l2:
	            x+=j
	            x+="<br>"
	        i.text = x

	return (box_list)