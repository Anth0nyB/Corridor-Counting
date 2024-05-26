import json
import os
import numpy as np

""" Returns the exit lines for the given cam """
def get_exits(cam_id):
    calling_dir = os.getcwd()
    this_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(this_dir)
    
    annotations = json.load(open("annotations/exit_lines.json", "r"))
    exits = annotations[str(cam_id)]
    
    os.chdir(calling_dir)
    
    ret = []
    for e in exits:
        line = e["line"]
        for i, point in enumerate(line):
            line[i] = tuple(point)
        ret.append(line)
    
    return len(ret), ret


""" Returns the movement vectors and corresponding exits for the given cam """
def get_lines(cam_id, *, absolute = False):
    calling_dir = os.getcwd()
    this_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(this_dir)
    
    # Read in movement vectors from annotation file
    annotations = json.load(open("annotations/movement_vectors.json", "r"))
    movements = annotations[str(cam_id)]
    
    os.chdir(calling_dir)
    
    moves = []
    exits = []
    for m in movements:
        exits.append(m["exit"])
        
        # Convert the coordinates of the movement line to a vector
        if not absolute:
            line = m["vector"]
            x = line[1][0] - line[0][0]
            y = line[1][1] - line[0][1]
            moves.append([x, y])
        else:
            vector = []
            for point in m["vector"]:
                vector.append(tuple(point))
            moves.append(vector)
    
    return len(moves), np.array(moves), exits
