import cv2
from PIL import Image, ImageDraw
import sys
sys.path.append("../")
from annotations.get_annotations import *

""" Draws the annotated exit lines and movement vectors """

def draw_annotations(video_id):
    video_path = f"../../AICITY2022_Track1_TAG/datasets/Dataset_A/validation/S05/c0{video_id}/vdo.avi"
    video = cv2.VideoCapture(video_path)
    
    _, frame = video.read()

    image = Image.fromarray(frame[:, :, ::-1])  # BGR to RGB
    draw = ImageDraw.Draw(image)

    # Draw exit lines
    _, exits = get_exits(video_id)
    for line in exits:
        draw.line(line, width=4, fill='red')

    # Draw annotated movement vectors
    _, movements, _ = get_lines(video_id, absolute = True)
    for i, mov in enumerate(movements):
        draw.line([(mov[0][0], mov[0][1]), (mov[1][0], mov[1][1])], width=4, fill='blue')
        draw.ellipse([(mov[1][0] - 10, mov[1][1] - 10), (mov[1][0] + 10, mov[1][1] + 10)], width=1, fill='blue')
        
    image.show()
    image.save(f"c0{video_id}_annotated_movements.jpg")


if __name__ == "__main__":
    video_id = input("Enter id of the camera you want movement assignments for\n")
    try:
        video_id = int(video_id)
    except ValueError:
        print("Input must be int")
        
    draw_annotations(video_id)
