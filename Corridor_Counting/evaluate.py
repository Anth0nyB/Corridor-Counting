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
    segment_size = int(VIDEO_LENGTH / k)
    
    for corridor, counts in enumerate(gt):
        true_count = counts[-1]
        nwRMSE = 0
        
        wRMSE = 0
        for i in range(k):
            start = i * segment_size
            end = (i + 1) * segment_size - 1
            
            if counts[start] == counts[end] and counts[start] == true_count:
                if pred[corridor][start] == pred[corridor][end] and pred[corridor][start] == pred[corridor][-1]:
                    print(f'Corridor {corridor} score evaluated through frame {start - 1}')
                    break
            
            x_bar = pred[corridor][end]
            x = gt[corridor][end]
            
            w = (2 * i) / (k * (k + 1))
            
            wRMSE += w * (x_bar - x)**2
            
        else:
            print(f'Corridor {corridor} score evaluated through frame {end}')
            
        wRMSE = sqrt(wRMSE)
        
        if wRMSE <= true_count:
            nwRMSE = 1 - (wRMSE/true_count)
            
        print(f"wRMSE: {wRMSE}")
        print(f"nwRMSE: {nwRMSE}\n")    
