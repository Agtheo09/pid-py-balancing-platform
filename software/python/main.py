import cv2 as cv
import numpy as np
import serial
import math
import cvzone.FPS
from apriltagging import AprilTagging

from localization import BallLocalization

# Set up Constands
BAUD_RATE = 9600
filterPercentage = 0.5

# arduino = serial.Serial(port="COM6", baudrate=BAUD_RATE, timeout=.6)

# Initialize CV
fpsReader = cvzone.FPS()
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

targetHSV = [0, 0, 0]

xValueFiltered = 90
yValueFiltered = 90

centerOfScreen = [0, 0]

ballLocalization = BallLocalization()
aprilTagDetector = AprilTagging()

blackImg = np.zeros((512, 512, 1), dtype = "uint8")

# Write Data to Serial
def sendBallPos(contourCoordinates):
    global xValueFiltered
    global yValueFiltered

    #Filter Values
    xValueFiltered = math.floor((contourCoordinates[0] * (1-filterPercentage)) + (xValueFiltered * filterPercentage))
    yValueFiltered = math.floor((contourCoordinates[1] * (1-filterPercentage)) + (yValueFiltered * filterPercentage))

    s = ":"
    strToSend = s.join((str(xValueFiltered), str(yValueFiltered)))
    print(strToSend)

    # try:
    #     arduino.write(bytes(strToSend, 'utf-8'))
    # except Exception as e:
    #     print("Serial type: " + e)

while True:
    ret, frame = cap.read();
    fps, img = fpsReader.update(frame, pos=(50, 80), color=(0, 255, 0), scale=2, thickness=5)

    viewportSize = [cap.get(3), cap.get(4)]
    print(viewportSize)

    blackImg = np.zeros((int(viewportSize[1]), int(viewportSize[0]), 1), dtype = "uint8")

    bluredView = cv.GaussianBlur(frame, (11, 11), 0)

    hsv = cv.cvtColor(bluredView, cv.COLOR_BGR2HSV)

    positionVirtualization = blackImg.copy()

    centerOfScreen = [int(viewportSize[0] / 2), int(viewportSize[1] / 2)]

    pixel1 = hsv[centerOfScreen[1], centerOfScreen[0]];
    pixel2 = hsv[(centerOfScreen[1] + 1), centerOfScreen[0]];
    pixel3 = hsv[(centerOfScreen[1] + 1), (centerOfScreen[0] + 1)];
    pixel4 = hsv[centerOfScreen[1], (centerOfScreen[0] + 1)];

    if cv.waitKey(1) == ord('p'):
        targetHSV[0] = (int(pixel1[0]) + int(pixel2[0]) + int(pixel3[0]) + int(pixel4[0])) / 4
        targetHSV[1] = (int(pixel1[1]) + int(pixel2[1]) + int(pixel3[1]) + int(pixel4[1])) / 4
        targetHSV[2] = (int(pixel1[2]) + int(pixel2[2]) + int(pixel3[2]) + int(pixel4[2])) / 4
        print("Color Picked: ", targetHSV)

    ballLocalization.update(frame, hsv, viewportSize, targetHSV, centerOfScreen)
    aprilTagDetector.update(frame)

    render = ballLocalization.getLocalizationRender()

    maskFiltered = ballLocalization.getMask(True)

    ballCoordinates = ballLocalization.getFilteredCoordinates()
    # ballCoordinates = ballLocalization.getCoordinates()

    if ballLocalization.isCntFound():
        sendBallPos(ballCoordinates)

    cv.circle(positionVirtualization, (ballCoordinates[0], ballCoordinates[1]), 15, (52, 155, 235), -1)
    cv.arrowedLine(positionVirtualization, ballCoordinates, centerOfScreen, (255, 0, 0), 2)

    cv.circle(render, centerOfScreen, 3, (0,255,127), -1)

    cv.imshow('View', render)
    # cv.imshow('Mask', maskFiltered)
    cv.imshow('Position Virtualization', positionVirtualization)

    if cv.waitKey(5) & 0xFF == 27:
        break
    
cap.release()
cv.destroyAllWindows()
