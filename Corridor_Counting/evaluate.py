import argparse
from prediction_counting import *
from ground_truth.gt_counting import *
from math import sqrt

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('k', type=int, help="The number of segments, k, to separate the counts into when calculating wRMSE")
    parser.add_argument('-f', action='store_true', help="Force recompute the predicted corridor counts instead of loading them.")
    args = parser.parse_args()

    k = args.k
    segment_size = int(VIDEO_LENGTH / k)
    
    print(f"\nEvaluating results using k={k} segments.\n")
    
    recompute = args.f
    
    gt = gt_counts('annotations/', "ground_truth/")
    pred = pred_counts('annotations/corridors.json', recompute=recompute)
    
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
