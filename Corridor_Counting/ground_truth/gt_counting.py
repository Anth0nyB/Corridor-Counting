import numpy as np
import json

VIDEO_LENGTH = 4300 # number of frames in longest video
NUM_CORRIDORS = 4 # number of predefined corridors

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

def gt_counts(corridors_path, gt_file):
    corridors = parse_corridors(corridors_path)
    gt_data = json.load(open(gt_file, "r"))
    
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
    print(gt_counts('../annotations/corridors.json', 'gt_sequences.json'))
    
                    
                    
        