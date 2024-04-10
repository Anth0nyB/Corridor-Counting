import pandas as pd

annotations = {10: [(10, 16), (16, 10)], 16: [(16, 17), (17, 16)], 17: [(18, 16), (16, 18)], 18: [(17, 20), (20, 17)], 20: [(18, 21), (21, 18)], 21: [(20, 22), (22, 20)], 22: [(23, 21), (21, 23)], 23: [(25, 22), (22, 25)], 25: [(25, 23), (23, 25)]}

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
    
    
    for u_id, sequence in vehicles.items():     
        vehicles[u_id] = sorted(sequence, key=lambda x: x[1])
        print(u_id, vehicles[u_id])
