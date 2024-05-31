import json
import os
import pickle
import numpy as np

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

def get_predicted_sequences(test_cluster_path, all_detections_root):
    local_to_universal_id_map = pickle.load(open(test_cluster_path, 'rb'))['cluster']
        
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
            sequences.setdefault(u_id, []).append((video_id, data['tid'], data['movement_info']['frame'], data['movement_info']['mov_id']))
    
    filtered_sequences = {}
    for u_id, sequence in sequences.items():
        # Filter out any vehicles that only appear once and aren't given a movement
        if len(sequence) == 1 and sequence[0][1] == -1:
            continue
        
        # Sort the vehicle's movement sequence based on which frame it appears for each camera
        filtered_sequences[u_id] = sorted(sequence, key=lambda x: x[2])
        
    return filtered_sequences    


def pred_counts(corridors_path, *, save_predicted_sequences = False):
    corridors = parse_corridors(corridors_path)
    
    test_cluster_path = '../AICITY2022_Track1_TAG/reid_bidir/reid-matching/tools/test_cluster.pkl'
    all_detections_root = '../AICITY2022_Track1_TAG/reid_bidir/reid-matching/tools/exp/viz/validation/S05/movement/'
    predictions = get_predicted_sequences(test_cluster_path, all_detections_root)
    
    if save_predicted_sequences:
        json.dump(predictions, open("predicted_sequences.json", "w"))
    
    # Get counts based on predefined corridors
    predicted_counts = np.zeros(shape=(NUM_CORRIDORS, VIDEO_LENGTH))
        
    for u_id, movs in predictions.items():
        # Check if the movement sequence for each corridor is contained within the prediction
        for cor_seq, cor_id in corridors:
            frame = 0
            for event in cor_seq:                    
                y = [(x[0], x[3]) for x in movs]
                if event not in y:
                    break
                frame = max(frame, int(movs[y.index(event)][2]))
            else:
                for j in range(frame, VIDEO_LENGTH):
                    predicted_counts[cor_id][j] += 1
                    
    # A frame by frame view of the corridor counts 
    # where row i corresponds to the corridor i counts
    # and column j corresponds to the count through frame j 
    return predicted_counts
    

if __name__ == '__main__':
    print(pred_counts("annotations/corridors.json"))
        
    
                    
        