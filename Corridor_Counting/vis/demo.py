import cv2
import ast
import pickle

def get_visual_data(target_uid):
    all_detections_root = '../../AICITY2022_Track1_TAG/reid_bidir/reid-matching/tools/exp/viz/validation/S05/movement/'
    
    for sequence in f:
        u_id, sequence = sequence.split("[")
        if int(u_id) != target_uid:
            continue
        
        visual_data = {"u_id": target_uid, "data": {}}
        
        sequence = "[" + sequence
        sequence = ast.literal_eval(sequence)
        
        for occurance in sequence:
            cam = occurance[0]
            local_id = occurance[1]
            
            cam_data = pickle.load(open(f"{all_detections_root}c0{cam}.pkl", 'rb'))
            
            frames = cam_data[local_id]["frame_list"]
            frames.sort()
            first_frame = frames[0]
            
            mov = cam_data[local_id]["movement_info"]["mov_id"]
            mov_frame = cam_data[local_id]["movement_info"]["frame"]
            
            # frames may need to be sorted 
            # One instance had the last few bboxes at front of values() causing all drawn boxes to be out of sync
            boxes = []
            for frame in cam_data[local_id]["tracklet"].values():
                boxes.append(frame['bbox'])

            visual_data["data"][f"c0{cam}"] = {"start_frame": first_frame, "movement": mov,  "frame_assigned": mov_frame, "bounding_boxes": boxes}
            
    return visual_data

def generate_videos(visual_data):
    u_id = visual_data['u_id']
    u_id_label = f"ID: {u_id}"
    
    text = []

    for cam, info in visual_data['data'].items():
        print(f"writing video {cam}")
        cam_id = int(cam[-3:])
        start_frame = int(info['start_frame'])
        mov_id = int(info['movement'])
        mov_frame = int(info['frame_assigned'])
        boxes = info['bounding_boxes']
        

        # Input video reader
        raw_video = cv2.VideoCapture(f'../../AICITY2022_Track1_TAG/datasets/Dataset_A/validation/S05/{cam}/vdo.avi')

        # Set up output video writer
        fps = 10
        width = int(raw_video.get(3))
        height = int(raw_video.get(4))
        codec = cv2.VideoWriter_fourcc(*'mp4v')
        out_video = cv2.VideoWriter(f'{cam}_annotated.mp4', codec, fps, (width, height))


        i = 0
        box_color = (0, 0, 255) # red
        matched = False
        while raw_video.isOpened():
            ret, frame = raw_video.read()
            if not ret:
                break
            
            # Skip ahead to the frame when the vehicle appears
            if i < start_frame:
                i += 1
                out_video.write(frame)
                continue
            
            # Once vehicle disappears from view, skip to end of video
            if len(boxes) <= i - start_frame:
                i += 1
                out_video.write(frame)
                continue
            
            # Change colors when movement is assigned
            if i == mov_frame:
                box_color = (255, 0, 0) # blue
                text.append(f"Cam {cam_id}: MOV {mov_id}")
                matched = True

            # Draw bounding box
            box = boxes[i - start_frame]
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
            
            # Write info near box
            
            # id on top left corner
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            text_color = (255, 255, 255) # white
            
            text_size, _ = cv2.getTextSize(u_id_label, font, font_scale, 2)
            
            pos = (x1, y1)
            box_tl = (pos[0] - 2, pos[1] - text_size[1] - 2)
            box_br = (pos[0] + text_size[0] + 2, y1) 
            
            cv2.rectangle(frame, box_tl, box_br, box_color, -1)
            cv2.putText(frame, u_id_label, pos, font, font_scale, text_color, 2)
            
            # cam, movements on bottom left corner
            text_color = (0, 0, 255) # red
            pos = (x1, y2 - 1)
            for j, line in enumerate(text):
                if (j == len(text) - 1) and matched:
                    text_color = (255, 0, 0) # blue
                    
                text_size, _ = cv2.getTextSize(line, font, font_scale, 2)
                pos = (pos[0], pos[1] + text_size[1] + 5)
                cv2.putText(frame, line, pos, font, font_scale, text_color, 2)
            
            out_video.write(frame)

            i += 1

        raw_video.release()
        out_video.release()

    cv2.destroyAllWindows()



if __name__ == '__main__':
    try:
        f = open("../predicted_sequences.txt", "r")
    except:
        print("Prediction file not found. Have you run 'get_sequences.py'?")
        
    
    target_uid = input("Enter u_id of vehicle you want visual data for\n")
    try:
        target_uid = int(target_uid)
    except ValueError:
        print("Input must be int")
        
        
    visual_data = get_visual_data(target_uid)
    if not visual_data['data']:
        print(f'Data for vehicle {target_uid} no found')
        exit()
    
    generate_videos(visual_data)