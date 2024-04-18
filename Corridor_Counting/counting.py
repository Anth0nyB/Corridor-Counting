import numpy as np
import ast

VIDEO_LENGTH = 5000 # number of frames in longest video
NUM_CORRIDORS = 4 # number of predefined corridors

if __name__ == '__main__':
    
    # Parse the predefined corridors
    corridors = []
    with open("ground_truth/corridors.txt", 'r') as f:
        predef_corridors = f.readlines()
        
        for cor in predef_corridors:
            cor_id, *movs = cor.split(sep=" ")
            
            for i, x in enumerate(movs):
                if '\n' in x:
                    x = x[:-1]
                movs[i] = ast.literal_eval(x)
            corridors.append((movs, int(cor_id)))
        
    
    # Get counts based on predefined corridors
    predicted_counts = np.zeros(shape=(NUM_CORRIDORS, VIDEO_LENGTH))
    with open("predicted_sequences.txt", 'r') as f:
        predictions = f.readlines()
        
        for pred in predictions:
            u_id, *movs = pred.split(sep=" ", maxsplit=1)
            movs = ast.literal_eval(movs[0])
            
            # Check if the movement sequence for each corridor is contained within the prediction
            for cor_seq, cor_id in corridors:
                i = 0
                started = False
                for mov in movs:
                    if i == len(cor_seq):
                        break
                    
                    cam, local_id, frame, mov_id = mov
                    
                    if cam == cor_seq[i][0] and mov_id == cor_seq[i][1]:
                        started = True
                        i += 1
                                
                        if i == len(cor_seq):
                            for j in range(frame, len(predicted_counts[0])):
                                predicted_counts[cor_id][j] += 1
                            break
                        
                    elif started:
                        break
                    
        # A frame by frame view of the corridor counts 
        # where row i corresponds to the corridor i counts
        # and column j corresponds to the count through frame j 
        print(predicted_counts)
        
        # Using AIC evaluation algorithm for vehicle counting (AIC20 Track1)
        # we should be able to get a score for this
        # Just need to create same array for ground truth, which should be same algo 
        # just change line 41 to:    cam, frame, mov_id = mov