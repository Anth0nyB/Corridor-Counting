import os
import numpy as np

def get_video_id(path):
    video_id_dict = {}
    with open(os.path.join(path,'list_video_id.txt'),'r') as f:
        for line in f:
            line = line.rstrip()
            video = line.split(' ')
            video_id_dict[int(video[0])] = video[1]
    return video_id_dict

def get_rois(cam_id,data_path):
    cam_path = os.path.join(data_path, 'ROIs/cam_{}.txt'.format(cam_id))
    print(cam_path)
    with open(cam_path, 'r') as f:
        rois=[]
        for line in f:
            line = line.rstrip()
            p0 = (int(line.split(',')[0]),int(line.split(',')[1]))
            pre=p0
            break
        for line in f:
            line = line.rstrip()
            now = (int(line.split(',')[0]),int(line.split(',')[1]))
            rois.append([pre,now])
            pre=now
        rois.append([pre,p0])
    return len(rois), rois

def get_exits(cam_id):
    """ Gives the lines marking where vehicles exit the intersection.
        These values are hardcoded on a per intersection basis """
    
    print("using exits from cam: ", cam_id)

    if cam_id == 41:
        exits = [
            [(65, 220), (110, 316)], # bottom left exit
            [(950, 866), (1278, 575)], # bottom right exit
            [(921, 167), (1096, 249)], # top right exit
            [(312, 138), (416, 106)] # top left exit
        ]

    elif cam_id == 42:
        exits = [
            [(18, 288), (49, 452)], # bottom left exit
            [(850, 960), (1150, 725)], # bottom right exit
            [(1009, 208), (875, 140)], # top right exit
            [(357, 124), (298, 197)] # top left exit
        ]

    elif cam_id == 43:
        exits = [
            [(10, 168), (44, 386)], # bottom left exit
            [(791, 960), (1029, 719)], # bottom right exit
            [(1280, 273), (1000, 190)], # top right exit
            [(412, 85), (196, 124)] # top left exit
        ]

    return len(exits), exits

def get_lines(cam_id):
    """ Gives the vectors describing each possible movement through the intersection
        These values are hardcoded on a per interseciton basis """
    
    print("using movements from cam: ", cam_id)

    if cam_id == 41:
        # Each movement described as [start_point, end_point]
        # where index i is movement i+1
        movements = [
            [(90, 476), (1000, 189)], # bl straight
            [(111, 408), (321, 126)], # bl left
            [(100, 839), (1187, 723)], # bl right
            [(111, 408), (79, 284)], # bl u-turn

            [(1195, 515), (338, 132)], # br straight
            [(1195, 515), (72, 286)], # br left
            [(1173, 440), (1071, 220)], # br right
            [(1185, 483), (1103, 679)], # br u-turn

            [(696, 114), (76, 270)], # tr straight
            [(785, 142), (1076, 719)], # tr left
            [(598, 116), (317, 127)], # tr right
            [(759, 153), (1005, 201)], # tr u-turn

            [(228, 150), (1088, 701)], # tl straight
            [(268, 137), (1019, 205)], # tl left
            [(177, 172), (76, 274)], # tl right
            [(273, 144), (314, 126)], # tl u-turn
        ]   

        # mov_exits[i] = index of line in exits[] that movement[i] ends at
        mov_exits = [2, 3, 1, 0, 3, 0, 2, 1, 0, 1, 3, 2, 1, 2, 0, 3]


    elif cam_id == 42:
        movements = [
            [(17, 597), (902, 169)], # bl straight
            [(13, 531), (277, 171)], # bl left
            [(81, 891), (1037, 889)], # bl right
            [(11, 534), (6, 413)], # bl u-turn

            [(1046, 450), (286, 170)], # br straight
            [(971, 519), (10, 396)], # br left
            [(1045, 420), (959, 186)], # br right
            [(967, 519), (1008, 869)], # br u-turn

            [(649, 136), (10, 376)], # tr straight
            [(698, 145), (1058, 831)], # tr left
            [(578, 126), (283, 173)], # tr right
            [(681, 146), (904, 186)], # tr u-turn

            [(168, 219), (1041, 805)], # tl straight
            [(230, 200), (892, 185)], # tl left
            [(81, 267), (8, 358)], # tl right
            [(230, 198), (288, 168)], # tl u-turn
        ]     

        mov_exits = [2, 3, 1, 0, 3, 0, 2, 1, 0, 1, 3, 2, 1, 2, 0, 3]


    elif cam_id == 43:
        movements = [
            [(46, 581), (1171, 210)], # bl straight
            [(55, 466), (238, 116)], # bl left
            [(118, 898), (1039, 907)], # bl right
            [(57, 471), (11, 309)], # bl u-turn

            [(1257, 592), (249, 119)], # br straight
            [(1202, 710), (22, 315)], # br left
            [(1269, 485), (1226, 221)], # br right
            [(1185, 712), (1058, 909)], # br u-turn

            [(718, 117), (3, 285)], # tr straight
            [(811, 147), (1051, 910)], # tr left
            [(615, 106), (254, 111)], # tr right
            [(815, 144), (1176, 230)], # tr u-turn

            [(128, 164), (1072, 912)], # tl straight
            [(181, 152), (1171, 213)], # tl left
            [(30, 183), (3, 307)], # tl right
            [(189, 161), (257, 119)], # tl u-turn
        ]

        mov_exits = [2, 3, 1, 0, 3, 0, 2, 1, 0, 1, 3, 2, 1, 2, 0, 3]


    # Convert movement lines to np vectors
    for index, mov in enumerate(movements):
        end = mov[1]
        start = mov[0]

        movements[index] = [end[0] - start[0], end[1] - start[1]]

    return len(movements), np.array(movements), mov_exits


