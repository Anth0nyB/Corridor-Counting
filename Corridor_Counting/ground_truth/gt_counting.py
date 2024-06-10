import numpy as np
import pandas as pd
import json
import os

VIDEO_LENGTH = 4300 # number of frames in longest video
NUM_CORRIDORS = 4 # number of predefined corridors

def parse_corridors(annotations_dir):
    corridors_path = os.path.join(annotations_dir, "corridors.json")
    corridors = json.load(open(corridors_path, "r"))
    
    parsed_corridors = []
    for key, corridor_data in corridors.items():
        if key == "notes":
            continue
        
        corridor_id = int(key.split(" ")[1])
        
        for sequence in corridor_data.values():
            movements = [(step["cam"], step["movement"]) for step in sequence]
            parsed_corridors.append((movements, corridor_id))
            
    return parsed_corridors


""" Converts ground truth format of 'from c0xx to c0xx' into movement ids """
def get_gt_sequences(gt_dir):
    conversions_path = os.path.join(gt_dir, "conversions.json")
    conversions = json.load(open(conversions_path, "r"))

    original_gt_filepath = os.path.join(gt_dir, "ccd.csv")
    data = pd.read_csv(original_gt_filepath)
    data['camera_id'] = data['camera_id'].apply(lambda x: int(x[-3:]))
    data['from_camera'] = data['from_camera'].apply(lambda x: x if pd.isna(x) else int(x[-3:]))
    data['to_camera'] = data['to_camera'].apply(lambda x: x if pd.isna(x) else int(x[-3:]))
    
    # Read in the data and convert to 'movement id' format
    # The format is as follows:
    # u_id [(cam, frame, movement_id), ...]
    # where frame corresponds to the last frame the vehicle is on camera
    vehicles = {}
    for index, row in data.iterrows():
        corridor = row['corridor_id']
        vehicles.setdefault(corridor, {})
        
        cam = str(row['camera_id'])
        if cam not in conversions.keys():
            print(f"No conversions provided for cam {cam}")
            continue
        mov_candidates = conversions[cam]
        
        movement = -1
        for candidate in mov_candidates:
            if row['from_camera'] == candidate["from_camera"] and row['to_camera'] == candidate["to_camera"]:
                movement = candidate["movement_id"]
                break
        else:
            # print(f"Could not find conversion for\n{row}")
            pass
                
        vehicles[corridor].setdefault(row['vehicle_id'], []).append((int(cam), row['to_frame'], movement))
    
    
    # Combine the corridors and assign universal ids (u_ids are not necessary for gt)
    sequences = {}
    u_id = 0
    for corridor, vehicle in vehicles.items():
        for i, sequence in vehicle.items():
            # Filter out any vehicles that only appear on one camera
            if len(sequence) == 1:
                continue
            
            # Filter out any vehicles that were not assigned a movement on any camera
            for detection in sequence:
                if detection[2] == -1:
                    break
                
            else:
                # Sort the vehicle's movement sequence based on which frame it appears for each camera
                vehicles[corridor][i] = sorted(sequence, key=lambda x: x[1])
                
                sequences[u_id] = vehicles[corridor][i]
                
                u_id += 1

    return sequences

# def gt_counts(corridors_path, original_gt_filepath):
def gt_counts(annotations_dir, gt_dir):
    corridors = parse_corridors(annotations_dir)
    gt_data = get_gt_sequences(gt_dir)
    
    # Get counts based on predefined corridors
    counts = np.zeros(shape=(NUM_CORRIDORS, VIDEO_LENGTH))
    
    for u_id, movs in gt_data.items():
        # Check if the movement sequence for each corridor is contained within the prediction
        for cor_seq, cor_id in corridors:
            frame = 0
            for event in cor_seq:                    
                y = [(x[0], x[2]) for x in movs]
                if event not in y:
                    break
                frame = max(frame, int(movs[y.index(event)][1]))
            else:
                for j in range(frame, VIDEO_LENGTH):
                    counts[cor_id][j] += 1

    # A frame by frame view of the corridor counts 
    # where row i corresponds to the corridor i counts
    # and column j corresponds to the count through frame j 
    return counts

if __name__ == '__main__':
    print(gt_counts('../annotations', "./"))
    
                    
                    
        