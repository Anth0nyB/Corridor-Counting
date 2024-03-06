"""
Quick and dirty script to visualize movements.
"""
import argparse

import cv2
from PIL import Image, ImageDraw

# ---

line_1 = [(220, 586), (855, 672)]
line_2 = [(1018, 655), (1525, 694)]
mov_rois = [2, 0]
lines = [line_1, line_2]


# ---


def main(file_path: str):
    video = cv2.VideoCapture(file_path)
    _, frame = video.read()
    image = Image.fromarray(frame[:, :, ::-1])  # BGR to RGB
    draw = ImageDraw.Draw(image)

    for line in lines:
        draw.line(line, width=4, fill=200)

    image.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str)
    args = parser.parse_args()
    main(args.file)
