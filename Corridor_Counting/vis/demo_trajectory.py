import cv2
import pickle
import argparse

""" Used to generate images of single camera tracking for our presentation """

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("cam", type=int)
    parser.add_argument("id", type=int)
    args = parser.parse_args()
    
    cam = int(args.cam)
    l_id = int(args.id)
    
    
    data = pickle.load(open(f'../../AICITY2022_Track1_TAG/reid_bidir/reid-matching/tools/exp/viz/validation/S05/movement/c0{cam}.pkl', 'rb'))
    
    boxes = {}
    for frame in data[l_id]["tracklet"].values():
        boxes[int(frame['frame'][3:])] = frame['bbox']
        
    
    frames = sorted(list(boxes.keys()))
    bboxes = list(boxes.values())
        
    
    raw_video = cv2.VideoCapture(f'../../AICITY2022_Track1_TAG/datasets/Dataset_A/validation/S05/c0{cam}/vdo.avi')
    
    i = 0
    while i < frames[-1]:
        _, frame =  raw_video.read()
        i += 1
    
    first = bboxes[0]
    prev = ((first[0] + first[2]) / 2, (first[1] + first[3]) / 2)
    for box in bboxes[:-1]:
        center = ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
        print(prev)
        cv2.line(frame, (int(prev[0]), int(prev[1])), (int(center[0]), int(center[1])), (0, 0, 255), 4)
        prev = center
        
    cv2.imwrite(f"trajectory_c0{cam}_{l_id}.jpg", frame)
    
    raw_video.release()                
