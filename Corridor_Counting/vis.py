"""
Quick and dirty script to visualize movements.
"""
import argparse

import cv2
from PIL import Image, ImageDraw

# ---

colors = ['blue', 'green', 'purple', 'yellow']

exits = [
    [(), ()],  # bottom right exit
    [(), ()],  # top right exit
    [(), ()],  # top exit
    [(), ()],  # left exit
]

movements = [
    [(), ()],  # bl straight
    [(), ()],  # bl left
    [(), ()],  # bl right
    [(), ()],  # bl u-turn

    [(), ()],  # r straight
    [(), ()],  # r left
    [(), ()],  # r right
    [(), ()],  # r u-turn

    [(), ()],  # tr straight
    [(), ()],  # tr left
    [(), ()],  # tr right
    [(), ()],  # tr u-turn

    [(), ()],  # tl straight
    [(), ()],  # tl left
    [(), ()],  # tl right
    [(), ()],  # tl u-turn
]


# ---


def main(file_path: str):
    video = cv2.VideoCapture(file_path)
    _, frame = video.read()
    image = Image.fromarray(frame[:, :, ::-1])  # BGR to RGB
    draw = ImageDraw.Draw(image)

    for line in exits:
        draw.line(line, width=4, fill='red')

    for i, mov in enumerate(movements):
        draw.line(mov, width=4, fill=colors[int(i/4)])
        draw.ellipse([(mov[1][0] - 10, mov[1][1] - 10), (mov[1][0] + 10, mov[1][1] + 10)], width=1, fill=colors[int(i/4)])

    image.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str)
    args = parser.parse_args()
    main(args.file)
