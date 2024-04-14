"""
Quick and dirty script to visualize movements.
"""
import argparse

import cv2
from PIL import Image, ImageDraw

# ---

colors = ['blue', 'green', 'purple', 'yellow']

# c0xx
exits = [
    [(), ()],  # middle exit
]

movements = [
    [(), ()],  # down
    [(), ()],  # up
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

    # for pair in boxes:
    #     start = pair[0]
    #     p0 = (((start[0] + start[2])/2), ((start[1] + start[3])/2))
    #     end = pair[1]
    #     p1 = (((end[0] + end[2])/2), ((end[1] + end[3])/2))
    #     draw.rectangle(start, width=4, outline="green")
    #     draw.rectangle(end, width=4, outline="teal")
    #     draw.line([p0, p1], width=4, fill="orange")
    image.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str)
    args = parser.parse_args()
    main(args.file)
