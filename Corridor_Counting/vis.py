"""
Quick and dirty script to visualize movements.
"""
import argparse

import cv2
from PIL import Image, ImageDraw

# ---


colors = [(200, 200, 100),
          (200, 100, 200),
          (0, 0, 200),
          (0, 200, 0)
          ]

exits = [
    [(), ()], # bottom left exit
    [(), ()], # bottom right exit
    [(), ()], # top right exit
    [(), ()] # top left exit
]

movements = [
            [(), ()], # bl straight
            [(), ()], # bl left
            [(), ()], # bl right
            [(), ()], # bl u-turn

            [(), ()], # br straight
            [(), ()], # br left
            [(), ()], # br right
            [(), ()], # br u-turn

            [(), ()], # tr straight
            [(), ()], # tr left
            [(), ()], # tr right
            [(), ()], # tr u-turn

            [(), ()], # tl straight
            [(), ()], # tl left
            [(), ()], # tl right
            [(), ()], # tl u-turn
        ]   

# mov_exits[i] = index of line in exits[] that movement[i] ends at
mov_exits = [2, 3, 1, 0, 3, 0, 2, 1, 0, 1, 3, 2, 1, 2, 0, 3]


# ---


def main(file_path: str):
    video = cv2.VideoCapture(file_path)
    _, frame = video.read()
    image = Image.fromarray(frame[:, :, ::-1])  # BGR to RGB
    draw = ImageDraw.Draw(image)

    for line in exits:
        draw.line(line, width=4, fill=200)

    for i, mov in enumerate(movements):
        draw.line(mov, width=4, fill=colors[int(i/4)])

    image.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str)
    args = parser.parse_args()
    main(args.file)
