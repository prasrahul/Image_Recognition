import cv2
import time
import face_recognition
import numpy as np
from face_recognition.api import face_locations

from db import read_encodings

def capture_image(person_name):
    """person image will be captured and return the image with name for adding to the database
    """
    feed = cv2.VideoCapture(0)

    while True:
        time.sleep(3)
        ret, frame = feed.read()
        time.sleep(3)
        frame = cv2.resize(frame,(512,512))

        break
    cv2.imwrite(f"images/{person_name}.jpg",frame)
    feed.release()
    cv2.destroyAllWindows()
    return frame,person_name

def generate_encode(image,name):
    """Generates encodings

    Args:
        image (image): person image 
        name (string): Name of the person

    Returns:
        name, encoding and face_location
    """ 
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    face_location = face_recognition.face_locations(image)
    
    encode = face_recognition.face_encodings(image,face_location)[0]

    return name,encode,face_location

def generate_encode_realtime(image):
    """Generates encodings

    Args:
        image (image): person image 
        name (string): Name of the person

    Returns:
        name, encoding and face_location
    """ 
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    #image = np.array([image])
    face_location = face_recognition.face_locations(image)
    #face_location = face_recognition.api.batch_face_locations(image, number_of_times_to_upsample=0, batch_size=1)
    encode = face_recognition.face_encodings(image,face_location,model = "large")


    return encode,face_location

def recognition():
    name,en = read_encodings()

    feed = cv2.VideoCapture(0)
    while True:
        ret,frame = feed.read()
        frame = cv2.resize(frame,(1012,1012))
        start_time = time.time()
        #frame = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        encodes, face_location = generate_encode_realtime(frame)
        for encode,face in zip(encodes,face_location):
            matches = face_recognition.compare_faces(en, encode)
            faceDis = face_recognition.face_distance(en, encode)

            # print(matches)
            # print(faceDis)

            matchIndex = np.argmin(faceDis)



            if matches[matchIndex]:
                detected_name = name[matchIndex].upper()
    # print(name)
                y1, x2, y2, x1 = face
                #print(face)
                #y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                #print(x1,x2,y1,y2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, detected_name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        end_time = time.time()
        #p_time = 
        processing_time = (1/(end_time-start_time))
        cv2.putText(frame,str(processing_time),(20,20),cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow('Webcam', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break



