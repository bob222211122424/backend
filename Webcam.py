import cv2
from PIL import Image

cam = cv2.VideoCapture(0) 

result, image = cam.read()  
if result: 
  
    cv2.imwrite("Picture-Text/photo.png", image)  # Can turn this off later, Just for testing

    img = Image.open("Picture-Text/photo.png") 


cam.release() 
