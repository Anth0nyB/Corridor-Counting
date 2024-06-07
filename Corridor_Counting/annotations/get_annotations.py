import json
import os
import numpy as np

""" Returns the exit lines for the given cam """
def get_exits(cam_id):
    # Messing with directories to find annotations file
    calling_dir = os.getcwd()
    this_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(this_dir)
    
    annotations = json.load(open("exit_lines.json", "r"))
    exits = annotations[str(cam_id)]
    
    os.chdir(calling_dir)
    
    # Not sure if necessary, but converts each point to a tuple
    ret = []
    for e in exits:
        line = e["line"]
        for i, point in enumerate(line):
            line[i] = tuple(point)
        ret.append(line)
    
    return len(ret), ret


""" Returns the movement vectors and corresponding exits for the given cam """
def get_lines(cam_id, *, absolute = False):
    # Messing with directories to find annotations file
    calling_dir = os.getcwd()
    this_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(this_dir)
    
    # Read in movement vectors from annotation file
    annotations = json.load(open("movement_vectors.json", "r"))
    movements = annotations[str(cam_id)]
    
    os.chdir(calling_dir)
    
    moves = []
    exits = []
    for m in movements:
        exits.append(m["exit"])
        
        # Convert the coordinates of the movement vector to <delta x, delta y>
        if not absolute:
            line = m["vector"]
            x = line[1][0] - line[0][0]
            y = line[1][1] - line[0][1]
            moves.append([x, y])
        # absolute = True, don't convert, used by vis scripts when generating images
        else:
            vector = []
            for point in m["vector"]:
                vector.append(tuple(point))
            moves.append(vector)
    
    return len(moves), np.array(moves), exits
