""" Converts ground truth format of 'from c0xx to c0xx' into movement ids """

import pandas as pd

# 10: [(10, 16), (16, 10)]
# means for c010
# from c010 to c016 is movement id 0
# from c016 to c010 is movement id 1
annotations = {10: [(10, 16), (16, 10)], 16: [(16, 17), (17, 16)], 17: [(18, 16), (16, 18)], 18: [(17, 20), (20, 17)], 19: [(24, 19), (19, 24)], 20: [(18, 21), (21, 18)], 21: [(20, 22), (22, 20)], 22: [(23, 21), (21, 23)], 23: [(25, 22), (22, 25)], 24: [(19, 27), (27, 19)], 25: [(25, 23), (23, 25)], 26: [(24, 26), (26, 24)], 27: [(27, 24), (24, 27)], 29: [(33, 29), (29, 33)], 33: [(34, 29), (29, 34)], 34: [(33, 34), (34, 33)]}

if __name__ == '__main__':
    data = pd.read_csv('ccd.csv')
    data['camera_id'] = data['camera_id'].apply(lambda x: int(x[-3:]))
    
    vehicles = {}
    for index, row in data.iterrows():
        cam = row['camera_id']
        if cam not in annotations:
            continue
        mov_candidates = annotations[cam]
        
        movement = -1
        for mov_id, candidate in enumerate(mov_candidates):
            if row['from_camera'] == f'c0{candidate[0]}' and row['to_camera'] == f'c0{candidate[1]}':
                movement = mov_id

        vehicles.setdefault(row['vehicle_id'], []).append((cam, row['to_frame'], movement))
    
    
    with open("gt_sequences.txt", "w") as f:
        for u_id, sequence in vehicles.items():
            if len(sequence) == 1:
                continue
            
            for detection in sequence:
                if detection[2] == -1:
                    break
            else:
                vehicles[u_id] = sorted(sequence, key=lambda x: x[1])
                f.write(f"{u_id} {vehicles[u_id]}\n")
