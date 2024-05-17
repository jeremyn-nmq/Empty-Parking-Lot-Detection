import cv2
import pickle
import cvzone
import numpy as np
import json

width, height = 105, 43
with open('data/carParkPositions', 'rb') as handle:
    positions = pickle.load(handle)
c = open("coord.txt", "w+")

start_point = (0, 0)
max_x = max(pos[0] for pos in positions) + width
max_y = max(pos[1] for pos in positions) + height
grid_width = max_x // width + 1
grid_height = max_y // height + 1

parking_lot_map = [[0] * grid_width for _ in range(grid_height)]

def calculate_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def check_parking_space(image_dilate, image, start_point):
    min_distance = float('inf')
    nearest_spot = None
    vacant_spots = []

    for index, pos in enumerate(positions):
        x, y = pos
        center_pos = (x + width // 2, y + height // 2)
        distance = calculate_distance(start_point, center_pos)

        image_crop = image_dilate[y:y + height, x:x + width]
        count = cv2.countNonZero(image_crop)
        cvzone.putTextRect(image, str(count), (x, y + height - 2), scale=1, thickness=2, offset=0)

        if count > 4350:
            vacant_spots.append((pos, distance))
            parking_lot_map[y // height][x // width] = 3
        else:
            cv2.rectangle(image, pos, (pos[0] + width, pos[1] + height), (0, 0, 255), 2)
            parking_lot_map[y // height][x // width] = 2

    for spot, dist in vacant_spots:
        if dist < min_distance:
            min_distance = dist
            nearest_spot = spot

    for spot, dist in vacant_spots:
        color = (0, 255, 0)
        thickness = 4
        if spot == nearest_spot:
            color = (0, 255, 255)
            thickness = 5
            parking_lot_map[spot[1] // height][spot[0] // width] = 4  # Mark as nearest vacant
        cv2.rectangle(image, spot, (spot[0] + width, spot[1] + height), color, thickness)

    return parking_lot_map

def save_parking_lot_map_json(parking_lot_map, filename="parking_lot_map.json"):
    with open(filename, 'w') as file:
        json.dump(parking_lot_map, file)

while True:
    # if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
    #     cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    image = cv2.imread('data/carParkImg.png')
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_blur = cv2.GaussianBlur(image_gray, (3, 3), 1)
    image_thresh = cv2.adaptiveThreshold(image_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                             cv2.THRESH_BINARY, 25, 16)
    image_median = cv2.medianBlur(image_thresh, 5)
    kernel = np.ones((3, 3), np.uint8)
    image_dilate = cv2.dilate(image_median, kernel, iterations=1)

    parking_lot_map = check_parking_space(image_dilate, image, start_point)
    cv2.imshow('Parking Lot', image)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

parking_lot_map = check_parking_space(image_dilate, image, start_point)
save_parking_lot_map_json(parking_lot_map)