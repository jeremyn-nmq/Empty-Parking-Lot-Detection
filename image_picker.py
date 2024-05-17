import cv2
import pickle

width, height = 105, 43
try:
    with open('data/carParkPositions', 'rb') as handle:
        positions = pickle.load(handle)
except:
    positions = []

c = open("coord.txt", "w+")
if len(positions) > 0:
    for i, pos in enumerate(positions):
        c.write(str(pos) + ", parked" + "\n")
    c.flush()
def mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        positions.append((x, y))
    if event == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(positions):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                positions.pop(i)
    with open('data/carParkPositions', 'wb') as handle:
        pickle.dump(positions, handle)

def check_parking_space(image):
    for pos in positions:
        cv2.rectangle(image, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)


while True:
    image = cv2.imread('data/carParkImg.png')
    check_parking_space(image)
    cv2.imshow("image", image)
    cv2.setMouseCallback("image", mouse_click)
    cv2.waitKey(1)
