"""
Quick and dirty script to visualize movements.
"""
import argparse

import cv2
from PIL import Image, ImageDraw

# ---


lines = [
    [(65, 263), (110, 316)],
    [(950, 866), (1278, 650)],
    [(970, 181), (1096, 249)],
    [(312, 138), (347, 124)]
]

movements = [
    [(90, 476), (1000, 189)], # bl straight
    [(111, 408), (321, 126)], # bl left
    [(100, 839), (1187, 723)], # bl right
    [(111, 408), (79, 284)], # bl u-turn
    [(1195, 515), (338, 132)], # br straight
    [(1195, 515), (72, 286)], # br left
    [(1173, 440), (1071, 220)], # br right
    [(), ()],
    [(), ()],
    [(), ()],
    [(), ()],
    [(), ()],
    [(), ()],
    [(), ()],
    [(), ()],
    [(), ()],
    [(), ()],
    [(), ()],
    [(), ()],
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
