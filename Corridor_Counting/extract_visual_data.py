import ast
import json
import pickle


if __name__ == '__main__':
    try:
        f = open("predicted_sequences.txt", "r")
    except:
        print("Prediction file not found. Have you run 'get_sequences.py'?")
        
        
    
    target_uid = input("Enter u_id of vehicle you want visual data for\n")
    try:
        target_uid = int(target_uid)
    except ValueError:
        print("Input must be int")
        
        
    all_detections_root = '../AICITY2022_Track1_TAG/reid_bidir/reid-matching/tools/exp/viz/validation/S05/movement/'
    for sequence in f:
        u_id, sequence = sequence.split("[")
        if int(u_id) != target_uid:
            continue
        
        outfile = open("visual_info.json", "w")
        result = {"u_id": target_uid, "data": {}}
        
        sequence = "[" + sequence
        sequence = ast.literal_eval(sequence)
        
        for occurance in sequence:
            cam = occurance[0]
            local_id = occurance[1]
            
            cam_data = pickle.load(open(f"{all_detections_root}c0{cam}.pkl", 'rb'))
            
            frames = cam_data[local_id]["frame_list"]
            frames.sort()
            first_frame = frames[0]
            
            boxes = []
            for frame in cam_data[local_id]["tracklet"].values():
                boxes.append(frame['bbox'])

            result["data"][f"c0{cam}"] = {"start_frame": first_frame, "bounding_boxes": boxes}
        
        json.dump(result, outfile)
