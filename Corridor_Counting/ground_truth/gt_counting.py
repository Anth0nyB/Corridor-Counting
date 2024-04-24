import numpy as np
import ast

VIDEO_LENGTH = 5000 # number of frames in longest video
NUM_CORRIDORS = 4 # number of predefined corridors

def parse_corridors(corridors_path):
    # Parse the predefined corridors
    corridors = []
    with open(corridors_path, 'r') as f:
        predef_corridors = f.readlines()
        
        for cor in predef_corridors:
            cor_id, *movs = cor.split(sep=" ")
            
            for i, x in enumerate(movs):
                if '\n' in x:
                    x = x[:-1]
                movs[i] = ast.literal_eval(x)
            corridors.append((movs, int(cor_id)))
        
    return corridors

def gt_counts(corridors_path, gt_file):
    corridors = parse_corridors(corridors_path)
    
    # Get counts based on predefined corridors
    counts = np.zeros(shape=(NUM_CORRIDORS, VIDEO_LENGTH))
    with open(gt_file, 'r') as f:
        predictions = f.readlines()
        
        for pred in predictions:
            u_id, *movs = pred.split(sep=" ", maxsplit=1)
            movs = ast.literal_eval(movs[0])
            
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
    print(gt_counts('corridors.txt', 'gt_sequences.txt'))
    
                    
                    
        