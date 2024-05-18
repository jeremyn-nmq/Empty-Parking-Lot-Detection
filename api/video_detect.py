import cv2
import pickle
import cvzone
import numpy as np

width, height = 105, 43
cap = cv2.VideoCapture('data/carPark.mp4')
with open('../data/carParkPositions', 'rb') as handle:
    positions = pickle.load(handle)
c = open("coord.txt", "w+")
def check_parking_space(image_dilate, image):
    for pos in positions:
        x, y = pos
        image_crop = image_dilate[y:y + height, x:x + width]
        count = cv2.countNonZero(image_crop)
        cvzone.putTextRect(image, str(count), (x, y + height - 2), scale=1, thickness=2, offset=0)

        if count > 4350:
            lines = c.readlines()
            for line in lines:
                print(line)
            color = (0, 255, 0)
            thickness = 4
        else:
            color = (0, 0, 255)
            thickness = 2
        cv2.rectangle(image, pos, (pos[0] + width, pos[1] + height), color, thickness)


while True:
    # if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
    #     cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, image = cap.read()
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_blur = cv2.GaussianBlur(image_gray, (3, 3), 1)
    image_thresh = cv2.adaptiveThreshold(image_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY, 25, 16)
    image_median = cv2.medianBlur(image_thresh, 5)
    kernel = np.ones((3, 3), np.uint8)
    image_dilate = cv2.dilate(image_median, kernel, iterations=1)

    check_parking_space(image_dilate, image)

    cv2.imshow('Video', image)
    cv2.waitKey(10)
