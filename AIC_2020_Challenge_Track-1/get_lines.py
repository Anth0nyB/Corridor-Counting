import os

def get_video_id(path):
    video_id_dict = {}
    with open(os.path.join(path,'list_video_id.txt'),'r') as f:
        for line in f:
            line = line.rstrip()
            video = line.split(' ')
            video_id_dict[int(video[0])] = video[1]
    return video_id_dict

def get_rois(cam_id,data_path):
    print(data_path)
    cam_path = os.path.join(data_path, 'ROIs/cam_{}.txt'.format(cam_id))
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
    if cam_id == 41:
        exit1 = [(), ()]
        exit2 = [(), ()]
        exit3 = [(), ()]
        exit4 = [(), ()]

        exits = [exit1, exit2, exit3, exit4]

    return len(exits), exits

def get_lines(cam_id):
    """ Gives the vectors describing each possible movement through the intersection
        These values are hardcoded on a per interseciton basis """
    
    if cam_id == 41:
        line_0 = [(), ()]
        line_1 = [(), ()]
        line_2 = [(), ()]
        line_3 = [(), ()]
        line_4 = [(), ()]
        lines=[line_0, line_1, line_2, line_3, line_4]        
    
    return len(lines), lines


