import argparse
import json
import os
import pickle
import numpy as np
import pandas as pd

VIDEO_LENGTH = 4300 # number of frames in longest video
NUM_CORRIDORS = 4 # number of predefined corridors
CAMS_OF_INTEREST = [10, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 33, 34]

def parse_corridors(corridors_path):
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

def get_predicted_sequences(local_to_universal_map_path, all_detections_root):
    local_to_universal_id_map = pickle.load(open(local_to_universal_map_path, 'rb'))['cluster']
        
    sequences = {}
    for pkl_file in os.listdir(all_detections_root):
        video_id = int(pkl_file.split('.')[0][1:])
        if video_id not in CAMS_OF_INTEREST:
            continue
        
        print(f'Extracting movement sequences for vehicles in c0{video_id}')
        
        pkl_file_path = os.path.join(all_detections_root, pkl_file)
        cam_detections = pickle.load(open(pkl_file_path, 'rb'))
        
        
        for local_id, data in cam_detections.items():
            if (video_id, local_id) not in local_to_universal_id_map:
                continue
            
            u_id = local_to_universal_id_map[(video_id, local_id)]
            sequences.setdefault(u_id, []).append({"cam": video_id, "local_id": data['tid'], "mov_id": data['movement_info']['mov_id'], "frame_assigned": data['movement_info']['frame']})
    
    filtered_sequences = {}
    for u_id, sequence in sequences.items():
        # Filter out any vehicles that only appear once and aren't given a movement
        if len(sequence) == 1 and sequence[0][1] == -1:
            continue
        
        # Sort the vehicle's movement sequence based on which frame it appears for each camera
        filtered_sequences[u_id] = sorted(sequence, key=lambda x: x["frame_assigned"])
        
    return filtered_sequences    


def pred_counts(corridors_path, *, recompute = False):
    if not recompute:
        predicted_counts = pd.read_csv("predicted_counts.csv", sep=",", index_col=0)
        return predicted_counts.to_numpy()
    
    corridors = parse_corridors(corridors_path)
    
    local_to_universal_map_path = '../AICITY2022_Track1_TAG/reid_bidir/reid-matching/tools/local_to_universal_map.pkl'
    all_detections_root = '../AICITY2022_Track1_TAG/reid_bidir/reid-matching/tools/exp/viz/validation/S05/movement/'
    
    print("computing vehicle movement sequences...")
    predictions = get_predicted_sequences(local_to_universal_map_path, all_detections_root)
    
    print("saving vehicle movement sequences to 'predicted_sequences.json'")
    json.dump(predictions, open("predicted_sequences.json", "w"))

    print()
    
    # Get counts based on predefined corridors.
    # A frame by frame view of the corridor counts 
    # where row i corresponds to the corridor i counts
    # and column j corresponds to the count through frame j.
    print("computing corridor counts...")
    predicted_counts = np.zeros(shape=(NUM_CORRIDORS, VIDEO_LENGTH))
        
    for u_id, movs in predictions.items():
        # Check if the movement sequence for each corridor is contained within the prediction
        for cor_seq, cor_id in corridors:
            frame = 0
            for event in cor_seq:                    
                y = [(x["cam"], x["mov_id"]) for x in movs]
                if event not in y:
                    break
                frame = max(frame, int(movs[y.index(event)]["frame_assigned"]))
            else:
                for j in range(frame, VIDEO_LENGTH):
                    predicted_counts[cor_id][j] += 1
                    
    
    # Results saved in csv in case they are needed 
    print("saving predicted corridor counts to 'predicted_counts.csv'")
    to_save = pd.DataFrame(predicted_counts)
    to_save = to_save.astype(int)
    to_save.index = [f'Corridor {i}' for i in range(0, len(to_save))]
    to_save.columns.name = "Frame"
    to_save.to_csv("predicted_counts.csv", sep=",")
    
    return predicted_counts
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', action='store_true', help="Force recompute the vehicle movement sequences and corridor counts instead of loading them.")

    args = parser.parse_args()

    pred_counts("annotations/corridors.json", recompute=args.f)