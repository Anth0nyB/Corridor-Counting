import os
import pickle
import cv2
import sys
sys.path.append("../")
from get_annotations import *
from PIL import Image, ImageDraw


""" For debugging annotations. Generates lines representing each vehicle's final trajectory 
    and groups them based on which movement they were assigned to. 
    
        Annotated movement lines are in blue
        Annotated exit lines are in red
        
        Vehicles with no assigned movement are in white
        All other vehicle trajectories are given a color according to their movement
        
"""
    
def get_assignments(movement_files):
    print("Loading assignment info...")
    assignment_info = {}
    for pkl_file in movement_files:
        video_id = int(pkl_file.split('.')[0][1:])
        assignment_info[video_id] = {}
        cam_detections = pickle.load(open(os.path.join(movements_root, pkl_file), 'rb'))
        
        for local_id, data in cam_detections.items():
            tracklet = [x for x in cam_detections[local_id]['tracklet'].items()]

            if data["movement_info"]["mov_id"] not in assignment_info[video_id]:
                assignment_info[video_id][data["movement_info"]["mov_id"]] = []
                
            assignment_info[video_id][data["movement_info"]["mov_id"]].append([tracklet[0][1]['bbox'], tracklet[-1][1]['bbox']])
    
    return assignment_info

def show_assignments(assignments, video_id):
    print("Generating image...")
    colors = ['white', 'yellow', 'green', 'purple', 'teal', 'orange']

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


    # Draw vectors of assigned movements
    for mov_id, bboxes in assignments[video_id].items():
        for pair in bboxes:
            start = pair[0]
            p0 = (((start[0] + start[2])/2), ((start[1] + start[3])/2))
            end = pair[1]
            p1 = (((end[0] + end[2])/2), ((end[1] + end[3])/2))

            draw.line([p0, p1], width=4, fill=colors[(mov_id + 1) % len(colors)])
            draw.ellipse([(p1[0] - 10, p1[1] - 10), (p1[0] + 10, p1[1] + 10)], width=1, fill=colors[(mov_id + 1) % len(colors)])

    image.show()
    image.save(f"c0{video_id}_assigned_movements.jpg")


if __name__ == '__main__':
    video_id = input("Enter id of the camera you want movement assignments for\n")
    try:
        video_id = int(video_id)
    except ValueError:
        print("Input must be int")
             
    movements_root = '../../AICITY2022_Track1_TAG/reid_bidir/reid-matching/tools/exp/viz/validation/S05/movement/'
    movement_files = os.listdir(movements_root)
    
    assignments = get_assignments(movement_files)
    show_assignments(assignments, video_id)
    