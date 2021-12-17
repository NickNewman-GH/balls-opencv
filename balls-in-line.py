import cv2
import numpy as np
from scipy import ndimage
import random
from skimage.measure import label, regionprops

def circularity(region):
    return region.perimeter ** 2 / region.area

cam = cv2.VideoCapture(0)

cv2.namedWindow("Camera")
colors = {
    'pink':[np.array([130, 70, 70]),np.array([170, 255, 255])],
    'blue':[np.array([90, 70, 70]),np.array([130, 255, 255])],
    'green':[np.array([50, 70, 70]),np.array([90, 255, 255])],
    'yellow':[np.array([25, 60, 60]),np.array([50, 255, 255])]}

random_colors = list(colors)
random.shuffle(random_colors)
random_colors = random_colors[:3]
print(random_colors)

is_played = False

while cam.isOpened():
    _, image = cam.read()
    image = image[:, ::-1, :]
    if not is_played:
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        balls_coords = {}
        for color in colors:
            mask = np.array(cv2.inRange(hsv, colors[color][0], colors[color][1]))
            mask = ndimage.binary_closing(mask).astype('uint8')
            labeled = label(mask)
            regions = regionprops(labeled)
            res = cv2.bitwise_and(image, image, mask=mask)
            for region in regions:
                if region.area > 7000 and circularity(region) < 40:
                    balls_coords[color] = region.centroid
                    break
            if len(balls_coords) == len(random_colors):
                prev = None
                if sorted(list(balls_coords)) != sorted(random_colors):
                    print("NO!\nPress 'f' if you want to try again")
                    is_played = True
                    break
                for c in random_colors:
                    if not prev:
                        prev = balls_coords[c][1]
                    elif prev > balls_coords[c][1]:
                        print("NO!\nPress 'f' if you want to try again")
                        is_played = True
                        break
                    else:
                        prev = balls_coords[c][1]
                    if c == random_colors[-1]:
                        print("CONGRATULATIONS!\nYou can restart by pressing the 'r' button")
                        is_played = True
                break

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

    if key == ord('r'):
        random_colors = list(colors)
        random.shuffle(random_colors)
        random_colors = random_colors[:3]
        is_played = False
        print(random_colors)
    
    if key == ord('f'):
        print("Let's try again!")
        is_played = False

    res = cv2.bitwise_and(image, image, mask=mask)
    cv2.imshow('Camera', image)

cam.release()
cv2.destroyAllWindows()