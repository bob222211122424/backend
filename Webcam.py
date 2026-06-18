import cv2
from PIL import Image
import pytesseract
import os

cam = cv2.VideoCapture(0)  # Open the default webcam (device 0)

result, image = cam.read()  # Capture a single frame from the webcam and store success flag + image
if result:  # Check if the image was successfully captured
  
    cv2.imwrite("Picture-Text/photo.png", image)  # Save the captured image to a file

    img = Image.open("Picture-Text/photo.png")  # Open the saved image using PIL


cam.release()  