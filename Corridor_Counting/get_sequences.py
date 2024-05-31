import pickle
import os
from get_annotations import *

CAMS_OF_INTEREST = [10, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 33, 34]

def get_sequences():
    local_to_universal_id_map = pickle.load(open('../AICITY2022_Track1_TAG/reid_bidir/reid-matching/tools/test_cluster.pkl', 'rb'))['cluster']
    
    all_detections_root = '../AICITY2022_Track1_TAG/reid_bidir/reid-matching/tools/exp/viz/validation/S05/movement/'
    
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
    
    return sequences
    
            
def write_sequences(sequences, out_file):
    out_data = {}
    for u_id, sequence in sequences.items():
        # Filter out any vehicles that only appear once and aren't given a movement
        if len(sequence) == 1 and sequence[0][1] == -1:
            continue
        
        # Sort the vehicle's movement sequence based on which frame it appears for each camera
        sequences[u_id] = sorted(sequence, key=lambda x: x[2])
        
        out_data[u_id] = sequences[u_id]
            
    json.dump(out_data, open(out_file, "w"))
            
if __name__ == '__main__':
    sequences = get_sequences()
    write_sequences(sequences, "predicted_sequences.json")