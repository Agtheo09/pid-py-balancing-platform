import cv2 as cv
import numpy as np

class BallLocalization:
    COLOR_ACCURACY = [8, 20, 100]
    OPEN_MORPH = 12
    CLOSE_MORPH = 28

    largestCntBoundingRect = [0, 0, 0, 0]

    # def __init__(self, targetColor, targetPos):
    #     self.targetColor = targetColor
    #     self.targetPos = targetPos

    def contoursMorphology(self, mask, openValue, closeValue):
        kernalOpen = np.ones((openValue, openValue), np.uint8)
        kernalClose = np.ones((closeValue, closeValue), np.uint8)

        finalMask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernalOpen)
        finalMask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernalClose)

        return finalMask

    def drawContourAspects(self, frame, contours, largestCntIndex):
        cv.drawContours(frame, contours, largestCntIndex, (255, 255, 0), 2)

        if(len(contours) > 0):
            self.contoursFound = True
            x,y,w,h = cv.boundingRect(contours[largestCntIndex])
            self.largestCntBoundingRect = [x, y, w, h]
            cv.rectangle(frame, (x, y), (x + w, y + h), (0,0,255), 2)
            self.centerOfContour = (x + int(w/2), y + int(h/2))
            cv.circle(frame, self.centerOfContour, 3, (0,255,127), -1)
        else:
            self.contoursFound = False

        self.contourRender = frame

    def drawLocalizationAspects(self, cntMat):
        boxX = self.largestCntBoundingRect[0]
        boxY = self.largestCntBoundingRect[1]
        boxW = self.largestCntBoundingRect[2]
        boxH = self.largestCntBoundingRect[3]
        if(self.contoursFound):
            cv.line(cntMat, (boxX+int(boxW/2), 0), (boxX+int(boxW/2), boxY), (0, 0, 255), 2)# Line 1
            cv.line(cntMat, (int(self.frameSize[0]), boxY+int(boxH/2)), (boxX+boxW, boxY+int(boxH/2)), (0, 0, 255), 2)# Line 2
            cv.line(cntMat, (boxX+int(boxW/2), int(self.frameSize[1])), (boxX+int(boxW/2), boxY+boxH), (0, 0, 255), 2)# Line 3
            cv.line(cntMat, (0, boxY+int(boxH/2)), (boxX, boxY+int(boxH/2)), (0, 0, 255), 2)# Line 4

        self.finalRender = cntMat
    
    def getLargestContourIndex(self, contoursList):
        index = 0
        largestCntArea = 0
        for i in range(0, len(contoursList)):
            if(cv.contourArea(contoursList[i]) > largestCntArea):
                largestCntArea = cv.contourArea(contoursList[i])
                index = i
        return index

    def update(self, frameFeed, hsvMat, frameSize, targetColor, targetPos):
        self.frameSize = frameSize
        self.targetColor = targetColor
        self.targetPos = targetPos

        # Creating Mask
        lowerTarget = np.array([self.targetColor[0] - self.COLOR_ACCURACY[0], self.targetColor[1] - self.COLOR_ACCURACY[1], self.targetColor[2] - self.COLOR_ACCURACY[2]])
        upperTarget = np.array([self.targetColor[0] + self.COLOR_ACCURACY[0], self.targetColor[1] + self.COLOR_ACCURACY[1], self.targetColor[2] + self.COLOR_ACCURACY[2]])
        self.mask = cv.inRange(hsvMat, lowerTarget, upperTarget)

        #Clearify Contours with Morphological Operations OPEN and CLOSE
        self.maskMod = self.contoursMorphology(self.mask, self.OPEN_MORPH, self.CLOSE_MORPH)

        #Finding Contours based on the Mask
        contours, _ = cv.findContours(self.maskMod, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

        # Find Largest Contour by its Area
        indexOfLargestCnt = self.getLargestContourIndex(contours)

        # Contour Drawing + Bounding Box
        self.drawContourAspects(frameFeed, contours, indexOfLargestCnt)

        # Coordinate Lines Drawing
        self.drawLocalizationAspects(self.contourRender)

    def getLocalizationRender(self):
        return self.finalRender

    def getMask(self, isFilter):
        if(isFilter):
            return self.maskMod
        else:
            return self.mask

    def getCoordinates(self):
        if(self.centerOfContour):
            return self.centerOfContour

    def isCntFound(self):
        return self.contoursFound