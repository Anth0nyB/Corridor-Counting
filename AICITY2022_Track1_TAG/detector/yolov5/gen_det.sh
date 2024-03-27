# Get the number of available GPUs
num_gpus=$(nvidia-smi --query-gpu=count --format=csv,noheader | wc -l)

seqs=(c010 c016 c017 c018 c019 c020 c021 c022 c023 c024 c025 c026 c027 c028 c029 c033 c034 c035 c036) 

# Loop through sequence IDs
for ((i = 0; i < ${#seqs[@]}; i += num_gpus)); do
    # Loop through available GPUs
    for ((j = 0; j < num_gpus && i + j < ${#seqs[@]}; j++)); do
        idx=$((i + j))
        seq=${seqs[$idx]}
        CUDA_VISIBLE_DEVICES=$j python detect2img.py --name $seq --weights yolov5x.pt --conf 0.1 --agnostic --save-conf --img-size 640 --classes 2 5 7 --exist-ok --cfg_file $1 &
    done
    wait
done
