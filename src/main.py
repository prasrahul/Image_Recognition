import face_recognition
import cv2
from face_recognition.api import face_locations
import numpy as np

from db import add_encode,read_encodings
from utils import capture_image,generate_encode,recognition








if __name__ == '__main__':
    val = int(input(" enter 1 for adding a face to the database: \n enter 2 for realtime face recognition:"))
    if val == 1:
        name = input(" \n Enter the name of the person:")


        image,name = capture_image(name)

        name,encoding,face_location = generate_encode(image,name)

        add_encode(name,encoding)
        print(f"{name} added successfully to the database")
    if val == 2:
        recognition()
