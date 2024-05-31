""" Converts ground truth format of 'from c0xx to c0xx' into movement ids """

import pandas as pd
import json

# 10: [(10, 16), (16, 10)]
# means for c010
# from c010 to c016 is movement id 0
# from c016 to c010 is movement id 1
annotations = {10: [(10, 16), (16, 10)], 16: [(16, 17), (17, 16)], 17: [(18, 16), (16, 18)], 18: [(17, 20), (20, 17)], 19: [(24, 19), (19, 24)], 20: [(18, 21), (21, 18)], 21: [(20, 22), (22, 20)], 22: [(23, 21), (21, 23)], 23: [(25, 22), (22, 25)], 24: [(19, 27), (27, 19)], 25: [(25, 23), (23, 25)], 26: [(26, 24), (24, 26)], 27: [(27, 24), (24, 27)], 29: [(33, 29), (29, 33)], 33: [(34, 29), (29, 34)], 34: [(33, 34), (34, 33)]}

original_gt_file = "ccd.csv"
formatted_gt_file = "gt_sequences.json"


if __name__ == '__main__':
    data = pd.read_csv(original_gt_file)
    data['camera_id'] = data['camera_id'].apply(lambda x: int(x[-3:]))
    
    # just to make consistent annotations for c024 to make translation easier
    temp = data.loc[data['camera_id'] == 24]
    temp = temp[['from_camera', 'to_camera']].replace("c026", "c027")
    data.loc[data['camera_id'] == 24, ['from_camera', 'to_camera']] = temp
    
    vehicles = {}
    for index, row in data.iterrows():
        corridor = row['corridor_id']
        vehicles.setdefault(corridor, {})
        
        cam = row['camera_id']
        if cam not in annotations:
            print(f"No annotations provided for cam {cam}")
            continue
        mov_candidates = annotations[cam]
        
        movement = -1
        for mov_id, candidate in enumerate(mov_candidates):
            if row['from_camera'] == f'c0{candidate[0]}' and row['to_camera'] == f'c0{candidate[1]}':
                movement = mov_id
                break
        else:
            print(f"Could not find annotation for\n{row}")
                
        vehicles[corridor].setdefault(row['vehicle_id'], []).append((cam, row['to_frame'], movement))
    
    
    # Writes the formatted ground truth to output file
    # The format is as follows:
    # u_id [(cam, frame, movement), ...]
    # where frame corresponds to the last frame the vehicle is on camera
    out_data = {}
    
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
                
                out_data[u_id] = vehicles[corridor][i]
                
                u_id += 1
    
    json.dump(out_data, open(formatted_gt_file, "w"))
