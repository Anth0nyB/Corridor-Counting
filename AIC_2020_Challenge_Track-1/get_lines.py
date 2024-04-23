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
    
    # print("using exits from cam: ", cam_id)
    
    if cam_id == 10:
        exits = [
            [(857, 300), (1200, 220)],  # top exit
            [(150, 900), (900, 900)],  # bottom exit
        ]
    
    elif cam_id == 16:
        exits = [
            [(450, 450), (1420, 450)],  # middle exit
        ]
        
    elif cam_id == 17:
        exits = [
            [(360, 500), (1500, 500)],  # middle exit
        ]
        
    elif cam_id == 18:
        exits = [
            [(1300, 1100), (2060, 1530)],  # middle exit
        ]

    elif cam_id == 19:
        exits = [
            # [(1250, 450), (1535, 450)],  # top exit
            [(715, 900), (715, 1620)],  # middle exit
            # [(2250, 1530), (2250, 1920)],  # right exit
        ]
        
    elif cam_id == 20:
        exits = [
            [(587, 1037), (1246, 746)],  # middle exit
        ]
        
    elif cam_id == 21:
        exits = [
            [(342, 435), (1787, 312)],  # middle exit
        ]
        
    elif cam_id == 22:
        exits = [
            [(100, 900), (700, 900)],  # bottom exit
            [(1000, 200), (1150, 200)],  # top exit
        ]
        
    elif cam_id == 23:
        exits = [
            [(1280, 850), (1870, 1175)],  # middle exit
        ]

    elif cam_id == 24:
        exits = [
            [(1360, 810), (1360, 1920)],  # middle
        ]
        
    elif cam_id == 25:
        exits = [
            [(966, 1163), (1315, 929)],  # middle exit
            [(2000, 1525), (1550, 1850)],  # bottom right exit
        ]
    
    elif cam_id == 26:
        exits = [
            [(1355, 580), (819, 584)],  # middle exit
        ]

    elif cam_id == 27:
        exits = [
            [(1120, 710), (1470, 500)],  # bottom
            [(490, 170), (670, 140)],  # top
        ]

    elif cam_id == 29:
        exits = [
            [(1250, 290), (1400, 290)],  # top
            [(260, 545), (990, 635)],  # bottom
        ]

    elif cam_id == 33:
        exits = [
            [(1000, 400), (1560, 400)],  # top
            [(135, 765), (985, 765)],  # bottom
        ]

    elif cam_id == 34:
        exits = [
            [(350, 150), (430, 145)],  # top
            [(1245, 685), (1735, 555)],  # bottom
        ]
        
    elif cam_id == 41:
        exits = [
            [(65, 220), (110, 316)], # bottom left exit
            [(950, 866), (1278, 575)], # bottom right exit
            [(921, 167), (1096, 249)], # top right exit
            [(312, 138), (416, 106)] # top left exit
        ]

    elif cam_id == 42:
        exits = [
            [(25, 288), (49, 452)], # bottom left exit
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

    elif cam_id == 44:
        exits = [
            [(30, 430), (90, 635)],  # bottom left exit
            [(970, 610), (800, 950)],  # bottom right exit
            [(860, 210), (990, 240)],  # top right exit
            [(595, 160), (450, 210)],  # top left exit
        ]

    elif cam_id == 45:
        exits = [
            [(60, 215), (60, 340)],  # bottom left exit
            [(680, 710), (1200, 510)],  # bottom right exit
            [(1075, 150), (1230, 195)],  # top right exit
            [(660, 110), (465, 130)],  # top left exit
        ]

    elif cam_id == 46:
        exits = [
            [(15, 250), (15, 370)],  # bottom left exit
            [(730, 710), (1270, 460)],  # bottom right exit
            [(1075, 150), (1275, 195)],  # top right exit
            [(575, 110), (440, 170)],  # top left exit
        ]

    return len(exits), exits

def get_lines(cam_id):
    """ Gives the vectors describing each possible movement through the intersection
        These values are hardcoded on a per interseciton basis """
    
    # print("using movements from cam: ", cam_id)

    # mov_exits[i] = index of line in exits[] that movement[i] ends at
    # This is really only important for intersections with many possible movements, to reduce candidates for matching movements
    # If there aren't many intersections, it will be None, as it is not needed for matching movements
    mov_exits = None
    
    if cam_id == 10:
        # Each movement described as [start_point, end_point]
        # where index i is movement i+1
        movements = [
            [(1100, 1080), (950, 200)],  # up
            [(730, 130), (550, 900)],  # down
        ]
        # c10 to c16: 0
        # c16 to c10: 1
        
        mov_exits = [0, 1]
    
    elif cam_id == 16:
        movements = [
            [(1111, 150), (800, 450)],  # down
            [(1500, 1000), (1200, 450)],  # up
        ]
        # c16 to c17: 0
        # c17 to c16: 1
        
        mov_exits = [0, 0]
        
    elif cam_id == 17:
        movements = [
            [(1100, 250), (800, 500)],  # down
            [(1900, 770), (1250, 500)],  # up
        ]
        # c18 to c16: 0
        # c16 to c18: 1
        
        mov_exits = [0, 0]
        
    elif cam_id == 18:
        movements = [
            [(100, 1700), (1800, 1400)],  # up
            [(2150, 1350), (1380, 1240)],  # down
        ]
        # c17 to c20: 0
        # c20 to c17: 1
        
        mov_exits = [0, 0]

    elif cam_id == 19:
        movements = [
            [(2450, 1250), (260, 1110)],  # r straight
            [(320, 1630), (2330, 1730)],  # l straight
            # [(2450, 1250), (1450, 475)],  # r right
            # [(1400, 450), (320, 1130)],  # t right
            # [(320, 1630), (1370, 420)],  # l left (illegal!)
        ]
        # c24 to c19: 0
        # c19 to c24: 1

        mov_exits = [0, 0]
        
    elif cam_id == 20:
        movements = [
            [(365, 769), (653, 956)],  # down
            [(2526, 900), (1080, 850)],  # up
        ]
        # c18 to c21: 0
        # c21 to c18: 1
        
        mov_exits = [0, 0]
        
    elif cam_id == 21:
        movements = [
            [(948, 127), (800, 400)],  # down
            [(1872, 729), (1250, 400)],  # up
        ]
        # c20 to c22: 0
        # c22 to c20: 1
        
        mov_exits = [0, 0]
        
    elif cam_id == 22:
        movements = [
            [(900, 200), (350, 900)],  # down
            [(1000, 1000), (1050, 200)],  # up
        ]
        # c23 to c21: 0
        # c21 to c23: 1

        mov_exits = [0, 1]
        
    elif cam_id == 23:
        movements = [
            [(1900, 930), (1400, 970)],  # down
            [(240, 1600), (1700, 1090)],  # up
        ]
        # c25 to c22: 0
        # c22 to c25: 1
        
        mov_exits = [0, 0]

    elif cam_id == 24:
        movements = [
            # [(530, 580), (1820, 1720)],  # tl left
            [(420, 1780), (2265, 1700)],  # l straight
            [(2200, 1085), (400, 1130)],  # r straight or left
        ]
        # c19 to c27: 0
        # c27 to c19: 1

        
        mov_exits = [0, 0, 0]
        
    elif cam_id == 25:
        # c25 to c23: 0
        # c23 to c25: 1
        movements = [
            [(2536, 1273), (1300, 1130)],  # left
            [(500, 1150), (2245, 1749)],  # right
        ]
        
        mov_exits = [0, 1]
    
    elif cam_id == 26:
        movements = [
            [(1106, 156), (895, 632)],  #down
            [(1176, 1031), (1216, 538)],  #up
        ]

        mov_exits = [0, 0]

    elif cam_id == 27:
        movements = [
            [(575, 235), (1710, 850)],  # down
            [(1550, 410), (430, 95)],  # up (long)
            # [(1390, 165), (430, 95)],  # up (from parking lot)
            # [(595, 180), (430, 95)],  # up (short)
        ]
        # c27 to c24: 0
        # c24 to c27: 1
        
        mov_exits = [0, 1, 1, 1]

    elif cam_id == 29:
        movements = [
            [(920, 540), (600, 725)],  # down
            [(1345, 410), (1340, 265)],  # up
        ]
        # c33 to c29: 0
        # c29 to c33: 1
        
        mov_exits = [1, 0]

    elif cam_id == 33:
        movements = [
            [(1495, 830), (1260, 355)],  # up
            [(735, 360), (520, 880)],  # down
        ]
        # c34 to c29: 0
        # c29 to c34: 1
        
        mov_exits = [0, 1]

    elif cam_id == 34:
        movements = [
            [(765, 255), (375, 135)],  # up
            [(655, 325), (1660, 650)]  # down
        ]
        # c33 to c34: 0
        # c34 to c33: 1
        
        mov_exits = [0, 1]

    elif cam_id == 41:
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


    elif cam_id == 44:
        movements = [
            [(100, 700), (940, 230)],  # bl straight
            [(100, 700), (530, 180)],  # bl left
            [(150, 850), (870, 810)],  # bl right
            [(100, 700), (55, 525)],  # bl u-turn

            [(1130, 385), (530, 180)],  # br straight
            [(1150, 465), (55, 525)],  # br left
            [(1140, 360), (940, 230)],  # br right
            [(1150, 465), (920, 720)],  # br u-turn

            [(860, 190), (55, 525)],  # tr straight
            [(860, 190), (895, 755)],  # tr left
            [(790, 180), (530, 180)],  # tr right
            [(860, 190), (905, 225)],  # tr u-turn

            [(205, 310), (895, 760)],  # tl straight
            [(330, 260), (920, 225)],  # tl left
            [(100, 350), (45, 480)],  # tl right
            [(360, 250), (500, 195)],  # tl u-turn
        ]

        mov_exits = [2, 3, 1, 0, 3, 0, 2, 1, 0, 1, 3, 2, 1, 2, 0, 3]


    elif cam_id == 45:
        movements = [
            [(40, 490), (1150, 170)],  # bl straight
            [(40, 425), (560, 120)],  # bl left
            [(50, 630), (705, 700)],  # bl right
            [(40, 375), (50, 275)],  # bl u-turn

            [(1270, 335), (560, 120)],  # br straight
            [(1270, 335), (40, 275)],  # br left
            [(1270, 310), (1150, 170)],  # br right
            [(1230, 425), (1100, 540)],  # br u-turn

            [(890, 140), (40, 275)],  # tr straight
            [(940, 155), (1120, 640)],  # tr left
            [(890, 140), (560, 120)],  # tr right
            [(970, 155), (1150, 170)],  # tr u-turn

            [(320, 155), (1020, 640)],  # tl straight
            [(415, 135), (1150, 170)],  # tl left
            [(190, 175), (40, 275)],  # tl right
            [(415, 135), (560, 120)],  # tl u-turn
        ]

        mov_exits = [2, 3, 1, 0, 3, 0, 2, 1, 0, 1, 3, 2, 1, 2, 0, 3]


    elif cam_id == 46:
        movements = [
            [(10, 710), (1175, 173)],  # bl straight
            [(10, 450), (495, 150)],  # bl left
            [(10, 700), (760, 700)],  # bl right
            [(10, 450), (10, 300)],  # bl u-turn

            [(1270, 335), (495, 150)],  # br straight
            [(1270, 335), (10, 300)],  # br left
            [(1270, 310), (1175, 173)],  # br right
            [(1270, 375), (1140, 550)],  # br u-turn

            [(827, 136), (10, 300)],  # tr straight
            [(940, 155), (1160, 660)],  # tr left
            [(750, 130), (495, 150)],  # tr right
            [(970, 155), (1175, 173)],  # tr u-turn

            [(255, 210), (870, 647)],  # tl straight
            [(358, 187), (1175, 173)],  # tl left
            [(155, 218), (10, 300)],  # tl right
            [(385, 180), (495, 150)],  # tl u-turn
        ] 

        mov_exits = [2, 3, 1, 0, 3, 0, 2, 1, 0, 1, 3, 2, 1, 2, 0, 3]
    
    
    # Convert movement lines to np vectors
    for index, mov in enumerate(movements):
        end = mov[1]
        start = mov[0]

        movements[index] = [end[0] - start[0], end[1] - start[1]]

    return len(movements), np.array(movements), mov_exits


