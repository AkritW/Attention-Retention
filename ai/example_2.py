"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import numpy as np
import math
import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()


# open video file
cap = cv2.VideoCapture('../prakash2.mp4')

# set video capture properties
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 60)

# create a video writer object
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # use appropriate codec
fps = 60.0 # frames per second
width = 640 # frame width
height = 360 # frame height
out = cv2.VideoWriter('output.mp4', fourcc, fps, (width, height))


frame_number = 0

inFile = open("data.csv", "w")
inFile.write("number,seconds,action,left_pupil,right_pupil")
inFile.close()

arr = []
while cap.isOpened():
    frame_number += 1
    # read frame
    ret, frame = cap.read()
    
    if not ret:
        # end of video file
        break
        
    #cv2.imshow('frame', frame)
    
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_blinking():
        text = "Blinking"
    elif gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    elif gaze.is_center():
        text = "Looking center"


    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    print(left_pupil)

    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    arr.append(frame)
    cv2.imshow("Demo", frame)

    print(right_pupil)
    print(left_pupil)
    print(text)

    if left_pupil != None:
        left_pupil = str(left_pupil[0]) + ":" + str(left_pupil[1])
    if right_pupil != None:
        right_pupil = str(right_pupil[0]) + ":" + str(right_pupil[1])


    print(text)
    ## Save in format number, seconds, action, left_pupil, right_pupil in csv
    if text == "" or text == None:
        text = "None"
    if left_pupil == None:
        left_pupil = "None"
    if right_pupil == None:
        right_pupil = "None"

    print(right_pupil)
    print(left_pupil)
    print(text)

    inFile = open("data.csv", "a")
    inFile.write(str(frame_number) + "," + str((frame_number//60) + 1) + "," + text + "," + left_pupil + "," + right_pupil + "\n")
    inFile.close()

    # wait for 1ms and check for keyboard interrupt
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release resources
cap.release()
cv2.destroyAllWindows()

# loop through the frames and write to video file
for frame in arr:
    # convert frame to uint8
    frame = np.uint8(frame)
    
    # write frame to video file
    out.write(frame)

# release resources
out.release()


def calculate_attention(coord1, coord2, threshold):
    print(coord1)
    print(coord2)
    # Calculate distance between the two sets of coordinates
    dist_left = math.sqrt((coord2[0][0] - coord1[0][0])**2 + (coord2[0][1] - coord1[0][1])**2)
    dist_right = math.sqrt((coord2[1][0] - coord1[1][0])**2 + (coord2[1][1] - coord1[1][1])**2)

    # Check if distance is below threshold and set attention accordingly
    if dist_left < threshold and dist_right < threshold:
        attention = 100.0
    else:
        # Calculate attention as a function of the difference between the two distances
        print(dist_left)
        print(dist_right)
        diff = abs(dist_left - dist_right)
        print(diff)
        attention = max(0, 100 - (diff * 10))

    return float(attention)


def calculate_attention_score(left_x, left_y, right_x, right_y, prev_left_x, prev_left_y, prev_right_x, prev_right_y):
    return calculate_attention(((left_x,left_y), (right_x, right_y)), ((prev_left_x, prev_left_y), (prev_right_x, prev_right_y)), 0.5)

def write_score():

    prev_number = None 
    prev_seconds = None 
    prev_action = None 
    prev_left = None
    prev_right = None
    prev_left_x = None
    prev_right_x = None
    prev_left_y = None
    prev_right_y = None
    
    total = -1
    outFile = open("output_data.csv", "w")
    outFile.write("number,attention%\n")
    outFile.close()

    inFile = open("data.csv", "r")
    a = inFile.readline()
    for line in inFile:
        total += 1
        number, seconds, action, left, right = line.strip().split(",")
        if left != "None":
            print(left)
            left_x, left_y = left.split(":")
            right_x, right_y = right.split(":")
    
            left_x = int(left_x)
            left_y = int(left_y)
            right_x = int(right_x)
            right_y = int(right_y)

            if prev_number != None:
                score = calculate_attention_score(left_x, left_y, right_x, right_y, prev_left_x, prev_left_y, prev_right_x, prev_right_y)
                outFile = open("output_data.csv", "a")
                outFile.write(str(total) + "," + str(score) + "\n")
                outFile.close()

            prev_number = number
            prev_seconds = seconds
            prev_action = action
            prev_left_x = left_x
            prev_left_y = left_y
            prev_right_x = right_x
            prev_right_y = right_y

write_score()
