import cv2
import pickle
import cvzone
import numpy as np

with open('./api/data/carParkPositions', 'rb') as handle:
    positions = pickle.load(handle)

width, height = 105, 43
image_path = './api/data/carParkImg.png'
image = cv2.imread(image_path)

map_height, map_width, _ = image.shape
parking_map = [[0 for _ in range(map_width)] for _ in range(map_height)]

def calculate_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def check_parking_space(image_dilate, image, start_point):
    min_distance = float('inf')
    nearest_spot = None

    for index, pos in enumerate(positions):
        x, y = pos
        center_pos = (x + width // 2, y + height // 2)
        distance = calculate_distance(start_point, center_pos)
        image_crop = image_dilate[y:y+height, x:x+width]
        count = cv2.countNonZero(image_crop)
        cvzone.putTextRect(image, str(count), (x, y + height - 2), scale=1, thickness=2, offset=0)

        if count > 4350:
            color = (0, 255, 0)
            thickness = 3
            for i in range(x, x + width):
                for j in range(y, y + height):
                    parking_map[j][i] = 3
            if distance < min_distance:
                min_distance = distance
                nearest_spot = (x, y)
        else:
            color = (0, 0, 255)
            thickness = 2
            for i in range(x, x + width):
                for j in range(y, y + height):
                    parking_map[j][i] = 2

        cv2.rectangle(image, (x, y), (x + width, y + height), color, thickness)

    if nearest_spot:
        x, y = nearest_spot
        cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 255), 5)
        for i in range(x, x + width):
            for j in range(y, y + height):
                parking_map[j][i] = 4

def detect_parking_spaces():
    global parking_map
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_blur = cv2.GaussianBlur(image_gray, (3, 3), 1)
    image_thresh = cv2.adaptiveThreshold(image_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25, 16)
    image_median = cv2.medianBlur(image_thresh, 5)
    kernel = np.ones((3, 3), np.uint8)
    image_dilate = cv2.dilate(image_median, kernel, iterations=1)

    start_point = (0, 0)
    check_parking_space(image_dilate, image, start_point)
    return parking_map

if __name__ == '__main__':
    parking_map = detect_parking_spaces()
    with open("./api/result/parking_map.txt", "w") as file:
        for row in parking_map:
            file.write(' '.join(map(str, row)) + '\n')
    cv2.imwrite('./api/result/detectedParkingSpot.png', image)
    cv2.imshow("Parking Map", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
