import cv2
import pickle
import argparse

""" Used to generate images of bounding boxes for our presentation """

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("cam", type=int)
    parser.add_argument("frame", type=int)
    args = parser.parse_args()
    
    cam = int(args.cam)
    frame = int(args.frame)
    
    
    data = pickle.load(open(f'../../AICITY2022_Track1_TAG/reid_bidir/reid-matching/tools/exp/viz/validation/S05/movement/c0{cam}.pkl', 'rb'))
    
    boxes = []
    for track in data.values():
        if frame in track["tracklet"]:
            boxes.append(track["tracklet"][frame]["bbox"])
        
        
    
    raw_video = cv2.VideoCapture(f'../../AICITY2022_Track1_TAG/datasets/Dataset_A/validation/S05/c0{cam}/vdo.avi')
    
    i = 0
    while i < frame:
        _, img =  raw_video.read()
        i += 1
    
    for box in boxes:
        img = cv2.rectangle(img, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 0, 255), 4) 
        
    cv2.imwrite(f"detection_c0{cam}_{frame}.jpg", img)
    
    raw_video.release()
                
