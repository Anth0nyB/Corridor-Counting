import os
import sys
sys.path.append("ground_truth/")
from pred_counting import *
from gt_counting import *
from get_sequences import *

from math import sqrt

if __name__ == '__main__':
    gt = gt_counts('ground_truth/corridors.txt', 'ground_truth/gt_sequences.txt')
    
    if not os.path.exists('predicted_sequences.txt'):
        pred_sequences = get_sequences()
        write_sequences(pred_sequences)
    pred = pred_counts('ground_truth/corridors.txt', 'predicted_sequences.txt')
    
    k = 50
    
    print("\nIndividual corridor scores:")
    for corridor, counts in enumerate(gt):
        true_count = counts[VIDEO_LENGTH - 1]
        nwRMSE = 0
        
        wRMSE = 0
        for i in range(int(VIDEO_LENGTH / k)):
            start = i * k
            end = (i + 1) * k - 1
            
            x_bar = pred[corridor][end]
            x = gt[corridor][end]
            
            w = (2 * i) / (k * (k + 1))
            
            wRMSE += w * (x_bar - x)**2
            
        wRMSE = sqrt(wRMSE)
        
        if wRMSE <= true_count:
            nwRMSE = 1 - (wRMSE/true_count)
            
        print(f"corridor: {corridor}, nwRMSE: {nwRMSE}")    
    