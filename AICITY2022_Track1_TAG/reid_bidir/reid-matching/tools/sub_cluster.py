from utils.filter import *
from utils.visual_rr import visual_rerank
from sklearn.cluster import AgglomerativeClustering
import sys
sys.path.append('../../../')
from config import cfg

def get_sim_matrix(_cfg,cid_tid_dict,cid_tids):
    count = len(cid_tids)
    print('count: ', count)

    q_arr = np.array([cid_tid_dict[cid_tids[i]]['mean_feat'] for i in range(count)])
    g_arr = np.array([cid_tid_dict[cid_tids[i]]['mean_feat'] for i in range(count)])
    q_arr = normalize(q_arr, axis=1)
    g_arr = normalize(g_arr, axis=1)
    # sim_matrix = np.matmul(q_arr, g_arr.T)

    # st mask
    st_mask = np.ones((count, count), dtype=np.float32)
    st_mask = intracam_ignore(st_mask, cid_tids)
    # st_mask = st_filter(st_mask, cid_tids, cid_tid_dict)

    # visual rerank
    visual_sim_matrix = visual_rerank(q_arr, g_arr, cid_tids, _cfg)
    visual_sim_matrix = visual_sim_matrix.astype('float32')
    
    # merge result
    np.set_printoptions(precision=3)
    sim_matrix = visual_sim_matrix * st_mask

    # sim_matrix[sim_matrix < 0] = 0
    np.fill_diagonal(sim_matrix, 0)
    return sim_matrix

def normalize(nparray, axis=0):
    nparray = preprocessing.normalize(nparray, norm='l2', axis=axis)
    return nparray

def get_match(cluster_labels):
    cluster_dict = dict()
    cluster = list()
    for i, l in enumerate(cluster_labels):
        if l in list(cluster_dict.keys()):
            cluster_dict[l].append(i)
        else:
            cluster_dict[l] = [i]
    for idx in cluster_dict:
        cluster.append(cluster_dict[idx])
    return cluster

def get_cid_tid(cluster_labels,cid_tids):
    cluster = list()
    for labels in cluster_labels:
        cid_tid_list = list()
        for label in labels:
            cid_tid_list.append(cid_tids[label])
        cluster.append(cid_tid_list)
    return cluster

def combin_cluster(grouped_labels,cid_tids):
    cluster = list()
    for group in grouped_labels:
        if len(cluster)<1:
            cluster = grouped_labels[group]
            continue

        for c_ts in grouped_labels[group]:
            is_add = False
            for i_c, c_set in enumerate(cluster):
                if len(set(c_ts) & set(c_set))>0:
                    new_list = list(set(c_ts) | set(c_set))
                    cluster[i_c] = new_list
                    is_add = True
                    break
            if not is_add:
                cluster.append(c_ts)
    labels = list()
    num_tr = 0
    for c_ts in cluster:
        label_list = list()
        for c_t in c_ts:
            label_list.append(cid_tids.index(c_t))
            num_tr+=1
        label_list.sort()
        labels.append(label_list)
    print("new tricklets:{}".format(num_tr))
    return labels,cluster

def combin_feature(cid_tid_dict,sub_cluster):
    for sub_ct in sub_cluster:
        if len(sub_ct)<2: continue
        mean_feat = np.array([cid_tid_dict[i]['mean_feat'] for i in sub_ct])
        for i in sub_ct:
            cid_tid_dict[i]['mean_feat'] = mean_feat.mean(axis=0)
    return cid_tid_dict

def get_labels(_cfg, cid_tid_dict, cid_tids, score_thr):
    dis_thrs = 0.1  # hyperparameter, could probably use some optimization
    
    # Divide up the vehicles based on adjacent cameras to perform reid
    # This reduces the size of the clustering problem and increases accuracy
    grouped_cid_tids = subcam_list(cid_tid_dict,cid_tids)
    grouped_labels = dict()
    for i,group in enumerate(grouped_cid_tids):
        sim_matrix = get_sim_matrix(_cfg,cid_tid_dict,grouped_cid_tids[group])
        cluster_labels = AgglomerativeClustering(n_clusters=None, distance_threshold=1-dis_thrs, metric='precomputed', linkage='complete').fit_predict(1 - sim_matrix)
        labels = get_match(cluster_labels)
        cluster_cid_tids = get_cid_tid(labels,grouped_cid_tids[group])
        grouped_labels[group] = cluster_cid_tids
    labels,sub_cluster = combin_cluster(grouped_labels,cid_tids)    
    clustered_cid_tids = get_cid_tid(labels, cid_tids)
    
    return clustered_cid_tids

if __name__ == '__main__':
    cfg.merge_from_file(f'../../../config/{sys.argv[1]}')
    cfg.freeze()
    scene_name = ['S05']
    cams = os.listdir(opj("../../..", cfg.DATA_DIR))
    cams = list(filter(lambda x: 'c' in x, cams))
    scene_cluster = [[int(x[1:]) for x in cams]]
    fea_dir = './exp/viz/validation/S05/movement/'
    cid_tid_dict = dict()

    for pkl_path in os.listdir(fea_dir):
        cid = int(pkl_path.split('.')[0][-3:])
        with open(opj(fea_dir, pkl_path),'rb') as f:
            lines = pickle.load(f)
        for line in lines:
            tracklet = lines[line]
            tid = tracklet['tid']
            if (cid, tid) not in cid_tid_dict:
                cid_tid_dict[(cid, tid)] = tracklet


    cid_tids = sorted([key for key in cid_tid_dict.keys() if key[0] in scene_cluster[0]])
    
    clu = get_labels(cfg,cid_tid_dict,cid_tids,score_thr=cfg.SCORE_THR)
    print('all_clu:', len(clu))
    print(clu)
    # Remove any vehicles with too many or too few cameras appeared on
    new_clu = list()
    for cid_tid_list in clu:
        if len(cid_tid_list) <= 1: continue
        cam_list = [cid_tid[0] for cid_tid in cid_tid_list] # Get camera id for each detection
        if len(cam_list)!=len(set(cam_list)): continue  # If any repeat camera ids, remove from clu
        new_clu.append([cid_tid for cid_tid in cid_tid_list])
    print('new_clu: ', len(new_clu))

    all_clu = new_clu
    print(all_clu)

    cid_tid_label = dict()
    for i, cid_tid_list in enumerate(all_clu):
        for cid_tid in cid_tid_list:
            cid_tid_label[cid_tid] = i + 1
    pickle.dump({'cluster': cid_tid_label}, open('local_to_universal_map.pkl', 'wb'))
