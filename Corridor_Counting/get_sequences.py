import pickle
import os
import sys
sys.path.append('../AIC_2020_Challenge_Track-1/')
from get_lines import *

CAMS_OF_INTEREST = [10, 16, 17, 18, 20, 21, 22, 23, 25]


if __name__ == '__main__':
    local_to_universal_id_map = pickle.load(open('../AICITY2022_Track1_TAG/reid_bidir/reid-matching/tools/test_cluster.pkl', 'rb'))['cluster']
    
    all_detections_root = '../AICITY2022_Track1_TAG/reid_bidir/reid-matching/tools/exp/viz/validation/S05/movement/'
    
    all_detections = {}
    for pkl_file in os.listdir(all_detections_root):
        video_id = int(pkl_file.split('.')[0][1:])
        if video_id not in CAMS_OF_INTEREST:
            continue
        
        pkl_file_path = os.path.join(all_detections_root, pkl_file)
        cam_detections = pickle.load(open(pkl_file_path, 'rb'))
        
        
        for local_id, data in cam_detections.items():
            if (video_id, local_id) not in local_to_universal_id_map:
                continue
            
            u_id = local_to_universal_id_map[(video_id, local_id)]
            all_detections.setdefault(u_id, []).append((video_id, data['tid'], data['movement_info']['frame'], data['movement_info']['mov_id']))
           
    with open('predicted_sequences.txt', 'w') as f:
        for u_id, sequence in all_detections.items():
            if len(sequence) == 1 and sequence[0][1] == -1:
                continue
            
            all_detections[u_id] = sorted(sequence, key=lambda x: x[2])
            f.write(f"{u_id} {all_detections[u_id]}\n")