import apriltag
import argparse
import cv2
import math

FOCAL_LENGTH = 0.05 # Meter
ACTUAL_WIDTH = 0.2
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to images")
args = vars(ap.parse_args())

def getPerceivedDistance(actualLength, detectedLength, focalLength):
    # Distance = width * focal length /  
    return (actualLength * focalLength / detectedLength)

def getDistanceBetweenPoints(x1, y1, x2, y2):
    return(math.sqrt((x1-x2)**2 + (y1-y2)**2))

# Convert to greyscale
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# AprilTag processing
options = apriltag.DetectorOptions(families="tag36h11")
detector = apriltag.Detector(options)
results = detector.detect(gray)
print("Found {} tags! ".format(len(results)))
for r in results:
    (pa, pb, pc, pd) = r.corners
    pointA = (int(pa[0]), int(pa[1]))
    pointB = (int(pb[0]), int(pb[1]))
    pointC = (int(pc[0]), int(pc[1]))
    pointD = (int(pd[0]), int(pd[1]))
    distA = getDistanceBetweenPoints(pa[0], pb[0], pa[1], pb[1])
    pdistanceA =getPerceivedDistance(ACTUAL_WIDTH, distA, FOCAL_LENGTH)
    distB = getDistanceBetweenPoints(pb[0], pc[0], pb[1], pc[1])
    pdistanceB =getPerceivedDistance(ACTUAL_WIDTH, distB, FOCAL_LENGTH)
    distC = getDistanceBetweenPoints(pc[0], pd[0], pc[1], pd[1])
    pdistanceC =getPerceivedDistance(ACTUAL_WIDTH, distC, FOCAL_LENGTH)
    distD = getDistanceBetweenPoints(pd[0], pa[0], pd[1], pa[1])
    pdistanceD =getPerceivedDistance(ACTUAL_WIDTH, distD, FOCAL_LENGTH)
    averageDistance = (distA + distB + distC + distD)/4
    averageDistance = "{dist:.2f}".format(dist = averageDistance)
    cv2.line(image, pointA, pointB, (0,255,0), 2)
    cv2.line(image, pointB, pointC, (0,255,0), 2)
    cv2.line(image, pointC, pointD, (0,255,0), 2)
    cv2.line(image, pointD, pointA, (0,255,0), 2)
    cv2.putText(image, averageDistance, (int(pa[0]), int(pa[1]) - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)
cv2.imshow("Image", image)
cv2.waitKey(0)


