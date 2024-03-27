
cd src
seqs=(c010 c016 c017 c018 c019 c020 c021 c022 c023 c024 c025 c026 c027 c028 c029 c033 c034 c035 c036)

TrackOneSeq(){
    seq=$1
    config=$2
    echo tracking $seq with ${config}
    python -W ignore fair_app.py \
        --min_confidence=0.1 \
        --display=False \
        --max_frame_idx -1 \
        --nms_max_overlap 0.99 \
        --min-box-area 750 \
        --cfg_file ${config} \
        --seq_name ${seq} \
        --max_cosine_distance 0.5

    cd ./post_processing
    python main.py ${seq} 'pp' ${config}
    cd ../
}

for seq in ${seqs[@]}
do 
    TrackOneSeq ${seq} $1 &
done
wait
