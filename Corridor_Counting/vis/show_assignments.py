import os
import pickle


""" For debugging annotations. Generates lines representing each vehicle's final trajectory 
    and groups them based on which movement they were assigned to. """
if __name__ == '__main__':        
    movements_root = '../../AICITY2022_Track1_TAG/reid_bidir/reid-matching/tools/exp/viz/validation/S05/movement/'
    
    
    assignment_info = {}
    for pkl_file in os.listdir(movements_root):
        video_id = int(pkl_file.split('.')[0][1:])
        assignment_info[video_id] = {}
        cam_detections = pickle.load(open(os.path.join(movements_root, pkl_file), 'rb'))
        
        for local_id, data in cam_detections.items():
            tracklet = [x for x in cam_detections[local_id]['tracklet'].items()]

            if data["movement_info"]["mov_id"] not in assignment_info[video_id]:
                assignment_info[video_id][data["movement_info"]["mov_id"]] = []
                
            assignment_info[video_id][data["movement_info"]["mov_id"]].append([tracklet[0][1]['bbox'], tracklet[-1][1]['bbox']])
    
    pickle.dump(assignment_info, open("assignment_info.pkl", "wb"))