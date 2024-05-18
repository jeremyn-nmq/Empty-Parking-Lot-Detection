import cv2
import numpy as np
import json

def draw_from_json(filename, output_image_path, width, height):
    with open(filename, 'r') as file:
        parking_lot_map = json.load(file)

    parking_lot_map = [[0] + row for row in parking_lot_map]
    with open(filename, 'w') as file:
        json.dump(parking_lot_map, file)

    # Create an empty black image
    image_height = len(parking_lot_map) * height
    image_width = len(parking_lot_map[0]) * width
    image = np.zeros((image_height, image_width, 3), dtype=np.uint8)

    # Color definitions
    colors = {
        0: (255, 255, 255),  # White for road
        1: (128, 128, 128),  # Gray for obstacle
        2: (0, 0, 255),      # Red for occupied
        3: (0, 255, 0),      # Green for vacant
        4: (0, 255, 255)     # Yellow for nearest vacant
    }

    # Draw rectangles based on the values
    for y, row in enumerate(parking_lot_map):
        for x, value in enumerate(row):
            cv2.rectangle(image, (x * width, y * height), ((x + 1) * width - 1, (y + 1) * height - 1), colors[value], -1)

    # Save the image
    cv2.imwrite(output_image_path, image)
    cv2.imshow('Parking Lot Map', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
draw_from_json('result/parking_lot_map.json', 'result/test_carParkImg.png', 105, 43)
