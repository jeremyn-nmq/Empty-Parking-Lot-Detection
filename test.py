import cv2
import numpy as np


def create_map_image(parking_map, original_image):
    colors = {
        0: (255, 255, 255),  # White for road
        1: (128, 128, 128),  # Gray for obstacle
        2: (0, 0, 255),      # Red for occupied
        3: (0, 255, 0),      # Green for vacant
        4: (0, 255, 255)     # Yellow for nearest vacant
    }

    map_height, map_width = len(parking_map), len(parking_map[0])
    map_image = np.zeros((map_height, map_width, 3), dtype=np.uint8)

    for y in range(map_height):
        for x in range(map_width):
            map_image[y, x] = colors[parking_map[y][x]]

    map_image = cv2.resize(map_image, (original_image.shape[1], original_image.shape[0]), interpolation=cv2.INTER_NEAREST)

    return map_image


with open("result/parking_map.txt", "r") as file:
    parking_map = [list(map(int, line.split())) for line in file.readlines()]

original_image = cv2.imread('data/carParkImg.png')

map_image = create_map_image(parking_map, original_image)
cv2.imwrite('result/ParkingSpaceMap.png', map_image)
cv2.imshow('Original Image', original_image)
cv2.imshow('Parking Map Image', map_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
