import pickle
import os
import numpy as np
from get_annotations import *

""" This algorithm was inspired by 'Countor: count without bells and whistles' (2020)
    by Ospina and Torres

    Portions of this code are from Team 26 in the 2020 AI City Challenge Track 1
        ccw() and line_intersect() are taken from them. We used their approach 
        for determining when a vehicle crosses an exit line
    
"""

CAMS_OF_INTEREST = [10, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 33, 34]


""" Used to determine if two lines intersect """
def ccw(A, B, C):
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

""" Returns True if line AB intersects line CD """
def line_intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


""" Returns True if any of the edges of bbox intersect with exit line """
def rect_intersect(bbox, exit_line):
    x1, y1, x2, y2 = bbox
    left = line_intersect((x1, y1), (x1, y2), exit_line[0], exit_line[1])
    right = line_intersect((x2, y2), (x2, y1), exit_line[0], exit_line[1])
    top = line_intersect((x1, y1), (x2, y1), exit_line[0], exit_line[1])
    bottom = line_intersect((x1, y2), (x2, y2), exit_line[0], exit_line[1])
    
    return left or right or top or bottom
    
#   reid_bidir/reid-matching/tools/exp/viz/validation/S05/trajectory/
#   has dictionaries {local_ids: (all needed info)}
#   so for each local_id, perform tracking based on bbox to match movement
if __name__ == '__main__':    
    detects_root = '../AICITY2022_Track1_TAG/reid_bidir/reid-matching/tools/exp/viz/validation/S05/trajectory/'
    
    movements_root = '../AICITY2022_Track1_TAG/reid_bidir/reid-matching/tools/exp/viz/validation/S05/movement/'

    for pkl_file in os.listdir(detects_root):
        # For cams whose lines are not implemented
        video_id = int(pkl_file.split('.')[0][1:])
        if video_id not in CAMS_OF_INTEREST:
            continue
        
        print("matching movements for cam", video_id)
        
        det_path = os.path.join(detects_root, pkl_file)
        cam_detections = pickle.load(open(det_path, 'rb'))
        
        # Get the exit and movement lines used for matching movements
        num_movs, mov_vectors, mov_exit = get_lines(video_id)
        num_exits, exits = get_exits(video_id)

        # Iterate through each tracklet in the detections
        for local_id in cam_detections.keys():
            # Iterate through each frame of a tracklet to see if/when it crosses an exit line
            matched = False
            tracklet = [x for x in cam_detections[local_id]['tracklet'].items()]
            
            if len(tracklet) > 1:
                frame_num, frame_info = tracklet[0]
                box = frame_info['bbox']
                x1, y1, x2, y2 = box
                
                p0 = ((x1 + x2)/2, (y1 + y2)/2)
                start_point = p0

                for frame_num, frame_info in tracklet[1:]:
                    box = frame_info['bbox']
                    x1, y1, x2, y2 = box

                    p1 = ((x1 + x2)/2, (y1 + y2) /2)

                    # Check if vehicle crossed exit line
                    for exit_num in range(num_exits):
                        if rect_intersect(box, (exits[exit_num][0], exits[exit_num][1])) or line_intersect(p0, p1, exits[exit_num][0], exits[exit_num][1]):
                        # if line_intersect(p0, p1, exits[exit_num][0], exits[exit_num][1]):
                            end_point = p1

                            # Find most similar movement vector
                            vector = np.array([end_point[0] - start_point[0], end_point[1] - start_point[1]])
                            mag_vector = np.linalg.norm(vector)
                            if mag_vector == 0:
                                continue

                            best_sim = 0
                            closest_mov = -1
                            for mov_num in range(num_movs):
                                # Reduce candidates to only movement lines associated with the exit the vehicle crossed
                                if mov_exit is None or mov_exit[mov_num] == exit_num:
                                    mag_mov = np.linalg.norm(mov_vectors[mov_num])
                                    curr_sim = np.dot(vector, mov_vectors[mov_num]) / (mag_vector * mag_mov)

                                    if curr_sim > best_sim:
                                        best_sim = curr_sim
                                        closest_mov = mov_num

                            if closest_mov != -1:
                                # Record the matched movement
                                cam_detections[local_id]["movement_info"] = {'mov_id': closest_mov, 'frame': frame_num}
                                matched = True
                                break
                    # Jump out to the next tracklet
                    if matched:
                        break
                    
                    p0 = p1
                    
                # Reached end of tracklet and it never crossed an exit line (ie parked cars)
                if not matched:
                    cam_detections[local_id]["movement_info"] = {'mov_id': -1, 'frame': -1}

            else:
                cam_detections[local_id]["movement_info"] = {'mov_id': -1, 'frame': -1}
                pass
        
        out_path = os.path.join(movements_root, pkl_file)
        print(f"saving movements in {out_path}")
        pickle.dump(cam_detections, open(out_path, 'wb'))

