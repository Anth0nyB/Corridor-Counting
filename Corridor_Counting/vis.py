"""
Quick and dirty script to visualize movements.
"""
import argparse

import cv2
from PIL import Image, ImageDraw

# ---


# 46
# lines = [
#     [(730, 710), (1270, 460)],  # bottom right exit
#     [(1075, 150), (1275, 195)],  # top right exit
#     [(545, 130), (440, 170)],  # top exit
#     [(15, 250), (15, 370)],  # left exit
# ]
#
# movements = [
#     [(10, 710), (1175, 173)],  # bl straight
#     [(10, 450), (495, 150)],  # bl left
#     [(10, 700), (760, 700)],  # bl right
#     [(10, 450), (10, 300)],  # bl u-turn
#
#     [(1270, 335), (495, 150)],  # r straight
#     [(1270, 335), (10, 300)],  # r left
#     [(1270, 310), (1175, 173)],  # r right
#     [(1270, 375), (1240, 640)],  # r u-turn
#
#     [(827, 136), (10, 300)],  # tr straight
#     [(940, 155), (1160, 660)],  # tr left
#     [(750, 130), (495, 150)],  # tr right
#     [(970, 155), (1175, 173)],  # tr u-turn
#
#     [(255, 210), (870, 647)],  # tl straight
#     [(358, 187), (1175, 173)],  # tl left
#     [(155, 218), (10, 300)],  # tl right
#     [(385, 180), (495, 150)],  # tl u-turn
# ]

# 45
# lines = [
#     [(680, 710), (1200, 510)],  # bottom right exit
#     [(1075, 150), (1230, 195)],  # top right exit
#     [(660, 110), (465, 130)],  # top exit
#     [(60, 215), (60, 340)],  # left exit
# ]
#
# movements = [
#     [(40, 490), (1150, 170)],  # bl straight
#     [(40, 425), (560, 120)],  # bl left
#     [(50, 630), (705, 700)],  # bl right
#     [(40, 375), (40, 275)],  # bl u-turn
#
#     [(1270, 335), (560, 120)],  # r straight
#     [(1270, 335), (40, 275)],  # r left
#     [(1270, 310), (1150, 170)],  # r right
#     [(1230, 425), (1170, 640)],  # r u-turn
#
#     [(890, 140), (40, 275)],  # tr straight
#     [(940, 155), (1120, 640)],  # tr left
#     [(890, 140), (560, 120)],  # tr right
#     [(970, 155), (1150, 170)],  # tr u-turn
#
#     [(320, 155), (1020, 640)],  # tl straight
#     [(415, 135), (1150, 170)],  # tl left
#     [(190, 175), (40, 275)],  # tl right
#     [(415, 135), (560, 120)],  # tl u-turn
# ]

# 44
lines = [
    [(970, 610), (800, 950)],  # bottom right exit
    [(860, 210), (990, 240)],  # top right exit
    [(595, 160), (450, 210)],  # top exit
    [(30, 430), (90, 635)],  # left exit
]

movements = [
    [(100, 700), (940, 230)],  # bl straight
    [(100, 700), (530, 180)],  # bl left
    [(150, 850), (870, 810)],  # bl right
    [(100, 700), (55, 525)],  # bl u-turn

    [(1130, 385), (530, 180)],  # r straight
    [(1150, 465), (55, 525)],  # r left
    [(1140, 360), (940, 230)],  # r right
    [(1150, 465), (920, 720)],  # r u-turn

    [(860, 190), (55, 525)],  # tr straight
    [(860, 190), (895, 755)],  # tr left
    [(790, 180), (530, 180)],  # tr right
    [(860, 190), (905, 225)],  # tr u-turn

    [(205, 310), (895, 760)],  # tl straight
    [(330, 260), (920, 225)],  # tl left
    [(100, 350), (45, 480)],  # tl right
    [(360, 250), (500, 195)],  # tl u-turn
]


# ---


def main(file_path: str):
    video = cv2.VideoCapture(file_path)
    _, frame = video.read()
    image = Image.fromarray(frame[:, :, ::-1])  # BGR to RGB
    draw = ImageDraw.Draw(image)

    for line in lines:
        draw.line(line, width=4, fill=200)

    for mov in movements:
        draw.line(mov, width=4, fill=(0, 0, 200))

    image.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str)
    args = parser.parse_args()
    main(args.file)
