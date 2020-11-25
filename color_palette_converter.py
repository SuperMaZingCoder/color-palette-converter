import argparse
import os
import time

from colorit import color
from colorit import Colors
from colorit import init_colorit
import cv2 as cv
import numpy


def distance(p1, p2):
    """Return a modified euclidean distance value between two points."""
    difference = numpy.subtract(p1, p2)
    squared = numpy.square(difference)
    distance = numpy.sum(squared)
    return distance


def nearest_color(rgb):
    return min(colors_rgb.values(), key=lambda c: distance(rgb, c))


colors_rgb = {
    "black": [49, 55, 61],
    "blue": [85, 172, 238],
    "brown": [193, 105, 79],
    "green": [120, 177, 89],
    "orange": [244, 144, 12],
    "purple": [244, 144, 12],
    "red": [221, 46, 68],
    "white": [230, 231, 232],
    "yellow": [253, 203, 88],
}


parser = argparse.ArgumentParser()
parser.add_argument("image", help="the image to convert")
parser.add_argument(
    "--percentage-interval",
    "-p",
    type=int,
    default=10,
    help="the interval at which percentages are printed, defaults to 10",
)
args = parser.parse_args()

init_colorit()

print(color("Retrieving image...", Colors.blue))
bgr_img = cv.imread(args.image)
rgb_img = cv.cvtColor(bgr_img, cv.COLOR_BGR2RGB)
height, width = rgb_img.shape[:2]
print(color("Image retrieved...", Colors.blue))

start = time.time()

interval = int(height / (100 / args.percentage_interval))
percentages = {
    interval * i: i * args.percentage_interval
    for i in range(1, int(100 / args.percentage_interval) + 1)
}

for row_number, row in enumerate(range(height)):
    for column in range(width):
        rgb_img[row, column] = nearest_color(rgb_img[row, column])
    if row_number in percentages:
        print(color(f"{percentages[row_number]}% finished.", Colors.green))

end = time.time()
print(f"Operation completed in {color(end - start, Colors.blue)} seconds.")


filename = os.path.splitext(args.image)[0]
cv.imwrite(f"{filename}_discord.png", rgb_img)
os.system(f"xclip -selection clipboard -t image/png -i {filename}_discord.png")
