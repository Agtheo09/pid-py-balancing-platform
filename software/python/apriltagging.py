import cv2 as cv
from pupil_apriltags import Detector

class AprilTagging:
    tagsDetected = None
    detector = Detector(
        families="tag36h11",
        nthreads=1,
        quad_decimate=1.0,
        quad_sigma=0.0,
        refine_edges=1,
        decode_sharpening=0.25,
        debug=0
    )
    tagIds = []

    def update(self, input):
        grayscaleImage = cv.cvtColor(input, cv.COLOR_BGR2GRAY)
        self.tagsDetected = self.detector.detect(grayscaleImage)

        tempIds = []

        for tag in self.tagsDetected:
            tempIds.append(tag.tag_id)

            ptA, ptB, ptC, ptD = tag.corners;

            ptB = (int(ptB[0]), int(ptB[1]))
            ptC = (int(ptC[0]), int(ptC[1]))
            ptD = (int(ptD[0]), int(ptD[1]))
            ptA = (int(ptA[0]), int(ptA[1]))

            cv.line(input, ptA, ptB, (255, 0, 0), 2)
            cv.line(input, ptB, ptC, (255, 0, 0), 2)
            cv.line(input, ptC, ptD, (255, 0, 0), 2)
            cv.line(input, ptD, ptA, (255, 0, 0), 2)

            cv.putText(input, str(tag.tag_id), (ptB[0] + 10, ptB[1] + 15), cv.FONT_HERSHEY_SIMPLEX, 
                   1, (255, 0, 0), 2, cv.LINE_AA)
        
        self.tagIds = tempIds


    def getDetectedIDs(self):
        return self.tagIds

