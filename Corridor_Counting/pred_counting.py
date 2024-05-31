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

def pred_counts(corridors_path, predictions_file):
    corridors = parse_corridors(corridors_path)
    predictions = json.load(open(predictions_file, "r"))
    
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
    print(pred_counts("annotations/corridors.json", "predicted_sequences.json"))
        
    
                    
        